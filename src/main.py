import pygame
import random

from jugador import Jugador
from obstaculo import Alga, ANCHO_HEBRA, SEPARACION_HEBRAS, VELOCIDAD_ALGA
from enemigo import AnimalMarino, elegir_tipo
from burbuja import Burbuja

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

ANCHO, ALTO = 1280, 720

# Medidas del escenario (escala para la pantalla de 1280x720)
ALTURA_HUECO = 230   # alto del hueco entre el alga de arriba y la de abajo
MARGEN_HUECO = 80    # distancia mínima del hueco al techo y al piso

# Matas de algas (como en un acuario): grupos de 1 a 3 hebras juntas,
# con espacio libre entre una mata y la siguiente
MAX_HEBRAS = 3
ESPACIO_LIBRE_ENTRE_ALGAS = (300, 550)   # px libres entre una mata y la siguiente
MAX_CAMBIO_HUECO = 200                   # px máx. de diferencia entre dos huecos seguidos

# Cada cuántos segundos aparece un animal marino (mínimo, máximo)
INTERVALO_ENEMIGOS = (2.5, 4.0)

# Burbujas de ambiente: cada cuántos segundos sale una nueva (mínimo, máximo)
INTERVALO_BURBUJAS = (0.25, 0.7)
BURBUJAS_INICIALES = 18   # ya hay burbujas en pantalla al empezar

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Ocean")

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
# GRUPOS DE SPRITES
# -----------------------------------------

todos_los_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
burbujas = pygame.sprite.Group()   # decoración: no chocan con nada


# -----------------------------------------
# JUGADOR
# -----------------------------------------

