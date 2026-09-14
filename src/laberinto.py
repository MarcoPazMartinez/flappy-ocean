import pygame 

MAPA = [
    "1111111111111111111111",
    "1000000000100000000001",
    "1011111010101111111101",
    "1010001010100000001001",
    "1010101011111110101001",
    "1000101000000010101001",
    "1110101110111010101101",
    "1000100010001000100001",
    "1011111011101111101101",
    "1000001000100000001001",
    "1111101110101111111011",
    "1000001010100000000001",
    "1011111010111111110101",
    "1000000010000000010101",
    "1111111111111111111111",
]


TILE = 40 

def obtener_paredes_y_dimensiones():
    paredes = []
    for fila, texto in enumerate(MAPA):
        for col, celda in enumerate(texto):
            if celda == "1":
                paredes.append(pygame.Rect(col * TILE, fila * TILE, TILE, TILE))
                
    ancho_mundo = len(MAPA[0]) * TILE
    alto_mundo = len(MAPA) * TILE
    return paredes, ancho_mundo, alto_mundo