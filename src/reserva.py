# =============================================================================
# reserva.py
# Clase Reserva - Integra cliente, servicio, duración y estado
# Software FJ - Sistema de Gestión
# =============================================================================

import datetime
from excepciones import (
    ErrorReserva, ErrorOperacionNoPermitida,
    ErrorCalculoCosto, ErrorDisponibilidad, ErrorValidacion
)


class Reserva:
    """
    Clase que representa una reserva de servicio en Software FJ.
    Integra cliente, servicio, duración y estado con manejo de excepciones.
    """

    # Estados válidos de una reserva
    ESTADO_PENDIENTE   = "pendiente"
    ESTADO_CONFIRMADA  = "confirmada"
    ESTADO_CANCELADA   = "cancelada"
    ESTADO_COMPLETADA  = "completada"

    # Contador para generar IDs automáticos
    _contador = 1

    def __init__(self, cliente, servicio, duracion_horas, **kwargs):
        """
        Constructor de la reserva.

        Args:
            cliente (Cliente): Objeto cliente que realiza la reserva.
            servicio (Servicio): Objeto servicio a reservar.
            duracion_horas (float): Duración de la reserva en horas.
            **kwargs: Parámetros adicionales para el cálculo del costo
                      (descuento, impuesto, personas, unidades, urgente, etc.)
        """
        self._id_reserva    = f"RES-{Reserva._contador:04d}"
        Reserva._contador  += 1
        self._cliente       = cliente
        self._servicio      = servicio
        self._duracion_horas = duracion_horas
        self._kwargs        = kwargs
        self._estado        = self.ESTADO_PENDIENTE
        self._fecha_creacion = datetime.datetime.now()
        self._costo_total   = 0.0
        self._validar_creacion()

    # -------------------------------------------------------------------------
    # Propiedades
    # -------------------------------------------------------------------------

    @property
    def id_reserva(self):
        """Retorna el ID de la reserva."""
        return self._id_reserva

    @property
    def estado(self):
        """Retorna el estado actual de la reserva."""
        return self._estado

    @property
    def cliente(self):
        """Retorna el cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self):
        """Retorna el servicio asociado a la reserva."""
        return self._servicio

    @property
    def costo_total(self):
        """Retorna el costo total de la reserva."""
        return self._costo_total

    # -------------------------------------------------------------------------
    # Validación interna
    # -------------------------------------------------------------------------

    def _validar_creacion(self):
        """Valida que los datos básicos de la reserva sean correctos."""
        if self._duracion_horas <= 0:
            raise ErrorValidacion("duracion_horas", "La duración debe ser mayor a 0.")
        if self._duracion_horas > 24:
            raise ErrorValidacion("duracion_horas", "La duración no puede superar las 24 horas.")
        if self._cliente is None:
            raise ErrorReserva("La reserva debe tener un cliente asociado.")
        if self._servicio is None:
            raise ErrorReserva("La reserva debe tener un servicio asociado.")

    # -------------------------------------------------------------------------
    # Métodos de gestión de la reserva
    # -------------------------------------------------------------------------

    def confirmar(self):
        """
        Confirma la reserva si está en estado pendiente.
        Calcula el costo total aplicando el descuento del cliente.

        Returns:
            float: Costo total de la reserva confirmada.
        """
        try:
            # Verificar que la reserva esté en estado pendiente
            if self._estado != self.ESTADO_PENDIENTE:
                raise ErrorOperacionNoPermitida(
                    f"No se puede confirmar una reserva en estado '{self._estado}'."
                )

            # Verificar disponibilidad del servicio
            if not self._servicio.disponible:
                raise ErrorDisponibilidad(self._servicio.nombre)

            # Incorporar el descuento del cliente automáticamente
            kwargs_calculo = dict(self._kwargs)
            descuento_cliente = self._cliente.obtener_descuento()
            # El descuento del cliente se suma al descuento adicional si existe
            descuento_adicional = kwargs_calculo.get("descuento", 0.0)
            kwargs_calculo["descuento"] = min(descuento_cliente + descuento_adicional, 0.5)

            # Calcular el costo
            self._costo_total = self._servicio.calcular_costo(
                self._duracion_horas, **kwargs_calculo
            )
            self._estado = self.ESTADO_CONFIRMADA

            # Agregar la reserva al historial del cliente
            self._cliente.agregar_reserva(self)

            return self._costo_total

        except (ErrorOperacionNoPermitida, ErrorDisponibilidad, ErrorCalculoCosto):
            raise  # Re-lanzar excepciones del sistema
        except Exception as e:
            raise ErrorReserva(f"Error al confirmar la reserva: {e}") from e

        finally:
            # Este bloque siempre se ejecuta, registra el intento
            pass  # El logger se maneja en el sistema principal

    def cancelar(self, motivo="Sin motivo especificado"):
        """
        Cancela la reserva si está en estado pendiente o confirmada.

        Args:
            motivo (str): Motivo de la cancelación.
        """
        try:
            if self._estado == self.ESTADO_CANCELADA:
                raise ErrorOperacionNoPermitida("La reserva ya está cancelada.")
            if self._estado == self.ESTADO_COMPLETADA:
                raise ErrorOperacionNoPermitida("No se puede cancelar una reserva completada.")

            self._estado = self.ESTADO_CANCELADA
            return f"Reserva {self._id_reserva} cancelada. Motivo: {motivo}"

        except ErrorOperacionNoPermitida:
            raise
        except Exception as e:
            raise ErrorReserva(f"Error al cancelar la reserva: {e}") from e

    def procesar(self):
        """
        Procesa (completa) la reserva si está confirmada.
        Simula la ejecución del servicio.
        """
        try:
            if self._estado != self.ESTADO_CONFIRMADA:
                raise ErrorOperacionNoPermitida(
                    f"Solo se pueden procesar reservas confirmadas. Estado actual: '{self._estado}'."
                )
            self._estado = self.ESTADO_COMPLETADA
            return f"Reserva {self._id_reserva} procesada exitosamente."

        except ErrorOperacionNoPermitida:
            raise
        except Exception as e:
            raise ErrorReserva(f"Error al procesar la reserva: {e}") from e

    # -------------------------------------------------------------------------
    # Métodos de descripción
    # -------------------------------------------------------------------------

    def describir(self):
        """Retorna una descripción completa de la reserva."""
        return (
            f"Reserva ID: {self._id_reserva} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion_horas}h | "
            f"Estado: {self._estado.upper()} | "
            f"Costo Total: ${self._costo_total:,.2f} | "
            f"Fecha: {self._fecha_creacion.strftime('%Y-%m-%d %H:%M')}"
        )

    def __repr__(self):
        return (
            f"Reserva(id={self._id_reserva}, cliente={self._cliente.nombre}, "
            f"servicio={self._servicio.nombre}, estado={self._estado})"
        )
