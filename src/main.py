import sys

import pygame

import db
from audio import (
    cargar_sonido,
    detener_musica,
    inicializar_audio,
    reproducir_musica,
)
from fin_de_partida import finalizar_partida
from interfaz import TITULO_JUEGO
from menu import mostrar_menu_principal
from partida import jugar
from rutas import ruta_recurso
from verificacion import verificar

ANCHO, ALTO = 1280, 720


def poner_icono():
    """Icono de la ventana: el pez. Si no se puede, queda el de pygame."""

    try:
        pygame.display.set_icon(pygame.image.load(ruta_recurso("assets", "images", "jugador.png")))
    except (pygame.error, FileNotFoundError):
        pass


def main():

    # `python main.py --verificar` (o `FlappyDiver.exe --verificar`): comprueba que el
    # juego está completo, sin abrir nada para jugar
    if "--verificar" in sys.argv[1:]:
        sys.exit(0 if verificar() else 1)

    pygame.init()

    poner_icono()                  # antes de crear la ventana

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO_JUEGO)

    reloj = pygame.time.Clock()

    # Audio
    inicializar_audio()

    sonidos = {
        "salto": cargar_sonido("salto.ogg"),
        "colision": cargar_sonido("colision.wav"),
        "perder": cargar_sonido("perder.ogg"),
    }

    reproducir_musica("musica_fondo.ogg", volumen=0.3)

    # Base de datos del ranking: se crea si no existe y se comprueba que responda
    base_ok, detalle = db.comprobar_base()
    print(f"Base de datos {'OK' if base_ok else 'CON PROBLEMAS'}: {detalle}")

    # Portada -> partida -> final -> portada ... hasta que se elija salir
    while True:

        if mostrar_menu_principal(pantalla, reloj) == "salir":
            break

        resultado = jugar(pantalla, reloj, sonidos)

        if resultado.estado == "salir":
            break

        if finalizar_partida(pantalla, reloj, resultado) == "salir":
            break

    detener_musica()

    pygame.quit()


if __name__ == "__main__":
    main()
