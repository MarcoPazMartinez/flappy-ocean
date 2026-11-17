import pygame
import random
import math

from recursos import cargar_imagen


# Cada tipo de animal tiene su imagen, su tamaño y su forma de moverse:
#   - velocidad: px/s hacia la izquierda (se elige un valor al azar entre los dos)
#   - amplitud:  cuánto sube y baja en su onda, en px (0 = avanza en línea recta)
#   - frecuencia: qué tan rápido sube y baja
#   - peso: qué tan seguido aparece (mayor número = más seguido)
TIPOS = {
    # Pez: velocidad media y ondula
    "pez": {
        "imagen": "enemigo.png",
        "tamano": (72, 72),
        "color": (255, 100, 100),
        "velocidad": (180, 280),
        "amplitud": (30, 90),
        "frecuencia": (2.0, 5.0),
        "peso": 5,
    },
    # Pulpo: lento, pero sube y baja mucho y tapa buena parte de la pantalla
    "pulpo": {
        "imagen": "pulpo.png",
        "tamano": (96, 96),
        "color": (214, 76, 110),
        "velocidad": (110, 150),
        "amplitud": (110, 170),
        "frecuencia": (1.0, 1.8),
        "peso": 3,
    },
    # Tiburón: grande y muy rápido, en línea recta
    "tiburon": {
        "imagen": "tiburon.png",
        "tamano": (170, 85),
        "color": (112, 132, 156),
        "velocidad": (420, 520),
        "amplitud": (0, 0),
        "frecuencia": (0.0, 0.0),
        "peso": 2,
    },
}


def elegir_tipo():
    """Elige un tipo de animal al azar, según el peso de cada uno."""

    nombres = list(TIPOS)
    pesos = [TIPOS[nombre]["peso"] for nombre in nombres]

    return random.choices(nombres, weights=pesos)[0]


class AnimalMarino(pygame.sprite.Sprite):

    def __init__(self, x_mundo, alto_pantalla, tipo="pez"):
        super().__init__()

        datos = TIPOS[tipo]
        self.tipo = tipo

        imagen = cargar_imagen(datos["imagen"], datos["tamano"], datos["color"])

        # Las imágenes miran hacia la derecha, pero el animal nada hacia la
        # izquierda: se da vuelta (espejo horizontal)
        self.image = pygame.transform.flip(imagen, True, False)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        # Movimiento horizontal
        self.velocidad_x = random.uniform(*datos["velocidad"])

        # Movimiento ondulatorio
        self.amplitud_movimiento = random.uniform(*datos["amplitud"])
        self.frecuencia_y = random.uniform(*datos["frecuencia"])

        # Posición: nace a la derecha. En vertical se deja un margen igual a
        # lo que sube y baja, para que la onda no se salga de la pantalla
        margen = int(self.amplitud_movimiento) + 20
        y_minimo = margen
        y_maximo = alto_pantalla - self.rect.height - margen

        self.rect.x = x_mundo + random.randint(50, 200)
        self.rect.y = random.randint(y_minimo, y_maximo)

        self.tiempo_acumulado = 0

        # La posición real se guarda como float: el rect solo admite enteros y
        # con velocidades chicas (como la del pulpo) se perdería movimiento
        self.pos_x = float(self.rect.x)
        self.posicion_inicial_y = float(self.rect.y)

    def update(self, dt):
        """Actualiza el movimiento del animal marino."""

        self.pos_x -= self.velocidad_x * dt
        self.rect.x = round(self.pos_x)

        self.tiempo_acumulado += dt

        desplazamiento_y = self.amplitud_movimiento * math.sin(
            self.tiempo_acumulado * self.frecuencia_y
        )

        self.rect.y = round(self.posicion_inicial_y + desplazamiento_y)

        # Eliminar cuando sale de la pantalla por la izquierda
        if self.rect.right < 0:
            self.kill()
