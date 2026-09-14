import pygame
import sys
from jugador import Jugador
from enemigo import Enemigo

def main():
    pygame.init()
    
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Práctico Pygame - Esquivar Enemigos")
    
    clock = pygame.time.Clock()
    screen_rect = pantalla.get_rect()
    
    todos_los_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    
    jugador = Jugador(ANCHO // 2, ALTO - 100)
    todos_los_sprites.add(jugador)
    
    timer_enemigo = 0.0
    puntaje = 0.0
    fuente = pygame.font.SysFont(None, 36)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time en segundos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        
        timer_enemigo += dt
        if timer_enemigo >= 1.0:
            timer_enemigo = 0.0
            nuevo_enemigo = Enemigo()
            todos_los_sprites.add(nuevo_enemigo)
            enemigos.add(nuevo_enemigo)
            
        puntaje += dt * 10
        
        
        jugador.update(dt, screen_rect)
        enemigos.update(dt, ALTO)
        
        
        if pygame.sprite.spritecollideany(jugador, enemigos):
            print("¡Game Over!")
            running = False
            
        
        pantalla.fill((30, 30, 30))
        todos_los_sprites.draw(pantalla)
        
        
        fps_texto = fuente.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        puntaje_texto = fuente.render(f"Puntaje: {int(puntaje)}", True, (255, 255, 255))
        
        pantalla.blit(fps_texto, (10, 10))
        pantalla.blit(puntaje_texto, (10, 45))
        
        pygame.display.flip(    )
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()