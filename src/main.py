import pygame
import random

from jugador import Jugador
from obstaculo import Alga
from enemigo import AnimalMarino
from camara import Camara

from hud import inicializar_fuente, dibujar_hud

from audio import (
    inicializar_audio,
    cargar_sonido,
    reproducir_efecto,
    reproducir_musica,
    detener_musica
)


# -----------------------------------------
# INICIALIZACIÓN
# -----------------------------------------

pygame.init()

ANCHO, ALTO = 800, 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Ocean - Modo Scroll")

clock = pygame.time.Clock()

color_fondo = (20, 40, 80)

# HUD
fuente_hud = inicializar_fuente(36)

# AUDIO
inicializar_audio()

sonido_salto = cargar_sonido("salto.ogg")
sonido_colision = cargar_sonido("colision.ogg")
sonido_perder = cargar_sonido("perder.ogg")

reproducir_musica("musica_fondo.ogg", volumen=0.3)


# -----------------------------------------
# MUNDO Y CÁMARA
# -----------------------------------------

ANCHO_MUNDO = 3000

camara = Camara(ANCHO_MUNDO, ALTO, ANCHO, ALTO)


# -----------------------------------------
# GRUPOS DE SPRITES
# -----------------------------------------

todos_los_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
enemigos = pygame.sprite.Group()


# -----------------------------------------
# JUGADOR
# -----------------------------------------

jugador = Jugador(150, 275)

todos_los_sprites.add(jugador)


# -----------------------------------------
# VARIABLES DEL JUEGO
# -----------------------------------------

vidas = 3
puntaje = 0

tiempo_transcurrido = 0
LIMITE_TIEMPO = 90.0

# Sistema de invulnerabilidad
invulnerabilidad = 0.0
DURACION_INVULNERABILIDAD = 1.0

running = True


# -----------------------------------------
# GENERACIÓN DE ALGAS
# -----------------------------------------

posicion_siguiente_alga = 600
distancia_entre_algas = 350


# -----------------------------------------
# GENERACIÓN DE ENEMIGOS
# -----------------------------------------

posicion_siguiente_enemigo = 400  # Ajustado para que aparezcan más cerca del inicio
distancia_entre_enemigos = 600


# -----------------------------------------
# BUCLE PRINCIPAL
# -----------------------------------------

while running:

    dt = clock.tick(60) / 1000.0

    tiempo_transcurrido += dt

    # Actualizar invulnerabilidad
    if invulnerabilidad > 0:
        invulnerabilidad = max(0, invulnerabilidad - dt)

    if tiempo_transcurrido >= LIMITE_TIEMPO:

        print("¡Felicidades! Has completado el tiempo del escenario submarino.")

        running = False
        break


    # -------------------------------------
    # EVENTOS
    # -------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                jugador.saltar()
                reproducir_efecto(sonido_salto)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                jugador.saltar()
                reproducir_efecto(sonido_salto)


    # -------------------------------------
    # GENERACIÓN DE ALGAS
    # -------------------------------------

    if (
        jugador.rect.x + ANCHO > posicion_siguiente_alga
        and posicion_siguiente_alga < ANCHO_MUNDO - 200
    ):

        altura_hueco = 160

        y_hueco = random.randint(100, ALTO - 260)

        anchos_alga = 70

        # Alga superior
        alga_sup = Alga(
            posicion_siguiente_alga,
            y_hueco,
            anchos_alga,
            y_hueco,
            es_superior=True
        )

        # Alga inferior
        altura_inf = ALTO - (y_hueco + altura_hueco)

        alga_inf = Alga(
            posicion_siguiente_alga,
            y_hueco + altura_hueco,
            anchos_alga,
            altura_inf,
            es_superior=False
        )

        todos_los_sprites.add(alga_sup, alga_inf)
        obstaculos.add(alga_sup, alga_inf)

        posicion_siguiente_alga += distancia_entre_algas


    # -------------------------------------
    # GENERACIÓN DE ANIMALES MARINOS
    # -------------------------------------

    if (
        jugador.rect.x + ANCHO > posicion_siguiente_enemigo
        and posicion_siguiente_enemigo < ANCHO_MUNDO - 200
    ):

        animal = AnimalMarino(
            posicion_siguiente_enemigo,
            ALTO
        )

        todos_los_sprites.add(animal)
        enemigos.add(animal)

        posicion_siguiente_enemigo += distancia_entre_enemigos


    # -------------------------------------
    # ACTUALIZACIÓN DE SPRITES
    # -------------------------------------

    todos_los_sprites.update(dt)


    # -------------------------------------
    # ELIMINAR ENEMIGOS QUE QUEDARON ATRÁS
    # -------------------------------------

    for animal in enemigos.copy():

        if animal.rect.right < jugador.rect.left - 200:
            animal.kill()


    # -------------------------------------
    # ACTUALIZACIÓN DE CÁMARA
    # -------------------------------------

    camara.seguir(jugador)


    # -------------------------------------
    # COLISIONES
    # -------------------------------------

    if invulnerabilidad <= 0:

        colision = None

        # Comprobar colisión con algas
        if pygame.sprite.spritecollideany(jugador, obstaculos):

            colision = "alga"

        # Comprobar colisión con enemigos
        elif pygame.sprite.spritecollideany(jugador, enemigos):

            colision = "enemigo"


        # ---------------------------------
        # PROCESAR COLISIÓN
        # ---------------------------------

        if colision is not None:

            vidas -= 1

            print(
                f"¡Colisión con {colision}! "
                f"Vidas restantes: {vidas}"
            )

            reproducir_efecto(sonido_colision)

            # Si choca con un enemigo, eliminarlo
            if colision == "enemigo":

                enemigo_colisionado = pygame.sprite.spritecollideany(
                    jugador,
                    enemigos
                )

                if enemigo_colisionado:
                    enemigo_colisionado.kill()

            # Reaparecer al jugador
            jugador.reaparecer()

            # Reiniciar posiciones de spawn para que no queden adelantadas al reaparecer
            posicion_siguiente_alga = 600
            posicion_siguiente_enemigo = 400

            # Activar invulnerabilidad
            invulnerabilidad = DURACION_INVULNERABILIDAD

            # Comprobar Game Over
            if vidas <= 0:

                print("Game Over")

                reproducir_efecto(sonido_perder)

                pygame.time.delay(500)

                running = False


    # -------------------------------------
    # PUNTAJE Y TIEMPO
    # -------------------------------------

    puntaje = int(jugador.rect.x)

    tiempo_restante = max(
        0,
        int(LIMITE_TIEMPO - tiempo_transcurrido)
    )


    # -------------------------------------
    # DIBUJADO
    # -------------------------------------

    pantalla.fill(color_fondo)

    for sprite in todos_los_sprites:

        # Efecto visual durante la invulnerabilidad
        if sprite == jugador and invulnerabilidad > 0:

            # Parpadeo del jugador
            if int(pygame.time.get_ticks() / 100) % 2 == 0:
                continue

        pantalla.blit(
            sprite.image,
            camara.aplicar(sprite.rect)
        )


    # -------------------------------------
    # HUD
    # -------------------------------------

    dibujar_hud(
        pantalla,
        fuente_hud,
        puntaje,
        vidas,
        tiempo_restante
    )


    # -------------------------------------
    # ACTUALIZAR PANTALLA
    # -------------------------------------

    pygame.display.flip()


# -----------------------------------------
# FINALIZACIÓN
# -----------------------------------------

detener_musica()

pygame.quit()