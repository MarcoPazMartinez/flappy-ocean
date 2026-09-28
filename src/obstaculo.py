import pygame
import random

class Alga(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, es_superior=False):
        super().__init__()
        
        self.image = pygame.Surface((ancho, alto))
        self.image.fill((46, 139, 87))  
        
        self.rect = self.image.get_rect()
        
        if es_superior:
            
            self.rect.bottomleft = (x, y)
        else:
            
            self.rect.topleft = (x, y)
            
       
        self.velocidad_x = 250  

    def update(self, dt):
        """Mueve el alga hacia la izquierda y la elimina si sale de la pantalla."""
        self.rect.x -= int(self.velocidad_x * dt)
        
        
        if self.rect.right < 0:
            self.kill()