# webapp/seed_sqlite.py
import os
import random
import datetime
from decimal import Decimal

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.webapp.barapp.settings")
django.setup()

from django.db import transaction, connection
from django.utils import timezone

from backend.webapp.gestion.models import (
    DetalleImpuesto, Producto, Empleado, Cliente, TipoPago,
    Factura, DetalleFactura, ConfiguracionFactura
)

# ====== CONFIG ======
RESET_ALL = True
N_CLIENTES = 10
N_EMPLEADOS = 5
N_PRODUCTOS = 20
N_FACTURAS = 40
DIAS_HACIA_ATRAS = 10
IVA_PORC = Decimal("19.000")
PROPINA_PROM = Decimal("0.10")

random.seed(42)

def borrar_tablas():
    with connection.cursor() as cur:
        cur.execute("DELETE FROM gestion_detallefactura;")
        cur.execute("DELETE FROM gestion_factura;")
        cur.execute("DELETE FROM gestion_producto;")
        cur.execute("DELETE FROM gestion_empleado;")
        cur.execute("DELETE FROM gestion_cliente;")
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ("
                    "'gestion_detallefactura','gestion_producto',"
                    "'gestion_empleado','gestion_cliente');")

def get_or_create_basicos():
    iva, _ = DetalleImpuesto.objects.get_or_create(
        nombre="IVA", defaults={"impuesto": IVA_PORC}
    )
    tp_efec, _ = TipoPago.objects.get_or_create(nombre="Efectivo")
    tp_tarj, _ = TipoPago.objects.get_or_create(nombre="Tarjeta")
    return iva, tp_efec, tp_tarj

def seed_clientes(n=N_CLIENTES):
    clientes = []
    for i in range(1, n+1):
        c, _ = Cliente.objects.get_or_create(
            nombre=f"Cliente {i}",
            defaults={"celular": 3000000000 + i, "email": f"cliente{i}@correo.com"}
        )
        clientes.append(c)
    return clientes

def seed_empleados(n=N_EMPLEADOS):
    empleados = []
    for i in range(1, n+1):
        e, _ = Empleado.objects.get_or_create(
            id=f"E{i:03d}",
            defaults={"nombre": f"Empleado{i}", "apellido": "Bar", "celular": 3100000000 + i, "estado": True}
        )
        empleados.append(e)
    return empleados

def seed_productos(n=N_PRODUCTOS):
    nombres = [
        "Cerveza Lager","Cerveza IPA","Ron Añejo","Vodka Premium","Ginebra","Whisky",
        "Tequila","Vino Tinto","Vino Blanco","Cuba Libre","Gin Tonic","Margarita",
        "Mojito","Piña Colada","Agua","Gaseosa","Jugo Natural","Nachos","Papas","Alitas"
    ]
    prods = []
    for i in range(n):
        nombre = nombres[i % len(nombres)]
        precio = Decimal(random.choice([8,10,12,15,18,20,25])) * 1000
        stock = random.randint(20, 150)
        p, _ = Producto.objects.get_or_create(
            nombre=f"{nombre} {i+1}",
            defaults={"precio": precio, "stock": stock, "cantidad_medida": 1, "unidad_medida": "UND"}
        )
        prods.append(p)
    return prods

def elegir_fecha_hora():
    hoy = timezone.localdate()
    delta = datetime.timedelta(days=random.randint(0, DIAS_HACIA_ATRAS))
    fecha = hoy - delta
    hora = datetime.time(hour=random.randint(17, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
    return fecha, hora

@transaction.atomic
def seed_facturas(iva, tp_efec, tp_tarj, clientes, empleados, productos, n=N_FACTURAS):
    # ✅ Configuración mínima válida (solo tiene 'prefijo')
    config, _ = ConfiguracionFactura.objects.get_or_create(prefijo="RC")

    for _ in range(n):
        cliente = random.choice(clientes)
        empleado = random.choice(empleados)
        tipo_pago = random.choice([tp_efec, tp_tarj])
        fecha, hora = elegir_fecha_hora()

        items = random.sample(productos, k=random.randint(1, 4))
        cantidades = [random.randint(1, 4) for _ in items]

        subtotal = Decimal("0.00")
        for prod, cant in zip(items, cantidades):
            subtotal += prod.precio * cant

        base_gravable = (subtotal / (Decimal("1.0") + (iva.impuesto / Decimal("100")))).quantize(Decimal("0.01"))
        total = subtotal.quantize(Decimal("0.01"))
        propina = (total * Decimal(str(random.uniform(float(PROPINA_PROM) * 0.5, float(PROPINA_PROM) * 1.5)))).quantize(Decimal("0.01"))
        recibido = (total + propina).quantize(Decimal("0.01"))

        fac = Factura(
            fecha_emision=fecha, hora_emision=hora,
            subtotal=subtotal, total=total, base_gravable=base_gravable,
            recibido=recibido, propina=propina,
            cliente=cliente, configuracion=config, empleado=empleado,
            tipo_impuesto=iva, tipo_pago=tipo_pago, anulado=False,
        )
        fac.save()

        for prod, cant in zip(items, cantidades):
            DetalleFactura.objects.create(
                factura=fac, producto=prod, cantidad=cant, precio_unitario=prod.precio
            )

def main():
    if RESET_ALL:
        print(">> Borrando datos previos…")
        borrar_tablas()

    print(">> Creando básicos (IVA, Tipos de pago)…")
    iva, tp_efec, tp_tarj = get_or_create_basicos()

    print(">> Sembrando clientes…")
    clientes = seed_clientes()

    print(">> Sembrando empleados…")
    empleados = seed_empleados()

    print(">> Sembrando productos…")
    productos = seed_productos()

    print(">> Generando facturas y detalles…")
    seed_facturas(iva, tp_efec, tp_tarj, clientes, empleados, productos)

    print("✅ Listo. Datos de ejemplo creados.")

if __name__ == "__main__":
    main()
