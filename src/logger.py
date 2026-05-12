# =============================================================================
# logger.py
# Módulo de registro de eventos y errores del sistema Software FJ
# =============================================================================

import datetime
import os


class Logger:
    """
    Clase encargada de registrar todos los eventos y errores del sistema
    en un archivo de logs con marca de tiempo.
    """

    def __init__(self, archivo_log="sistema_log.txt"):
        """
        Inicializa el logger con el nombre del archivo de logs.
        
        Args:
            archivo_log (str): Nombre del archivo donde se guardarán los logs.
        """
        self.archivo_log = archivo_log
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        """Crea el archivo de logs si no existe y escribe el encabezado."""
        try:
            if not os.path.exists(self.archivo_log):
                with open(self.archivo_log, "w", encoding="utf-8") as f:
                    f.write("=" * 70 + "\n")
                    f.write("   SISTEMA DE LOGS - Software FJ\n")
                    f.write(f"   Iniciado: {self._timestamp()}\n")
                    f.write("=" * 70 + "\n\n")
        except Exception as e:
            print(f"[ADVERTENCIA] No se pudo crear el archivo de logs: {e}")

    def _timestamp(self):
        """Retorna la fecha y hora actual formateada."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _escribir(self, nivel, mensaje):
        """
        Escribe una entrada en el archivo de logs.
        
        Args:
            nivel (str): Nivel del log (INFO, ERROR, ADVERTENCIA).
            mensaje (str): Mensaje a registrar.
        """
        try:
            entrada = f"[{self._timestamp()}] [{nivel}] {mensaje}\n"
            with open(self.archivo_log, "a", encoding="utf-8") as f:
                f.write(entrada)
            # También se imprime en consola para seguimiento
            print(entrada.strip())
        except Exception as e:
            print(f"[FALLO LOG] No se pudo escribir en el log: {e}")

    def info(self, mensaje):
        """Registra un evento informativo."""
        self._escribir("INFO", mensaje)

    def error(self, mensaje):
        """Registra un error del sistema."""
        self._escribir("ERROR", mensaje)

    def advertencia(self, mensaje):
        """Registra una advertencia."""
        self._escribir("ADVERTENCIA", mensaje)

    def separador(self):
        """Escribe una línea separadora en el log para mejor legibilidad."""
        try:
            with open(self.archivo_log, "a", encoding="utf-8") as f:
                f.write("-" * 70 + "\n")
        except Exception:
            pass
