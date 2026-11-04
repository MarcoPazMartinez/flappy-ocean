
import pygame


class Jugador(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 200, 255))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.velocidad_y = 0
        self.gravedad = 600
        self.fuerza_salto = -300


    def saltar(self):

        """Impulsa al pez hacia arriba."""

        self.velocidad_y = self.fuerza_salto


    def reaparecer(self):

        """Reposiciona al pez después de una colisión."""

        self.rect.x = max(0, self.rect.x - 120)

        self.rect.y = 275

        self.velocidad_y = 0


    def update(self, dt):

        """Actualiza el movimiento aplicando gravedad."""

        self.velocidad_y += self.gravedad * dt

        self.rect.y += self.velocidad_y * dt

        pantalla_rect = pygame.display.get_surface().get_rect()

        self.rect.clamp_ip(pantalla_rect)
