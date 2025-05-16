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

    # Tabla para registrar qué temas ha visto el alumno mediante AR
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS temas_vistos (
        usuario_id INTEGER,
        tema INTEGER,
        PRIMARY KEY (usuario_id, tema),
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
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

    # Crear usuario admin si no existe
    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute('''
            INSERT INTO usuarios (nombre, usuario, contraseña, rol, encoding, idioma)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Administrador', 'admin', 'admin', 'profesor', None, 'es'))

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


def marcar_tema_como_visto(usuario_id, tema):
    """Marca un tema como 'visto' por un usuario (tras escanear AR)."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO temas_vistos (usuario_id, tema)
            VALUES (?, ?)
        ''', (usuario_id, tema))
        conn.commit()
    finally:
        conn.close()

def obtener_temas_vistos(usuario_id):
    """Devuelve una lista de números de tema que el usuario ya ha visto con AR."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tema FROM temas_vistos WHERE usuario_id = ?
    ''', (usuario_id,))
    resultados = cursor.fetchall()
    conn.close()
    return [fila[0] for fila in resultados]

def guardar_resultado(usuario_id, tema, nota):
    """Guarda o actualiza la nota e incrementa el número de intentos."""
    conn = conectar()
    cursor = conn.cursor()
    
    # Ver si ya existe entrada para este usuario y tema
    cursor.execute('''
        SELECT nota, intentos FROM resultados
        WHERE usuario_id = ? AND tema = ?
    ''', (usuario_id, f"Tema {tema}"))
    
    existente = cursor.fetchone()

    if existente:
        mejor_nota = max(nota, existente[0])
        nuevos_intentos = existente[1] + 1
        cursor.execute('''
            UPDATE resultados
            SET nota = ?, intentos = ?
            WHERE usuario_id = ? AND tema = ?
        ''', (mejor_nota, nuevos_intentos, usuario_id, f"Tema {tema}"))
    else:
        cursor.execute('''
            INSERT INTO resultados (usuario_id, tema, nota, intentos)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, f"Tema {tema}", nota, 1))

    conn.commit()
    conn.close()
