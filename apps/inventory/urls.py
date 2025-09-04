from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
   # Panel principal de inventario
   path('', views.inventario_panel, name='inventario_panel'),
   
   # CRUD de productos
   path('productos/registrar/', views.registrar_producto, name='registrar_producto'),
   path('productos/<int:producto_id>/modificar/', views.modificar_producto, name='modificar_producto'),
]
