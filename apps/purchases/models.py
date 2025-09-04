from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Proveedor(models.Model):
    """
    Modelo para gestionar proveedores.
    
    Almacena información de contacto y detalles de proveedores.
    """
    nombre = models.CharField(
        max_length=150,
        help_text="Nombre del proveedor"
    )
    celular = models.BigIntegerField(
        null=True, 
        blank=True,
        help_text="Número de celular del proveedor"
    )
    direccion = models.TextField(
        blank=True,
        help_text="Dirección física del proveedor"
    )
    email = models.EmailField(
        max_length=100, 
        blank=True,
        help_text="Correo electrónico del proveedor"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Si el proveedor está activo"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de registro del proveedor"
    )

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    """
    Modelo para gestionar compras a proveedores.
    
    Registra las compras realizadas, incluyendo proveedor y total.
    """
    fecha = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de la compra"
    )
    proveedor = models.ForeignKey(
        Proveedor, 
        null=True, 
        blank=True, 
        on_delete=models.PROTECT, 
        related_name='compras',
        help_text="Proveedor de la compra"
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        help_text="Total de la compra"
    )
    observaciones = models.TextField(
        blank=True,
        help_text="Notas adicionales sobre la compra"
    )

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha']

    def __str__(self):
        return f"Compra #{self.pk} - {self.fecha.date()}"
    
    def calcular_total(self):
        """Calcula el total de la compra basado en sus detalles."""
        total = sum(
            detalle.cantidad * detalle.costo_producto 
            for detalle in self.detalles.all()
        )
        return total
    
    def actualizar_total(self):
        """Actualiza el campo total con el cálculo de detalles."""
        self.total = self.calcular_total()
        self.save(update_fields=['total'])

class DetalleCompra(models.Model):
    """
    Modelo para detalles de compras.
    
    Registra los productos individuales dentro de una compra.
    """
    compra = models.ForeignKey(
        Compra, 
        on_delete=models.CASCADE, 
        related_name='detalles'
    )
    producto = models.ForeignKey(
        'inventory.Producto', 
        on_delete=models.PROTECT
    )
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Cantidad comprada"
    )
    costo_producto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Costo unitario del producto"
    )

    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compras"

    def __str__(self):
        return f"{self.producto} x{self.cantidad}"
    
    @property
    def subtotal(self):
        """Calcula el subtotal de este detalle."""
        return self.cantidad * self.costo_producto
