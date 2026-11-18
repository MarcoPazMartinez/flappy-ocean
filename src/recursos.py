"""Carga de imágenes con caché y color de respaldo."""
import os

import pygame

from rutas import ruta_recurso

RUTA_IMAGENES = ruta_recurso("assets", "images")

_cache = {}

# Nombres de las imágenes que no se pudieron cargar y se reemplazaron por un color.
# El juego sigue andando igual, pero la verificación (`main.py --verificar`) lo usa
# para avisar que falta un archivo.
imagenes_faltantes = []


def cargar_imagen(nombre, tamano, color_respaldo):
    """Devuelve la imagen escalada. Se carga una sola vez por (nombre, tamaño).

    Hay que llamarla DESPUÉS de pygame.display.set_mode(), porque
    convert_alpha() necesita la ventana creada.
    """
    clave = (nombre, tamano)
    if clave in _cache:
        return _cache[clave]

    ruta = os.path.join(RUTA_IMAGENES, nombre)
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        imagen = pygame.transform.smoothscale(imagen, tamano)
    except (pygame.error, FileNotFoundError):
        print(f"Aviso: no se pudo cargar '{nombre}', se usa un color de respaldo.")
        imagenes_faltantes.append(nombre)
        imagen = pygame.Surface(tamano, pygame.SRCALPHA)
        imagen.fill(color_respaldo)

    _cache[clave] = imagen
    return imagen


def cargar_fondo(nombre, tamano, color_respaldo):
    """Devuelve una imagen de fondo que llena toda la pantalla sin deformarse.

    La imagen se agranda hasta cubrir el tamaño pedido y se recorta lo que
    sobra por los bordes (siempre desde el centro).
    """
    clave = (nombre, tamano, "fondo")
    if clave in _cache:
        return _cache[clave]

    ancho, alto = tamano
    ruta = os.path.join(RUTA_IMAGENES, nombre)
    try:
        imagen = pygame.image.load(ruta).convert()

        escala = max(ancho / imagen.get_width(), alto / imagen.get_height())
        nuevo_tamano = (
            round(imagen.get_width() * escala),
            round(imagen.get_height() * escala),
        )
        imagen = pygame.transform.smoothscale(imagen, nuevo_tamano)

        recorte = pygame.Rect(0, 0, ancho, alto)
        recorte.center = imagen.get_rect().center
        imagen = imagen.subsurface(recorte).copy()
    except (pygame.error, FileNotFoundError):
        print(f"Aviso: no se pudo cargar '{nombre}', se usa un color de respaldo.")
        imagenes_faltantes.append(nombre)
        imagen = pygame.Surface(tamano)
        imagen.fill(color_respaldo)

    _cache[clave] = imagen
    return imagen
