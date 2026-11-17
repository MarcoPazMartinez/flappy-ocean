"""Pantallas del final de la partida.

El orden es siempre el mismo:

    cartel (¡GANASTE! o GAME OVER)
        -> nombre (solo si el puntaje entra en el ranking)
            -> resultados (puntaje, ranking y botones)

Cada pantalla tiene su propio bucle y devuelve un texto cuando termina.
`finalizar_partida()` las encadena.
"""
import random
import sqlite3

import pygame

import db
from interfaz import (
    COLOR_BORDE_TITULO,
    COLOR_TITULO,
    Boton,
    crear_panel,
    procesar_evento,
    texto_con_borde,
)
from ranking import altura_tabla, dibujar_tabla, leer_ranking
from recursos import cargar_fondo

COLOR_FONDO_RESPALDO = (20, 60, 140)

# Al terminar la partida el jugador suele estar apretando Espacio o haciendo clic.
# Durante este tiempo el cartel ignora las teclas para que no se salte sin querer.
SEGUNDOS_SIN_RESPUESTA = 0.8

COLORES_CONFETI = [(255, 215, 60), (255, 120, 60), (90, 200, 255), (255, 110, 200), (120, 230, 120)]

# Cómo terminó lo de guardar el puntaje (para el mensaje de los resultados)
GUARDADO = "guardado"
OMITIDO = "omitido"
NO_ENTRA = "no_entra"
SIN_PUNTOS = "sin_puntos"
ERROR = "error"


