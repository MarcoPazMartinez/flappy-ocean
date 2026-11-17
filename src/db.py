"""Ranking de puntajes en SQLite.

La tabla `puntajes` guarda como máximo los LIMITE_RANKING mejores puntajes:
cada vez que se guarda uno nuevo, lo que queda fuera del Top se borra.
"""
import os
import sqlite3
from contextlib import contextmanager

# La base vive en database/ranking.db, sin importar desde dónde se ejecute el juego
RUTA_DB = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "database",
    "ranking.db",
)

LIMITE_RANKING = 10          # cuántos puntajes se conservan
LARGO_MAXIMO_NOMBRE = 10
NOMBRE_POR_DEFECTO = "Anónimo"

# Orden del ranking: mayor puntaje primero; si empatan, gana el que llegó antes
ORDEN = "puntaje DESC, id ASC"


@contextmanager
def _conexion(ruta):
    """Abre la base, hace commit (o rollback si algo falla) y SIEMPRE la cierra.

    `with sqlite3.connect(...)` solo hace el commit: no cierra la conexión.
    """
    con = sqlite3.connect(ruta)
    try:
        with con:
            yield con
    finally:
        con.close()


def limpiar_nombre(nombre):
    """Deja el nombre en una sola línea, sin espacios de más y con el largo máximo."""
    nombre = " ".join(str(nombre).split())[:LARGO_MAXIMO_NOMBRE].strip()
    return nombre or NOMBRE_POR_DEFECTO


def init_db(ruta=RUTA_DB):
    """Crea la carpeta y la tabla si no existen."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with _conexion(ruta) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS puntajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                puntaje INTEGER NOT NULL,
                fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            )
            """
        )


def comprobar_base(ruta=RUTA_DB):
    """Prueba que la base responde. Devuelve (ok, detalle) y nunca lanza errores."""
    try:
        init_db(ruta)
        with _conexion(ruta) as con:
            cantidad = con.execute("SELECT COUNT(*) FROM puntajes").fetchone()[0]
        return True, f"{cantidad} puntaje(s) guardado(s) en {ruta}"
    except (sqlite3.Error, OSError) as error:
        return False, f"{error} ({ruta})"


def obtener_top(cantidad=LIMITE_RANKING, ruta=RUTA_DB):
    """Devuelve [(nombre, puntaje), ...] de mayor a menor."""
    with _conexion(ruta) as con:
        cur = con.execute(
            f"SELECT nombre, puntaje FROM puntajes ORDER BY {ORDEN} LIMIT ?",
            (cantidad,),
        )
        return cur.fetchall()


def entra_en_el_ranking(puntaje, ruta=RUTA_DB):
    """True si un puntaje nuevo quedaría dentro del Top.

    Un puntaje de 0 o menos nunca entra. Si empata con el último del Top, no
    entra: el que llegó primero se queda con el lugar.
    """
    if puntaje <= 0:
        return False

    with _conexion(ruta) as con:
        ultimo = con.execute(
            f"SELECT puntaje FROM puntajes ORDER BY {ORDEN} LIMIT 1 OFFSET ?",
            (LIMITE_RANKING - 1,),
        ).fetchone()

    return ultimo is None or puntaje > ultimo[0]


def guardar_puntaje(nombre, puntaje, ruta=RUTA_DB):
    """Guarda un puntaje y deja solo los mejores LIMITE_RANKING.

    Devuelve la posición (1 = primero) que ocupó en el ranking, o None si no
    entró. Todo ocurre en una sola transacción: o se hace todo o no se hace nada.
    """
    puntaje = int(puntaje)
    nombre = limpiar_nombre(nombre)

    with _conexion(ruta) as con:
        id_nuevo = con.execute(
            "INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)",
            (nombre, puntaje),
        ).lastrowid

        # Se borra lo que quedó fuera del Top
        con.execute(
            f"""
            DELETE FROM puntajes WHERE id NOT IN (
                SELECT id FROM puntajes ORDER BY {ORDEN} LIMIT ?
            )
            """,
            (LIMITE_RANKING,),
        )

        ids = [
            fila[0]
            for fila in con.execute(
                f"SELECT id FROM puntajes ORDER BY {ORDEN} LIMIT ?",
                (LIMITE_RANKING,),
            )
        ]

    return ids.index(id_nuevo) + 1 if id_nuevo in ids else None
