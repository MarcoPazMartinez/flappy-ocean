"""Pantalla de Ranking: muestra los mejores puntajes guardados en SQLite."""
import sqlite3

import pygame

import db
from interfaz import (
    COLOR_BORDE_TITULO,
    COLOR_TITULO,
    Boton,
    crear_panel,
    procesar_evento,
    texto_con_borde,
)
from recursos import cargar_fondo

COLOR_FONDO_RESPALDO = (20, 60, 140)
COLORES_PODIO = [(255, 215, 60), (215, 220, 230), (225, 150, 90)]   # oro, plata y bronce
COLOR_FILA = (255, 255, 255)
ALTO_FILA = 40


def leer_ranking():
    """Devuelve (filas, hubo_error). Si la base falla, el juego no se cae."""
    try:
        return db.obtener_top(db.LIMITE_RANKING), False
    except sqlite3.Error as error:
        print(f"Aviso: no se pudo leer el ranking ({error}).")
        return [], True


def altura_tabla(cantidad_de_filas=db.LIMITE_RANKING):
    """Alto del panel que contiene la tabla."""
    return cantidad_de_filas * ALTO_FILA + 40


def dibujar_tabla(pantalla, filas, rect, fuente, destacada=None):
    """Dibuja las filas del ranking dentro de `rect`.

    `destacada` es la posición (empezando en 0) que se resalta, por ejemplo el
    puntaje que acaba de hacer el jugador.
    """
    for posicion, (nombre, puntaje) in enumerate(filas):

        y = rect.top + 20 + posicion * ALTO_FILA
        color = COLORES_PODIO[posicion] if posicion < 3 else COLOR_FILA

        if posicion == destacada:
            resaltado = pygame.Surface((rect.width - 30, ALTO_FILA - 4), pygame.SRCALPHA)
            pygame.draw.rect(resaltado, (255, 255, 255, 60), resaltado.get_rect(), border_radius=10)
            pygame.draw.rect(resaltado, (255, 215, 60), resaltado.get_rect(), 2, border_radius=10)
            pantalla.blit(resaltado, (rect.left + 15, y - 4))

        numero = fuente.render(f"{posicion + 1}.", True, color)
        texto_nombre = fuente.render(str(nombre)[:db.LARGO_MAXIMO_NOMBRE + 4], True, color)
        texto_puntaje = fuente.render(str(puntaje), True, color)

        pantalla.blit(numero, (rect.left + 40, y))
        pantalla.blit(texto_nombre, (rect.left + 120, y))
        pantalla.blit(texto_puntaje, texto_puntaje.get_rect(topright=(rect.right - 40, y)))


def mostrar_ranking(pantalla, reloj):
    """Muestra el ranking hasta que se vuelva a la portada.

    Devuelve "volver" o "salir" (si se cerró la ventana).
    """
    ancho, alto = pantalla.get_size()
    centro_x = ancho // 2

    fondo = cargar_fondo("portada.png", (ancho, alto), COLOR_FONDO_RESPALDO)

    fuente_titulo = pygame.font.Font(None, 100)
    fuente_fila = pygame.font.Font(None, 42)
    fuente_mensaje = pygame.font.Font(None, 40)
    fuente_boton = pygame.font.Font(None, 48)

    titulo = texto_con_borde(fuente_titulo, "Ranking", COLOR_TITULO, COLOR_BORDE_TITULO, 5)

    # La base se consulta UNA vez al entrar, no en cada vuelta del bucle
    filas, hubo_error = leer_ranking()

    panel = crear_panel((700, altura_tabla()))
    rect_panel = panel.get_rect(center=(centro_x, int(alto * 0.50)))

    boton_volver = Boton("Volver", "volver", (centro_x, int(alto * 0.92)), (260, 56))
    botones = [boton_volver]
    seleccionado = 0

    while True:
        reloj.tick(60)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "volver"

            seleccionado, accion = procesar_evento(evento, botones, seleccionado)

            if accion is not None:
                return accion

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(titulo, titulo.get_rect(center=(centro_x, int(alto * 0.09))))
        pantalla.blit(panel, rect_panel)

        if filas:
            dibujar_tabla(pantalla, filas, rect_panel, fuente_fila)
        else:
            if hubo_error:
                mensajes = ["No se pudo leer el ranking."]
            else:
                mensajes = ["Todavía no hay puntajes.", "¡Jugá una partida para aparecer acá!"]

            for numero, mensaje in enumerate(mensajes):
                texto = fuente_mensaje.render(mensaje, True, COLOR_FILA)
                pantalla.blit(texto, texto.get_rect(center=(centro_x, rect_panel.centery - 20 + numero * 50)))

        boton_volver.dibujar(pantalla, fuente_boton, True)

        pygame.display.flip()
