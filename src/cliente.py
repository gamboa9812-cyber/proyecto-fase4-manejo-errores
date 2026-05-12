# =============================================================================
# cliente.py
# Clase Cliente con validaciones robustas y encapsulación - Software FJ
# =============================================================================

import re
from entidades import EntidadBase
from excepciones import ErrorCliente, ErrorValidacion


class Cliente(EntidadBase):
    """
    Clase que representa a un cliente de Software FJ.
    Implementa encapsulación de datos personales con validaciones estrictas.
    """

    def __init__(self, id_cliente, nombre, correo, telefono, tipo="regular"):
        """
        Constructor del cliente.

        Args:
            id_cliente (str): Identificador único del cliente.
            nombre (str): Nombre completo del cliente.
            correo (str): Correo electrónico del cliente.
            telefono (str): Teléfono de contacto.
            tipo (str): Tipo de cliente: 'regular', 'premium' o 'corporativo'.
        """
        super().__init__(id_cliente, nombre)
        self._correo = correo
        self._telefono = telefono
        self._tipo = tipo
        self._reservas = []  # Lista interna de reservas del cliente
        self.validar()       # Validar al momento de crear

    # -------------------------------------------------------------------------
    # Propiedades (getters y setters con encapsulación)
    # -------------------------------------------------------------------------

    @property
    def correo(self):
        """Retorna el correo del cliente."""
        return self._correo

    @correo.setter
    def correo(self, nuevo_correo):
        """Actualiza el correo con validación."""
        if not self._validar_correo(nuevo_correo):
            raise ErrorValidacion("correo", "El formato del correo no es válido.")
        self._correo = nuevo_correo

    @property
    def telefono(self):
        """Retorna el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        """Actualiza el teléfono con validación."""
        if not self._validar_telefono(nuevo_telefono):
            raise ErrorValidacion("telefono", "El teléfono debe tener entre 7 y 15 dígitos.")
        self._telefono = nuevo_telefono

    @property
    def tipo(self):
        """Retorna el tipo de cliente."""
        return self._tipo

    @property
    def reservas(self):
        """Retorna la lista de reservas del cliente (copia protegida)."""
        return list(self._reservas)

    # -------------------------------------------------------------------------
    # Métodos privados de validación
    # -------------------------------------------------------------------------

    def _validar_correo(self, correo):
        """Verifica que el correo tenga un formato válido usando expresión regular."""
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(patron, correo) is not None

    def _validar_telefono(self, telefono):
        """Verifica que el teléfono contenga solo dígitos y tenga longitud válida."""
        return telefono.isdigit() and 7 <= len(telefono) <= 15

    def _validar_tipo(self, tipo):
        """Verifica que el tipo de cliente sea uno de los permitidos."""
        return tipo in ["regular", "premium", "corporativo"]

    # -------------------------------------------------------------------------
    # Métodos públicos
    # -------------------------------------------------------------------------

    def validar(self):
        """
        Valida todos los datos del cliente.
        Lanza excepciones si algún campo es inválido.
        """
        if not self._nombre or len(self._nombre.strip()) < 3:
            raise ErrorValidacion("nombre", "El nombre debe tener al menos 3 caracteres.")
        if not self._validar_correo(self._correo):
            raise ErrorValidacion("correo", "El formato del correo no es válido.")
        if not self._validar_telefono(self._telefono):
            raise ErrorValidacion("telefono", "El teléfono debe tener entre 7 y 15 dígitos numéricos.")
        if not self._validar_tipo(self._tipo):
            raise ErrorValidacion("tipo", f"Tipo '{self._tipo}' no válido. Use: regular, premium, corporativo.")
        return True

    def agregar_reserva(self, reserva):
        """
        Agrega una reserva a la lista interna del cliente.

        Args:
            reserva: Objeto Reserva asociado al cliente.
        """
        self._reservas.append(reserva)

    def obtener_descuento(self):
        """
        Retorna el porcentaje de descuento según el tipo de cliente.
        
        Returns:
            float: Porcentaje de descuento (0.0 a 1.0).
        """
        descuentos = {
            "regular": 0.0,
            "premium": 0.10,
            "corporativo": 0.20
        }
        return descuentos.get(self._tipo, 0.0)

    def describir(self):
        """Retorna una descripción completa del cliente."""
        return (
            f"Cliente: {self._nombre} | ID: {self._id_entidad} | "
            f"Correo: {self._correo} | Teléfono: {self._telefono} | "
            f"Tipo: {self._tipo} | Reservas activas: {len(self._reservas)}"
        )

    def __repr__(self):
        return f"Cliente(id={self._id_entidad}, nombre='{self._nombre}', tipo='{self._tipo}')"
