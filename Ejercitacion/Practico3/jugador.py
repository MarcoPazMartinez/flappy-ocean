import os
import pygame


class Jugador(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()

    
    ruta_imagen = os.path.join(
        os.path.dirname(__file__), "assets", "images", "jugador.png"
    )

    try:
      self.image = pygame.image.load(ruta_imagen).convert_alpha()
      self.image = pygame.transform.scale(
          self.image, (50, 50)
      )  
    except FileNotFoundError:
      
      self.image = pygame.Surface((50, 50))
      self.image.fill((0, 200, 255))

    self.rect = self.image.get_rect(center=(400, 500))
    self.velocidad = 350  

  def update(self, dt):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      self.rect.x -= self.velocidad * dt
    if keys[pygame.K_RIGHT]:
      self.rect.x += self.velocidad * dt
    if keys[pygame.K_UP]:
      self.rect.y -= self.velocidad * dt
    if keys[pygame.K_DOWN]:
      self.rect.y += self.velocidad * dt

    self.rect.clamp_ip(pygame.display.get_surface().get_rect())