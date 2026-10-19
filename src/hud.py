# src/hud.py
import pygame

def inicializar_fuente(tamano=36):
    """Carga la fuente una sola vez para optimizar rendimiento."""
    return pygame.font.Font(None, tamano)

def dibujar_hud(pantalla, fuente, puntaje, vidas, tiempo_restante):
    """
    dibuja el HUD en la pantalla con la información del juego.
    - Puntaje: Arriba a la izquierda.
    - Vidas: Arriba a la derecha.
    - Tiempo: En el centro.
    """
    ancho_pantalla = pantalla.get_width()

    #Puntaje arriba a la izquierda[cite: 2, 4]
    txt_puntaje = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(txt_puntaje, (10, 10))

    #Vidas arriba a la derecha[cite: 2, 4]
    txt_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 120, 120))
    pantalla.blit(txt_vidas, (ancho_pantalla - 130, 10))

    #Tiempo en el centro[cite: 2, 4]
    txt_tiempo = fuente.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 120))
    pantalla.blit(txt_tiempo, (ancho_pantalla // 2 - 60, 10))