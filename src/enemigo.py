import pygame
import random
import math


class AnimalMarino(pygame.sprite.Sprite):

    def __init__(self, x_mundo, alto_pantalla):
        super().__init__()

        self.image = pygame.Surface((72, 72))
        self.image.fill((255, 100, 100))

        self.rect = self.image.get_rect()

        # Posición dentro del mundo
        self.rect.x = x_mundo + random.randint(50, 200)
        # Margen arriba y abajo para que la onda (hasta 90 px) y el alto
        # del sprite (72 px) no se salgan de la pantalla
        self.rect.y = random.randint(120, alto_pantalla - 200)

        # Movimiento horizontal
        self.velocidad_x = random.randint(180, 280)

        # Movimiento ondulatorio
        self.amplitud_movimiento = random.randint(30, 90)
        self.frecuencia_y = random.randint(2, 5)

        self.tiempo_acumulado = 0
        self.posicion_inicial_y = self.rect.y

    def update(self, dt):
        """Actualiza el movimiento del animal marino."""

        self.rect.x -= int(self.velocidad_x * dt)

        self.tiempo_acumulado += dt

        desplazamiento_y = self.amplitud_movimiento * math.sin(
            self.tiempo_acumulado * self.frecuencia_y
        )

        self.rect.y = int(
            self.posicion_inicial_y + desplazamiento_y
        )