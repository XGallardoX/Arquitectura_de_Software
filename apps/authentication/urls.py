from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
   # Ruta raíz redirige al login
   path('', views.login_view, name='login'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
]
