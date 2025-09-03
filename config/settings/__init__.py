"""
Configuración modular del proyecto POS Radiocity.

Importa la configuración base y permite override por entorno.
"""
from .base import *

# Cargar configuración específica del entorno
try:
    from .local import *
except ImportError:
    try:
        from .production import *
    except ImportError:
        pass
