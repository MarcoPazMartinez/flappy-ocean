# Diagrama de Flujo de Pantallas - Flappy Diver

## Descripción
Este documento describe el flujo de pantallas y navegación del juego Flappy Diver (antes Flappy Ocean).

> El diagrama visual de abajo corresponde al diseño original y todavía no está actualizado: usá las tablas de este documento, que describen cómo funciona el juego hoy.

## Pantallas del Juego

| Pantalla | Descripción | Cómo se llega |
| :--- | :--- | :--- |
| **Portada** | Muestra el título "Flappy Diver", la imagen de fondo marino y tres botones: "Jugar", "Ranking" y "Salir". | Al iniciar la aplicación o al elegir "Volver al inicio". |
| **Juego** | Desarrollo de la partida. Muestra al pez, algas, fauna marina, burbujas y el HUD (Puntaje, Vidas, Tiempo y, cuando se agregue, Energía). Al final aparece la meta: un tubo de cristal al que el pez entra. | Al elegir "Jugar". |
| **Cartel final** | "¡GANASTE!" si el pez llegó a la meta, o "GAME OVER" si perdió las vidas (o la energía). Muestra el puntaje. | Al terminar la partida. |
| **Nombre** | Pide el nombre del jugador para anotar el puntaje en el ranking. Solo aparece si el puntaje entra en el Top 10. | Después del cartel final, si el puntaje entra en el ranking. |
| **Resultados** | Muestra el puntaje final, el Top 10 con el puesto del jugador resaltado y los botones "Volver al inicio" y "Salir". Si el puntaje entró, ya se guardó en SQLite. | Después del cartel final o de ingresar el nombre. |
| **Ranking** | Consulta SQLite y muestra la lista ordenada con los 10 mejores puntajes (Top 10). | Desde el botón "Ranking" de la portada. |

## Transiciones

| Desde | Evento / Condición | Hacia |
| :--- | :--- | :--- |
| Portada | Clic en "Jugar" (o Enter) | Juego |
| Portada | Clic en "Ranking" | Ranking |
| Portada | Clic en "Salir" (o Esc) | Cierre del programa |
| Ranking | Clic en "Volver" (o Esc) | Portada |
| Juego | Vidas = 0 o Energía = 0 | Cartel final (Game Over) |
| Juego | Tiempo = 120 s (el pez llega a la meta) | Cartel final (¡Ganaste!) |
| Cartel final | Clic en "Continuar" (o Enter) y el puntaje entra en el Top 10 | Nombre |
| Cartel final | Clic en "Continuar" (o Enter) y el puntaje no entra en el Top 10 | Resultados |
| Nombre | Enter / "Guardar" (se guarda el puntaje) u "Omitir" | Resultados |
| Resultados | Clic en "Volver al inicio" (o Esc) | Portada (otra partida empieza de cero) |
| Resultados | Clic en "Salir" | Cierre del programa |

## Diagrama Visual

<img width="1290" height="260" alt="Diagrama sin título drawio (1)" src="https://github.com/user-attachments/assets/5051353e-137d-4c89-9711-0b7b429e9b09" />
