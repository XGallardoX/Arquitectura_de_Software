from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import datetime

class Cliente(models.Model):
    """Modelo para clientes"""
    nombre = models.CharField(max_length=100, blank=True)
    celular = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre if self.nombre else f"Cliente #{self.pk}"

class TipoPago(models.Model):
    """Modelo para tipos de pago"""
    nombre = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de Pago"
        verbose_name_plural = "Tipos de Pago"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class ConfiguracionFactura(models.Model):
    """Configuración de facturas"""
    prefijo = models.CharField(max_length=10, blank=True)
    
    class Meta:
        verbose_name = "Configuración de Factura"
        verbose_name_plural = "Configuraciones de Facturas"

    def __str__(self):
        return f"Prefijo: {self.prefijo}"

class Factura(models.Model):
    """Modelo para facturas de venta"""
    id = models.CharField(primary_key=True, max_length=20, editable=False)
    configuracion = models.ForeignKey(ConfiguracionFactura, on_delete=models.PROTECT, default=1)
    fecha_emision = models.DateField(auto_now_add=True)
    hora_emision = models.TimeField(auto_now_add=True)
    empleado = models.ForeignKey('employees.Empleado', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    tipo_impuesto = models.ForeignKey('core.DetalleImpuesto', on_delete=models.PROTECT)
    base_gravable = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.PROTECT)
    recibido = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    propina = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    anulado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_emision', '-hora_emision']

    def __str__(self):
        return f"Factura #{self.id}"

    def save(self, *args, **kwargs):
        """Genera ID automáticamente"""
        if not self.id:
            hoy = datetime.date.today()
            fecha_str = hoy.strftime("%y%m%d")
            cantidad = Factura.objects.filter(fecha_emision=hoy).count() + 1
            self.id = f"{fecha_str}{cantidad:04d}"
        super().save(*args, **kwargs)

    def calcular_totales(self):
        """Calcula totales de la factura"""
        subtotal = sum(detalle.cantidad * detalle.precio_unitario for detalle in self.detalles.all())
        impuesto_decimal = self.tipo_impuesto.impuesto / Decimal('100.0')
        impuesto_total = (subtotal * impuesto_decimal).quantize(Decimal('0.01'))
        total = subtotal + impuesto_total + self.propina
        
        return {
            'subtotal': subtotal,
            'base_gravable': subtotal,
            'impuesto': impuesto_total,
            'total': total
        }
    
    def anular(self):
        """Anula la factura y revierte stock"""
        if self.anulado:
            raise ValueError("La factura ya está anulada")
        
        for detalle in self.detalles.all():
            detalle.producto.aumentar_stock(detalle.cantidad)
        
        self.anulado = True
        self.save(update_fields=['anulado'])

class DetalleFactura(models.Model):
    """Detalle de factura"""
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('inventory.Producto', on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        verbose_name = "Detalle de Factura"
        verbose_name_plural = "Detalles de Facturas"

    def __str__(self):
        return f"{self.producto} x{self.cantidad}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
