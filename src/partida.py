"""Una partida: todo lo que pasa desde que se aprieta Jugar hasta que termina.

La partida es un objeto (`Partida`) que guarda todo su estado. Para empezar otra
partida se crea un objeto nuevo y no queda nada de la anterior.
"""
import os
import random
from collections import namedtuple

import pygame

from audio import reproducir_efecto
from burbuja import Burbuja
from enemigo import AnimalMarino, elegir_tipo
from hud import dibujar_hud, inicializar_fuente
from jugador import Jugador
from meta import ANCHO_META, Meta
from obstaculo import ANCHO_HEBRA, SEPARACION_HEBRAS, VELOCIDAD_ALGA, Alga


FPS = 60

# Un cuadro nunca cuenta más que esto, aunque haya tardado mucho (por ejemplo, al arrastrar
# la ventana el juego se congela). Sin este tope, al volver los obstáculos "saltan" y pueden
# atravesar al pez sin chocarlo, y el tiempo de la partida avanza de golpe.
DT_MAXIMO = 0.05
COLOR_FONDO = (20, 40, 80)


SEGUNDOS_DE_PARTIDA = 120.0       # 2 minutos hasta llegar a la meta


def leer_limite_de_tiempo():
    """Segundos que dura la partida (SEGUNDOS_DE_PARTIDA).

    Para probar el final del juego sin esperar, se puede acortar desde la terminal
    (mínimo 10 segundos):  FLAPPY_LIMITE_TIEMPO=20 python main.py
    """
    try:
        return max(10.0, float(os.environ.get("FLAPPY_LIMITE_TIEMPO", SEGUNDOS_DE_PARTIDA)))
    except ValueError:
        return SEGUNDOS_DE_PARTIDA


# Reglas
VIDAS_INICIALES = 3
LIMITE_TIEMPO = leer_limite_de_tiempo()   # segundos: al llegar a la meta se gana
DURACION_INVULNERABILIDAD = 1.0

# Puntos
PUNTOS_POR_ALGA = 10              # cada mata de algas que se deja atrás
BONUS_META = 100                  # por llegar a la meta (ganar)
# Los animales dan puntos según su tipo: ver "puntos" en TIPOS (enemigo.py)

# Medidas del escenario (escala para la pantalla de 1280x720)
ALTURA_HUECO = 230                # alto del hueco entre el alga de arriba y la de abajo
MARGEN_HUECO = 80                 # distancia mínima del hueco al techo y al piso

# Matas de algas (como en un acuario): grupos de 1 a 3 hebras juntas,
# con espacio libre entre una mata y la siguiente
MAX_HEBRAS = 3
ESPACIO_LIBRE_ENTRE_ALGAS = (300, 550)   # px libres entre una mata y la siguiente
MAX_CAMBIO_HUECO = 200                   # px máx. de diferencia entre dos huecos seguidos
X_PRIMERA_MATA = 700                     # la primera mata ya se ve al empezar

# Cada cuántos segundos aparece un animal marino (mínimo, máximo)
INTERVALO_ENEMIGOS = (2.5, 4.0)

# Burbujas de ambiente: cada cuántos segundos sale una nueva (mínimo, máximo)
INTERVALO_BURBUJAS = (0.25, 0.7)
BURBUJAS_INICIALES = 18

# Antes de la meta se dejan de generar obstáculos, para que el final quede despejado
SEGUNDOS_DESPEJADOS = 1.5

# Cuando el tubo de la meta está a esta distancia del pez (px), el pez se acomoda
# solo a su altura y no puede chocar: así siempre entra al tubo
DISTANCIA_PILOTO = 450

# Avisos de puntos ("+10") que suben desde el pez
DURACION_AVISO = 0.9
COLOR_AVISO_ALGA = (255, 255, 255)
COLOR_AVISO_ANIMAL = (255, 215, 60)

# Cómo terminó la partida:
#   estado:  "victoria", "derrota" o "salir" (se cerró la ventana)
#   puntaje: puntos finales (ya incluye el bonus de la meta si ganó)
#   bonus:   puntos extra por llegar a la meta (0 si perdió)
#   captura: la última imagen del juego (sirve de fondo para el cartel final)
Resultado = namedtuple("Resultado", "estado puntaje bonus captura")


