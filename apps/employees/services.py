from typing import Dict, List
from django.db import transaction

from .models import Empleado
from core.services.base_service import BaseService

class EmployeesService(BaseService):
    """
    Servicio para gestión de empleados.
    
    Maneja operaciones relacionadas con empleados:
    - Registrar empleados
    - Actualizar información
    - Gestión de estados (activo/inactivo)
    - Validaciones específicas
    """
    
    @transaction.atomic
    def registrar_empleado(self, empleado_data: Dict) -> Empleado:
        """Registra un nuevo empleado."""
        campos_requeridos = ['id', 'nombre', 'apellido', 'celular']
        self.validate_required_fields(empleado_data, campos_requeridos)
        
        # Validaciones específicas
        if Empleado.objects.filter(id=empleado_data['id']).exists():
            raise ValueError(f"Ya existe un empleado con ID {empleado_data['id']}")
        
        if Empleado.objects.filter(celular=empleado_data['celular']).exists():
            raise ValueError(f"Ya existe un empleado con el celular {empleado_data['celular']}")
        
        empleado = Empleado.objects.create(
            id=empleado_data['id'],
            nombre=empleado_data['nombre'].strip(),
            apellido=empleado_data['apellido'].strip(),
            celular=empleado_data['celular'],
            email=empleado_data.get('email', ''),
            estado=True
        )
        
        self.log_operation("EMPLEADO_REGISTRADO", f"ID: {empleado.id}, Nombre: {empleado.nombre_completo}")
        return empleado
    
    def actualizar_empleado(self, empleado_id: str, empleado_data: Dict) -> Empleado:
        """Actualiza un empleado existente."""
        try:
            empleado = Empleado.objects.get(id=empleado_id)
        except Empleado.DoesNotExist:
            raise ValueError(f"Empleado con ID {empleado_id} no encontrado")
        
        # Actualizar campos permitidos
        campos_actualizables = ['nombre', 'apellido', 'celular', 'email', 'estado']
        for campo, valor in empleado_data.items():
            if campo in campos_actualizables and hasattr(empleado, campo):
                setattr(empleado, campo, valor)
        
        empleado.save()
        self.log_operation("EMPLEADO_ACTUALIZADO", f"ID: {empleado_id}")
        return empleado
    
    def cambiar_estado_empleado(self, empleado_id: str, activo: bool) -> Empleado:
        """Cambia el estado de un empleado (activo/inactivo)."""
        return self.actualizar_empleado(empleado_id, {'estado': activo})
    
    def obtener_empleados_activos(self) -> List[Empleado]:
        """Obtiene todos los empleados activos."""
        return list(Empleado.objects.filter(estado=True).order_by('nombre'))
