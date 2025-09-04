from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class BaseService(ABC):
    """
    Clase base para todos los servicios de negocio.
    
    Proporciona funcionalidades comunes como logging, validaciones y manejo de errores.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def log_operation(self, operation: str, details: str = ""):
        """Registra operaciones importantes para auditoría."""
        self.logger.info(f"{operation}: {details}")
    
    def validate_required_fields(self, data: Dict, required_fields: List[str]):
        """
        Valida que todos los campos requeridos estén presentes.
        
        Args:
            data (Dict): Datos a validar
            required_fields (List[str]): Lista de campos requeridos
            
        Raises:
            ValueError: Si falta algún campo requerido
        """
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing_fields)}")
