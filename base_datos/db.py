import sqlite3
import pickle
import os

# Ruta de la base de datos (misma carpeta que este archivo)
DB_PATH = os.path.join(os.path.dirname(__file__), "biobookar.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabla de usuarios con codificación facial y preferencia de idioma
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        contraseña TEXT NOT NULL,
        rol TEXT CHECK(rol IN ('alumno', 'profesor')) NOT NULL,
        encoding BLOB,
        idioma TEXT DEFAULT 'es'
    );
    ''')
    
    # Tabla de resultados por tema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        tema TEXT NOT NULL,
        nota REAL,
        intentos INTEGER,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    );
    ''')
    
    conn.commit()
    conn.close()

def insertar_usuario(nombre, usuario, contraseña, rol, encoding=None, idioma='es'):
    """Inserta un nuevo usuario en la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        blob = pickle.dumps(encoding) if encoding is not None else None
        cursor.execute('''
            INSERT INTO usuarios (nombre, usuario, contraseña, rol, encoding, idioma)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, usuario, contraseña, rol, blob, idioma))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def obtener_usuario_por_credenciales(usuario, contraseña):
    """Devuelve el usuario que coincide con usuario y contraseña."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?
    ''', (usuario, contraseña))
    user = cursor.fetchone()
    conn.close()
    return user

def obtener_todos_los_encodings():
    """Devuelve una lista de tuplas (id, encoding) para todos los usuarios registrados con rostro."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, encoding FROM usuarios WHERE encoding IS NOT NULL')
    resultados = cursor.fetchall()
    conn.close()
    return [(id_, pickle.loads(enc)) for id_, enc in resultados]

def actualizar_idioma(usuario_id, nuevo_idioma):
    """Actualiza el idioma preferido de un usuario."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE usuarios SET idioma = ? WHERE id = ?
    ''', (nuevo_idioma, usuario_id))
    conn.commit()
    conn.close()

def obtener_idioma_usuario(usuario_id):
    """Obtiene el idioma preferido del usuario."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT idioma FROM usuarios WHERE id = ?', (usuario_id,))
    idioma = cursor.fetchone()
    conn.close()
    return idioma[0] if idioma else 'es'
