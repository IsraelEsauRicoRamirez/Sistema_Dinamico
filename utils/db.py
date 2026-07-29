import sqlite3
import os

# Ruta absoluta a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "sistema.db")

def init_db():
    """Crea las tablas necesarias si no existen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear la tabla de usuarios
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
    """Registra un nuevo usuario en la base de datos."""
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
        # Esto ocurre si el correo o la matrícula ya existen (por la restricción UNIQUE)
        return False
    finally:
        conn.close()


def validar_login(usuario_o_correo, password):
    """
    Verifica si las credenciales son correctas.
    Permite iniciar sesión usando el correo o la matrícula.
    Retorna un diccionario con los datos del usuario si es exitoso, o None si falla.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Buscamos donde el correo o la matrícula coincidan, y la contraseña sea correcta
    cursor.execute('''
        SELECT nombre, matricula, correo, rol 
        FROM usuarios 
        WHERE (correo = ? OR matricula = ?) AND password = ?
    ''', (usuario_o_correo, usuario_o_correo, password))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Si se encontró un registro, devolvemos los datos estructurados en un diccionario
        return {
            "nombre": row[0],
            "matricula": row[1],
            "correo": row[2],
            "rol": row[3]
        }
    else:
        # Si no coincide nada, el login falla
        return None

def eliminar_usuario(correo):
    """Elimina permanentemente a un usuario de la base de datos."""
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