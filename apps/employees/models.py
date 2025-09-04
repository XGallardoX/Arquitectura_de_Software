from django.db import models
from django.core.validators import RegexValidator

class Empleado(models.Model):
    """
    Modelo para gestionar empleados del sistema POS.
    
    Maneja información básica de empleados y su estado.
    """
    id = models.CharField(
        primary_key=True, 
        max_length=20, 
        editable=False,
        help_text="ID único del empleado"
    )
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre del empleado"
    )
    apellido = models.CharField(
        max_length=100,
        help_text="Apellido del empleado"
    )
    celular = models.BigIntegerField(
        unique=True,
        help_text="Número de celular único del empleado"
    )
    estado = models.BooleanField(
        default=True,
        help_text="Si el empleado está activo"
    )
    
    # Campos adicionales
    email = models.EmailField(
        max_length=100, 
        blank=True,
        help_text="Correo electrónico del empleado"
    )
    fecha_ingreso = models.DateField(
        auto_now_add=True,
        help_text="Fecha de ingreso del empleado"
    )

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del empleado."""
        return f"{self.nombre} {self.apellido}"