def mostrar_cartel(pantalla, reloj, resultado):
    """Cartel grande sobre la última imagen de la partida.

    Devuelve "continuar" o "salir" (si se cerró la ventana).
    """
    ancho, alto = pantalla.get_size()
    centro_x = ancho // 2
    ganaste = resultado.estado == "victoria"

    fuente_titulo = pygame.font.Font(None, 150)
    fuente_subtitulo = pygame.font.Font(None, 50)
    fuente_puntaje = pygame.font.Font(None, 84)
    fuente_detalle = pygame.font.Font(None, 34)
    fuente_boton = pygame.font.Font(None, 48)

    if ganaste:
        titulo = texto_con_borde(fuente_titulo, "¡GANASTE!", COLOR_TITULO, COLOR_BORDE_TITULO, 6)
        subtitulo = fuente_subtitulo.render("¡Llegaste a la meta!", True, (255, 255, 255))
    else:
        titulo = texto_con_borde(fuente_titulo, "GAME OVER", (255, 95, 95), (80, 0, 0), 6)
        subtitulo = fuente_subtitulo.render("Te quedaste sin vidas", True, (255, 255, 255))

    puntaje = texto_con_borde(
        fuente_puntaje, f"Puntaje: {resultado.puntaje}", (255, 255, 255), (0, 30, 80), 3
    )

    detalle = None
    if resultado.bonus:
        detalle = fuente_detalle.render(
            f"Incluye +{resultado.bonus} de bonus por llegar a la meta", True, (255, 230, 150)
        )

    oscuro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    oscuro.fill((0, 10, 40, 170))

    panel = crear_panel((800, 470))
    rect_panel = panel.get_rect(center=(centro_x, alto // 2))

    boton = Boton("Continuar", "continuar", (centro_x, rect_panel.bottom - 60), (300, 60))
    botones = [boton]
    seleccionado = 0

    # Confeti: solo cuando se gana
    confeti = []
    if ganaste:
        for _ in range(70):
            confeti.append([
                random.uniform(0, ancho), random.uniform(-alto, 0),    # x, y
                random.uniform(-40, 40), random.uniform(120, 260),     # velocidad x, y
                random.choice(COLORES_CONFETI),
                random.randint(8, 14), random.randint(8, 14),          # ancho, alto
            ])

    pygame.event.clear()      # lo que se apretó durante la partida no cuenta
    transcurrido = 0.0

    while True:
        dt = reloj.tick(60) / 1000.0
        transcurrido += dt

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return "salir"

            if transcurrido < SEGUNDOS_SIN_RESPUESTA:
                continue

            seleccionado, accion = procesar_evento(evento, botones, seleccionado)

            if accion is not None:
                return accion

        for pieza in confeti:
            pieza[0] += pieza[2] * dt
            pieza[1] += pieza[3] * dt
            if pieza[1] > alto:
                pieza[0], pieza[1] = random.uniform(0, ancho), -20

        pantalla.blit(resultado.captura, (0, 0))
        pantalla.blit(oscuro, (0, 0))
        pantalla.blit(panel, rect_panel)

        pantalla.blit(titulo, titulo.get_rect(center=(centro_x, rect_panel.top + 95)))
        pantalla.blit(subtitulo, subtitulo.get_rect(center=(centro_x, rect_panel.top + 190)))
        pantalla.blit(puntaje, puntaje.get_rect(center=(centro_x, rect_panel.top + 265)))
        if detalle:
            pantalla.blit(detalle, detalle.get_rect(center=(centro_x, rect_panel.top + 322)))

        boton.dibujar(pantalla, fuente_boton, True)

        for x, y, _, _, color, ancho_pieza, alto_pieza in confeti:
            pygame.draw.rect(pantalla, color, (x, y, ancho_pieza, alto_pieza))

        pygame.display.flip()


def pedir_nombre(pantalla, reloj, puntaje):
    """Pide el nombre para anotar el puntaje en el ranking.

    Devuelve (acción, nombre). La acción es "guardar", "omitir" o "salir".
    """
    ancho, alto = pantalla.get_size()
    centro_x = ancho // 2

    fondo = cargar_fondo("portada.png", (ancho, alto), COLOR_FONDO_RESPALDO)

    fuente_titulo = pygame.font.Font(None, 84)
    fuente_puntaje = pygame.font.Font(None, 64)
    fuente_texto = pygame.font.Font(None, 40)
    fuente_nombre = pygame.font.Font(None, 56)
    fuente_chica = pygame.font.Font(None, 30)
    fuente_boton = pygame.font.Font(None, 44)

    titulo = texto_con_borde(fuente_titulo, "¡Entraste al ranking!", COLOR_TITULO, COLOR_BORDE_TITULO, 5)
    texto_puntaje = fuente_puntaje.render(f"Tu puntaje: {puntaje}", True, (255, 255, 255))
    pedido = fuente_texto.render("Escribí tu nombre:", True, (255, 255, 255))

    panel = crear_panel((780, 500))
    rect_panel = panel.get_rect(center=(centro_x, alto // 2))

    caja = pygame.Rect(0, 0, 460, 66)
    caja.center = (centro_x, rect_panel.top + 270)

    boton_guardar = Boton("Guardar", "guardar", (centro_x - 140, rect_panel.bottom - 60), (240, 56))
    boton_omitir = Boton("Omitir", "omitir", (centro_x + 140, rect_panel.bottom - 60), (240, 56))

    nombre = ""
    segundos_aviso = 0.0           # cuánto tiempo más se muestra el aviso de "nombre vacío"

    pygame.event.clear()           # lo que se apretó durante el cartel no cuenta
    pygame.key.start_text_input()

    try:
        while True:
            dt = reloj.tick(60) / 1000.0
            segundos_aviso = max(0.0, segundos_aviso - dt)

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return "salir", ""

                elif evento.type == pygame.TEXTINPUT:
                    # TEXTINPUT trae el carácter ya escrito (mayúsculas, acentos, ñ...)
                    for caracter in evento.text:
                        es_valido = caracter.isalnum() or caracter in " -_."
                        es_espacio_inicial = caracter == " " and not nombre
                        if es_valido and not es_espacio_inicial and len(nombre) < db.LARGO_MAXIMO_NOMBRE:
                            nombre += caracter

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "omitir", ""
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if nombre.strip():
                            return "guardar", nombre.strip()
                        segundos_aviso = 1.5

                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if boton_omitir.contiene(evento.pos):
                        return "omitir", ""
                    if boton_guardar.contiene(evento.pos):
                        if nombre.strip():
                            return "guardar", nombre.strip()
                        segundos_aviso = 1.5

            pantalla.blit(fondo, (0, 0))
            pantalla.blit(panel, rect_panel)

            pantalla.blit(titulo, titulo.get_rect(center=(centro_x, rect_panel.top + 70)))
            pantalla.blit(texto_puntaje, texto_puntaje.get_rect(center=(centro_x, rect_panel.top + 150)))
            pantalla.blit(pedido, pedido.get_rect(center=(centro_x, rect_panel.top + 215)))

            # Caja de texto con cursor que parpadea
            pygame.draw.rect(pantalla, (10, 20, 50), caja, border_radius=12)
            pygame.draw.rect(pantalla, (255, 215, 60), caja, 3, border_radius=12)

            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            texto_nombre = fuente_nombre.render(nombre + cursor, True, (255, 255, 255))
            pantalla.blit(texto_nombre, texto_nombre.get_rect(midleft=(caja.left + 18, caja.centery)))

            contador = fuente_chica.render(f"{len(nombre)}/{db.LARGO_MAXIMO_NOMBRE}", True, (190, 210, 240))
            pantalla.blit(contador, contador.get_rect(topright=(caja.right, caja.bottom + 8)))

            if segundos_aviso > 0:
                aviso = fuente_chica.render("Escribí un nombre para guardar", True, (255, 130, 130))
                pantalla.blit(aviso, aviso.get_rect(topleft=(caja.left, caja.bottom + 8)))

            boton_guardar.dibujar(pantalla, fuente_boton, True)
            boton_omitir.dibujar(pantalla, fuente_boton, False)

            pygame.display.flip()

    finally:
        pygame.key.stop_text_input()


def mostrar_resultados(pantalla, reloj, resultado, estado_guardado, posicion):
    """Puntaje final, ranking (con tu puesto resaltado) y botones.

    Devuelve "inicio" o "salir".
    """
    ancho, alto = pantalla.get_size()
    centro_x = ancho // 2

    fondo = cargar_fondo("portada.png", (ancho, alto), COLOR_FONDO_RESPALDO)

    fuente_puntaje = pygame.font.Font(None, 96)
    fuente_mensaje = pygame.font.Font(None, 40)
    fuente_fila = pygame.font.Font(None, 42)
    fuente_boton = pygame.font.Font(None, 44)

    puntaje = texto_con_borde(
        fuente_puntaje, f"Tu puntaje: {resultado.puntaje}", COLOR_TITULO, COLOR_BORDE_TITULO, 5
    )

    if estado_guardado == GUARDADO:
        mensaje, color_mensaje = f"¡Quedaste en el puesto {posicion} del ranking!", (255, 215, 60)
    elif estado_guardado == OMITIDO:
        mensaje, color_mensaje = "No guardaste tu puntaje en el ranking.", (255, 255, 255)
    elif estado_guardado == SIN_PUNTOS:
        mensaje, color_mensaje = "Necesitás sumar puntos para entrar al ranking.", (255, 255, 255)
    elif estado_guardado == ERROR:
        mensaje, color_mensaje = "No se pudo guardar el puntaje (falló la base de datos).", (255, 130, 130)
    else:
        mensaje = f"No alcanzaste el Top {db.LIMITE_RANKING} esta vez. ¡Seguí intentando!"
        color_mensaje = (255, 255, 255)

    texto_mensaje = texto_con_borde(fuente_mensaje, mensaje, color_mensaje, (0, 25, 70), 2)

    # La base se consulta UNA vez al entrar
    filas, hubo_error = leer_ranking()

    panel = crear_panel((640, altura_tabla()))
    rect_panel = panel.get_rect(center=(centro_x, int(alto * 0.52)))

    botones = [
        Boton("Volver al inicio", "inicio", (centro_x - 170, int(alto * 0.92)), (300, 58)),
        Boton("Salir", "salir", (centro_x + 170, int(alto * 0.92)), (300, 58)),
    ]
    seleccionado = 0
    destacada = posicion - 1 if estado_guardado == GUARDADO and posicion else None

    pygame.event.clear()

    while True:
        reloj.tick(60)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "inicio"

            seleccionado, accion = procesar_evento(evento, botones, seleccionado)

            if accion is not None:
                return accion

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(puntaje, puntaje.get_rect(center=(centro_x, int(alto * 0.075))))
        pantalla.blit(texto_mensaje, texto_mensaje.get_rect(center=(centro_x, int(alto * 0.165))))
        pantalla.blit(panel, rect_panel)

        if filas:
            dibujar_tabla(pantalla, filas, rect_panel, fuente_fila, destacada)
        else:
            sin_datos = "No se pudo leer el ranking." if hubo_error else "Todavía no hay puntajes."
            texto = fuente_mensaje.render(sin_datos, True, (255, 255, 255))
            pantalla.blit(texto, texto.get_rect(center=rect_panel.center))

        for numero, boton in enumerate(botones):
            boton.dibujar(pantalla, fuente_boton, numero == seleccionado)

        pygame.display.flip()


def finalizar_partida(pantalla, reloj, resultado):
    """Cartel -> nombre (si entra en el ranking) -> resultados.

    Devuelve "inicio" (volver a la portada) o "salir".
    """
    if mostrar_cartel(pantalla, reloj, resultado) == "salir":
        return "salir"

    estado_guardado = SIN_PUNTOS if resultado.puntaje <= 0 else NO_ENTRA
    posicion = None

    try:
        if db.entra_en_el_ranking(resultado.puntaje):

            accion, nombre = pedir_nombre(pantalla, reloj, resultado.puntaje)

            if accion == "salir":
                return "salir"

            if accion == "guardar":
                posicion = db.guardar_puntaje(nombre, resultado.puntaje)
                estado_guardado = GUARDADO if posicion else NO_ENTRA
            else:
                estado_guardado = OMITIDO

    except sqlite3.Error as error:
        # Si la base falla, el juego sigue: solo se avisa que no se guardó
        print(f"Aviso: no se pudo guardar el puntaje ({error}).")
        estado_guardado = ERROR

    return mostrar_resultados(pantalla, reloj, resultado, estado_guardado, posicion)
