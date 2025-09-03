"""
Configuración para entorno de desarrollo.
"""
from .base import *
import os
from pathlib import Path

# Build paths - será ajustado después
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database SQLite para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
