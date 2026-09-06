# 🐟 Flappy Ocean

## Descripción
**Flappy Ocean** es un juego 2D desarrollado en Python utilizando Pygame. El jugador controla a un pez que debe navegar a través de las profundidades marinas evitando obstáculos colisionables (algas) y esquivando animales marinos con trayectorias fijas. El juego incluye un sistema de vidas, barra de energía, escenarios dinámicos y un límite de tiempo de 1 minuto por sesión.

Proyecto desarrollado para la materia Software Factory II.

## Cómo jugar
1. Al iniciar, presiona el botón **Jugar** o la **Barra Espaciadora**.
2. Presiona el **Clic Izquierdo del Mouse** o la **Barra Espaciadora** para impulsar el pez hacia arriba. Al soltar, el pez descenderá.
3. Atraviesa las aberturas entre las algas de colores para sumar puntos.
4. Evita los animales marinos; tocar uno reducirá tu **barra de energía**.
5. Si chocas contra un alga, perderás una **vida** y retrocederás a una posición segura.
6. Sobrevive el máximo tiempo posible antes de que se agote el tiempo (1 minuto).

## Funcionalidades
- [x] Pantalla de inicio con menú y tutorial de controles
- [ ] Mecánica de físicas de nado (impulso y gravedad)
- [ ] Sistema de escenarios variados (2-3 mapas)
- [ ] Obstáculos fijos (algas) y móviles (fauna marina)
- [ ] HUD en tiempo real (Puntaje, Vidas, Energía, Tiempo)
- [ ] Sistema de persistencia de datos (Ranking Top 5 con SQLite)
- [ ] Opciones de reinicio y salida

## Requisitos e Instalación

### Requisitos previos
- Python 3.8 o superior
- Pygame

### Instalación de dependencias
```bash
pip install pygame


### Ejecutar el juego

cd src
python main.py


## Estructura del Proyecto

flappy-ocean/
├── .gitignore
├── README.md
├── docs/
│   ├── requerimientos.md
│   └── diagrama_flujo.md
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── src/
├── database/

Tecnologías
Python 3
Pygame
SQLite3
Git / GitHub

Autor
Marco Paz - @MarcoPazMartinez

Software Factory II - ITES 2026