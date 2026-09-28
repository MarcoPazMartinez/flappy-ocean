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
        """Centra la cámara horizontalmente en el jugador y calcula el desplazamiento."""
    
        self.offset_x = objetivo.rect.centerx - self.ancho_pantalla // 3
        self.offset_y = 0  

        
        self.offset_x = max(0, min(self.offset_x, self.ancho_mundo - self.ancho_pantalla))

    def aplicar(self, rect):
        """Devuelve un rectángulo trasladado a las coordenadas de pantalla usando el offset."""
        return rect.move(-self.offset_x, -self.offset_y)