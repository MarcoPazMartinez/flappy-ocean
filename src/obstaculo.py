
import pygame

from recursos import cargar_imagen

ALTO_SEGMENTO = 120   # alto de assets/images/alga.png


def construir_imagen_alga(ancho, alto, es_superior):
    """Arma un alga del alto pedido repitiendo (en mosaico) un segmento vertical."""

    segmento = cargar_imagen("alga.png", (ancho, ALTO_SEGMENTO), (46, 139, 87))

    imagen = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    for y in range(0, alto, ALTO_SEGMENTO):
        imagen.blit(segmento, (0, y))

    if es_superior:
        # El alga de arriba cuelga del techo: se da vuelta (espejo vertical)
        imagen = pygame.transform.flip(imagen, False, True)

    return imagen


class Alga(pygame.sprite.Sprite):

    def __init__(self, x, y, ancho, alto, es_superior=False):

        super().__init__()

        self.image = construir_imagen_alga(ancho, alto, es_superior)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        if es_superior:

            self.rect.bottomleft = (x, y)

        else:

            self.rect.topleft = (x, y)

        self.velocidad_x = 250


    def update(self, dt):

        """Mueve el alga hacia la izquierda."""

        self.rect.x -= int(self.velocidad_x * dt)

        # Eliminar cuando sale de la pantalla
        if self.rect.right < 0:

            self.kill()
