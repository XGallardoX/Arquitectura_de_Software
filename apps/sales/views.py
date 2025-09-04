from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from decimal import Decimal
from typing import List, Tuple

from .models import Factura, Cliente, TipoPago, ConfiguracionFactura
from .services import SalesService
from apps.inventory.models import Producto
from apps.employees.models import Empleado  
from core.models import DetalleImpuesto
from apps.authentication.views import es_admin
from .utils.pdf_generator import generar_factura_pdf

@login_required
def ventas_panel(request):
    """
    Panel de gestión de ventas.
    
    Permite:
    - Ver facturas existentes
    - Buscar facturas por ID
    - Anular/reactivar ventas (según permisos)
    """
    if request.method == 'POST':
        # Anular/reactivar venta
        venta_id = request.POST.get('venta_id')
        
        if not venta_id:
            messages.error(request, 'ID de venta no proporcionado.')
            return redirect('sales:ventas_panel')
        
        try:
            sales_service = SalesService()
            factura = get_object_or_404(Factura, pk=venta_id)
            
            if factura.anulado:
                # Reactivar no está implementado en el servicio, se haría manualmente
                factura.anulado = False
                factura.save()
                messages.success(request, f'Venta #{factura.id} reactivada correctamente.')
            else:
                factura = sales_service.anular_venta(venta_id)
                messages.success(request, f'Venta #{factura.id} anulada correctamente.')
                
        except Exception as e:
            messages.error(request, f'Error al procesar venta: {str(e)}')
        
        return redirect('sales:ventas_panel')
    
    # GET request - mostrar ventas
    query_id = request.GET.get('id', '').strip()
    
    if query_id:
        ventas = Factura.objects.filter(id=query_id).select_related('cliente', 'empleado')
    else:
        ventas = Factura.objects.select_related('cliente', 'empleado').order_by('-fecha_emision')
    
    configuracion = ConfiguracionFactura.objects.first()
    
    # Determinar panel de retorno según permisos
    panel_url = 'dashboard:panel_admin' if es_admin(request.user) else 'dashboard:panel_user'
    
    context = {
        'ventas': ventas,
        'query_id': query_id,
        'configuracion': configuracion,
        'panel_url': panel_url,
    }
    
    return render(request, 'sales/ventas_panel.html', context)

@login_required
def detalle_factura(request, factura_id):
    """
    Muestra el detalle completo de una factura.
    
    Args:
        factura_id (str): ID de la factura
    """
    factura = get_object_or_404(
        Factura.objects.select_related(
            'cliente', 'empleado', 'tipo_impuesto', 'tipo_pago', 'configuracion'
        ).prefetch_related('detalles__producto'),
        pk=factura_id
    )
    
    context = {
        'factura': factura,
    }
    
    return render(request, 'sales/detalle_factura.html', context)

@login_required
def registrar_venta(request):
    """
    Registra una nueva venta/factura.
    
    Proceso:
    1. Valida disponibilidad de productos
    2. Calcula totales incluyendo impuestos
    3. Crea factura y detalles
    4. Actualiza stock automáticamente
    """
    if request.method == 'POST':
        try:
            sales_service = SalesService()
            
            # Obtener y validar productos seleccionados
            productos_ids = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            
            if not productos_ids or not cantidades:
                raise ValueError('Debe seleccionar al menos un producto')
            
            # Convertir a lista de tuplas (producto_id, cantidad)
            productos_cantidades = []
            for pid, cant in zip(productos_ids, cantidades):
                if pid and cant:
                    productos_cantidades.append((int(pid), int(cant)))
            
            if not productos_cantidades:
                raise ValueError('Debe seleccionar productos válidos con cantidades')
            
            # Preparar datos de la venta
            venta_data = {
                'cliente_id': request.POST.get('cliente') or None,
                'empleado_id': request.POST.get('empleado'),
                'tipo_pago_id': int(request.POST.get('tipo_pago')),
                'tipo_impuesto_id': int(request.POST.get('tipo_impuesto')),
                'recibido': Decimal(request.POST.get('recibido', '0')),
                'propina': Decimal(request.POST.get('propina', '0')),
                'productos': productos_cantidades,
            }
            
            # Crear venta usando el servicio
            factura = sales_service.crear_venta(venta_data)
            
            messages.success(request, f'Venta #{factura.id} registrada exitosamente. Total: ${factura.total}')
            return redirect('sales:ventas_panel')
            
        except ValueError as e:
            messages.error(request, str(e))
            
            # Mantener datos del formulario para reintento
            context = {
                'productos': Producto.objects.filter(activo=True, stock__gt=0),
                'clientes': Cliente.objects.filter(activo=True),
                'empleados': Empleado.objects.filter(estado=True),
                'tipos_pago': TipoPago.objects.filter(activo=True),
                'impuestos': DetalleImpuesto.objects.all(),
                'form_data': request.POST,  # Para mantener valores ingresados
            }
            return render(request, 'sales/registrar_venta.html', context)
            
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    # GET request - mostrar formulario
    context = {
        'productos': Producto.objects.filter(activo=True, stock__gt=0),
        'clientes': Cliente.objects.filter(activo=True),
        'empleados': Empleado.objects.filter(estado=True),
        'tipos_pago': TipoPago.objects.filter(activo=True),
        'impuestos': DetalleImpuesto.objects.all(),
    }
    
    return render(request, 'sales/registrar_venta.html', context)

@login_required
def factura_pdf(request, factura_id):
    """
    Genera y retorna el PDF de una factura.
    
    Args:
        factura_id (str): ID de la factura
        
    Returns:
        HttpResponse: PDF de la factura
    """
    try:
        factura = get_object_or_404(
            Factura.objects.prefetch_related('detalles__producto'), 
            pk=factura_id
        )
        
        # Generar PDF usando utilidad específica
        pdf_response = generar_factura_pdf(factura)
        
        return pdf_response
        
    except Exception as e:
        messages.error(request, f'Error al generar PDF: {str(e)}')
        return redirect('sales:detalle_factura', factura_id=factura_id)
