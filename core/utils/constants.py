"""
Constantes para el sistema POS.
"""

# Estados de productos
PRODUCTO_ACTIVO = True
PRODUCTO_INACTIVO = False

# Estados de empleados
EMPLEADO_ACTIVO = True
EMPLEADO_INACTIVO = False

# Límites de stock
STOCK_BAJO_DEFAULT = 10
STOCK_CRITICO = 5

# Configuración de facturación
PREFIJO_FACTURA_DEFAULT = "FAC-"

# Tipos de impuesto comunes
IMPUESTOS_COMUNES = [
   {'nombre': 'Exento', 'impuesto': 0.000},
   {'nombre': 'IVA 19%', 'impuesto': 0.190},
   {'nombre': 'IVA 5%', 'impuesto': 0.050},
]

# Tipos de pago comunes
TIPOS_PAGO_COMUNES = [
   'Efectivo',
   'Tarjeta Débito',
   'Tarjeta Crédito',
   'Transferencia',
   'Nequi',
   'Daviplata'
]

# Unidades de medida comunes
UNIDADES_MEDIDA = [
   'unidad',
   'ml',
   'gr',
   'kg',
   'litro',
   'caja',
   'paquete'
]
