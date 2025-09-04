from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
   # Paneles principales
   path('admin/', views.panel_admin, name='panel_admin'),
   path('user/', views.panel_user, name='panel_user'),
   
   # Configuración del sistema
   path('opciones/', views.opciones_panel, name='opciones_panel'),
]
