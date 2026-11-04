import pygame
import random
import math


class AnimalMarino(pygame.sprite.Sprite):

    def __init__(self, x_mundo, alto_pantalla):
        super().__init__()

        self.image = pygame.Surface((40, 30))
        self.image.fill((255, 100, 100))

        self.rect = self.image.get_rect()

        # Posición dentro del mundo
        self.rect.x = x_mundo + random.randint(50, 200)
        self.rect.y = random.randint(50, alto_pantalla - 100)

        # Movimiento horizontal
        self.velocidad_x = random.randint(180, 280)

        # Movimiento ondulatorio
        self.amplitud_movimiento = random.randint(20, 50)
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