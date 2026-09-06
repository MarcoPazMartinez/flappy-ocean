# Requerimientos - Flappy Ocean

## Requerimientos Funcionales

* **RF-01**: El jugador controla un pez cuyo movimiento vertical se eleva al hacer clic izquierdo con el mouse o presionar la barra espaciadora, y desciende automáticamente al soltar el control.
* **RF-02**: El escenario avanza horizontalmente generando obstáculos representados por algas de colores con aberturas para el paso del pez.
* **RF-03**: Aparecen animales marinos con trayectorias y patrones de movimiento predefinidos dentro del escenario.
* **RF-04**: El jugador inicia la partida con 3 vidas y una barra de energía llena.
* **RF-05**: Al chocar contra un alga, el jugador pierde 1 vida, el pez es reubicado en una posición segura detrás del obstáculo y el juego se pausa hasta que el jugador vuelva a presionar la barra espaciadora o haga clic.
* **RF-06**: Al colisionar con un animal marino, se reduce un porcentaje de la barra de energía del jugador.
* **RF-07**: La partida finaliza (Game Over) si el jugador pierde las 3 vidas, si la barra de energía llega a cero, o si transcurre el tiempo límite de 1 minuto (60 segundos).
* **RF-08**: Durante la partida se muestra un HUD en la parte superior con: puntaje acumulado, vidas restantes, barra de energía y tiempo transcurrido.
* **RF-09**: El juego dispone de 2 a 3 diseños de escenarios (mapas) con distintas disposiciones de algas y rutas de animales marinos para evitar la memorización.
* **RF-10**: Al finalizar la partida, el puntaje final se registra automáticamente en una base de datos SQLite.
* **RF-11**: Existe una pantalla de Ranking que consulta SQLite y despliega el Top 5 de puntuaciones más altas registradas.
* **RF-12**: El juego permite al jugador reiniciar la partida (reestableciendo vidas y energía) o salir del programa desde la pantalla final.

## Requerimientos No Funcionales

* **RNF-01**: El juego debe ejecutarse de forma fluida a 60 FPS estables utilizando Pygame.
* **RNF-02**: Los controles de entrada deben responder de manera inmediata y suave aplicando Delta Time (`dt`).
* **RNF-03**: El código debe estructurarse de manera modular en archivos independientes dentro de `src/`.
* **RNF-04**: La interfaz del juego debe adaptarse a una resolución fija de 800x600 píxeles.