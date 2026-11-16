
import pygame

from recursos import cargar_imagen


class Jugador(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image = cargar_imagen("jugador.png", (80, 80), (0, 200, 255))

        # La máscara marca los píxeles dibujados del pez: las colisiones
        # ignoran las esquinas transparentes de la imagen
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Posición vertical inicial: se usa al reaparecer
        self.y_inicial = y

        self.velocidad_y = 0
        self.gravedad = 600
        self.fuerza_salto = -300


    def saltar(self):

        """Impulsa al pez hacia arriba."""

        self.velocidad_y = self.fuerza_salto


    def reaparecer(self):

        """Reposiciona al pez después de una colisión."""

        self.rect.x = max(0, self.rect.x - 120)

        self.rect.y = self.y_inicial

        self.velocidad_y = 0


    def update(self, dt):

        """Actualiza el movimiento aplicando gravedad."""

        self.velocidad_y += self.gravedad * dt

        self.rect.y += self.velocidad_y * dt

        pantalla_rect = pygame.display.get_surface().get_rect()

        self.rect.clamp_ip(pantalla_rect)
