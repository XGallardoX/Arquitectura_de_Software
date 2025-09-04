"""
Validadores personalizados para el sistema POS.
"""
from decimal import Decimal
import re

def validar_precio(precio):
   """Valida que el precio sea válido."""
   if not isinstance(precio, (Decimal, float, int)):
       raise ValueError("El precio debe ser un número")
   
   if precio <= 0:
       raise ValueError("El precio debe ser mayor a 0")
   
   return True

def validar_stock(stock):
   """Valida que el stock sea válido."""
   if not isinstance(stock, int):
       raise ValueError("El stock debe ser un número entero")
   
   if stock < 0:
       raise ValueError("El stock no puede ser negativo")
   
   return True

def validar_celular(celular):
   """Valida formato de número celular colombiano."""
   if not isinstance(celular, (int, str)):
       raise ValueError("El celular debe ser un número")
   
   celular_str = str(celular)
   if not re.match(r'^3\d{9}$', celular_str):
       raise ValueError("El celular debe tener formato 3XXXXXXXXX (10 dígitos)")
   
   return True

def validar_email(email):
   """Valida formato de email."""
   if not email:
       return True  # Email es opcional
   
   if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
       raise ValueError("Formato de email inválido")
   
   return True
