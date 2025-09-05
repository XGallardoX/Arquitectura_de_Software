# Proyecto Backend - Arquitectura de Software

Este proyecto es un backend en Django para el curso de Arquitectura de Software.


## Requisitos

- Python 3.10+
- pip
- Virtualenv (opcional pero recomendado)
- Docker 

---

## Ejecutar en entorno local

1. **Clonar el proyecto** (si no lo tienes ya):

```bash
git clone https://github.com/XGallardoX/Arquitectura_de_Software/tree/fix-rutas
````


Ir al directorio de la aplicación:

````
cd proyecto/backend
````


Crear y activar un entorno virtual (opcional pero recomendado):

````bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
: .\.venv\Scripts\Activate.ps1 # o en Windows PowerShell
.\.venv\Scripts\activate.bat # o en Windows CMD: 
````

Instalar dependencias:

````
pip install -r requirements.txt
````


Ir a la app
````
cd webapp
````


Correr el servidor de desarrollo de Django:

````
bash
python manage.py runserver
````
La aplicación estará disponible en: http://127.0.0.1:8000/

Para detener el servidor, presiona CONTROL-C.