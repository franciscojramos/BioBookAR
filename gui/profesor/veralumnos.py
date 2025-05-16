import tkinter as tk
from tkinter import ttk, messagebox
from gui.profesor import profesor


from base_datos.db import conectar

def mostrar_lista_alumnos(root, user):
    # Limpiar ventana actual
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="👥 Lista de Alumnos", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Contenedor con ancho mayor solo para la tabla
    contenedor_tabla = tk.Frame(root, width=750)
    contenedor_tabla.pack(padx=10, pady=10)

    columnas = ("nombre", "usuario", "media", "intentos", "mejor")
    tabla = ttk.Treeview(contenedor_tabla, columns=columnas, show="headings", height=10)
    tabla.pack(fill="both", expand=True)

    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=140, anchor="center")  # Ancho fijo por columna

    # Scroll horizontal opcional si la tabla se desborda
    scroll_x = ttk.Scrollbar(contenedor_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(xscrollcommand=scroll_x.set)
    scroll_x.pack(fill="x")

    # Conexión BD
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, usuario FROM usuarios WHERE rol = 'alumno'")
    alumnos = cursor.fetchall()

    for alumno in alumnos:
        alumno_id, nombre, usuario = alumno
        cursor.execute('''
            SELECT AVG(nota), SUM(intentos), MAX(nota)
            FROM resultados WHERE usuario_id = ?
        ''', (alumno_id,))
        stats = cursor.fetchone() or (0, 0, 0)
        media, intentos, mejor = [round(s, 2) if s else 0 for s in stats]

        tabla.insert("", "end", iid=alumno_id, values=(nombre, usuario, media, intentos, mejor))

    conn.close()

    # Función para eliminar alumno seleccionado
    def eliminar_alumno():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un alumno para eliminar.")
            return

        alumno_id = seleccionado[0]
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este alumno?\nSe borrarán también sus resultados.")
        if confirmar:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM resultados WHERE usuario_id = ?", (alumno_id,))
            cursor.execute("DELETE FROM temas_vistos WHERE usuario_id = ?", (alumno_id,))
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (alumno_id,))
            conn.commit()
            conn.close()
            tabla.delete(alumno_id)
            messagebox.showinfo("Eliminado", "Alumno eliminado correctamente.")

    # Botón para eliminar
    tk.Button(root, text="🗑️ Eliminar Alumno Seleccionado", bg="#FFCCCC", command=eliminar_alumno).pack(pady=10)
    tk.Button(root, text="← Volver", bg="#CCCCCC", command=lambda: profesor.abrir_ventana(user, root)).pack(pady=20)
