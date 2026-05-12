# =============================================================================
# excepciones.py
# Módulo de excepciones personalizadas del sistema Software FJ
# =============================================================================

class ErrorSistema(Exception):
    """Excepción base del sistema. Todas las excepciones heredan de esta."""
    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        if self.codigo:
            return f"[Código {self.codigo}] {self.mensaje}"
        return self.mensaje


class ErrorCliente(ErrorSistema):
    """Excepción para errores relacionados con clientes."""
    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="CLI-001")


class ErrorServicio(ErrorSistema):
    """Excepción para errores relacionados con servicios."""
    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="SRV-002")


class ErrorReserva(ErrorSistema):
    """Excepción para errores relacionados con reservas."""
    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="RES-003")


class ErrorValidacion(ErrorSistema):
    """Excepción para errores de validación de datos."""
    def __init__(self, campo, mensaje):
        super().__init__(f"Campo '{campo}': {mensaje}", codigo="VAL-004")
        self.campo = campo


class ErrorDisponibilidad(ErrorSistema):
    """Excepción cuando un servicio no está disponible."""
    def __init__(self, servicio):
        super().__init__(f"El servicio '{servicio}' no está disponible.", codigo="DIS-005")


class ErrorCalculoCosto(ErrorSistema):
    """Excepción para errores en el cálculo de costos."""
    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="COS-006")


class ErrorOperacionNoPermitida(ErrorSistema):
    """Excepción para operaciones no permitidas."""
    def __init__(self, operacion):
        super().__init__(f"Operación no permitida: {operacion}", codigo="OPE-007")
