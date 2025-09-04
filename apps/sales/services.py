from decimal import Decimal
from typing import List, Dict, Tuple, Optional
from django.db import transaction
from django.utils import timezone

from .models import Factura, DetalleFactura, Cliente, TipoPago, ConfiguracionFactura
from apps.employees.models import Empleado
from apps.inventory.models import Producto
from apps.inventory.services import InventoryService
from core.models import DetalleImpuesto
from core.services.base_service import BaseService

class SalesService(BaseService):
    """Servicio para gestión de ventas y facturación."""
    
    def __init__(self):
        super().__init__()
        self.inventory_service = InventoryService()
    
    @transaction.atomic
    def crear_venta(self, venta_data: Dict) -> Factura:
        """Crea una nueva venta/factura."""
        # Validar campos requeridos
        campos_requeridos = ['empleado_id', 'productos', 'tipo_pago_id', 'tipo_impuesto_id', 'recibido']
        self.validate_required_fields(venta_data, campos_requeridos)
        
        # Obtener objetos relacionados
        try:
            empleado = Empleado.objects.get(id=venta_data['empleado_id'])
            tipo_pago = TipoPago.objects.get(id=venta_data['tipo_pago_id'])
            tipo_impuesto = DetalleImpuesto.objects.get(id=venta_data['tipo_impuesto_id'])
        except (Empleado.DoesNotExist, TipoPago.DoesNotExist, DetalleImpuesto.DoesNotExist) as e:
            raise ValueError(f"Objeto relacionado no encontrado: {str(e)}")
        
        cliente = None
        if venta_data.get('cliente_id'):
            try:
                cliente = Cliente.objects.get(id=venta_data['cliente_id'])
            except Cliente.DoesNotExist:
                raise ValueError("Cliente no encontrado")
        
        # Verificar stock de productos
        productos_cantidades = venta_data['productos']
        verificacion_stock = self.inventory_service.verificar_stock_multiple(productos_cantidades)
        
        if not verificacion_stock['valido']:
            raise ValueError("; ".join(verificacion_stock['errores']))
        
        # Calcular totales
        totales = self._calcular_totales_venta(productos_cantidades, tipo_impuesto, venta_data.get('propina', Decimal('0')))
        
        # Validar que el recibido sea suficiente
        recibido = venta_data['recibido']
        if recibido < totales['total']:
            raise ValueError(f"Cantidad recibida insuficiente. Total: ${totales['total']}, Recibido: ${recibido}")
        
        # Obtener configuración
        configuracion = ConfiguracionFactura.objects.first()
        if not configuracion:
            configuracion = ConfiguracionFactura.objects.create(prefijo="")
        
        # Crear factura
        factura = Factura.objects.create(
            configuracion=configuracion,
            empleado=empleado,
            cliente=cliente,
            subtotal=totales['subtotal'],
            base_gravable=totales['base_gravable'],
            tipo_impuesto=tipo_impuesto,
            total=totales['total'],
            tipo_pago=tipo_pago,
            recibido=recibido,
            propina=venta_data.get('propina', Decimal('0'))
        )
        
        # Crear detalles y reducir stock
        self._crear_detalles_factura(factura, productos_cantidades)
        self.inventory_service.reducir_stock_multiple(productos_cantidades)
        
        self.log_operation("VENTA_CREADA", f"Factura ID: {factura.id}, Total: ${factura.total}")
        return factura
    
    def _calcular_totales_venta(self, productos_cantidades: List[Tuple[int, int]], 
                               tipo_impuesto: DetalleImpuesto, propina: Decimal) -> Dict[str, Decimal]:
        """Calcula los totales de una venta."""
        subtotal = Decimal('0')
        
        for producto_id, cantidad in productos_cantidades:
            producto = Producto.objects.get(id=producto_id)
            subtotal += producto.precio * cantidad
        
        base_gravable = subtotal
        impuesto_decimal = tipo_impuesto.impuesto / Decimal('100')
        impuesto_total = (base_gravable * impuesto_decimal).quantize(Decimal('0.01'))
        total = base_gravable + impuesto_total + propina
        
        return {
            'subtotal': subtotal,
            'base_gravable': base_gravable,
            'impuesto': impuesto_total,
            'total': total
        }
    
    def _crear_detalles_factura(self, factura: Factura, productos_cantidades: List[Tuple[int, int]]):
        """Crea los detalles de la factura."""
        for producto_id, cantidad in productos_cantidades:
            producto = Producto.objects.get(id=producto_id)
            DetalleFactura.objects.create(
                factura=factura,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
    
    @transaction.atomic
    def anular_venta(self, factura_id: str) -> Factura:
        """Anula una venta y revierte el stock."""
        try:
            factura = Factura.objects.get(id=factura_id)
        except Factura.DoesNotExist:
            raise ValueError(f"Factura {factura_id} no encontrada")
        
        factura.anular()
        self.log_operation("VENTA_ANULADA", f"Factura ID: {factura_id}")
        return factura
