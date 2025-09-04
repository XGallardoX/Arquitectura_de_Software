from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
   # Panel principal de empleados
   path('', views.empleados_panel, name='empleados_panel'),
   
   # Alias para compatibilidad con templates existentes
   path('listar/', views.empleados_panel, name='listar_empleados'),
   
   # CRUD de empleados
   path('registrar/', views.registrar_empleado, name='registrar_empleado'),
   path('<str:empleado_id>/modificar/', views.modificar_empleado, name='modificar_empleado'),
]
