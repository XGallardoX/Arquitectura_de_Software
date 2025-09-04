"""
Formateadores para el sistema POS.
"""
from decimal import Decimal

def formatear_precio(precio):
   """Formatea un precio para mostrar."""
   if isinstance(precio, (Decimal, float)):
       return f"${precio:,.2f}"
   return f"${precio}"

def formatear_celular(celular):
   """Formatea un número celular para mostrar."""
   celular_str = str(celular)
   if len(celular_str) == 10:
       return f"{celular_str[:3]} {celular_str[3:6]} {celular_str[6:]}"
   return celular_str

def formatear_stock(stock):
   """Formatea el stock para mostrar."""
   if stock == 0:
       return "Sin stock"
   elif stock < 10:
       return f"⚠️ {stock} unidades"
   else:
       return f"{stock} unidades"
