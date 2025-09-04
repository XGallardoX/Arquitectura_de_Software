from decimal import Decimal
from typing import Dict, List, Any
from datetime import date, datetime, timedelta
from django.db.models import Sum, Count, Avg
from django.utils import timezone

from apps.sales.models import Factura
from apps.inventory.models import Producto
from core.services.base_service import BaseService

class AnalyticsService(BaseService):
    """
    Servicio para análisis y reportes del sistema POS.
    
    Genera diferentes tipos de reportes y análisis:
    - Ventas por período
    - Productos más vendidos
    - Análisis de empleados
    - Reportes de inventario
    - Métricas de negocio
    """
    
    def ventas_por_dia(self, fecha: date = None) -> Dict[str, Any]:
        """Obtiene estadísticas de ventas para un día específico."""
        if fecha is None:
            fecha = timezone.localdate()
        
        ventas = Factura.objects.filter(
            fecha_emision=fecha,
            anulado=False
        )
        
        stats = ventas.aggregate(
            total_ventas=Sum('total'),
            cantidad_ventas=Count('id'),
            venta_promedio=Avg('total'),
            total_propinas=Sum('propina')
        )
        
        return {
            'fecha': fecha,
            'total_ventas': stats['total_ventas'] or Decimal('0'),
            'cantidad_ventas': stats['cantidad_ventas'] or 0,
            'venta_promedio': stats['venta_promedio'] or Decimal('0'),
            'total_propinas': stats['total_propinas'] or Decimal('0'),
            'ventas_detalle': list(ventas.select_related('cliente', 'empleado'))
        }
    
    def ventas_por_mes(self, year: int = None, month: int = None) -> Dict[str, Any]:
        """Obtiene estadísticas de ventas para un mes específico."""
        if year is None or month is None:
            hoy = timezone.localdate()
            year = year or hoy.year
            month = month or hoy.month
        
        ventas = Factura.objects.filter(
            fecha_emision__year=year,
            fecha_emision__month=month,
            anulado=False
        )
        
        stats = ventas.aggregate(
            total_ventas=Sum('total'),
            cantidad_ventas=Count('id'),
            venta_promedio=Avg('total')
        )
        
        # Ventas por día del mes
        ventas_por_dia = []
        for dia in range(1, 32):
            try:
                fecha_dia = date(year, month, dia)
                ventas_dia = ventas.filter(fecha_emision=fecha_dia)
                total_dia = ventas_dia.aggregate(total=Sum('total'))['total'] or Decimal('0')
                ventas_por_dia.append({
                    'dia': dia,
                    'fecha': fecha_dia,
                    'total': total_dia,
                    'cantidad': ventas_dia.count()
                })
            except ValueError:
                break  # Día inválido para el mes
        
        return {
            'year': year,
            'month': month,
            'total_ventas': stats['total_ventas'] or Decimal('0'),
            'cantidad_ventas': stats['cantidad_ventas'] or 0,
            'venta_promedio': stats['venta_promedio'] or Decimal('0'),
            'ventas_por_dia': ventas_por_dia
        }
    
    def productos_mas_vendidos(self, fecha_inicio: date, fecha_fin: date, limite: int = 10) -> List[Dict]:
        """Obtiene los productos más vendidos en un período."""
        from apps.sales.models import DetalleFactura
        
        detalles = DetalleFactura.objects.filter(
            factura__fecha_emision__gte=fecha_inicio,
            factura__fecha_emision__lte=fecha_fin,
            factura__anulado=False
        ).select_related('producto')
        
        # Agrupar por producto
        productos_stats = {}
        for detalle in detalles:
            producto_id = detalle.producto.id
            if producto_id not in productos_stats:
                productos_stats[producto_id] = {
                    'producto': detalle.producto,
                    'cantidad_vendida': 0,
                    'total_ingresos': Decimal('0')
                }
            
            productos_stats[producto_id]['cantidad_vendida'] += detalle.cantidad
            productos_stats[producto_id]['total_ingresos'] += detalle.subtotal
        
        # Ordenar por cantidad vendida
        productos_ordenados = sorted(
            productos_stats.values(),
            key=lambda x: x['cantidad_vendida'],
            reverse=True
        )
        
        return productos_ordenados[:limite]
    
    def reporte_inventario(self) -> Dict[str, Any]:
        """Genera un reporte completo del estado del inventario."""
        productos = Producto.objects.filter(activo=True)
        
        total_productos = productos.count()
        valor_total_inventario = sum(
            producto.precio * producto.stock 
            for producto in productos
        )
        
        productos_sin_stock = productos.filter(stock=0).count()
        productos_stock_bajo = productos.filter(stock__lt=10, stock__gt=0).count()
        
        return {
            'total_productos': total_productos,
            'valor_total_inventario': valor_total_inventario,
            'productos_sin_stock': productos_sin_stock,
            'productos_stock_bajo': productos_stock_bajo,
            'productos_detalle': list(productos.order_by('stock'))}
