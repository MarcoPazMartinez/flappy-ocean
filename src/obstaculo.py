import random

import pygame

from recursos import cargar_imagen

ALTO_SEGMENTO = 120       # alto de las imágenes de alga
ANCHO_HEBRA = 90          # ancho de una hebra de alga
SEPARACION_HEBRAS = 70    # distancia entre hebras de una misma mata (las hojas se superponen)
VELOCIDAD_ALGA = 250      # px/s hacia la izquierda

# Imágenes de alga y su color de respaldo (si falta el archivo)
ALGA_VERDE = "alga.png"
ALGA_VIOLETA = "alga_violeta.png"
COLOR_RESPALDO = {
    ALGA_VERDE: (46, 139, 87),
    ALGA_VIOLETA: (130, 70, 180),
}


def elegir_colores(cantidad):
    """Elige el color de cada hebra de una mata.

    Con 2 o más hebras siempre aparecen verde y violeta mezclados.
    """
    if cantidad == 1:
        return [random.choice((ALGA_VERDE, ALGA_VIOLETA))]

    colores = [ALGA_VERDE, ALGA_VIOLETA]
    colores += [random.choice((ALGA_VERDE, ALGA_VIOLETA)) for _ in range(cantidad - 2)]
    random.shuffle(colores)
    return colores


def construir_imagen_alga(ancho, alto, es_superior):
    """Arma una mata de algas del ancho y alto pedidos.

    - Cada hebra repite (en mosaico) un segmento vertical hasta llegar al alto.
    - Las hebras van una al lado de la otra, verdes y violetas mezcladas.
    - Cada hebra empieza en un punto distinto del segmento, para que las
      hojas no queden alineadas.
    """
    cantidad = max(1, round((ancho - ANCHO_HEBRA) / SEPARACION_HEBRAS) + 1)

    imagen = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    for numero, nombre in enumerate(elegir_colores(cantidad)):

        segmento = cargar_imagen(
            nombre,
            (ANCHO_HEBRA, ALTO_SEGMENTO),
            COLOR_RESPALDO[nombre]
        )

        x = numero * SEPARACION_HEBRAS
        desfase = random.randint(0, ALTO_SEGMENTO - 1)

        for y in range(-desfase, alto, ALTO_SEGMENTO):
            imagen.blit(segmento, (x, y))

    if es_superior:
        # El alga de arriba cuelga del techo: se da vuelta (espejo vertical)
        imagen = pygame.transform.flip(imagen, False, True)

    return imagen


class Alga(pygame.sprite.Sprite):

    def __init__(self, x, y, ancho, alto, es_superior=False):

        super().__init__()

        # Cada mata es un par (arriba y abajo): para sumar puntos se cuenta
        # solo el alga de arriba, y solo una vez
        self.es_superior = es_superior
        self.superada = False

        self.image = construir_imagen_alga(ancho, alto, es_superior)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        if es_superior:

            self.rect.bottomleft = (x, y)

        else:

            self.rect.topleft = (x, y)

        self.velocidad_x = VELOCIDAD_ALGA


    def update(self, dt):

        """Mueve el alga hacia la izquierda."""

        self.rect.x -= int(self.velocidad_x * dt)

        # Eliminar cuando sale de la pantalla
        if self.rect.right < 0:

            self.kill()
