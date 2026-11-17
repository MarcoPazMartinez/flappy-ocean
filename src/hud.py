import pygame

ALTO_BARRA = 52
COLOR_BARRA = (5, 20, 55, 190)        # azul oscuro, un poco transparente
COLOR_LINEA_BARRA = (255, 255, 255, 90)

# La barra se dibuja una sola vez por ancho de pantalla y se reutiliza
_barras = {}


def inicializar_fuente(tamano=36):
    """Carga la fuente una sola vez para optimizar rendimiento."""
    return pygame.font.Font(None, tamano)


def crear_barra(ancho):
    """Barra semitransparente para que el texto se lea sobre cualquier fondo."""

    if ancho not in _barras:

        barra = pygame.Surface((ancho, ALTO_BARRA), pygame.SRCALPHA)
        barra.fill(COLOR_BARRA)

        # Línea fina abajo que separa la barra del juego
        pygame.draw.line(barra, COLOR_LINEA_BARRA, (0, ALTO_BARRA - 1), (ancho, ALTO_BARRA - 1), 2)

        _barras[ancho] = barra

    return _barras[ancho]


def dibujar_hud(pantalla, fuente, puntaje, vidas, tiempo_restante):
    """
    Dibuja el HUD en una barra arriba de la pantalla.
    - Puntaje: a la izquierda.
    - Tiempo: en el centro.
    - Vidas: a la derecha.
    """
    ancho_pantalla = pantalla.get_width()
    centro_y = ALTO_BARRA // 2

    pantalla.blit(crear_barra(ancho_pantalla), (0, 0))

    txt_puntaje = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(txt_puntaje, txt_puntaje.get_rect(midleft=(20, centro_y)))

    txt_tiempo = fuente.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 120))
    pantalla.blit(txt_tiempo, txt_tiempo.get_rect(center=(ancho_pantalla // 2, centro_y)))

    txt_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 120, 120))
    pantalla.blit(txt_vidas, txt_vidas.get_rect(midright=(ancho_pantalla - 20, centro_y)))
