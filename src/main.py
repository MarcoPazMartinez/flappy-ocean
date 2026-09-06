import pygame
import sys

#inicio
pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Ocean - Dev Build")
clock = pygame.time.Clock()

#variables del juego
pez = pygame.Rect(100, 275, 40, 30)
velocidad_y = 0
GRAVEDAD = 800
IMPULSO = -300

# colores
COLOR_AGUA = (20, 40, 80)
COLOR_PEZ = (255, 140, 0)
COLOR_TEXTO = (255, 255, 255)

fuente = pygame.font.Font(None, 30)

#loop del juego
running = True
while running:
    # tiempo delta (dt) para movimiento suave
    dt = clock.tick(60) / 1000.0

    # manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocidad_y = IMPULSO
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic izquierdo
                velocidad_y = IMPULSO

    # actualizar estado del juego
    # aplicar gravedad y actualizar posición del pez
    velocidad_y += GRAVEDAD * dt
    pez.y += velocidad_y * dt

    # limitar al pez dentro de la pantalla
    if pez.top < 0:
        pez.top = 0
        velocidad_y = 0
    if pez.bottom > ALTO:
        pez.bottom = ALTO
        velocidad_y = 0

    # dibujar en pantalla
    pantalla.fill(COLOR_AGUA) # limpiar fondo
    
    # dibujar el pez
    pygame.draw.rect(pantalla, COLOR_PEZ, pez)
    
    # contador de fps
    fps_texto = fuente.render(f"FPS: {int(clock.get_fps())}", True, COLOR_TEXTO)
    pantalla.blit(fps_texto, (10, 10))

    pygame.display.flip()

# cierre del juego  
pygame.quit()
sys.exit()