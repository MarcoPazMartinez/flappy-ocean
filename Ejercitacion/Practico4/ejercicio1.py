import sys
import pygame
from camara import Camara

pygame.init()
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Práctico 4 - Ejercicio 1: Cámara de Seguimiento")
clock = pygame.time.Clock()

ANCHO_MUNDO, ALTO_MUNDO = 2000, 1500

jugador = pygame.Rect(1000, 750, 40, 40)
velocidad = 300  

obstaculos = [
    pygame.Rect(400, 300, 150, 150),
    pygame.Rect(1200, 400, 200, 100),
    pygame.Rect(800, 1100, 120, 180),
    pygame.Rect(1600, 1200, 150, 150),
]

camara = Camara(ANCHO_MUNDO, ALTO_MUNDO, ANCHO, ALTO)

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

  jugador.clamp_ip(pygame.Rect(0, 0, ANCHO_MUNDO, ALTO_MUNDO))

  camara.seguir(jugador)

  pantalla.fill((30, 30, 40))

  for obs in obstaculos:
    rect_pantalla = camara.aplicar(obs)
    pygame.draw.rect(pantalla, (100, 200, 120), rect_pantalla)

  rect_jugador_pantalla = camara.aplicar(jugador)
  pygame.draw.rect(pantalla, (240, 200, 80), rect_jugador_pantalla)

  pygame.display.flip()

pygame.quit()
sys.exit()