# =============================================================================
# servicios.py
# Clases concretas de servicios especializados de Software FJ
# Herencia, polimorfismo y métodos sobrescritos
# =============================================================================

from entidades import Servicio
from excepciones import ErrorServicio, ErrorValidacion, ErrorCalculoCosto, ErrorDisponibilidad


# =============================================================================
# SERVICIO 1: Reserva de Sala
# =============================================================================

class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de reuniones o conferencias.
    Hereda de la clase abstracta Servicio.
    """

    def __init__(self, id_servicio, nombre, precio_base, capacidad, equipada=False, disponible=True):
        """
        Constructor del servicio de reserva de sala.

        Args:
            id_servicio (str): ID único del servicio.
            nombre (str): Nombre de la sala.
            precio_base (float): Precio base por hora.
            capacidad (int): Capacidad máxima de personas.
            equipada (bool): Si la sala incluye equipos audiovisuales.
            disponible (bool): Disponibilidad del servicio.
        """
        super().__init__(id_servicio, nombre, precio_base, disponible)
        self._capacidad = capacidad
        self._equipada = equipada
        self.validar()

    @property
    def capacidad(self):
        """Retorna la capacidad de la sala."""
        return self._capacidad

    def calcular_costo(self, duracion_horas, descuento=0.0, impuesto=0.19, personas=1):
        """
        Calcula el costo total de la reserva de sala.

        Args:
            duracion_horas (float): Horas de uso de la sala.
            descuento (float): Porcentaje de descuento (0.0 a 1.0).
            impuesto (float): Porcentaje de impuesto (por defecto 19% IVA).
            personas (int): Número de personas (valida contra capacidad).

        Returns:
            float: Costo total calculado.
        """
        try:
            # Validación de parámetros
            if duracion_horas <= 0:
                raise ErrorCalculoCosto("La duración debe ser mayor a 0 horas.")
            if personas > self._capacidad:
                raise ErrorServicio(
                    f"La sala '{self._nombre}' tiene capacidad para {self._capacidad} personas, "
                    f"pero se solicitaron {personas}."
                )
            if not self._disponible:
                raise ErrorDisponibilidad(self._nombre)

            # Cálculo del costo
            subtotal = self._precio_base * duracion_horas
            # Recargo del 20% si la sala está equipada
            if self._equipada:
                subtotal *= 1.20
            # Aplicar descuento
            subtotal -= subtotal * descuento
            # Aplicar impuesto
            total = subtotal * (1 + impuesto)
            return round(total, 2)

        except (ErrorCalculoCosto, ErrorServicio, ErrorDisponibilidad):
            raise  # Re-lanzar excepciones del sistema
        except Exception as e:
            raise ErrorCalculoCosto(f"Error inesperado en cálculo de sala: {e}") from e

    def describir(self):
        """Describe el servicio de sala de forma detallada."""
        equipada_txt = "Sí" if self._equipada else "No"
        disponible_txt = "Disponible" if self._disponible else "No disponible"
        return (
            f"[SALA] {self._nombre} | ID: {self._id_entidad} | "
            f"Precio/hora: ${self._precio_base:,.0f} | "
            f"Capacidad: {self._capacidad} personas | "
            f"Equipada: {equipada_txt} | Estado: {disponible_txt}"
        )

    def validar(self):
        """Valida los datos específicos del servicio de sala."""
        super().validar()
        if self._capacidad <= 0:
            raise ErrorValidacion("capacidad", "La capacidad de la sala debe ser mayor a 0.")
        return True


# =============================================================================
# SERVICIO 2: Alquiler de Equipos
# =============================================================================

class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    Hereda de la clase abstracta Servicio.
    """

    def __init__(self, id_servicio, nombre, precio_base, tipo_equipo, unidades_disponibles, disponible=True):
        """
        Constructor del servicio de alquiler de equipos.

        Args:
            id_servicio (str): ID único del servicio.
            nombre (str): Nombre del equipo.
            precio_base (float): Precio base por hora por unidad.
            tipo_equipo (str): Tipo de equipo (laptop, proyector, tablet, etc.).
            unidades_disponibles (int): Número de unidades disponibles.
            disponible (bool): Disponibilidad general del servicio.
        """
        super().__init__(id_servicio, nombre, precio_base, disponible)
        self._tipo_equipo = tipo_equipo
        self._unidades_disponibles = unidades_disponibles
        self.validar()

    @property
    def unidades_disponibles(self):
        """Retorna las unidades disponibles."""
        return self._unidades_disponibles

    @unidades_disponibles.setter
    def unidades_disponibles(self, valor):
        """Actualiza las unidades disponibles."""
        if valor < 0:
            raise ErrorValidacion("unidades", "Las unidades no pueden ser negativas.")
        self._unidades_disponibles = valor

    def calcular_costo(self, duracion_horas, descuento=0.0, impuesto=0.19, unidades=1):
        """
        Calcula el costo total del alquiler de equipos.

        Args:
            duracion_horas (float): Horas de alquiler.
            descuento (float): Porcentaje de descuento.
            impuesto (float): Porcentaje de impuesto.
            unidades (int): Cantidad de unidades a alquilar.

        Returns:
            float: Costo total calculado.
        """
        try:
            if duracion_horas <= 0:
                raise ErrorCalculoCosto("La duración debe ser mayor a 0 horas.")
            if unidades <= 0:
                raise ErrorCalculoCosto("La cantidad de unidades debe ser mayor a 0.")
            if unidades > self._unidades_disponibles:
                raise ErrorServicio(
                    f"Solo hay {self._unidades_disponibles} unidades de '{self._nombre}' disponibles, "
                    f"se solicitaron {unidades}."
                )
            if not self._disponible:
                raise ErrorDisponibilidad(self._nombre)

            # Cálculo: precio_hora * horas * unidades
            subtotal = self._precio_base * duracion_horas * unidades
            # Descuento por volumen (más de 3 unidades = 5% extra)
            if unidades > 3:
                subtotal *= 0.95
            subtotal -= subtotal * descuento
            total = subtotal * (1 + impuesto)
            return round(total, 2)

        except (ErrorCalculoCosto, ErrorServicio, ErrorDisponibilidad):
            raise
        except Exception as e:
            raise ErrorCalculoCosto(f"Error inesperado en cálculo de equipo: {e}") from e

    def describir(self):
        """Describe el servicio de alquiler de equipo."""
        disponible_txt = "Disponible" if self._disponible else "No disponible"
        return (
            f"[EQUIPO] {self._nombre} | ID: {self._id_entidad} | "
            f"Tipo: {self._tipo_equipo} | "
            f"Precio/hora/unidad: ${self._precio_base:,.0f} | "
            f"Unidades: {self._unidades_disponibles} | Estado: {disponible_txt}"
        )

    def validar(self):
        """Valida los datos del equipo."""
        super().validar()
        if self._unidades_disponibles < 0:
            raise ErrorValidacion("unidades_disponibles", "Las unidades no pueden ser negativas.")
        if not self._tipo_equipo or len(self._tipo_equipo.strip()) == 0:
            raise ErrorValidacion("tipo_equipo", "El tipo de equipo no puede estar vacío.")
        return True


