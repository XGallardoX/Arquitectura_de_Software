from decimal import Decimal
from typing import List, Dict, Optional
from django.db import transaction

from .models import Compra, DetalleCompra, Proveedor
from apps.inventory.models import Producto
from core.services.base_service import BaseService

class PurchasesService(BaseService):
    """
    Servicio para gestión de compras a proveedores.
    
    Maneja todas las operaciones relacionadas con compras:
    - Registrar compras
    - Modificar compras existentes
    - Gestión de proveedores
    - Actualización automática de stock
    """
    
    @transaction.atomic
    def registrar_compra(self, compra_data: Dict) -> Compra:
        """Registra una nueva compra."""
        # Validar campos requeridos
        if not compra_data.get('productos'):
            raise ValueError("Debe incluir al menos un producto en la compra")
        
        # Obtener proveedor si se especifica
        proveedor = None
        if compra_data.get('proveedor_id'):
            try:
                proveedor = Proveedor.objects.get(id=compra_data['proveedor_id'])
            except Proveedor.DoesNotExist:
                raise ValueError("Proveedor no encontrado")
        
        # Crear compra
        compra = Compra.objects.create(
            proveedor=proveedor,
            observaciones=compra_data.get('observaciones', '')
        )
        
        # Procesar productos
        total_compra = Decimal('0')
        for producto_id, cantidad, costo_producto in compra_data['productos']:
            # Validar producto existe
            try:
                producto = Producto.objects.get(id=producto_id)
            except Producto.DoesNotExist:
                raise ValueError(f"Producto con ID {producto_id} no encontrado")
            
            # Validar datos
            if cantidad <= 0:
                raise ValueError(f"La cantidad debe ser mayor a 0 para {producto.nombre}")
            
            if costo_producto <= 0:
                raise ValueError(f"El costo debe ser mayor a 0 para {producto.nombre}")
            
            # Crear detalle de compra
            DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=cantidad,
                costo_producto=costo_producto
            )
            
            # Actualizar stock del producto
            producto.aumentar_stock(cantidad)
            
            # Sumar al total
            total_compra += cantidad * costo_producto
        
        # Actualizar total de la compra
        compra.total = total_compra
        compra.save()
        
        self.log_operation("COMPRA_REGISTRADA", f"ID: {compra.id}, Total: ${total_compra}")
        return compra
    
    @transaction.atomic
    def modificar_compra(self, compra_id: int, compra_data: Dict) -> Compra:
        """Modifica una compra existente."""
        try:
            compra = Compra.objects.get(id=compra_id)
        except Compra.DoesNotExist:
            raise ValueError(f"Compra con ID {compra_id} no encontrada")
        
        # Revertir stock de la compra original
        for detalle in compra.detalles.all():
            detalle.producto.reducir_stock(detalle.cantidad)
        
        # Eliminar detalles anteriores
        compra.detalles.all().delete()
        
        # Actualizar proveedor si se especifica
        if 'proveedor_id' in compra_data:
            if compra_data['proveedor_id']:
                try:
                    compra.proveedor = Proveedor.objects.get(id=compra_data['proveedor_id'])
                except Proveedor.DoesNotExist:
                    raise ValueError("Proveedor no encontrado")
            else:
                compra.proveedor = None
        
        # Actualizar observaciones
        if 'observaciones' in compra_data:
            compra.observaciones = compra_data['observaciones']
        
        # Procesar nuevos productos (similar a registrar_compra)
        total_compra = Decimal('0')
        for producto_id, cantidad, costo_producto in compra_data['productos']:
            producto = Producto.objects.get(id=producto_id)
            
            DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=cantidad,
                costo_producto=costo_producto
            )
            
            producto.aumentar_stock(cantidad)
            total_compra += cantidad * costo_producto
        
        compra.total = total_compra
        compra.save()
        
        self.log_operation("COMPRA_MODIFICADA", f"ID: {compra_id}")
        return compra
    
    def crear_proveedor(self, nombre: str, celular: int = None, 
                       direccion: str = "", email: str = "") -> Proveedor:
        """Crea un nuevo proveedor."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del proveedor es requerido")
        
        proveedor = Proveedor.objects.create(
            nombre=nombre.strip(),
            celular=celular,
            direccion=direccion,
            email=email
        )
        
        self.log_operation("PROVEEDOR_CREADO", f"Nombre: {nombre}")
        return proveedor
