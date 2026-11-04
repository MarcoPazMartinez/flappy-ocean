
import pygame
import os


RUTA_SONIDOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets",
    "sounds"
)


def inicializar_audio():
    """Inicializa el sistema de audio de Pygame."""
    if not pygame.mixer.get_init():
        pygame.mixer.init()


def cargar_sonido(nombre_archivo):
    """Carga un efecto de sonido."""
    ruta = os.path.join(RUTA_SONIDOS, nombre_archivo)

    if os.path.exists(ruta):
        return pygame.mixer.Sound(ruta)

    print(f"Error: No se encontró el sonido '{nombre_archivo}'.")
    return None


def reproducir_efecto(sonido):
    """Reproduce un efecto de sonido cargado."""
    if sonido is not None:
        sonido.play()


def reproducir_musica(nombre_archivo="musica_fondo.ogg", volumen=0.3):
    """Carga y reproduce música de fondo en bucle."""
    ruta = os.path.join(RUTA_SONIDOS, nombre_archivo)

    if os.path.exists(ruta):
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)
    else:
        print(f"Error: No se encontró la música '{nombre_archivo}'.")


def pausar_musica():
    pygame.mixer.music.pause()


def reanudar_musica():
    pygame.mixer.music.unpause()


def detener_musica():
    pygame.mixer.music.stop()


def cambiar_volumen_musica(volumen):
    pygame.mixer.music.set_volume(
        max(0.0, min(1.0, volumen))
    )
