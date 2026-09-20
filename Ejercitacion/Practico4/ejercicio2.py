import sys
import pygame
from camara import Camara

pygame.init()
TILE = 40
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(
    "Práctico 4 - Ejercicio 2: Laberinto con Scroll y Colisiones"
)
clock = pygame.time.Clock()

MAPA = [
    "1111111111111111111111",
    "1000000000100000000001",
    "1011111010101111111101",
    "1010001010100000001001",
    "1010101011111110101001",
    "1000101000000010101001",
    "1110101110111010101101",
    "1000100010001000100001",
    "1011111011101111101101",
    "1000001000100000001001",
    "1111101110101111111011",
    "1000001010100000000001",
    "1011111010111111110101",
    "1000000010000000010101",
    "1111111111111111111111",
]

ANCHO_MUNDO = len(MAPA[0]) * TILE
ALTO_MUNDO = len(MAPA) * TILE

paredes = []
for fila, texto in enumerate(MAPA):
  for col, celda in enumerate(texto):
    if celda == "1":
      paredes.append(pygame.Rect(col * TILE, fila * TILE, TILE, TILE))

jugador = pygame.Rect(TILE * 1.5, TILE * 1.5, 30, 30)
velocidad = 250  

camara = Camara(ANCHO_MUNDO, ALTO_MUNDO, ANCHO, ALTO)

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  dt = clock.tick(60) / 1000.0

  keys = pygame.key.get_pressed()
  dx = dy = 0
  if keys[pygame.K_LEFT]:
    dx = -velocidad * dt
  if keys[pygame.K_RIGHT]:
    dx = velocidad * dt
  if keys[pygame.K_UP]:
    dy = -velocidad * dt
  if keys[pygame.K_DOWN]:
    dy = velocidad * dt

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

  camara.seguir(jugador)

  pantalla.fill((20, 20, 30))

  for p in paredes:
    rect_pantalla = camara.aplicar(p)
    pygame.draw.rect(pantalla, (70, 110, 200), rect_pantalla)

  rect_jugador_pantalla = camara.aplicar(jugador)
  pygame.draw.rect(pantalla, (240, 200, 80), rect_jugador_pantalla)

  pygame.display.flip()

pygame.quit()
sys.exit()