# src/audio.py
import os
import pygame

def inicializar_audio():
    """Inicializa el mixer de pygame para preparar el sistema de audio del juego"""
    pygame.mixer.init()
    
def cargar_sonido(larutadelsonido):
    """Carga un archivo de sonido y devuelve un objeto Sound en pygame"""
    if os.path.exists(larutadelsonido):
        sonido = pygame.mixer.Sound(larutadelsonido)
        return sonido
    print(f"Error: No se pudo cargar el sonido '{larutadelsonido}' porque el archivo no existe.")
    return None

def reproducir_musica(larutadelamusica, volumen=0.3):
    """Reproduce un archivo de música de fondo en bucle"""
    # Corregido: os.path.exists (sin la 'st' de más)
    if os.path.exists(larutadelamusica):
        pygame.mixer.music.load(larutadelamusica)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)  # -1 para repetir en bucle infinito
    else:
        print(f"Error: No se pudo reproducir la música '{larutadelamusica}' porque el archivo no existe.")