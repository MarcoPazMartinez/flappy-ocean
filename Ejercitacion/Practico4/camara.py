import pygame


class Camara:

  def __init__(self, ancho_mundo, alto_mundo, ancho_pantalla, alto_pantalla):
    self.ancho_mundo = ancho_mundo
    self.alto_mundo = alto_mundo
    self.ancho_pantalla = ancho_pantalla
    self.alto_pantalla = alto_pantalla
    self.offset_x = 0
    self.offset_y = 0

  def seguir(self, objetivo):
    
    self.offset_x = objetivo.centerx - self.ancho_pantalla // 2
    self.offset_y = objetivo.centery - self.alto_pantalla // 2

    
    self.offset_x = max(
        0, min(self.offset_x, self.ancho_mundo - self.ancho_pantalla)
    )
    self.offset_y = max(
        0, min(self.offset_y, self.alto_mundo - self.alto_pantalla)
    )

  def aplicar(self, rect):
    
    return rect.move(-self.offset_x, -self.offset_y)