"""Autoverificación del juego, sin necesidad de jugar.

    python main.py --verificar          (código normal)
    FlappyDiver.exe --verificar         (el ejecutable)

Comprueba que el juego está completo y funciona: que están todos los archivos, que las
imágenes y los sonidos se cargan, que se puede simular una partida sin errores y que el
ranking se guarda en la base de datos. Escribe el resultado en `verificacion.txt` (el .exe
no tiene consola) y termina con código 0 si todo está bien o 1 si algo falló.

Sirve sobre todo para el .exe: si falta una imagen o un sonido dentro del ejecutable, el
juego igual arranca (usa colores de respaldo o queda sin sonido) y nadie se entera hasta
que lo ve. Esta verificación lo detecta.
"""
import os
import shutil
import sys
import tempfile

import pygame

import db
import recursos
from rutas import carpeta_datos, carpeta_recursos, esta_empaquetado, ruta_recurso

IMAGENES = (
    "portada.png", "jugador.png", "enemigo.png", "pulpo.png",
    "tiburon.png", "alga.png", "alga_violeta.png",
)
SONIDOS = ("salto.ogg", "colision.wav", "perder.ogg", "musica_fondo.ogg")

OK, AVISO, ERROR = "OK   ", "AVISO", "ERROR"


class Informe:
    """Junta los resultados de cada comprobación."""

    def __init__(self):
        self.lineas = []
        self.errores = 0

    def agregar(self, estado, texto):
        self.lineas.append(f"[{estado}] {texto}")
        if estado == ERROR:
            self.errores += 1

    def comprobar(self, condicion, texto_ok, texto_error):
        self.agregar(OK if condicion else ERROR, texto_ok if condicion else texto_error)
        return condicion


def verificar_archivos(informe):
    """Que estén todos los archivos del juego (y que no se hayan quedado afuera del .exe)."""
    for nombre in IMAGENES:
        ruta = ruta_recurso("assets", "images", nombre)
        if not os.path.exists(ruta):
            informe.agregar(ERROR, f"falta la imagen {nombre} ({ruta})")
            continue
        try:
            ancho, alto = pygame.image.load(ruta).get_size()
            informe.agregar(OK, f"imagen {nombre} ({ancho}x{alto})")
        except pygame.error as error:
            informe.agregar(ERROR, f"la imagen {nombre} no se puede abrir: {error}")

    for nombre in SONIDOS:
        ruta = ruta_recurso("assets", "sounds", nombre)
        informe.comprobar(
            os.path.exists(ruta),
            f"archivo de sonido {nombre} ({os.path.getsize(ruta) // 1024} KB)" if os.path.exists(ruta) else "",
            f"falta el sonido {nombre} ({ruta})",
        )


def verificar_audio(informe):
    """Que los sonidos se puedan decodificar (si hay un dispositivo de audio)."""
    import audio

    if not audio.inicializar_audio():
        informe.agregar(AVISO, "no hay dispositivo de audio: el juego funciona, pero en silencio")
        return

    informe.agregar(OK, f"audio iniciado: {pygame.mixer.get_init()}")

    for nombre in SONIDOS[:-1]:
        sonido = audio.cargar_sonido(nombre)
        if sonido is None:
            informe.agregar(ERROR, f"el sonido {nombre} no se pudo cargar")
        else:
            informe.comprobar(sonido.get_length() > 0.02,
                              f"sonido {nombre} se decodifica ({sonido.get_length():.2f} s)",
                              f"el sonido {nombre} está vacío")

    try:
        pygame.mixer.music.load(ruta_recurso("assets", "sounds", SONIDOS[-1]))
        informe.agregar(OK, f"música {SONIDOS[-1]} se carga")
    except pygame.error as error:
        informe.agregar(ERROR, f"la música no se pudo cargar: {error}")


