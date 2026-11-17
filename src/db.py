"""Ranking de puntajes en SQLite."""
import os
import sqlite3

# La base vive en database/ranking.db, sin importar desde dónde se ejecute el juego
RUTA_DB = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "database",
    "ranking.db",
)


def init_db(ruta=RUTA_DB):
    """Crea la carpeta y la tabla si no existen."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with sqlite3.connect(ruta) as con:
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


def guardar_puntaje(nombre, puntaje, ruta=RUTA_DB):
    with sqlite3.connect(ruta) as con:
        con.execute("INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)", (nombre, puntaje))


def obtener_top(cantidad=5, ruta=RUTA_DB):
    with sqlite3.connect(ruta) as con:
        cur = con.execute(
            "SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC, id ASC LIMIT ?",
            (cantidad,),
        )
        return cur.fetchall()
