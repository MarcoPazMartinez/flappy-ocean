import pygame
import random
from jugador import Jugador
from obstaculo import Alga
from enemigo import AnimalMarino
from camara import Camara

#Importamos los módulos solicitados en el práctico
from hud import inicializar_fuente, dibujar_hud
# asegúrate de que la función reproducir_efecto esté definida en audio.py y que acepte un argumento de nombre de efecto
from audio import inicializar_audio, reproducir_efecto 

pygame.init()
pygame.mixer.init() #Inicializar el mixer para el sonido

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Ocean - Modo Scroll")

clock = pygame.time.Clock()
color_fondo = (20, 40, 80)

# Cargar la fuente del HUD una sola vez al inicio
fuente_hud = inicializar_fuente(36)

# Inicializar sistema de audio y música de fondo en bucle
inicializar_audio() # O pon aquí tu lógica de pygame.mixer.music.load() y play(-1)

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

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.saltar()
                reproducir_efecto("salto") # Sonido al saltar
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                jugador.saltar()
                reproducir_efecto("salto") # Sonido al saltar

    #Generación de algas (Timer / Spawn basado en posición o delta time)
    if jugador.rect.x + ANCHO > posicion_siguiente_alga and posicion_siguiente_alga < ANCHO_MUNDO - 200:
        altura_hueco = 160
        y_hueco = random.randint(100, ALTO - 260)
        anchos_alga = 70
        
        alga_sup = Alga(posicion_siguiente_alga, y_hueco, anchos_alga, y_hueco, es_superior=True)
        altura_inf = ALTO - (y_hueco + altura_hueco)
        alga_inf = Alga(posicion_siguiente_alga, y_hueco + altura_hueco, anchos_alga, altura_inf, es_superior=False)
        
        todos_los_sprites.add(alga_sup, alga_inf)
        obstaculos.add(alga_sup, alga_inf)
        
        posicion_siguiente_alga += distancia_entre_algas

    todos_los_sprites.update(dt)
    camara.seguir(jugador)

    # Colisiones con obstáculos
    if pygame.sprite.spritecollideany(jugador, obstaculos):
        vidas -= 1
        print(f"¡Colisión con alga! Vidas restantes: {vidas}")
        reproducir_efecto("choque") # Sonido al chocar
        jugador.rect.x -= 50  
        if vidas <= 0:
            print("Game Over")
            reproducir_efecto("game_over")
            running = False

    # Colisiones con enemigos
    colision_enemigos = pygame.sprite.spritecollide(jugador, enemigos, True)
    if colision_enemigos:
        vidas -= len(colision_enemigos)
        print(f"¡Colisión con animal marino! Vidas restantes: {vidas}")
        reproducir_efecto("choque") # Sonido al chocar con enemigo
        if vidas <= 0:
            print("Game Over")
            reproducir_efecto("game_over")
            running = False

    puntaje = int(jugador.rect.x) 
    tiempo_restante = max(0, int(LIMITE_TIEMPO - tiempo_transcurrido))

    # --- DIBUJADO DE JUEGO ---
    pantalla.fill(color_fondo)
    
    for sprite in todos_los_sprites:
        pantalla.blit(sprite.image, camara.aplicar(sprite.rect))

    # --- DIBUJAR EL HUD AL FINAL Y SIN OFFSET DE CÁMARA ---
    # Reemplazamos los blits manuales por la función modularizada del HUD
    dibujar_hud(pantalla, fuente_hud, puntaje, vidas, tiempo_restante)

    pygame.display.flip()

pygame.quit()