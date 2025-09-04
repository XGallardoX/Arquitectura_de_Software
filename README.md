# POS Radiocity - Sistema Modular

Sistema de Punto de Venta completamente refactorizado con arquitectura modular Django.

## 🚀 Inicio Rápido

### 1. Configurar Entorno
```bash
# Clonar repositorio
git clone [URL_DEL_REPO]
cd POS-Radiocity

# Crear y activar entorno virtual
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# source venv/bin/activate     # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
# Aplicar migraciones
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser
# Iniciar servidor de desarrollo
python manage.py runserver

# Abrir navegador en: http://127.0.0.1:8000/
python manage.py shell << 'USERS'
from django.contrib.auth.models import User, Group

# Usuario Administrador
admin = User.objects.create_user('admin', 'admin@radiocity.com', 'admin123')
admin.is_superuser = True
admin.is_staff = True
admin.save()

# Usuario Empleado
empleado = User.objects.create_user('empleado', 'empleado@radiocity.com', 'empleado123')
empleado.save()

print("Usuarios creados:")
print("Admin: admin / admin123")
print("Empleado: empleado / empleado123")
USERS
POS-Radiocity/
├── config/                 # Configuración Django
│   ├── settings/
│   └── urls.py
├── core/                   # Modelos compartidos
│   ├── models.py
│   └── services/
├── apps/                   # Aplicaciones modulares
│   ├── authentication/    # Login/logout
│   ├── dashboard/         # Paneles principales
│   ├── inventory/         # Gestión inventario
│   ├── sales/            # Gestión ventas
│   ├── purchases/        # Gestión compras
│   ├── employees/        # Gestión empleados
│   └── analytics/        # Reportes (futuro)
├── templates/            # Templates globales
├── static/              # CSS, JS, imágenes
└── requirements.txt
# Verificar configuración
python manage.py check

# Ver migraciones
python manage.py showmigrations

# Acceder a shell de Django
python manage.py shell

# Crear nueva migración
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
"

