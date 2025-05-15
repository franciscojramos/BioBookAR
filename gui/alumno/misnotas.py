import tkinter as tk
from base_datos import db
from gui.alumno import alumno 

def obtener_notas(usuario_id):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT tema, nota, intentos FROM resultados WHERE usuario_id = ?", (usuario_id,))
    datos = cursor.fetchall()
    conn.close()
    return datos

def ver_notas(usuario_id, root, user):
    for widget in root.winfo_children():
        widget.destroy()

    notas = obtener_notas(usuario_id)

    root.title("Mis Notas")
    root.configure(bg="white")

    tk.Label(root, text="📊 Historial de Notas", font=("Helvetica", 12, "bold"), bg="white").pack(pady=10)

    if not notas:
        tk.Label(root, text="No tienes notas aún.", bg="white").pack()
    else:
        for tema, nota, intentos in notas:
            texto = f"{tema} | Nota: {nota} | Intentos: {intentos}"
            tk.Label(root, text=texto, bg="white").pack(anchor="w", padx=20, pady=2)

    # Botón volver
    tk.Button(root, text="← Volver", command=lambda: alumno.abrir_ventana(user, root), bg="#cccccc").pack(pady=20)
