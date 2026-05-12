# =============================================================================
# main.py
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Software FJ - Programación 213023 - UNAD
# Fase 4: Manejo avanzado de excepciones
# =============================================================================

from logger import Logger
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import (
    ErrorSistema, ErrorCliente, ErrorServicio, ErrorReserva,
    ErrorValidacion, ErrorDisponibilidad, ErrorCalculoCosto,
    ErrorOperacionNoPermitida
)


def encabezado(titulo, logger):
    """Imprime y registra un encabezado de sección."""
    separador = "=" * 70
    mensaje = f"\n{separador}\n  {titulo}\n{separador}"
    print(mensaje)
    logger.separador()
    logger.info(f"INICIO OPERACIÓN: {titulo}")


def main():
    """
    Función principal que ejecuta las 10 operaciones del sistema.
    Demuestra manejo de excepciones, POO, herencia y polimorfismo.
    """

    # Inicializar el logger del sistema
    logger = Logger("sistema_log.txt")
    logger.info("Sistema Software FJ iniciado correctamente.")

    print("\n" + "=" * 70)
    print("   SISTEMA DE GESTIÓN - Software FJ")
    print("   Programación 213023 - UNAD - Fase 4")
    print("=" * 70)

    # =========================================================================
    # OPERACIÓN 1: Registro de clientes válidos
    # =========================================================================
    encabezado("OPERACIÓN 1: Registro de clientes válidos", logger)

    clientes = []
    try:
        c1 = Cliente("CLI001", "Ana María López", "ana.lopez@email.com", "3001234567", "premium")
        c2 = Cliente("CLI002", "Carlos Ruiz", "carlos.ruiz@gmail.com", "3109876543", "corporativo")
        c3 = Cliente("CLI003", "Lucía Martínez", "lucia.m@empresa.co", "6012345678", "regular")
        clientes.extend([c1, c2, c3])
        for c in clientes:
            logger.info(f"Cliente registrado: {c.describir()}")
        print(f"\n✔ Se registraron {len(clientes)} clientes exitosamente.")
    except ErrorValidacion as e:
        logger.error(f"Error de validación al registrar cliente: {e}")
    except ErrorSistema as e:
        logger.error(f"Error del sistema al registrar clientes: {e}")

    # =========================================================================
    # OPERACIÓN 2: Registro de cliente con datos inválidos
    # =========================================================================
    encabezado("OPERACIÓN 2: Registro de clientes con datos inválidos", logger)

    datos_invalidos = [
        ("CLI004", "Jo", "correo-invalido", "123", "regular"),      # nombre corto + correo malo
        ("CLI005", "Pedro García", "pedro@correo.com", "abc123", "vip"),  # teléfono con letras + tipo inválido
        ("CLI006", "", "maria@test.com", "3001111111", "premium"),  # nombre vacío
    ]

    for datos in datos_invalidos:
        try:
            cliente_invalido = Cliente(*datos)
            logger.advertencia(f"[INESPERADO] Cliente creado sin error: {cliente_invalido}")
        except ErrorValidacion as e:
            logger.error(f"Validación fallida (esperado): {e}")
            print(f"  ✘ Error capturado: {e}")
        except ErrorSistema as e:
            logger.error(f"Error del sistema: {e}")
            print(f"  ✘ Error capturado: {e}")

    # =========================================================================
    # OPERACIÓN 3: Creación de servicios válidos
    # =========================================================================
    encabezado("OPERACIÓN 3: Creación de servicios válidos", logger)

    servicios = []
    try:
        sala1 = ReservaSala("SRV001", "Sala Innovación", 80000, capacidad=10, equipada=True)
        sala2 = ReservaSala("SRV002", "Sala Reuniones A", 50000, capacidad=6, equipada=False)
        equipo1 = AlquilerEquipo("SRV003", "Laptop Dell i7", 25000, "laptop", unidades_disponibles=5)
        equipo2 = AlquilerEquipo("SRV004", "Proyector HD", 30000, "proyector", unidades_disponibles=3)
        asesoria1 = AsesoriaEspecializada("SRV005", "Asesoría Cloud AWS", 120000, "cloud", "avanzado")
        asesoria2 = AsesoriaEspecializada("SRV006", "Asesoría Seguridad", 100000, "seguridad", "intermedio")

        servicios.extend([sala1, sala2, equipo1, equipo2, asesoria1, asesoria2])
        for s in servicios:
            logger.info(f"Servicio registrado: {s.describir()}")
        print(f"\n✔ Se crearon {len(servicios)} servicios exitosamente.")
    except ErrorValidacion as e:
        logger.error(f"Error de validación al crear servicio: {e}")
    except ErrorSistema as e:
        logger.error(f"Error del sistema al crear servicios: {e}")

    # =========================================================================
    # OPERACIÓN 4: Creación de servicios con datos inválidos
    # =========================================================================
    encabezado("OPERACIÓN 4: Creación de servicios con datos inválidos", logger)

    intentos_invalidos = [
        lambda: ReservaSala("SRV099", "Sala Error", -5000, capacidad=10),       # precio negativo
        lambda: AlquilerEquipo("SRV098", "Equipo X", 20000, "", unidades_disponibles=2),  # tipo vacío
        lambda: AsesoriaEspecializada("SRV097", "Asesoría Z", 50000, "marketing", "experto"),  # área y nivel inválidos
    ]

    for intento in intentos_invalidos:
        try:
            servicio_invalido = intento()
            logger.advertencia(f"[INESPERADO] Servicio creado sin error: {servicio_invalido}")
        except ErrorValidacion as e:
            logger.error(f"Validación de servicio fallida (esperado): {e}")
            print(f"  ✘ Error capturado: {e}")
        except ErrorSistema as e:
            logger.error(f"Error del sistema en servicio: {e}")
            print(f"  ✘ Error capturado: {e}")

    # =========================================================================
    # OPERACIÓN 5: Reservas exitosas con polimorfismo en cálculo de costos
    # =========================================================================
    encabezado("OPERACIÓN 5: Reservas exitosas con cálculo de costos", logger)

    reservas_exitosas = []
    try:
        # Reserva 1: Cliente premium reserva sala equipada
        r1 = Reserva(c1, sala1, duracion_horas=3, personas=8)
        costo1 = r1.confirmar()
        reservas_exitosas.append(r1)
        logger.info(f"Reserva confirmada: {r1.describir()}")
        print(f"\n  ✔ {r1.describir()}")
    except ErrorSistema as e:
        logger.error(f"Error en reserva 1: {e}")

    try:
        # Reserva 2: Cliente corporativo alquila equipos
        r2 = Reserva(c2, equipo1, duracion_horas=8, unidades=3)
        costo2 = r2.confirmar()
        reservas_exitosas.append(r2)
        logger.info(f"Reserva confirmada: {r2.describir()}")
        print(f"  ✔ {r2.describir()}")
    except ErrorSistema as e:
        logger.error(f"Error en reserva 2: {e}")

    try:
        # Reserva 3: Cliente regular solicita asesoría urgente
        r3 = Reserva(c3, asesoria1, duracion_horas=2, urgente=True)
        costo3 = r3.confirmar()
        reservas_exitosas.append(r3)
        logger.info(f"Reserva confirmada: {r3.describir()}")
        print(f"  ✔ {r3.describir()}")
    except ErrorSistema as e:
        logger.error(f"Error en reserva 3: {e}")

    # =========================================================================
    # OPERACIÓN 6: Reservas con errores (parámetros inválidos)
    # =========================================================================
    encabezado("OPERACIÓN 6: Reservas con parámetros inválidos", logger)

    try:
        # Error: duración de 0 horas
        r_invalida = Reserva(c1, sala2, duracion_horas=0)
        r_invalida.confirmar()
    except ErrorValidacion as e:
        logger.error(f"Reserva inválida - duración 0: {e}")
        print(f"  ✘ Error capturado: {e}")

    try:
        # Error: más personas que la capacidad de la sala
        r_invalida2 = Reserva(c2, sala2, duracion_horas=2, personas=20)
        r_invalida2.confirmar()
    except ErrorServicio as e:
        logger.error(f"Reserva inválida - excede capacidad: {e}")
        print(f"  ✘ Error capturado: {e}")
    except ErrorSistema as e:
        logger.error(f"Error sistema: {e}")

    try:
        # Error: más unidades de equipo que las disponibles
        r_invalida3 = Reserva(c3, equipo2, duracion_horas=4, unidades=10)
        r_invalida3.confirmar()
    except ErrorServicio as e:
        logger.error(f"Reserva inválida - unidades insuficientes: {e}")
        print(f"  ✘ Error capturado: {e}")
    except ErrorSistema as e:
        logger.error(f"Error sistema: {e}")

    # =========================================================================
    # OPERACIÓN 7: Servicio no disponible (try/except/else)
    # =========================================================================
    encabezado("OPERACIÓN 7: Intento de reserva de servicio no disponible", logger)

    try:
        # Desactivar el servicio
        asesoria2.disponible = False
        logger.advertencia(f"Servicio desactivado: {asesoria2.nombre}")

        r_no_disponible = Reserva(c1, asesoria2, duracion_horas=1)
        r_no_disponible.confirmar()

    except ErrorDisponibilidad as e:
        logger.error(f"Servicio no disponible: {e}")
        print(f"  ✘ Error capturado: {e}")
    else:
        logger.info("Reserva procesada (servicio disponible).")
        print("  ✔ Reserva procesada exitosamente.")
    finally:
        # Reactivar el servicio
        asesoria2.disponible = True
        logger.info(f"Servicio reactivado: {asesoria2.nombre}")
        print(f"  ℹ Servicio '{asesoria2.nombre}' reactivado.")

    # =========================================================================
    # OPERACIÓN 8: Cancelación de reservas y operaciones no permitidas
    # =========================================================================
    encabezado("OPERACIÓN 8: Cancelación de reservas", logger)

    try:
        # Cancelar una reserva confirmada (válido)
        if reservas_exitosas:
            mensaje_cancel = reservas_exitosas[0].cancelar("El cliente cambió de fecha.")
            logger.info(mensaje_cancel)
            print(f"  ✔ {mensaje_cancel}")

        # Intentar cancelar la misma reserva otra vez (inválido)
        reservas_exitosas[0].cancelar("Segundo intento de cancelación.")
    except ErrorOperacionNoPermitida as e:
        logger.error(f"Operación no permitida: {e}")
        print(f"  ✘ Error capturado: {e}")
    except ErrorSistema as e:
        logger.error(f"Error del sistema: {e}")

    # =========================================================================
    # OPERACIÓN 9: Procesar reservas y encadenamiento de excepciones
    # =========================================================================
    encabezado("OPERACIÓN 9: Procesamiento de reservas", logger)

    try:
        # Procesar una reserva confirmada (válido)
        if len(reservas_exitosas) > 1:
            resultado = reservas_exitosas[1].procesar()
            logger.info(resultado)
            print(f"  ✔ {resultado}")

        # Intentar procesar una reserva ya completada (inválido)
        reservas_exitosas[1].procesar()
    except ErrorOperacionNoPermitida as e:
        logger.error(f"Operación no permitida: {e}")
        print(f"  ✘ Error capturado: {e}")

    try:
        # Intentar confirmar una reserva ya cancelada (encadenamiento de excepciones)
        reservas_exitosas[0].confirmar()
    except ErrorOperacionNoPermitida as e:
        try:
            raise ErrorReserva("No se puede retomar una reserva cancelada.") from e
        except ErrorReserva as e2:
            logger.error(f"Excepción encadenada: {e2} | Causa: {e2.__cause__}")
            print(f"  ✘ Excepción encadenada: {e2}")
            print(f"     Causa original: {e2.__cause__}")

    # =========================================================================
    # OPERACIÓN 10: Resumen general del sistema
    # =========================================================================
    encabezado("OPERACIÓN 10: Resumen final del sistema", logger)

    try:
        print("\n  📋 CLIENTES REGISTRADOS:")
        for cliente in clientes:
            print(f"     • {cliente.describir()}")

        print("\n  🛠️  SERVICIOS DISPONIBLES:")
        for servicio in servicios:
            print(f"     • {servicio.describir()}")

        print("\n  📅 RESERVAS DEL SISTEMA:")
        for reserva in reservas_exitosas:
            print(f"     • {reserva.describir()}")

        # Estadísticas generales
        total_ingresos = sum(
            r.costo_total for r in reservas_exitosas
            if r.estado in [Reserva.ESTADO_CONFIRMADA, Reserva.ESTADO_COMPLETADA]
        )
        print(f"\n  💰 INGRESOS PROYECTADOS (reservas activas): ${total_ingresos:,.2f}")
        logger.info(f"Resumen generado. Ingresos proyectados: ${total_ingresos:,.2f}")

    except Exception as e:
        logger.error(f"Error al generar resumen: {e}")
        print(f"  ✘ Error al generar resumen: {e}")
    finally:
        logger.info("Sistema Software FJ finalizado correctamente.")
        print("\n" + "=" * 70)
        print("  Sistema finalizado. Revisa 'sistema_log.txt' para ver el registro completo.")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