jugador = Jugador(150, ALTO // 2)

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
# GENERACIÓN DE ALGAS Y ENEMIGOS
# -----------------------------------------
#
# Los obstáculos nacen fuera de la pantalla, a la derecha, y se mueven hacia
# la izquierda. Cuándo aparece el siguiente se decide con un temporizador
# (y no con la posición del pez, que no se mueve en horizontal).

def generar_mata_de_algas(x, centro_anterior):
    """Crea el par de algas (arriba y abajo) con un hueco en el medio.

    Cada alga es una mata de 1 a MAX_HEBRAS hebras juntas, verdes y violetas.
    Devuelve (ancho de la mata, centro del hueco).
    """

    hebras = random.randint(1, MAX_HEBRAS)
    ancho = ANCHO_HEBRA + (hebras - 1) * SEPARACION_HEBRAS

    # El hueco cambia de altura de a poco para que siempre se pueda llegar
    minimo = MARGEN_HUECO + ALTURA_HUECO // 2
    maximo = ALTO - MARGEN_HUECO - ALTURA_HUECO // 2
    centro = centro_anterior + random.randint(-MAX_CAMBIO_HUECO, MAX_CAMBIO_HUECO)
    centro = max(minimo, min(maximo, centro))

    borde_superior = centro - ALTURA_HUECO // 2
    borde_inferior = centro + ALTURA_HUECO // 2

    alga_sup = Alga(x, borde_superior, ancho, borde_superior, es_superior=True)
    alga_inf = Alga(x, borde_inferior, ancho, ALTO - borde_inferior, es_superior=False)

    todos_los_sprites.add(alga_sup, alga_inf)
    obstaculos.add(alga_sup, alga_inf)

    return ancho, centro


def segundos_hasta_la_proxima_mata(ancho_mata):
    """Tiempo que tarda una mata (que nace en el borde derecho) en dejar
    el espacio libre para que nazca la siguiente."""

    espacio_libre = random.randint(*ESPACIO_LIBRE_ENTRE_ALGAS)

    return (ancho_mata + espacio_libre) / VELOCIDAD_ALGA


# Primera mata: ya visible al empezar, a 700 px del borde izquierdo
X_PRIMERA_MATA = 700

ancho_mata, centro_hueco = generar_mata_de_algas(X_PRIMERA_MATA, ALTO // 2)

# Como no nació en el borde derecho sino más adelante, ya recorrió parte del camino
adelanto = (ANCHO - X_PRIMERA_MATA) / VELOCIDAD_ALGA
temporizador_alga = max(0.0, segundos_hasta_la_proxima_mata(ancho_mata) - adelanto)

# Primer animal marino: a los pocos segundos de empezar
temporizador_enemigo = random.uniform(2.0, 4.0)


# -----------------------------------------
# BURBUJAS
# -----------------------------------------

def generar_burbuja_del_fondo(y=None):
    """Crea una burbuja que sube desde el piso (o desde la altura y indicada)."""

    if y is None:
        y = ALTO + 20

    burbujas.add(Burbuja(random.randint(0, ANCHO), y))


def soltar_burbujas_del_pez():
    """Un par de burbujas chicas salen de la boca del pez al nadar."""

    for _ in range(2):
        burbujas.add(
            Burbuja(
                jugador.rect.right - 8 + random.randint(-4, 4),
                jugador.rect.centery - 6 + random.randint(-6, 6),
                radio=random.randint(3, 6)
            )
        )


def hacer_nadar_al_pez():
    """El pez salta hacia arriba: impulso, sonido y burbujas."""

    jugador.saltar()
    reproducir_efecto(sonido_salto)
    soltar_burbujas_del_pez()


for _ in range(BURBUJAS_INICIALES):
    generar_burbuja_del_fondo(random.randint(0, ALTO))

temporizador_burbuja = random.uniform(*INTERVALO_BURBUJAS)


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

                hacer_nadar_al_pez()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                hacer_nadar_al_pez()


    # -------------------------------------
    # GENERACIÓN DE ALGAS
    # -------------------------------------

    temporizador_alga -= dt

    if temporizador_alga <= 0:

        # Nace justo fuera de la pantalla, a la derecha
        ancho_mata, centro_hueco = generar_mata_de_algas(ANCHO, centro_hueco)

        temporizador_alga += segundos_hasta_la_proxima_mata(ancho_mata)


    # -------------------------------------
    # GENERACIÓN DE ANIMALES MARINOS
    # -------------------------------------

    temporizador_enemigo -= dt

    if temporizador_enemigo <= 0:

        # Pez, pulpo o tiburón (cada uno se mueve distinto, ver enemigo.py)
        # AnimalMarino suma entre 50 y 200 px a la x que recibe
        animal = AnimalMarino(
            ANCHO,
            ALTO,
            elegir_tipo()
        )

        todos_los_sprites.add(animal)
        enemigos.add(animal)

        temporizador_enemigo = random.uniform(*INTERVALO_ENEMIGOS)


    # -------------------------------------
    # ACTUALIZACIÓN DE SPRITES
    # -------------------------------------

    todos_los_sprites.update(dt)

    # Burbujas de ambiente
    burbujas.update(dt)

    temporizador_burbuja -= dt

    if temporizador_burbuja <= 0:

        generar_burbuja_del_fondo()

        temporizador_burbuja = random.uniform(*INTERVALO_BURBUJAS)


    # -------------------------------------
    # COLISIONES
    # -------------------------------------

    if invulnerabilidad <= 0:

        colision = None

        # Comprobar colisión con algas
        # (collide_mask: solo cuentan los píxeles dibujados, no el rectángulo)
        if pygame.sprite.spritecollideany(
            jugador, obstaculos, pygame.sprite.collide_mask
        ):

            colision = "alga"

        # Comprobar colisión con enemigos
        elif pygame.sprite.spritecollideany(
            jugador, enemigos, pygame.sprite.collide_mask
        ):

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
                    enemigos,
                    pygame.sprite.collide_mask
                )

                if enemigo_colisionado:
                    enemigo_colisionado.kill()

            # Reaparecer al jugador
            jugador.reaparecer()

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

    # Las burbujas van por detrás de todo lo demás
    burbujas.draw(pantalla)

    for sprite in todos_los_sprites:

        # Efecto visual durante la invulnerabilidad
        if sprite == jugador and invulnerabilidad > 0:

            # Parpadeo del jugador
            if int(pygame.time.get_ticks() / 100) % 2 == 0:
                continue

        pantalla.blit(sprite.image, sprite.rect)


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