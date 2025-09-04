from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from decimal import Decimal

from .models import Producto
from .services import InventoryService
from apps.authentication.views import es_admin

@login_required
def inventario_panel(request):
    """
    Panel de gestión de inventario.
    
    Permite:
    - Ver productos existentes
    - Buscar productos por nombre
    - Acceso a CRUD de productos (según permisos)
    """
    inventory_service = InventoryService()
    
    # Buscar productos
    query_nombre = request.GET.get('nombre', '').strip()
    
    if query_nombre:
        productos = inventory_service.buscar_productos(query_nombre)
    else:
        productos = Producto.objects.all().order_by('nombre')
    
    # Determinar permisos
    puede_editar = es_admin(request.user)
    panel_url = 'dashboard:panel_admin' if puede_editar else 'dashboard:panel_user'
    
    context = {
        'productos': productos,
        'query_nombre': query_nombre,
        'panel_url': panel_url,
        'puede_editar': puede_editar,
    }
    
    return render(request, 'inventory/inventario_panel.html', context)

@login_required
@user_passes_test(es_admin)
def registrar_producto(request):
    """
    Registra un nuevo producto en el inventario.
    
    Solo accesible para administradores.
    """
    if request.method == 'POST':
        try:
            inventory_service = InventoryService()
            
            # Obtener datos del formulario
            producto_data = {
                'nombre': request.POST.get('nombre', '').strip(),
                'precio': Decimal(request.POST.get('precio', '0')),
                'stock': int(request.POST.get('stock', '0')),
                'cantidad_medida': int(request.POST.get('cantidad_medida', '1')),
                'unidad_medida': request.POST.get('unidad_medida', '').strip(),
                'codigo_producto': request.POST.get('codigo_producto', '').strip() or None,
                'descripcion': request.POST.get('descripcion', '').strip(),
            }
            
            # Crear producto usando el servicio
            producto = inventory_service.crear_producto(**producto_data)
            
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('inventory:inventario_panel')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    return render(request, 'inventory/registrar_producto.html')

@login_required
@user_passes_test(es_admin)
def modificar_producto(request, producto_id):
    """
    Modifica un producto existente.
    
    Args:
        producto_id (int): ID del producto a modificar
    """
    producto = get_object_or_404(Producto, pk=producto_id)
    
    if request.method == 'POST':
        try:
            inventory_service = InventoryService()
            
            # Preparar datos de actualización
            update_data = {
                'nombre': request.POST.get('nombre', '').strip(),
                'precio': Decimal(request.POST.get('precio', '0')),
                'stock': int(request.POST.get('stock', '0')),
                'cantidad_medida': int(request.POST.get('cantidad_medida', '1')),
                'unidad_medida': request.POST.get('unidad_medida', '').strip(),
                'descripcion': request.POST.get('descripcion', '').strip(),
            }
            
            # Actualizar usando el servicio
            producto_actualizado = inventory_service.actualizar_producto(
                producto_id, **update_data
            )
            
            messages.success(request, f'Producto "{producto_actualizado.nombre}" actualizado exitosamente.')
            return redirect('inventory:inventario_panel')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    context = {
        'producto': producto,
    }
    
    return render(request, 'inventory/modificar_producto.html', context)
