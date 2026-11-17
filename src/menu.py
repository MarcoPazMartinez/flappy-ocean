"""Portada del juego: botones Jugar, Ranking y Salir."""
import pygame

from interfaz import (
    COLOR_BORDE_TITULO,
    COLOR_TITULO,
    TITULO_JUEGO,
    Boton,
    procesar_evento,
    texto_con_borde,
)
from ranking import mostrar_ranking
from recursos import cargar_fondo

COLOR_FONDO_RESPALDO = (20, 60, 140)   # si no se encuentra portada.png


def mostrar_portada(pantalla, reloj):
    """Dibuja la portada y espera a que se elija un botón.

    Devuelve "jugar", "ranking" o "salir".
    """
    ancho, alto = pantalla.get_size()
    centro_x = ancho // 2

    # Todo lo que se puede preparar una sola vez se hace antes del bucle
    fondo = cargar_fondo("portada.png", (ancho, alto), COLOR_FONDO_RESPALDO)

    fuente_titulo = pygame.font.Font(None, 140)
    fuente_boton = pygame.font.Font(None, 52)
    fuente_ayuda = pygame.font.Font(None, 28)

    titulo = texto_con_borde(fuente_titulo, TITULO_JUEGO, COLOR_TITULO, COLOR_BORDE_TITULO, 6)
    # El texto de ayuda va sobre una barra oscura para que se lea bien sobre la imagen
    texto_ayuda = fuente_ayuda.render(
        "Flechas: elegir     Enter: aceptar     Esc: salir", True, (255, 255, 255)
    )
    ayuda = pygame.Surface((texto_ayuda.get_width() + 40, texto_ayuda.get_height() + 16), pygame.SRCALPHA)
    pygame.draw.rect(ayuda, (5, 25, 70, 200), ayuda.get_rect(), border_radius=12)
    ayuda.blit(texto_ayuda, texto_ayuda.get_rect(center=ayuda.get_rect().center))

    botones = [
        Boton("Jugar", "jugar", (centro_x, int(alto * 0.46))),
        Boton("Ranking", "ranking", (centro_x, int(alto * 0.60))),
        Boton("Salir", "salir", (centro_x, int(alto * 0.74))),
    ]
    seleccionado = 0

    while True:
        reloj.tick(60)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "salir"

            seleccionado, accion = procesar_evento(evento, botones, seleccionado)

            if accion is not None:
                return accion

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(titulo, titulo.get_rect(center=(centro_x, int(alto * 0.20))))

        for numero, boton in enumerate(botones):
            boton.dibujar(pantalla, fuente_boton, numero == seleccionado)

        pantalla.blit(ayuda, ayuda.get_rect(midbottom=(centro_x, alto - 20)))

        pygame.display.flip()


def mostrar_menu_principal(pantalla, reloj):
    """Muestra la portada hasta que se elija Jugar o Salir.

    Si se elige Ranking, abre el ranking y al volver muestra la portada de nuevo.
    Devuelve "jugar" o "salir".
    """
    while True:
        accion = mostrar_portada(pantalla, reloj)

        if accion == "ranking":
            if mostrar_ranking(pantalla, reloj) == "salir":
                return "salir"
        else:
            return accion
