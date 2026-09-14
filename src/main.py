import pygame
import sys
from camara import Camara
from laberinto import obtener_paredes_y_dimensiones, TILE

def main():
    pygame.init()
    
    ANCHO, ALTO = 640, 480
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Laberinto con cámara y colisiones")
    
    clock = pygame.time.Clock()
    
    paredes, ancho_mundo, alto_mundo = obtener_paredes_y_dimensiones()
    camara = Camara(ancho_mundo, alto_mundo, ANCHO, ALTO)
    
    jugador = pygame.Rect(TILE * 1.5, TILE * 1.5, 30, 30)
    velocidad = 4
    
    
    meta = pygame.Rect(ancho_mundo - (TILE * 2), alto_mundo - (TILE * 2), 30, 30)
    
    fuente = pygame.font.SysFont(None, 48)
    ganado = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        dx = dy = 0
        keys = pygame.key.get_pressed()
        if not ganado:
            if keys[pygame.K_LEFT]:
                dx = -velocidad
            if keys[pygame.K_RIGHT]:
                dx = velocidad
            if keys[pygame.K_UP]:
                dy = -velocidad
            if keys[pygame.K_DOWN]:
                dy = velocidad
                
        
        jugador.x += dx
        for p in paredes:
            if jugador.colliderect(p):
                if dx > 0:
                    jugador.right = p.left
                elif dx < 0:
                    jugador.left = p.right
                    
        
        jugador.y += dy
        for p in paredes:
            if jugador.colliderect(p):
                if dy > 0:
                    jugador.bottom = p.top
                elif dy < 0:
                    jugador.top = p.bottom
                    
        
        if not ganado and jugador.colliderect(meta):
            print("¡Ganaste!")
            ganado = True
            
        
        camara.seguir(jugador)
        
        
        pantalla.fill((20, 20, 30))
        
        
        for p in paredes:
            pygame.draw.rect(pantalla, (70, 110, 200), camara.aplicar(p))
            
        
        pygame.draw.rect(pantalla, (50, 220, 100), camara.aplicar(meta))
        
        
        pygame.draw.rect(pantalla, (240, 200, 80), camara.aplicar(jugador))
        
        if ganado:
            texto_ganar = fuente.render("¡Ganaste!", True, (255, 255, 0))
            pantalla.blit(texto_ganar, (ANCHO // 2 - 100, ALTO // 2 - 30))
            
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    
    
