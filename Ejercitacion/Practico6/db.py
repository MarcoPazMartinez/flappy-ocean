import sqlite3

DB = "ranking.db"

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe[cite: 26]."""
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS puntajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puntaje INTEGER NOT NULL
        )
    """)
    con.commit()
    con.close()

def guardar_puntaje(nombre, puntaje):
    """Guarda un nuevo puntaje en la base de datos[cite: 26]."""
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)", (nombre, puntaje))
    con.commit()
    con.close()

def obtener_top(cantidad=5):
    """Obtiene los mejores puntajes ordenados de mayor a menor[cite: 26]."""
    con = sqlite3.connect(DB)
    cur = con.execute(
        "SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT ?", 
        (cantidad,)
    )
    datos = cur.fetchall()
    con.close()
    return datos