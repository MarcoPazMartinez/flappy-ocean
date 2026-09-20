import os
import random
import pygame


class Enemigo(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()

    ruta_imagen = os.path.join(
        os.path.dirname(__file__), "assets", "images", "enemigo.png"
    )

    try:
      self.image = pygame.image.load(ruta_imagen).convert_alpha()
      self.image = pygame.transform.scale(self.image, (40, 40))
    except FileNotFoundError:
      
      self.image = pygame.Surface((40, 40))
      self.image.fill((255, 60, 60))

    self.rect = self.image.get_rect()
    self.rect.x = random.randint(0, 760)
    self.rect.y = random.randint(-100, -40)
    self.velocidad = random.randint(100, 250)

  def update(self, dt):
    self.rect.y += self.velocidad * dt
    if self.rect.top > 600:
      self.kill()