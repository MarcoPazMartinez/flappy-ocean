import sys
import pygame

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Práctico Clase 2 - Ejercicio 1")
clock = pygame.time.Clock()

jugador = pygame.Rect(375, 275, 50, 50)
velocidad = 300  
color_jugador = (0, 200, 255)
color_fondo = (30, 30, 30)


fuente = pygame.font.Font(None, 30)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000.0  

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        jugador.x -= velocidad * dt
    if keys[pygame.K_RIGHT]:
        jugador.x += velocidad * dt
    if keys[pygame.K_UP]:
        jugador.y -= velocidad * dt
    if keys[pygame.K_DOWN]:
        jugador.y += velocidad * dt

    jugador.clamp_ip(pantalla.get_rect())

    pantalla.fill(color_fondo)
    pygame.draw.rect(pantalla, color_jugador, jugador)

    fps_texto = fuente.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    pantalla.blit(fps_texto, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()