from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from decimal import Decimal

from apps.authentication.views import es_admin, es_user
from apps.inventory.services import InventoryService
from apps.analytics.services import AnalyticsService
from apps.sales.models import ConfiguracionFactura

@login_required
@user_passes_test(es_admin)
def panel_admin(request):
    """
    Panel de administrador con métricas principales.
    
    Muestra:
    - Productos con stock bajo
    - Ventas del día
    - Métricas principales del negocio
    """
    try:
        inventory_service = InventoryService()
        analytics_service = AnalyticsService()
        
        # Obtener productos con stock bajo
        productos_bajo_stock = inventory_service.obtener_productos_stock_bajo(limite=10)
        
        # Obtener ventas del día
        ventas_hoy = analytics_service.ventas_por_dia()
        
        # Métricas adicionales
        reporte_inventario = analytics_service.reporte_inventario()
        
        context = {
            'productos_bajo_stock': productos_bajo_stock,
            'ventas_hoy_admin': ventas_hoy['total_ventas'],
            'cantidad_ventas_hoy': ventas_hoy['cantidad_ventas'],
            'productos_sin_stock': reporte_inventario['productos_sin_stock'],
            'valor_total_inventario': reporte_inventario['valor_total_inventario'],
        }
        
    except Exception as e:
        messages.error(request, f'Error al cargar el panel: {str(e)}')
        context = {
            'productos_bajo_stock': [],
            'ventas_hoy_admin': Decimal('0'),
            'cantidad_ventas_hoy': 0,
        }
    
    return render(request, 'dashboard/panel_admin.html', context)

@login_required 
@user_passes_test(es_user)
def panel_user(request):
    """
    Panel de usuario con información básica.
    
    Muestra:
    - Ventas del día (para cuadre de caja)
    - Acceso a funciones básicas
    """
    try:
        analytics_service = AnalyticsService()
        
        # Obtener ventas del día
        ventas_hoy = analytics_service.ventas_por_dia()
        
        context = {
            'ventas_hoy_general': ventas_hoy['total_ventas'],
            'cantidad_ventas_hoy': ventas_hoy['cantidad_ventas'],
            'venta_promedio': ventas_hoy['venta_promedio'],
        }
        
    except Exception as e:
        messages.error(request, f'Error al cargar el panel: {str(e)}')
        context = {
            'ventas_hoy_general': Decimal('0'),
            'cantidad_ventas_hoy': 0,
        }
    
    return render(request, 'dashboard/panel_user.html', context)

@login_required
@user_passes_test(es_admin)  
def opciones_panel(request):
    """
    Panel de opciones y configuración del sistema.
    
    Permite configurar:
    - Prefijo de facturas
    - Otros parámetros del sistema
    """
    if request.method == 'POST':
        nuevo_prefijo = request.POST.get('prefijo', '').strip()
        
        try:
            configuracion = ConfiguracionFactura.objects.first()
            if configuracion:
                configuracion.prefijo = nuevo_prefijo
                configuracion.save()
            else:
                ConfiguracionFactura.objects.create(prefijo=nuevo_prefijo)
            
            messages.success(request, 'Configuración actualizada correctamente.')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar configuración: {str(e)}')
        
        return redirect('dashboard:opciones_panel')
    
    # GET request
    configuracion = ConfiguracionFactura.objects.first()
    
    context = {
        'configuracion': configuracion,
    }
    
    return render(request, 'dashboard/opciones_panel.html', context)
