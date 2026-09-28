import pygame
import random
from jugador import Jugador
from obstaculo import Alga
from enemigo import AnimalMarino
from camara import Camara

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Ocean - Modo Scroll")

clock = pygame.time.Clock()
color_fondo = (20, 40, 80)
fuente = pygame.font.Font(None, 36)

ANCHO_MUNDO = 3000
camara = Camara(ANCHO_MUNDO, ALTO, ANCHO, ALTO)

todos_los_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

jugador = Jugador(150, 275)
todos_los_sprites.add(jugador)

vidas = 3
puntaje = 0
tiempo_transcurrido = 0
LIMITE_TIEMPO = 90.0 


posicion_siguiente_alga = 600
distancia_entre_algas = 350


running = True
while running:
    dt = clock.tick(60) / 1000.0
    tiempo_transcurrido += dt

    
    if tiempo_transcurrido >= LIMITE_TIEMPO:
        print("¡Felicidades! Has completado el tiempo del escenario submarino.")
        running = False

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.saltar()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                jugador.saltar()

    if jugador.rect.x + ANCHO > posicion_siguiente_alga and posicion_siguiente_alga < ANCHO_MUNDO - 200:
        altura_hueco = 160
        y_hueco = random.randint(100, ALTO - 260)
        ancho_alga = 70
        
        alga_sup = Alga(posicion_siguiente_alga, y_hueco, ancho_alga, y_hueco, es_superior=True)
        altura_inf = ALTO - (y_hueco + altura_hueco)
        alga_inf = Alga(posicion_siguiente_alga, y_hueco + altura_hueco, ancho_alga, altura_inf, es_superior=False)
        
        todos_los_sprites.add(alga_sup, alga_inf)
        obstaculos.add(alga_sup, alga_inf)
        
        posicion_siguiente_alga += distancia_entre_algas

    todos_los_sprites.update(dt)

    camara.seguir(jugador)

    if pygame.sprite.spritecollideany(jugador, obstaculos):
        vidas -= 1
        print(f"¡Colisión con alga! Vidas restantes: {vidas}")
        jugador.rect.x -= 50  retroceso seguro
        if vidas <= 0:
            print("Game Over")
            running = False

    colision_enemigos = pygame.sprite.spritecollide(jugador, enemigos, True)
    if colision_enemigos:
        vidas -= len(colision_enemigos)
        print(f"¡Colisión con animal marino! Vidas restantes: {vidas}")
        if vidas <= 0:
            print("Game Over")
            running = False

    puntaje = int(jugador.rect.x) 

    pantalla.fill(color_fondo)
    
    for sprite in todos_los_sprites:
        pantalla.blit(sprite.image, camara.aplicar(sprite.rect))

    texto_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 255, 255))
    texto_puntaje = fuente.render(f"Distancia/Puntaje: {puntaje}", True, (255, 255, 255))
    tiempo_restante = max(0, int(LIMITE_TIEMPO - tiempo_transcurrido))
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 255))
    
    pantalla.blit(texto_vidas, (10, 10))
    pantalla.blit(texto_puntaje, (10, 50))
    pantalla.blit(texto_tiempo, (10, 90))

    pygame.display.flip()

pygame.quit()