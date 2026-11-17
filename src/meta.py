import pygame

from obstaculo import VELOCIDAD_ALGA

ANCHO_META = 520          # largo del tubo
ALTO_TUBO = 270           # alto del tubo (el pez mide 80: entra con mucho margen)
ALTO_CARTEL = 110         # el cartel "META" y sus soportes van arriba del tubo
ANCHO_ARO = 28


def crear_imagen_meta():
    """Dibuja la meta: un tubo de cristal de acuario con aros a cuadros y un cartel."""

    alto = ALTO_CARTEL + ALTO_TUBO
    imagen = pygame.Surface((ANCHO_META, alto), pygame.SRCALPHA)

    tubo = pygame.Rect(0, ALTO_CARTEL, ANCHO_META, ALTO_TUBO)

    # Cristal: casi transparente, para que se vea el pez nadando adentro
    pygame.draw.rect(imagen, (150, 215, 255, 55), tubo, border_radius=24)
    pygame.draw.rect(imagen, (220, 245, 255, 200), tubo, 4, border_radius=24)

    # Reflejos del cristal
    pygame.draw.rect(imagen, (255, 255, 255, 120), (50, tubo.top + 16, ANCHO_META - 100, 12), border_radius=6)
    pygame.draw.rect(
        imagen, (255, 255, 255, 60), (50, tubo.bottom - 24, ANCHO_META - 100, 7), border_radius=4
    )

    # Aros a cuadros blanco y negro en las dos puntas (como una línea de llegada).
    # Se dibujan aparte y se recortan con la forma redondeada del tubo, para que
    # los cuadros no se salgan por las esquinas.
    aros = pygame.Surface((ANCHO_META, alto), pygame.SRCALPHA)
    lado = ANCHO_ARO // 2

    for x_aro in (0, ANCHO_META - ANCHO_ARO):
        for fila in range(ALTO_TUBO // lado + 1):
            for columna in range(2):

                color = (20, 20, 20) if (fila + columna) % 2 == 0 else (245, 245, 245)
                cuadro = pygame.Rect(x_aro + columna * lado, tubo.top + fila * lado, lado, lado)

                pygame.draw.rect(aros, color, cuadro)

    forma = pygame.Surface((ANCHO_META, alto), pygame.SRCALPHA)
    pygame.draw.rect(forma, (255, 255, 255, 255), tubo, border_radius=24)
    aros.blit(forma, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    imagen.blit(aros, (0, 0))
    pygame.draw.rect(imagen, (220, 245, 255, 255), tubo, 4, border_radius=24)

    # Cartel META con dos soportes que lo unen al tubo
    for x_soporte in (ANCHO_META // 2 - 90, ANCHO_META // 2 + 76):
        pygame.draw.rect(imagen, (120, 135, 155), (x_soporte, 74, 14, ALTO_CARTEL - 74))

    cartel = pygame.Rect(0, 0, 300, 80)
    cartel.midtop = (ANCHO_META // 2, 0)

    pygame.draw.rect(imagen, (200, 30, 40), cartel, border_radius=14)
    pygame.draw.rect(imagen, (255, 255, 255), cartel, 4, border_radius=14)

    texto = pygame.font.Font(None, 76).render("META", True, (255, 255, 255))
    imagen.blit(texto, texto.get_rect(center=cartel.center))

    return imagen


class Meta(pygame.sprite.Sprite):
    """La llegada: un tubo de cristal al que el pez entra nadando.

    Aparece por la derecha y avanza como las algas. No choca con nada.
    Se dibuja por encima del pez: como es de cristal, el pez se ve adentro.
    """

    def __init__(self, x, alto_pantalla):
        super().__init__()

        self.image = crear_imagen_meta()

        # El tubo queda en el centro de la pantalla
        self.centro_tubo_y = alto_pantalla // 2
        y = self.centro_tubo_y - ALTO_CARTEL - ALTO_TUBO // 2

        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_x = float(self.rect.x)

    def update(self, dt):
        self.pos_x -= VELOCIDAD_ALGA * dt
        self.rect.x = round(self.pos_x)

        if self.rect.right < 0:
            self.kill()
