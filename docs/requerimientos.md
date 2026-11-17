# Requerimientos - Flappy Ocean

## Requerimientos Funcionales

* **RF-01**: El jugador controla un pez cuyo movimiento vertical se eleva al hacer clic izquierdo con el mouse o presionar la barra espaciadora, y desciende automáticamente al soltar el control.
* **RF-02**: El escenario avanza horizontalmente generando obstáculos representados por algas de colores con aberturas para el paso del pez.
* **RF-03**: Aparecen animales marinos con trayectorias y patrones de movimiento predefinidos dentro del escenario.
* **RF-04**: El jugador inicia la partida con 3 vidas y una barra de energía llena.
* **RF-05**: Al chocar contra un alga, el jugador pierde 1 vida, el pez es reubicado en una posición segura (en el centro del hueco entre las algas, sin moverse de su posición horizontal) y el juego se pausa hasta que el jugador vuelva a presionar la barra espaciadora o haga clic.
* **RF-06**: Al colisionar con un animal marino, se reduce un porcentaje de la barra de energía del jugador.
* **RF-07**: La partida finaliza con **Game Over** si el jugador pierde las 3 vidas o si la barra de energía llega a cero. Si sobrevive hasta que se cumple el tiempo límite de 2 minutos (120 segundos), llega a la meta (un tubo de cristal al que el pez entra nadando) y **gana** la partida.
* **RF-08**: Durante la partida se muestra un HUD en la parte superior con: puntaje acumulado, vidas restantes, barra de energía y tiempo transcurrido.
* **RF-09**: El juego dispone de 2 a 3 diseños de escenarios (mapas) con distintas disposiciones de algas y rutas de animales marinos para evitar la memorización.
* **RF-10**: Al finalizar la partida, si el puntaje entra entre los 10 mejores, se le pide el nombre al jugador y se registra en una base de datos SQLite. La base conserva únicamente los 10 mejores puntajes.
* **RF-11**: Existe una pantalla de Ranking que consulta SQLite y despliega el Top 10 de puntuaciones más altas registradas. Se accede desde la portada y también se muestra al final de cada partida, con el puesto del jugador resaltado.
* **RF-12**: Al terminar la partida, la pantalla de resultados permite **volver al inicio** (y empezar una partida nueva con vidas, energía y puntaje en su valor inicial) o **salir** del programa.
* **RF-13**: El puntaje suma 10 puntos por cada mata de algas que el pez deja atrás y puntos por cada animal marino esquivado según su dificultad (pez 5, pulpo 15, tiburón 25). Si el animal toca al pez no suma. Al llegar a la meta se suman 100 puntos de bonus.
* **RF-14**: El juego arranca en una portada con tres botones: **Jugar**, **Ranking** y **Salir**.

## Requerimientos No Funcionales

* **RNF-01**: El juego debe ejecutarse de forma fluida a 60 FPS estables utilizando Pygame.
* **RNF-02**: Los controles de entrada deben responder de manera inmediata y suave aplicando Delta Time (`dt`).
* **RNF-03**: El código debe estructurarse de manera modular en archivos independientes dentro de `src/`.
* **RNF-04**: La interfaz del juego debe adaptarse a una resolución fija de 1280x720 píxeles.