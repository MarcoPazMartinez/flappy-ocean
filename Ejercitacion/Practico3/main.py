import sys
import pygame
from enemigo import Enemigo
from jugador import Jugador

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(
    "Práctico Clase 3 - Ejercicio 2: Esquivar Enemigos"
)
clock = pygame.time.Clock()
fuente = pygame.font.Font(None, 36)

todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

jugador = Jugador()
todos_los_sprites.add(jugador)

puntaje = 0
timer_enemigo = 0.0

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  dt = clock.tick(60) / 1000.0

  timer_enemigo += dt
  if timer_enemigo >= 1.0:
    timer_enemigo = 0.0
    nuevo_enemigo = Enemigo()
    todos_los_sprites.add(nuevo_enemigo)
    enemigos.add(nuevo_enemigo)

  todos_los_sprites.update(dt)

  if pygame.sprite.spritecollide(jugador, enemigos, False):
    print(f"¡Game Over! Puntaje final: {int(puntaje)}")
    running = False

  puntaje += 60 * dt

  pantalla.fill((20, 20, 40))
  todos_los_sprites.draw(pantalla)

  texto_puntaje = fuente.render(
      f"Puntaje: {int(puntaje)}", True, (255, 255, 255)
  )
  pantalla.blit(texto_puntaje, (10, 10))

  pygame.display.flip()

pygame.quit()
sys.exit()