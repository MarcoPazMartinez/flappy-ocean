import math
import random

import pygame


# Las burbujas son solo decoración: no chocan con nada.
# Se dibujan con código y se guardan por radio, para no recrearlas cada vez.
_imagenes = {}


def crear_imagen_burbuja(radio):
    """Dibuja una burbuja transparente con borde y un brillo."""

    if radio in _imagenes:
        return _imagenes[radio]

    lado = radio * 2 + 2
    imagen = pygame.Surface((lado, lado), pygame.SRCALPHA)
    centro = (lado // 2, lado // 2)

    # Relleno casi transparente, borde y brillo arriba a la izquierda
    pygame.draw.circle(imagen, (170, 215, 255, 45), centro, radio)
    pygame.draw.circle(imagen, (205, 232, 255, 170), centro, radio, 2 if radio >= 8 else 1)

    radio_brillo = max(1, radio // 4)
    pygame.draw.circle(
        imagen,
        (255, 255, 255, 210),
        (centro[0] - radio // 3, centro[1] - radio // 3),
        radio_brillo
    )

    _imagenes[radio] = imagen
    return imagen


class Burbuja(pygame.sprite.Sprite):

    def __init__(self, x, y, radio=None):
        super().__init__()

        if radio is None:
            radio = random.randint(4, 16)

        self.image = crear_imagen_burbuja(radio)
        self.rect = self.image.get_rect(center=(x, y))

        # Las burbujas grandes suben más rápido
        self.velocidad_y = -random.uniform(30, 70) - radio * 3

        # Una corriente suave las lleva hacia la izquierda
        self.velocidad_x = -random.uniform(10, 40)

        # Se balancean de lado a lado mientras suben
        self.balanceo = random.uniform(4, 14)
        self.fase = random.uniform(0, math.tau)

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.tiempo = 0.0

    def update(self, dt):
        self.tiempo += dt

        self.pos_x += self.velocidad_x * dt
        self.pos_y += self.velocidad_y * dt

        self.rect.centerx = round(self.pos_x + self.balanceo * math.sin(self.tiempo * 2 + self.fase))
        self.rect.centery = round(self.pos_y)

        # Eliminar al salir por arriba o por la izquierda
        if self.rect.bottom < 0 or self.rect.right < 0:
            self.kill()
