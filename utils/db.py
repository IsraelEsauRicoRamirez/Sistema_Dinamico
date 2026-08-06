import sqlite3
import os
import sys

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
else:
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_PATH = os.path.join(ruta_base, "sistema.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def registrar_usuario(nombre, matricula, correo, password, rol):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, matricula, correo, password, rol) VALUES (?, ?, ?, ?, ?)",
            (nombre, matricula, correo, password, rol)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validar_login(usuario_o_correo, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT nombre, matricula, correo, rol 
        FROM usuarios 
        WHERE (correo = ? OR matricula = ?) AND password = ?
    ''', (usuario_o_correo, usuario_o_correo, password))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "nombre": row[0],
            "matricula": row[1],
            "correo": row[2],
            "rol": row[3]
        }
    else:
        return None

def eliminar_usuario(correo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE correo = ?", (correo,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar: {e}")
        return False
    finally:
        conn.close()