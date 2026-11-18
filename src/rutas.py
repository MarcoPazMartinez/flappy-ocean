"""Dónde están los recursos del juego y dónde se guardan los datos.

Funciona igual ejecutando el código normalmente (`python main.py`) que dentro del
ejecutable (.exe) que genera PyInstaller. La diferencia es esta:

- **Recursos** (imágenes, sonidos): vienen "adentro" del juego y no cambian.
  En el .exe, PyInstaller los descomprime en una carpeta temporal (`sys._MEIPASS`).
- **Datos** (la base del ranking): tienen que **sobrevivir** a cerrar el juego.
  La carpeta temporal del .exe se borra al cerrarlo, así que ahí no sirve: se
  guardan al lado del .exe.
"""
import os
import sys

NOMBRE_CARPETA_RESPALDO = "FlappyDiver"


def esta_empaquetado():
    """True si el juego corre dentro del .exe generado con PyInstaller."""
    return getattr(sys, "frozen", False)


def carpeta_recursos():
    """Carpeta que contiene `assets/`."""
    if esta_empaquetado():
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))

    # Código normal: la raíz del repositorio (una carpeta arriba de src/)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _se_puede_escribir(carpeta):
    """True si se pueden crear archivos en la carpeta (la crea si hace falta)."""
    try:
        os.makedirs(carpeta, exist_ok=True)
        return os.access(carpeta, os.W_OK)
    except OSError:
        return False


def carpeta_datos():
    """Carpeta donde se guarda lo que debe persistir (el ranking en `database/`).

    - Código normal: la raíz del repositorio.
    - .exe: la carpeta donde está el .exe. Si ahí no se puede escribir (por ejemplo,
      un pendrive protegido), se usa una carpeta `FlappyDiver` dentro de la carpeta
      personal del usuario, para que el ranking igual funcione.
    """
    if not esta_empaquetado():
        return carpeta_recursos()

    junto_al_exe = os.path.dirname(os.path.abspath(sys.executable))

    if _se_puede_escribir(os.path.join(junto_al_exe, "database")):
        return junto_al_exe

    respaldo = os.path.join(os.path.expanduser("~"), NOMBRE_CARPETA_RESPALDO)
    _se_puede_escribir(respaldo)        # la crea si no existe

    return respaldo


def ruta_recurso(*partes):
    """Ruta a un archivo de recursos. Ejemplo: ruta_recurso("assets", "images", "jugador.png")."""
    return os.path.join(carpeta_recursos(), *partes)


def ruta_dato(*partes):
    """Ruta a un archivo de datos. Ejemplo: ruta_dato("database", "ranking.db")."""
    return os.path.join(carpeta_datos(), *partes)
