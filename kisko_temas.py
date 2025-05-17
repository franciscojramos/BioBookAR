import sqlite3
from base_datos import db

def marcar_todos_los_temas_vistos(usuario='kisko'):
    conn = db.conectar()
    cursor = conn.cursor()

    # Obtener ID del usuario
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    if not resultado:
        print(f"❌ Usuario '{usuario}' no encontrado.")
        return
    usuario_id = resultado[0]

    # Insertar los temas 1 a 8 como vistos
    for tema in range(1, 9):
        db.marcar_tema_como_visto(usuario_id, tema)

    print(f"✅ Usuario '{usuario}' tiene ahora todos los temas marcados como vistos.")

if __name__ == "__main__":
    marcar_todos_los_temas_vistos()
