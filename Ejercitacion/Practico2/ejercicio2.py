import random
import sys
import pygame

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Práctico Clase 2 - Ejercicio 2: Recoger el objetivo")
clock = pygame.time.Clock()

jugador = pygame.Rect(375, 275, 50, 50)
velocidad = 300  
color_jugador = (0, 150, 255) 

objetivo = pygame.Rect(
    random.randint(0, ANCHO - 50), random.randint(0, ALTO - 50), 50, 50
)
color_objetivo = (255, 50, 50)  

puntaje = 0
fuente = pygame.font.Font(None, 30)
color_fondo = (30, 30, 30)

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

    
    if jugador.colliderect(objetivo):
        puntaje += 1
        objetivo.x = random.randint(0, ANCHO - 50)
        objetivo.y = random.randint(0, ALTO - 50)

    
    pantalla.fill(color_fondo)

    # Dibujar formas
    pygame.draw.rect(pantalla, color_jugador, jugador)
    pygame.draw.rect(pantalla, color_objetivo, objetivo)


    texto_puntaje = fuente.render(f"Puntos: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto_puntaje, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()