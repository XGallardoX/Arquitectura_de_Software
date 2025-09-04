from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Empleado
from .services import EmployeesService
from apps.authentication.views import es_admin

@login_required
@user_passes_test(es_admin)
def empleados_panel(request):
    """
    Panel de gestión de empleados.
    
    Solo accesible para administradores.
    Permite ver y buscar empleados por ID.
    """
    query_id = request.GET.get('id', '').strip()
    
    if query_id:
        empleados = Empleado.objects.filter(id=query_id)
    else:
        empleados = Empleado.objects.all().order_by('nombre', 'apellido')
    
    context = {
        'empleados': empleados,
        'query_id': query_id,
    }
    
    return render(request, 'employees/empleados_panel.html', context)

@login_required
@user_passes_test(es_admin)
def registrar_empleado(request):
    """
    Registra un nuevo empleado en el sistema.
    
    Valida que el ID y celular sean únicos.
    """
    if request.method == 'POST':
        try:
            employees_service = EmployeesService()
            
            # Obtener datos del formulario
            empleado_data = {
                'id': request.POST.get('id', '').strip(),
                'nombre': request.POST.get('nombre', '').strip(),
                'apellido': request.POST.get('apellido', '').strip(),
                'celular': request.POST.get('celular', '').strip(),
                'email': request.POST.get('email', '').strip(),
            }
            
            # Validar y convertir celular
            if empleado_data['celular']:
                try:
                    empleado_data['celular'] = int(empleado_data['celular'])
                except ValueError:
                    raise ValueError('El celular debe ser un número válido')
            else:
                raise ValueError('El celular es requerido')
            
            # Registrar usando el servicio
            empleado = employees_service.registrar_empleado(empleado_data)
            
            messages.success(request, f'Empleado {empleado.nombre_completo} registrado exitosamente.')
            return redirect('employees:empleados_panel')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    return render(request, 'employees/registrar_empleado.html')

@login_required
@user_passes_test(es_admin)
def modificar_empleado(request, empleado_id):
    """
    Modifica un empleado existente.
    
    Args:
        empleado_id (str): ID del empleado a modificar
    """
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    
    if request.method == 'POST':
        try:
            employees_service = EmployeesService()
            
            # Obtener datos de actualización
            empleado_data = {
                'nombre': request.POST.get('nombre', '').strip(),
                'apellido': request.POST.get('apellido', '').strip(),
                'celular': request.POST.get('celular', '').strip(),
                'email': request.POST.get('email', '').strip(),
                'estado': request.POST.get('estado') == 'on',  # Checkbox
            }
            
            # Validar y convertir celular
            if empleado_data['celular']:
                try:
                    empleado_data['celular'] = int(empleado_data['celular'])
                except ValueError:
                    raise ValueError('El celular debe ser un número válido')
            
            # Actualizar usando el servicio
            empleado_actualizado = employees_service.actualizar_empleado(
                empleado_id, empleado_data
            )
            
            messages.success(request, f'Empleado {empleado_actualizado.nombre_completo} actualizado exitosamente.')
            return redirect('employees:empleados_panel')
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
    
    context = {
        'empleado': empleado,
    }
    
    return render(request, 'employees/modificar_empleado.html', context)

# Alias para compatibilidad con URLs existentes
listar_empleados = empleados_panel
