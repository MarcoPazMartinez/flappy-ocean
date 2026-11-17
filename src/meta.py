import pygame

from obstaculo import VELOCIDAD_ALGA

ANCHO_META = 200


def crear_imagen_meta(alto):
    """Dibuja la meta: una franja a cuadros blanco y negro con un cartel rojo."""

    imagen = pygame.Surface((ANCHO_META, alto), pygame.SRCALPHA)

    # Franja a cuadros, centrada
    lado = 40
    ancho_franja = 80
    x_inicial = (ANCHO_META - ancho_franja) // 2

    for fila in range(alto // lado + 1):
        for columna in range(ancho_franja // lado):

            if (fila + columna) % 2 == 0:
                color = (20, 20, 20)
            else:
                color = (245, 245, 245)

            pygame.draw.rect(
                imagen,
                color,
                (x_inicial + columna * lado, fila * lado, lado, lado)
            )

    # Cartel con la palabra META en el medio de la franja
    cartel = pygame.Rect(0, 0, ANCHO_META, 80)
    cartel.center = (ANCHO_META // 2, alto // 2)

    pygame.draw.rect(imagen, (200, 30, 40), cartel, border_radius=14)
    pygame.draw.rect(imagen, (255, 255, 255), cartel, 4, border_radius=14)

    texto = pygame.font.Font(None, 72).render("META", True, (255, 255, 255))
    imagen.blit(texto, texto.get_rect(center=cartel.center))

    return imagen


class Meta(pygame.sprite.Sprite):
    """La línea de llegada. Aparece por la derecha y avanza como las algas.

    No choca con nada: es solo para que se vea cuándo termina la carrera.
    """

    def __init__(self, x, alto):
        super().__init__()

        self.image = crear_imagen_meta(alto)
        self.rect = self.image.get_rect(topleft=(x, 0))

        self.pos_x = float(self.rect.x)

    def update(self, dt):
        self.pos_x -= VELOCIDAD_ALGA * dt
        self.rect.x = round(self.pos_x)

        if self.rect.right < 0:
            self.kill()
