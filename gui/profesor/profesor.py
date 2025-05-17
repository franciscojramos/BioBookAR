import tkinter as tk
from tkinter import messagebox
from base_datos import db

from gui.profesor.veralumnos import mostrar_lista_alumnos
from gui.profesor.editarpreguntas import mostrar_editor_preguntas
from gui.profesor.estadisticas import mostrar_estadisticas
from gui.profesor.cambiarcontrasena import cambiar_contraseña

# Cerrar sesión
def cerrar_sesion(root): 
    from gui.login import LoginApp 
    
    for widget in root.winfo_children():
        widget.destroy()
    LoginApp(root)

def abrir_ventana(user, root):
    for widget in root.winfo_children():
        widget.destroy()

    # Obtener datos del profesor
    profesor_id = user[0]
    nombre = user[1]

    # Crear ventana
    root.title("BioBookAR - Profesor")
    root.geometry("500x420")
    root.configure(bg="white")

    # Forzar cambio de contraseña si aún es admin/admin
    if user[2] == "admin" and user[3] == "admin":
        user = cambiar_contraseña(user, root, forzado=True)


    # Cabecera
    tk.Label(root, text=f"👨‍🏫 Bienvenido, {nombre}", font=("Helvetica", 14, "bold"), bg="white").pack(pady=20)

    # Botones de acción
    tk.Button(root, text="👥 Ver Alumnos", width=25, command=lambda: mostrar_lista_alumnos(root, user)).pack(pady=10)
    tk.Button(root, text="📝 Editar Preguntas", width=25, command=lambda: mostrar_editor_preguntas(root, user)).pack(pady=10)
    tk.Button(root, text="📊 Ver Estadísticas", width=25, command=lambda: mostrar_estadisticas(root, user)).pack(pady=10)
    tk.Button(root, text="🔒 Cerrar sesión", width=25, command=lambda: cerrar_sesion(root)).pack(pady=30)
