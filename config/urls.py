"""
URLs principales del sistema POS Radiocity.

Distribuye las rutas a cada aplicación modular.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   # Admin de Django
   path('admin/', admin.site.urls),
   
   # Autenticación
   path('', include('apps.authentication.urls')),
   
   # Dashboard principal  
   path('dashboard/', include('apps.dashboard.urls')),
   
   # Módulos principales
   path('inventario/', include('apps.inventory.urls')),
   path('ventas/', include('apps.sales.urls')),
   path('compras/', include('apps.purchases.urls')),
   path('empleados/', include('apps.employees.urls')),
   path('reportes/', include('apps.analytics.urls')),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
