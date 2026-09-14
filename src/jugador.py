import pygame

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            self.image = pygame.image.load("assets/images/jugador.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 200, 255))
            
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 300  
        
    def update(self, dt, screen_rect):
        keys = pygame.key.get_pressed()
        movimiento = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            movimiento.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            movimiento.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            movimiento.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            movimiento.y = 1
            
        
        if movimiento.length() > 0:
            movimiento = movimiento.normalize()
            
        
        self.rect.x += movimiento.x * self.velocidad * dt
        self.rect.y += movimiento.y * self.velocidad * dt
        
        
        self.rect.clamp_ip(screen_rect)