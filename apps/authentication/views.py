from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

def es_admin(user):
    """Verifica si el usuario es administrador."""
    return user.is_superuser or user.groups.filter(name='Administrador').exists()

def es_user(user):
    """Verifica si el usuario es usuario regular.""" 
    return not es_admin(user)

def login_view(request):
    """
    Vista de inicio de sesión.
    
    Autentica usuarios y los redirige según su tipo (admin/user).
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Por favor ingrese usuario y contraseña.')
            return render(request, 'authentication/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirigir según tipo de usuario
            if es_admin(user):
                return redirect('dashboard:panel_admin')
            else:
                return redirect('dashboard:panel_user')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'authentication/login.html')

def logout_view(request):
    """Vista de cierre de sesión."""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('authentication:login')
