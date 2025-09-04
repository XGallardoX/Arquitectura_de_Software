from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from decimal import Decimal

from .models import Compra, Proveedor
from .services import PurchasesService
from apps.inventory.models import Producto
from apps.authentication.views import es_admin

@login_required
def compras_panel(request):
    """
    Panel de gestión de compras.
    
    Permite ver compras existentes y buscar por ID.
    """
    query_id = request.GET.get('id', '').strip()
    
    if query_id:
        try:
            compras = Compra.objects.filter(id=int(query_id)).select_related('proveedor')
        except ValueError:
            compras = Compra.objects.none()
            messages.warning(request, 'ID de compra inválido.')
    else:
        compras = Compra.objects.select_related('proveedor').order_by('-fecha')
    
    context = {
        'compras': compras,
        'query_id': query_id,
    }
    
    return render(request, 'purchases/compras_panel.html', context)

@login_required
@user_passes_test(es_admin)
def registrar_compra(request):
    """
    Registra una nueva compra a proveedor.
    
    Proceso:
    1. Selecciona productos y cantidades
    2. Define costos de compra
    3. Actualiza stock automáticamente
    4. Calcula total de la compra
    """
    if request.method == 'POST':
        try:
            purchases_service = PurchasesService()
            
            # Obtener datos del formulario
            proveedor_id = request.POST.get('proveedor') or None
            productos_ids = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            costos = request.POST.getlist('costo')
            observaciones = request.POST.get('observaciones', '').strip()
            
            if not productos_ids or not cantidades or not costos:
                raise ValueError('Debe agregar al menos un producto a la compra')
            
            # Preparar productos para la compra
            productos_compra = []
            for pid, cant, costo in zip(productos_ids, cantidades, costos):
                if pid and cant and costo:
                    productos_compra.append((
                        int(pid), 
                        int(cant), 
                        Decimal(costo)
                    ))
            
            if not productos_compra:
                raise ValueError('Debe especificar productos válidos con cantidades y costos')
            
            # Preparar datos de la compra
            compra_data = {
                'proveedor_id': int(proveedor_id) if proveedor_id else None,
                'productos': productos_compra,
                'observaciones': observaciones,
            }
            
            # Registrar compra usando el servicio
            compra = purchases_service.registrar_compra(compra_data)
            
            messages.success(request, f'Compra #{compra.id} registrada exitosamente. Total: ${compra.total}')
            return redirect('purchases:compras_panel')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    # GET request - mostrar formulario
    context = {
        'productos': Producto.objects.filter(activo=True).order_by('nombre'),
        'proveedores': Proveedor.objects.filter(activo=True).order_by('nombre'),
    }
    
    return render(request, 'purchases/registrar_compra.html', context)
