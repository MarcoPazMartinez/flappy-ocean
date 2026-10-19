import sqlite3

def ejecutar_ejercicio1():
    #Crear la base de datos y la tabla puntajes
    con = sqlite3.connect("ranking.db")
    con.execute("""
        CREATE TABLE IF NOT EXISTS puntajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puntaje INTEGER NOT NULL
        )
    """)
    con.commit()

    # 2Guardar 3 puntajes de ejemplo
    ejemplos = [("Ana", 1500), ("Carlos", 2300), ("Lucía", 1900)]
    con.executemany("INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)", ejemplos)
    con.commit()

    # 3Mostrar en consola el top 3 ordenado de mayor a menor
    print("--- TOP 3 PUNTAJES ---")
    cur = con.execute("SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT 3")
    for nombre, puntaje in cur.fetchall():
        print(f"{nombre}: {puntaje}")

    con.close()

if __name__ == "__main__":
    ejecutar_ejercicio1()