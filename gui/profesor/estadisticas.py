import tkinter as tk
from tkinter import ttk, messagebox
from base_datos.db import conectar
from gui.profesor import profesor

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_estadisticas(root, user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="📈 Rendimiento Global por Tema", font=("Helvetica", 14, "bold")).pack(pady=10)

    columnas = ("tema", "media", "max", "min", "alumnos")
    tabla = ttk.Treeview(root, columns=columnas, show="headings", height=10)
    tabla.pack(padx=20, pady=10, fill="both", expand=True)

    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center")

    conn = conectar()
    cursor = conn.cursor()

    # Recolectar todos los temas con estadísticas
    datos_temas = []
    for i in range(1, 9):
        tema = f"Tema {i}"
        cursor.execute('''
            SELECT AVG(nota), MAX(nota), MIN(nota)
            FROM resultados WHERE tema = ?
        ''', (tema,))
        media, max_nota, min_nota = cursor.fetchone() or (0, 0, 0)
        media = round(media, 2) if media else 0
        max_nota = round(max_nota, 2) if max_nota else 0
        min_nota = round(min_nota, 2) if min_nota else 0

        cursor.execute('''
            SELECT COUNT(DISTINCT usuario_id)
            FROM resultados WHERE tema = ?
        ''', (tema,))
        total_alumnos = cursor.fetchone()[0] or 0

        datos_temas.append((tema, media, max_nota, min_nota, total_alumnos))

    # Ordenar por nota media descendente
    datos_temas.sort(key=lambda x: x[1], reverse=True)

    # Mostrar en tabla
    for fila in datos_temas:
        tabla.insert("", "end", values=fila)

    conn.close()

    def mostrar_distribucion(event):
        item = tabla.selection()
        if not item:
            return
        tema = tabla.item(item)["values"][0]

        # Obtener todas las notas de ese tema
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nota FROM resultados WHERE tema = ?", (tema,))
        notas = [fila[0] for fila in cursor.fetchall()]
        conn.close()

        if not notas:
            messagebox.showinfo("Sin datos", f"No hay notas registradas para {tema}")
            return

        # Crear ventana emergente
        ventana = tk.Toplevel(root)
        ventana.title(f"Distribución de Notas - {tema}")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(notas, bins=10, color="#88C0D0", edgecolor="black", alpha=0.85)
        ax.set_title(f"Distribución de notas - {tema}", fontsize=12)
        ax.set_xlabel("Nota")
        ax.set_ylabel("Número de alumnos")
        ax.grid(True, linestyle="--", alpha=0.5)

        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)

    # Evento doble clic en fila
    tabla.bind("<Double-1>", mostrar_distribucion)

    # Botón volver
    tk.Button(root, text="← Volver", bg="#CCCCCC", command=lambda: profesor.abrir_ventana(user, root)).pack(pady=20)