def verificar_partida(informe):
    """Simula una partida entera: imágenes, fuentes, animales, meta, puntaje y dibujo."""
    from enemigo import TIPOS, AnimalMarino
    from hud import dibujar_hud, inicializar_fuente
    from interfaz import Boton, crear_panel, texto_con_borde
    from meta import Meta
    from partida import Partida

    ANCHO, ALTO = 1280, 720

    try:
        pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.HIDDEN)   # sin mostrar la ventana
    except (AttributeError, pygame.error):
        pantalla = pygame.display.set_mode((ANCHO, ALTO))

    sonidos = {"salto": None, "colision": None, "perder": None}
    partida = Partida(pantalla, sonidos)

    # Los tres tipos de animal y la meta, así se cargan todas las imágenes
    for tipo in TIPOS:
        animal = AnimalMarino(ANCHO, ALTO, tipo)
        partida.todos.add(animal)
    partida.todos.add(Meta(ANCHO, ALTO))

    fuente = inicializar_fuente(36)
    partida.dibujar(pantalla, fuente)

    # Piezas de las pantallas (portada, ranking, cartel final)
    recursos.cargar_fondo("portada.png", (ANCHO, ALTO), (20, 60, 140))
    texto_con_borde(pygame.font.Font(None, 100), "Flappy Diver", (255, 170, 50), (110, 50, 0), 4)
    Boton("Jugar", "jugar", (640, 300)).dibujar(pantalla, fuente, True)
    crear_panel((700, 400))

    # Una partida de 12 segundos jugando (el pez salta cuando baja del centro)
    pasos = 0
    for pasos in range(720):
        if partida.jugador.rect.centery > ALTO // 2 + 40 and partida.jugador.velocidad_y >= 0:
            partida.nadar()
        partida.actualizar(1 / 60)
        if pasos % 6 == 0:
            partida.dibujar(pantalla, fuente)
        if partida.estado_final:
            break
    dibujar_hud(pantalla, fuente, partida.puntaje, partida.vidas, partida.tiempo_restante)

    informe.agregar(
        OK,
        f"partida simulada: {pasos + 1} cuadros, puntaje {partida.puntaje}, vidas {partida.vidas}, "
        f"{len(partida.todos)} sprites y {len(partida.burbujas)} burbujas",
    )

    faltantes = sorted(set(recursos.imagenes_faltantes))
    informe.comprobar(
        not faltantes,
        "todas las imágenes del juego se dibujaron (ninguna con color de respaldo)",
        f"imágenes que se reemplazaron por un color de respaldo: {', '.join(faltantes)}",
    )


def verificar_base(informe):
    """Que el ranking se guarde, se ordene y se limite a 10, y que se guarde en un lugar permanente."""
    temporal = tempfile.mkdtemp()
    try:
        ruta = os.path.join(temporal, "prueba.db")
        db.init_db(ruta)
        for numero in range(1, 13):
            db.guardar_puntaje(f"Prueba{numero}", numero * 10, ruta)
        mejores = db.obtener_top(50, ruta)
        informe.comprobar(
            len(mejores) == db.LIMITE_RANKING and mejores[0][1] == 120 and mejores[-1][1] == 30,
            f"base de datos: se guardan 12 puntajes y quedan solo los {db.LIMITE_RANKING} mejores, ordenados",
            f"base de datos con resultados inesperados: {mejores}",
        )
    finally:
        shutil.rmtree(temporal, ignore_errors=True)

    ok_real, detalle = db.comprobar_base()
    informe.comprobar(ok_real, f"base del ranking: {detalle}", f"la base del ranking no responde: {detalle}")

    datos = os.path.abspath(carpeta_datos())
    if esta_empaquetado():
        temporal_exe = os.path.abspath(carpeta_recursos())
        informe.comprobar(
            not datos.startswith(temporal_exe),
            f"los datos se guardan en un lugar permanente: {datos}",
            f"los datos quedarían en la carpeta temporal del .exe y se perderían al cerrar: {datos}",
        )


def verificar():
    """Corre todas las comprobaciones. Devuelve True si no hay ningún error."""
    informe = Informe()

    modo = "ejecutable (.exe)" if esta_empaquetado() else "código de Python"
    informe.agregar(OK, f"corre como: {modo}")
    informe.agregar(OK, f"Python {sys.version.split()[0]}, pygame {pygame.version.ver}")
    informe.agregar(OK, f"recursos en: {carpeta_recursos()}")
    informe.agregar(OK, f"datos en: {carpeta_datos()}")

    pygame.init()

    for etapa in (verificar_archivos, verificar_audio, verificar_partida, verificar_base):
        try:
            etapa(informe)
        except Exception as error:      # cualquier falla de una etapa se informa, no corta la verificación
            informe.agregar(ERROR, f"{etapa.__name__} falló: {type(error).__name__}: {error}")

    resumen = "TODO BIEN" if informe.errores == 0 else f"HAY {informe.errores} ERROR(ES)"
    informe.lineas.append("")
    informe.lineas.append(f"RESULTADO: {resumen}")
    texto = "\n".join(informe.lineas)

    print(texto)

    try:
        with open(os.path.join(carpeta_datos(), "verificacion.txt"), "w", encoding="utf-8") as archivo:
            archivo.write(texto + "\n")
    except OSError:
        pass

    return informe.errores == 0
