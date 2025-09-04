from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
   # Panel principal de ventas
   path('', views.ventas_panel, name='ventas_panel'),
   
   # CRUD de ventas
   path('registrar/', views.registrar_venta, name='registrar_venta'),
   
   # Detalles y documentos
   path('<str:factura_id>/detalle/', views.detalle_factura, name='detalle_factura'),
   path('<str:factura_id>/pdf/', views.factura_pdf, name='factura_pdf'),
]
