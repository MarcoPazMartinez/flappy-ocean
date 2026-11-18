import os

import pygame

from rutas import ruta_recurso


RUTA_SONIDOS = ruta_recurso("assets", "sounds")


# Si la computadora no tiene audio (o está ocupado), el juego sigue sin sonido
# en lugar de cerrarse. Por eso cada función revisa antes si el audio existe.

def audio_disponible():
    """True si el sistema de audio está iniciado."""
    return pygame.mixer.get_init() is not None


def inicializar_audio():
    """Inicializa el sistema de audio de Pygame.

    Devuelve True si pudo; si no hay dispositivo de sonido devuelve False y el
    juego sigue funcionando sin audio.
    """
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        return True

    except pygame.error as error:
        print(f"Aviso: no se pudo iniciar el audio ({error}). El juego sigue sin sonido.")
        return False


def cargar_sonido(nombre_archivo):
    """Carga un efecto de sonido (o devuelve None si no se puede)."""
    if not audio_disponible():
        return None

    ruta = os.path.join(RUTA_SONIDOS, nombre_archivo)

    if os.path.exists(ruta):
        try:
            return pygame.mixer.Sound(ruta)
        except pygame.error as error:
            print(f"Aviso: no se pudo cargar el sonido '{nombre_archivo}' ({error}).")
            return None

    print(f"Error: No se encontró el sonido '{nombre_archivo}'.")
    return None


def reproducir_efecto(sonido):
    """Reproduce un efecto de sonido cargado."""
    if sonido is not None:
        sonido.play()


def reproducir_musica(nombre_archivo="musica_fondo.ogg", volumen=0.3):
    """Carga y reproduce música de fondo en bucle."""
    if not audio_disponible():
        return

    ruta = os.path.join(RUTA_SONIDOS, nombre_archivo)

    if os.path.exists(ruta):
        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(-1)
        except pygame.error as error:
            print(f"Aviso: no se pudo reproducir la música '{nombre_archivo}' ({error}).")
    else:
        print(f"Error: No se encontró la música '{nombre_archivo}'.")


def pausar_musica():
    if audio_disponible():
        pygame.mixer.music.pause()


def reanudar_musica():
    if audio_disponible():
        pygame.mixer.music.unpause()


def detener_musica():
    if audio_disponible():
        pygame.mixer.music.stop()


def cambiar_volumen_musica(volumen):
    if audio_disponible():
        pygame.mixer.music.set_volume(
            max(0.0, min(1.0, volumen))
        )
