from django.db import models

class DetalleImpuesto(models.Model):
    """
    Modelo para configurar diferentes tipos de impuestos.
    
    Usado por múltiples módulos (ventas, compras) para calcular impuestos.
    """
    nombre = models.CharField(max_length=45)
    impuesto = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        verbose_name = "Detalle de Impuesto"
        verbose_name_plural = "Detalles de Impuestos"

    def __str__(self):
        return f"{self.nombre} ({self.impuesto}%)"
