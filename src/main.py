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

ANCHO, ALTO = 1280, 720


def main():

    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO_JUEGO)

    reloj = pygame.time.Clock()

    # Audio
    inicializar_audio()

    sonidos = {
        "salto": cargar_sonido("salto.ogg"),
        "colision": cargar_sonido("colision.ogg"),
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
