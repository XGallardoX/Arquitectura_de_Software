from decimal import Decimal
from typing import List, Dict, Tuple, Optional
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import models

from .models import Producto
from core.services.base_service import BaseService

class InventoryService(BaseService):
    """
    Servicio para gestión de inventario y productos.
    
    Maneja todas las operaciones relacionadas con productos:
    - Crear, actualizar, eliminar productos
    - Control de stock
    - Validaciones de inventario
    - Reportes de stock bajo
    """
    
    @transaction.atomic
    def crear_producto(self, nombre: str, precio: Decimal, stock: int = 0, 
                      cantidad_medida: int = 1, unidad_medida: str = "unidad",
                      codigo_producto: str = None, descripcion: str = "") -> Producto:
        """
        Crea un nuevo producto en el inventario.
        """
        # Validaciones
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto es requerido")
        
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        if cantidad_medida <= 0:
            raise ValueError("La cantidad de medida debe ser mayor a 0")
        
        # Verificar código único si se proporciona
        if codigo_producto and Producto.objects.filter(codigo_producto=codigo_producto).exists():
            raise ValueError(f"El código {codigo_producto} ya existe")
        
        producto = Producto.objects.create(
            nombre=nombre.strip(),
            precio=precio,
            stock=stock,
            cantidad_medida=cantidad_medida,
            unidad_medida=unidad_medida,
            codigo_producto=codigo_producto,
            descripcion=descripcion
        )
        
        self.log_operation("PRODUCTO_CREADO", f"ID: {producto.id}, Nombre: {nombre}")
        return producto
    
    @transaction.atomic
    def actualizar_producto(self, producto_id: int, **kwargs) -> Producto:
        """Actualiza un producto existente."""
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            raise ValueError(f"Producto con ID {producto_id} no existe")
        
        # Validaciones específicas
        if 'precio' in kwargs and kwargs['precio'] <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        if 'stock' in kwargs and kwargs['stock'] < 0:
            raise ValueError("El stock no puede ser negativo")
        
        # Actualizar campos
        for field, value in kwargs.items():
            if hasattr(producto, field):
                setattr(producto, field, value)
        
        producto.save()
        self.log_operation("PRODUCTO_ACTUALIZADO", f"ID: {producto_id}")
        return producto
    
    def verificar_stock_disponible(self, producto_id: int, cantidad_requerida: int) -> bool:
        """Verifica si hay stock suficiente de un producto."""
        try:
            producto = Producto.objects.get(id=producto_id)
            return producto.tiene_stock(cantidad_requerida)
        except Producto.DoesNotExist:
            return False
    
    def verificar_stock_multiple(self, productos_requeridos: List[Tuple[int, int]]) -> Dict[str, any]:
        """Verifica stock para múltiples productos."""
        resultado = {
            'valido': True,
            'errores': [],
            'productos_verificados': []
        }
        
        for producto_id, cantidad in productos_requeridos:
            try:
                producto = Producto.objects.get(id=producto_id)
                if not producto.tiene_stock(cantidad):
                    resultado['valido'] = False
                    resultado['errores'].append(
                        f"Stock insuficiente para {producto.nombre}. "
                        f"Disponible: {producto.stock}, Requerido: {cantidad}"
                    )
                
                resultado['productos_verificados'].append({
                    'producto': producto,
                    'cantidad_requerida': cantidad,
                    'stock_disponible': producto.stock,
                    'suficiente': producto.tiene_stock(cantidad)
                })
                
            except Producto.DoesNotExist:
                resultado['valido'] = False
                resultado['errores'].append(f"Producto con ID {producto_id} no existe")
        
        return resultado
    
    @transaction.atomic
    def reducir_stock_multiple(self, productos_cantidades: List[Tuple[int, int]]) -> Dict[str, any]:
        """Reduce stock de múltiples productos de forma atómica."""
        # Primero verificar que todo esté disponible
        verificacion = self.verificar_stock_multiple(productos_cantidades)
        if not verificacion['valido']:
            raise ValueError("; ".join(verificacion['errores']))
        
        # Reducir stock
        productos_actualizados = []
        for producto_id, cantidad in productos_cantidades:
            producto = Producto.objects.get(id=producto_id)
            producto.reducir_stock(cantidad)
            productos_actualizados.append(producto)
        
        self.log_operation("STOCK_REDUCIDO", f"Productos actualizados: {len(productos_actualizados)}")
        
        return {
            'productos_actualizados': productos_actualizados,
            'cantidad_productos': len(productos_actualizados)
        }
    
    def obtener_productos_stock_bajo(self, limite: int = 10) -> List[Producto]:
        """Obtiene productos con stock por debajo del límite especificado."""
        return list(Producto.objects.filter(
            stock__lt=limite, 
            activo=True
        ).order_by('stock', 'nombre'))
    
    def buscar_productos(self, termino: str, activos_solo: bool = True) -> List[Producto]:
        """Busca productos por nombre o código."""
        queryset = Producto.objects.all()
        
        if activos_solo:
            queryset = queryset.filter(activo=True)
        
        if termino:
            queryset = queryset.filter(
                models.Q(nombre__icontains=termino) |
                models.Q(codigo_producto__icontains=termino)
            )
        
        return list(queryset.order_by('nombre'))
