import pygame
import sys
from camara import Camara

def main():
    pygame.init()
    
    ANCHO_VENTANA, ALTO_VENTANA = 640, 480
    ANCHO_MUNDO, ALTO_MUNDO = 2000, 1500
    
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Práctico Clase 4 - Cámara de Seguimiento")
    
    clock = pygame.time.Clock()
    
    jugador = pygame.Rect(1000, 750, 40, 40)
    velocidad = 5
    
    obstaculos = [
        pygame.Rect(300, 200, 150, 150),
        pygame.Rect(1500, 400, 200, 100),
        pygame.Rect(800, 1200, 120, 120),
        pygame.Rect(200, 1000, 100, 200),
    ]
    
    camara = Camara(ANCHO_MUNDO, ALTO_MUNDO, ANCHO_VENTANA, ALTO_VENTANA)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador.x -= velocidad
        if keys[pygame.K_RIGHT]:
            jugador.x += velocidad
        if keys[pygame.K_UP]:
            jugador.y -= velocidad
        if keys[pygame.K_DOWN]:
            jugador.y += velocidad
            
        camara.seguir(jugador)
        
        
        pantalla.fill((30, 30, 40)) 
        
        for obs in obstaculos:
            rect_pantalla = camara.aplicar(obs)
            pygame.draw.rect(pantalla, (100, 200, 120), rect_pantalla)
            
        
        rect_jugador_pantalla = camara.aplicar(jugador)
        pygame.draw.rect(pantalla, (240, 200, 80), rect_jugador_pantalla)
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()