"""Pantalla de Ranking: muestra los 5 mejores puntajes guardados en SQLite."""
import sqlite3

import pygame

import db
from interfaz import (
    COLOR_BORDE_TITULO,
    COLOR_TITULO,
    Boton,
    procesar_evento,
    texto_con_borde,
)
from recursos import cargar_fondo

COLOR_FONDO_RESPALDO = (20, 60, 140)
COLORES_PODIO = [(255, 215, 60), (215, 220, 230), (225, 150, 90)]   # oro, plata y bronce
COLOR_FILA = (255, 255, 255)


def leer_ranking():
    """Devuelve (filas, hubo_error). Si la base falla, el juego no se cae."""
    try:
        return db.obtener_top(5), False
    except sqlite3.Error as error:
        print(f"Aviso: no se pudo leer el ranking ({error}).")
        return [], True


def mostrar_ranking(pantalla, reloj):
    """Muestra el Top 5 hasta que se vuelva a la portada.

    Devuelve "volver" o "salir" (si se cerró la ventana).
    """
    ancho, alto = pantalla.get_size()
    centro_x = ancho // 2

    fondo = cargar_fondo("portada.png", (ancho, alto), COLOR_FONDO_RESPALDO)

    fuente_titulo = pygame.font.Font(None, 110)
    fuente_fila = pygame.font.Font(None, 52)
    fuente_mensaje = pygame.font.Font(None, 40)
    fuente_boton = pygame.font.Font(None, 48)

    titulo = texto_con_borde(fuente_titulo, "Ranking", COLOR_TITULO, COLOR_BORDE_TITULO, 5)

    # La base se consulta UNA vez al entrar, no en cada vuelta del bucle
    filas, hubo_error = leer_ranking()

    panel = pygame.Surface((680, 380), pygame.SRCALPHA)
    pygame.draw.rect(panel, (5, 25, 70, 215), panel.get_rect(), border_radius=20)
    pygame.draw.rect(panel, (255, 255, 255), panel.get_rect(), 3, border_radius=20)
    rect_panel = panel.get_rect(center=(centro_x, int(alto * 0.50)))

    boton_volver = Boton("Volver", "volver", (centro_x, int(alto * 0.88)), (260, 60))
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
        pantalla.blit(titulo, titulo.get_rect(center=(centro_x, int(alto * 0.15))))
        pantalla.blit(panel, rect_panel)

        if filas:
            for posicion, (nombre, puntaje) in enumerate(filas):
                y = rect_panel.top + 60 + posicion * 62
                color = COLORES_PODIO[posicion] if posicion < 3 else COLOR_FILA

                numero = fuente_fila.render(f"{posicion + 1}.", True, color)
                texto_nombre = fuente_fila.render(str(nombre)[:14], True, color)
                texto_puntaje = fuente_fila.render(str(puntaje), True, color)

                pantalla.blit(numero, (rect_panel.left + 50, y))
                pantalla.blit(texto_nombre, (rect_panel.left + 130, y))
                pantalla.blit(texto_puntaje, texto_puntaje.get_rect(topright=(rect_panel.right - 50, y)))
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
