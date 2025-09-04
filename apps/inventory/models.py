from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Categoria(models.Model):
    """Modelo para categorías de productos"""
    nombre = models.CharField(max_length=45)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    """Modelo para productos del inventario"""
    nombre = models.CharField(max_length=100, help_text="Nombre del producto")
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
    def tiene_stock(self, cantidad):
        """Verifica si hay stock suficiente"""
        return self.stock_actual >= cantidad
    
    def reducir_stock(self, cantidad):
        """Reduce el stock del producto"""
        if not self.tiene_stock(cantidad):
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock_actual}, Solicitado: {cantidad}")
        self.stock_actual -= cantidad
        self.save(update_fields=['stock_actual'])
    
    def aumentar_stock(self, cantidad):
        """Aumenta el stock del producto"""
        self.stock_actual += cantidad
        self.save(update_fields=['stock_actual'])
