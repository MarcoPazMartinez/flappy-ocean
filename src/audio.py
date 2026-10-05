import os
import pygame

def inicializar_audio():
    "inicializa el mixer de pygame para preparar el sistema de audio del juego"
    pygame.mixer.init()
    
def cargar_sonido(larutadelsonido):
    "carga un archivo de sonido y devuelve un objeto sound en pygame"
    
    if os.path.exists(larutadelsonido):
        sonido = pygame.mixer.Sound(larutadelsonido)
        return sonido
    print(f"Error: No se pudo cargar el sonido '{larutadelsonido}' porque el archivo no existe.")
    return None

def reproducir_musica(larutadelamusica, volumen=0.3):
    "reproduce un archivo de música de fondo en bucle"
    if os.path.existists(larutadelamusica):
        pygame.mixer.music.load(larutadelamusica)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)
    else:
        print(f"Error: No se pudo reproducir la música '{larutadelamusica}' porque el archivo no existe.")
        
        