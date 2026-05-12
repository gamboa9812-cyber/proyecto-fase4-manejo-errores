# =============================================================================
# entidades.py
# Clases abstractas base del sistema Software FJ
# =============================================================================

from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """
    Clase abstracta base que representa cualquier entidad del sistema.
    Todas las clases del dominio deben heredar de esta.
    """

    def __init__(self, id_entidad, nombre):
        """
        Constructor de la entidad base.
        
        Args:
            id_entidad (str): Identificador único de la entidad.
            nombre (str): Nombre de la entidad.
        """
        self._id_entidad = id_entidad
        self._nombre = nombre

    @property
    def id_entidad(self):
        """Retorna el identificador único de la entidad."""
        return self._id_entidad

    @property
    def nombre(self):
        """Retorna el nombre de la entidad."""
        return self._nombre

    @abstractmethod
    def describir(self):
        """Método abstracto: cada entidad debe describirse a sí misma."""
        pass

    @abstractmethod
    def validar(self):
        """Método abstracto: cada entidad debe validar sus propios datos."""
        pass

    def __str__(self):
        return f"{self.__class__.__name__}(id={self._id_entidad}, nombre={self._nombre})"


class Servicio(EntidadBase):
    """
    Clase abstracta que representa un servicio ofrecido por Software FJ.
    Los servicios concretos deben heredar de esta clase.
    """

    def __init__(self, id_servicio, nombre, precio_base, disponible=True):
        """
        Constructor del servicio.
        
        Args:
            id_servicio (str): Identificador único del servicio.
            nombre (str): Nombre del servicio.
            precio_base (float): Precio base del servicio.
            disponible (bool): Indica si el servicio está disponible.
        """
        super().__init__(id_servicio, nombre)
        self._precio_base = precio_base
        self._disponible = disponible

    @property
    def precio_base(self):
        """Retorna el precio base del servicio."""
        return self._precio_base

    @property
    def disponible(self):
        """Retorna si el servicio está disponible."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        """Establece la disponibilidad del servicio."""
        self._disponible = valor

    @abstractmethod
    def calcular_costo(self, duracion_horas, **kwargs):
        """
        Método abstracto para calcular el costo del servicio.
        
        Args:
            duracion_horas (float): Duración en horas del servicio.
            **kwargs: Parámetros opcionales (descuento, impuesto, etc.).
        """
        pass

    @abstractmethod
    def describir(self):
        """Describe el servicio de forma detallada."""
        pass

    def validar(self):
        """Valida los datos base del servicio."""
        from excepciones import ErrorServicio, ErrorValidacion
        if not self._nombre or len(self._nombre.strip()) == 0:
            raise ErrorValidacion("nombre", "El nombre del servicio no puede estar vacío.")
        if self._precio_base <= 0:
            raise ErrorValidacion("precio_base", "El precio base debe ser mayor a 0.")
        return True