# =============================================================================
# SERVICIO 3: Asesoría Especializada
# =============================================================================

class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoría especializada por expertos de Software FJ.
    Hereda de la clase abstracta Servicio.
    """

    AREAS_VALIDAS = ["sistemas", "redes", "seguridad", "datos", "software", "cloud"]

    def __init__(self, id_servicio, nombre, precio_base, area, nivel="basico", disponible=True):
        """
        Constructor del servicio de asesoría.

        Args:
            id_servicio (str): ID único del servicio.
            nombre (str): Nombre de la asesoría.
            precio_base (float): Precio base por hora.
            area (str): Área de especialización.
            nivel (str): Nivel de la asesoría: 'basico', 'intermedio', 'avanzado'.
            disponible (bool): Disponibilidad del servicio.
        """
        super().__init__(id_servicio, nombre, precio_base, disponible)
        self._area = area.lower()
        self._nivel = nivel.lower()
        self.validar()

    @property
    def area(self):
        """Retorna el área de la asesoría."""
        return self._area

    @property
    def nivel(self):
        """Retorna el nivel de la asesoría."""
        return self._nivel

    def calcular_costo(self, duracion_horas, descuento=0.0, impuesto=0.19, urgente=False):
        """
        Calcula el costo de la asesoría especializada.

        Args:
            duracion_horas (float): Horas de asesoría.
            descuento (float): Porcentaje de descuento.
            impuesto (float): Porcentaje de impuesto.
            urgente (bool): Si la asesoría es urgente (recargo del 30%).

        Returns:
            float: Costo total calculado.
        """
        try:
            if duracion_horas <= 0:
                raise ErrorCalculoCosto("La duración debe ser mayor a 0 horas.")
            if not self._disponible:
                raise ErrorDisponibilidad(self._nombre)

            # Factor por nivel de asesoría
            factores_nivel = {"basico": 1.0, "intermedio": 1.5, "avanzado": 2.0}
            factor = factores_nivel.get(self._nivel, 1.0)

            subtotal = self._precio_base * duracion_horas * factor

            # Recargo por urgencia
            if urgente:
                subtotal *= 1.30

            subtotal -= subtotal * descuento
            total = subtotal * (1 + impuesto)
            return round(total, 2)

        except (ErrorCalculoCosto, ErrorDisponibilidad):
            raise
        except Exception as e:
            raise ErrorCalculoCosto(f"Error inesperado en cálculo de asesoría: {e}") from e

    def describir(self):
        """Describe el servicio de asesoría especializada."""
        disponible_txt = "Disponible" if self._disponible else "No disponible"
        return (
            f"[ASESORÍA] {self._nombre} | ID: {self._id_entidad} | "
            f"Área: {self._area} | Nivel: {self._nivel} | "
            f"Precio/hora: ${self._precio_base:,.0f} | Estado: {disponible_txt}"
        )

    def validar(self):
        """Valida los datos de la asesoría."""
        super().validar()
        if self._area not in self.AREAS_VALIDAS:
            raise ErrorValidacion(
                "area",
                f"Área '{self._area}' no válida. Áreas permitidas: {', '.join(self.AREAS_VALIDAS)}"
            )
        if self._nivel not in ["basico", "intermedio", "avanzado"]:
            raise ErrorValidacion("nivel", "El nivel debe ser: basico, intermedio o avanzado.")
        return True
