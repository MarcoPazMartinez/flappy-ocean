
import pygame

from recursos import cargar_imagen

VELOCIDAD_PILOTO = 350   # px/s con que el pez se acomoda solo frente a la meta


class Jugador(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image = cargar_imagen("jugador.png", (80, 80), (0, 200, 255))

        # La máscara marca los píxeles dibujados del pez: las colisiones
        # ignoran las esquinas transparentes de la imagen
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Posición con la que empieza: el pez siempre vuelve a la misma x
        self.x_inicial = x
        self.y_inicial = y

        self.velocidad_y = 0
        self.gravedad = 600
        self.fuerza_salto = -300

        # Piloto automático (se usa al llegar a la meta)
        self.objetivo_y = None
        self.y_piloto = 0.0


    def saltar(self):

        """Impulsa al pez hacia arriba."""

        self.velocidad_y = self.fuerza_salto


    def reaparecer(self, centro_y=None):

        """Vuelve a poner al pez en su lugar después de una colisión.

        Nunca retrocede: la posición horizontal es siempre la inicial. Si se
        indica centro_y (por ejemplo, el centro del hueco entre las algas), el
        pez aparece a esa altura, a salvo del obstáculo; si no, queda a la
        altura en la que estaba.
        """

        self.rect.x = self.x_inicial

        if centro_y is not None:
            self.rect.centery = round(centro_y)

        self.velocidad_y = 0


    def activar_piloto(self, objetivo_y):

        """El pez deja de caer y se acomoda solo a la altura indicada."""

        self.objetivo_y = objetivo_y
        self.y_piloto = float(self.rect.centery)
        self.velocidad_y = 0


    def update(self, dt):

        """Actualiza el movimiento aplicando gravedad."""

        if self.objetivo_y is not None:

            # Piloto automático: va hacia la altura objetivo sin gravedad
            diferencia = self.objetivo_y - self.y_piloto
            paso = VELOCIDAD_PILOTO * dt

            self.y_piloto += max(-paso, min(paso, diferencia))
            self.rect.centery = round(self.y_piloto)

            return

        self.velocidad_y += self.gravedad * dt

        self.rect.y += self.velocidad_y * dt

        pantalla_rect = pygame.display.get_surface().get_rect()

        self.rect.clamp_ip(pantalla_rect)
