"""
URL configuration for POS Radiocity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path

# URL patterns mínimas durante la migración
urlpatterns = [
    path('admin/', admin.site.urls),
    # Las URLs de las apps modulares se agregarán en el Paso 8
    # path('', include('apps.authentication.urls')),
    # path('inventario/', include('apps.inventory.urls')),
    # path('ventas/', include('apps.sales.urls')),
]

# Comentar handlers de error temporalmente durante migración
# handler404 = 'django.views.defaults.page_not_found'
# handler500 = 'django.views.defaults.server_error'
