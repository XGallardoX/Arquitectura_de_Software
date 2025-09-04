from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
   # Panel principal de compras
   path('', views.compras_panel, name='compras_panel'),
   
   # CRUD de compras
   path('registrar/', views.registrar_compra, name='registrar_compra'),
]