class Partida:

    def __init__(self, pantalla, sonidos):

        self.ancho, self.alto = pantalla.get_size()
        self.sonidos = sonidos

        # Grupos de sprites
        self.todos = pygame.sprite.Group()
        self.obstaculos = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.burbujas = pygame.sprite.Group()   # decoración: no chocan con nada

        self.jugador = Jugador(150, self.alto // 2)
        self.todos.add(self.jugador)

        # Estado de la partida
        self.vidas = VIDAS_INICIALES
        self.puntaje = 0
        self.bonus = 0
        self.tiempo = 0.0
        self.invulnerable = 0.0
        self.estado_final = None          # "victoria" o "derrota" cuando termina
        self.piloto_automatico = False    # el pez entra solo al tubo de la meta

        # Avisos de puntos: [superficie, x, y, segundos que le quedan]
        self.avisos = []
        self.fuente_avisos = pygame.font.Font(None, 48)

        # La meta aparece cuando falta el tiempo justo para que llegue al pez
        # exactamente cuando se termina el tiempo
        self.meta = None
        distancia_hasta_el_pez = self.ancho + ANCHO_META // 2 - self.jugador.rect.centerx
        self.segundos_meta = distancia_hasta_el_pez / VELOCIDAD_ALGA

        # Algas: la primera mata ya está en pantalla al empezar
        ancho_mata, self.centro_hueco = self.generar_mata_de_algas(X_PRIMERA_MATA, self.alto // 2)

        # Como no nació en el borde derecho sino más adelante, ya recorrió parte del camino
        adelanto = (self.ancho - X_PRIMERA_MATA) / VELOCIDAD_ALGA
        self.temporizador_alga = max(
            0.0, self.segundos_hasta_la_proxima_mata(ancho_mata) - adelanto
        )

        # Primer animal marino: a los pocos segundos de empezar
        self.temporizador_enemigo = random.uniform(2.0, 4.0)

        # Burbujas: ya hay algunas en pantalla al empezar
        for _ in range(BURBUJAS_INICIALES):
            self.generar_burbuja_del_fondo(random.randint(0, self.alto))

        self.temporizador_burbuja = random.uniform(*INTERVALO_BURBUJAS)


    # ---------------------------------------------------------------
    # Generación de algas, animales y burbujas
    #
    # Los obstáculos nacen fuera de la pantalla, a la derecha, y se mueven hacia
    # la izquierda. Cuándo aparece el siguiente se decide con un temporizador
    # (y no con la posición del pez, que no se mueve en horizontal).
    # ---------------------------------------------------------------

    def generar_mata_de_algas(self, x, centro_anterior):
        """Crea el par de algas (arriba y abajo) con un hueco en el medio.

        Cada alga es una mata de 1 a MAX_HEBRAS hebras juntas, verdes y violetas.
        Devuelve (ancho de la mata, centro del hueco).
        """

        hebras = random.randint(1, MAX_HEBRAS)
        ancho = ANCHO_HEBRA + (hebras - 1) * SEPARACION_HEBRAS

        # El hueco cambia de altura de a poco para que siempre se pueda llegar
        minimo = MARGEN_HUECO + ALTURA_HUECO // 2
        maximo = self.alto - MARGEN_HUECO - ALTURA_HUECO // 2
        centro = centro_anterior + random.randint(-MAX_CAMBIO_HUECO, MAX_CAMBIO_HUECO)
        centro = max(minimo, min(maximo, centro))

        borde_superior = centro - ALTURA_HUECO // 2
        borde_inferior = centro + ALTURA_HUECO // 2

        alga_sup = Alga(x, borde_superior, ancho, borde_superior, es_superior=True)
        alga_inf = Alga(x, borde_inferior, ancho, self.alto - borde_inferior, es_superior=False)

        # Cada alga sabe dónde está el centro de su hueco (se usa al reaparecer)
        alga_sup.centro_hueco = centro
        alga_inf.centro_hueco = centro

        self.todos.add(alga_sup, alga_inf)
        self.obstaculos.add(alga_sup, alga_inf)

        return ancho, centro

    def segundos_hasta_la_proxima_mata(self, ancho_mata):
        """Tiempo que tarda una mata (que nace en el borde derecho) en dejar
        el espacio libre para que nazca la siguiente."""

        espacio_libre = random.randint(*ESPACIO_LIBRE_ENTRE_ALGAS)

        return (ancho_mata + espacio_libre) / VELOCIDAD_ALGA

    def generar_animal(self):
        """Pez, pulpo o tiburón (cada uno se mueve distinto, ver enemigo.py).

        AnimalMarino suma entre 50 y 200 px a la x que recibe.
        """

        animal = AnimalMarino(self.ancho, self.alto, elegir_tipo())

        self.todos.add(animal)
        self.enemigos.add(animal)

    def generar_burbuja_del_fondo(self, y=None):
        """Crea una burbuja que sube desde el piso (o desde la altura y indicada)."""

        if y is None:
            y = self.alto + 20

        self.burbujas.add(Burbuja(random.randint(0, self.ancho), y))

    def soltar_burbujas_del_pez(self):
        """Un par de burbujas chicas salen de la boca del pez al nadar."""

        for _ in range(2):
            self.burbujas.add(
                Burbuja(
                    self.jugador.rect.right - 8 + random.randint(-4, 4),
                    self.jugador.rect.centery - 6 + random.randint(-6, 6),
                    radio=random.randint(3, 6)
                )
            )


    # ---------------------------------------------------------------
    # Eventos
    # ---------------------------------------------------------------

    def nadar(self):
        """El pez salta hacia arriba: impulso, sonido y burbujas."""

        # Cuando va hacia el tubo de la meta, maneja solo
        if self.piloto_automatico:
            return

        self.jugador.saltar()
        reproducir_efecto(self.sonidos["salto"])
        self.soltar_burbujas_del_pez()

    def manejar_evento(self, evento):
        """Espacio o clic izquierdo: el pez nada hacia arriba."""

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            self.nadar()

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.nadar()


    # ---------------------------------------------------------------
    # Puntaje
    # ---------------------------------------------------------------

    def sumar_puntos(self, cantidad, color, desde):
        """Suma puntos y muestra un aviso ("+10") que sube desde el pez."""

        self.puntaje += cantidad

        texto = self.fuente_avisos.render(f"+{cantidad}", True, color)
        contorno = self.fuente_avisos.render(f"+{cantidad}", True, (0, 20, 60))

        aviso = pygame.Surface((texto.get_width() + 4, texto.get_height() + 4), pygame.SRCALPHA)
        aviso.blit(contorno, (2, 3))
        aviso.blit(texto, (0, 0))

        self.avisos.append([aviso, desde[0], desde[1], DURACION_AVISO])

    def contar_puntos(self):
        """Suma los puntos de lo que el pez acaba de dejar atrás.

        - Una mata de algas da PUNTOS_POR_ALGA (se cuenta solo el alga de arriba,
          así el par no suma doble).
        - Un animal da los puntos de su tipo, pero solo si se lo esquivó: si el pez
          lo toca, el animal desaparece y no suma nada.

        Se cuenta cuando el objeto ya pasó por completo el borde izquierdo del pez.
        """

        borde_pez = self.jugador.rect.left
        posicion_aviso = (self.jugador.rect.right + 10, self.jugador.rect.top - 10)

        for alga in self.obstaculos:

            if alga.es_superior and not alga.superada and alga.rect.right < borde_pez:

                alga.superada = True
                self.sumar_puntos(PUNTOS_POR_ALGA, COLOR_AVISO_ALGA, posicion_aviso)

        for animal in self.enemigos:

            if not animal.esquivado and animal.rect.right < borde_pez:

                animal.esquivado = True
                self.sumar_puntos(animal.puntos, COLOR_AVISO_ANIMAL, posicion_aviso)


    # ---------------------------------------------------------------
    # Colisiones
    # ---------------------------------------------------------------

    def procesar_colisiones(self):

        # Mientras entra al tubo de la meta no puede chocar
        if self.invulnerable > 0 or self.piloto_automatico:
            return

        # collide_mask: solo cuentan los píxeles dibujados, no el rectángulo
        alga = pygame.sprite.spritecollideany(
            self.jugador, self.obstaculos, pygame.sprite.collide_mask
        )
        animal = None

        if not alga:
            animal = pygame.sprite.spritecollideany(
                self.jugador, self.enemigos, pygame.sprite.collide_mask
            )

        if not alga and not animal:
            return

        self.vidas -= 1

        print(
            f"¡Colisión con {'alga' if alga else 'enemigo'}! "
            f"Vidas restantes: {self.vidas}"
        )

        reproducir_efecto(self.sonidos["colision"])

        # Si choca con un enemigo, desaparece (y no suma puntos)
        if animal:
            animal.kill()

        # El pez sigue en su lugar (nunca retrocede). Si chocó con un alga, se lo
        # acomoda en el centro del hueco para que el mismo alga no lo vuelva a tocar
        self.jugador.reaparecer(alga.centro_hueco if alga else None)

        # Activar invulnerabilidad
        self.invulnerable = DURACION_INVULNERABILIDAD

        if self.vidas <= 0:
            reproducir_efecto(self.sonidos["perder"])
            self.estado_final = "derrota"


    # ---------------------------------------------------------------
    # Actualización
    # ---------------------------------------------------------------

    @property
    def tiempo_restante(self):
        return max(0, int(LIMITE_TIEMPO - self.tiempo))

    def actualizar(self, dt):
        """Avanza la partida dt segundos."""

        dt = min(dt, DT_MAXIMO)

        self.tiempo += dt

        if self.invulnerable > 0:
            self.invulnerable = max(0, self.invulnerable - dt)

        restante = LIMITE_TIEMPO - self.tiempo

        # La meta sale cuando falta el tiempo justo para que llegue al pez
        if self.meta is None and restante <= self.segundos_meta:
            self.meta = Meta(self.ancho, self.alto)
            self.todos.add(self.meta)

        # Cuando el tubo se acerca, el pez se acomoda solo a su altura
        if (
            self.meta is not None
            and not self.piloto_automatico
            and self.meta.rect.left <= self.jugador.rect.right + DISTANCIA_PILOTO
        ):
            self.piloto_automatico = True
            self.jugador.activar_piloto(self.meta.centro_tubo_y)

        # Hasta poco antes de la meta se siguen generando algas y animales
        if restante > self.segundos_meta + SEGUNDOS_DESPEJADOS:

            self.temporizador_alga -= dt

            if self.temporizador_alga <= 0:
                # Nace justo fuera de la pantalla, a la derecha
                ancho_mata, self.centro_hueco = self.generar_mata_de_algas(self.ancho, self.centro_hueco)
                self.temporizador_alga += self.segundos_hasta_la_proxima_mata(ancho_mata)

            self.temporizador_enemigo -= dt

            if self.temporizador_enemigo <= 0:
                self.generar_animal()
                self.temporizador_enemigo = random.uniform(*INTERVALO_ENEMIGOS)

        self.todos.update(dt)

        # Burbujas de ambiente
        self.burbujas.update(dt)
        self.temporizador_burbuja -= dt

        if self.temporizador_burbuja <= 0:
            self.generar_burbuja_del_fondo()
            self.temporizador_burbuja = random.uniform(*INTERVALO_BURBUJAS)

        # Avisos de puntos: suben y se apagan
        for aviso in self.avisos:
            aviso[2] -= 70 * dt
            aviso[3] -= dt
        self.avisos = [aviso for aviso in self.avisos if aviso[3] > 0]

        self.contar_puntos()
        self.procesar_colisiones()

        # Fin de la partida (perder tiene prioridad sobre ganar)
        if self.estado_final is None and self.tiempo >= LIMITE_TIEMPO:

            self.estado_final = "victoria"
            self.bonus = BONUS_META
            self.puntaje += self.bonus


    # ---------------------------------------------------------------
    # Dibujado
    # ---------------------------------------------------------------

    def dibujar(self, pantalla, fuente_hud):

        pantalla.fill(COLOR_FONDO)

        # Las burbujas van por detrás de todo lo demás
        self.burbujas.draw(pantalla)

        for sprite in self.todos:

            # Efecto visual durante la invulnerabilidad: el pez parpadea
            if sprite is self.jugador and self.invulnerable > 0:

                if int(pygame.time.get_ticks() / 100) % 2 == 0:
                    continue

            pantalla.blit(sprite.image, sprite.rect)

        # Avisos de puntos
        for imagen, x, y, segundos in self.avisos:

            transparencia = int(255 * min(1.0, segundos / 0.4))
            imagen.set_alpha(transparencia)
            pantalla.blit(imagen, (x, y))

        dibujar_hud(
            pantalla,
            fuente_hud,
            self.puntaje,
            self.vidas,
            self.tiempo_restante
        )


def jugar(pantalla, reloj, sonidos):
    """Juega una partida completa.

    Devuelve un Resultado (ver arriba). Si se cierra la ventana, el estado es "salir".
    """

    partida = Partida(pantalla, sonidos)
    fuente_hud = inicializar_fuente(36)

    while True:

        dt = reloj.tick(FPS) / 1000.0

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return Resultado("salir", partida.puntaje, 0, None)

            partida.manejar_evento(evento)

        partida.actualizar(dt)
        partida.dibujar(pantalla, fuente_hud)
        pygame.display.flip()

        if partida.estado_final is not None:

            return Resultado(
                partida.estado_final,
                partida.puntaje,
                partida.bonus,
                pantalla.copy()
            )
