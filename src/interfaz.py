"""Piezas de interfaz que usan la portada y el ranking: botones y texto con borde."""
import pygame

TITULO_JUEGO = "Flappy Diver"

COLOR_TITULO = (255, 170, 50)
COLOR_BORDE_TITULO = (110, 50, 0)
COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (10, 45, 100, 205)
COLOR_BOTON_RESALTADO = (240, 130, 20, 235)
COLOR_BORDE_BOTON = (255, 255, 255)


def texto_con_borde(fuente, texto, color, color_borde, grosor=4):
    """Devuelve el texto dibujado con un borde de otro color alrededor.

    Es lento de armar (dibuja el texto muchas veces), así que hay que crearlo
    una sola vez, antes del bucle, y después solo dibujarlo.
    """
    base = fuente.render(texto, True, color)
    borde = fuente.render(texto, True, color_borde)

    superficie = pygame.Surface(
        (base.get_width() + grosor * 2, base.get_height() + grosor * 2),
        pygame.SRCALPHA,
    )

    for dx in range(-grosor, grosor + 1):
        for dy in range(-grosor, grosor + 1):
            if dx * dx + dy * dy <= grosor * grosor:
                superficie.blit(borde, (grosor + dx, grosor + dy))

    superficie.blit(base, (grosor, grosor))
    return superficie


class Boton:
    """Un botón rectangular con texto. Se resalta cuando está seleccionado."""

    def __init__(self, texto, accion, centro, tamano=(340, 64)):
        self.texto = texto
        self.accion = accion   # lo que devuelve la pantalla cuando se elige este botón
        self.rect = pygame.Rect((0, 0), tamano)
        self.rect.center = centro

    def contiene(self, posicion):
        return self.rect.collidepoint(posicion)

    def dibujar(self, pantalla, fuente, resaltado):
        fondo = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        color = COLOR_BOTON_RESALTADO if resaltado else COLOR_BOTON

        pygame.draw.rect(fondo, color, fondo.get_rect(), border_radius=16)
        pygame.draw.rect(fondo, COLOR_BORDE_BOTON, fondo.get_rect(), 3, border_radius=16)
        pantalla.blit(fondo, self.rect)

        texto = fuente.render(self.texto, True, COLOR_TEXTO)
        pantalla.blit(texto, texto.get_rect(center=self.rect.center))


def procesar_evento(evento, botones, seleccionado):
    """Maneja mouse y teclado sobre una lista de botones.

    Devuelve (botón seleccionado, acción elegida). La acción es None si todavía
    no se eligió ninguna.
    """
    if evento.type == pygame.MOUSEMOTION:
        for numero, boton in enumerate(botones):
            if boton.contiene(evento.pos):
                seleccionado = numero

    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        for boton in botones:
            if boton.contiene(evento.pos):
                return seleccionado, boton.accion

    elif evento.type == pygame.KEYDOWN:
        if evento.key in (pygame.K_UP, pygame.K_w):
            seleccionado = (seleccionado - 1) % len(botones)
        elif evento.key in (pygame.K_DOWN, pygame.K_s):
            seleccionado = (seleccionado + 1) % len(botones)
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            return seleccionado, botones[seleccionado].accion

    return seleccionado, None
