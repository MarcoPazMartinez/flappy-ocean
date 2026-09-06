# Diagrama de Flujo de Pantallas - Flappy Ocean

## Descripción
Este documento describe el flujo de pantallas y navegación del juego Flappy Ocean.

## Pantallas del Juego

| Pantalla | Descripción | Cómo se llega |
| :--- | :--- | :--- |
| **Inicio** | Muestra el título "Flappy Ocean", arte de fondo marino, controles básicos y botón "Jugar". | Al iniciar la aplicación. |
| **Juego** | Desarrollo de la partida. Muestra al pez, algas, fauna marina y el HUD (Puntaje, Vidas, Energía, Tiempo). | Al presionar "Jugar" o la tecla indicada. |
| **Game Over** | Muestra la puntuación alcanzada e indica el motivo del fin de partida. Guarda el registro en SQLite. | Al perder las 3 vidas, agotar la energía o cumplirse 1 minuto. |
| **Ranking** | Consulta SQLite y muestra la lista ordenada con los 5 mejores puntajes (Top 5). | Automáticamente tras la pantalla de Game Over. |
| **Opciones Finales** | Opciones para reintentar ("Jugar nuevamente") o cerrar el programa ("Salir"). | Desde la Pantalla de Ranking. |

## Transiciones

| Desde | Evento / Condición | Hacia |
| :--- | :--- | :--- |
| Inicio | Clic en "Jugar" / Barra Espaciadora | Juego |
| Juego | Vidas = 0, Energía = 0 o Tiempo = 60s | Game Over |
| Game Over | Procesamiento automático (guardar récord) | Ranking |
| Ranking | Selección de "Continuar" | Opciones Finales |
| Opciones Finales | Clic en "Jugar nuevamente" | Juego (Reinicia parámetros) |
| Opciones Finales | Clic en "Salir" | Cierre del programa |

## Diagrama Visual

<img width="1290" height="260" alt="Diagrama sin título drawio (1)" src="https://github.com/user-attachments/assets/5051353e-137d-4c89-9711-0b7b429e9b09" />
