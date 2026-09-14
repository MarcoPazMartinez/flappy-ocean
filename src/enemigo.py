import pygame
import random

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 50, 50))
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 760)
        self.rect.y = random.randint(-100, -40)
        self.velocidad_y = random.randint(100, 250)
        
    def update(self, dt, screen_height):
        self.rect.y += self.velocidad_y * dt
        
       
        if self.rect.top > screen_height:
            self.kill()