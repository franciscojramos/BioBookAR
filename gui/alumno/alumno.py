import tkinter as tk
from tkinter import messagebox
from base_datos import db
from gui.alumno.misnotas import ver_notas
from gui.alumno.realizartest import realizar_test
from gui.alumno.AR import ARventana 



    #Al cerrar sesion volver atras
def cerrar_sesion(root): 
    from gui.login import LoginApp 
    
    for widget in root.winfo_children():
        widget.destroy()
    LoginApp(root)

def abrir_ventana(user,root):
    for widget in root.winfo_children():
        widget.destroy()

    # Obtener datos del usuario
    alumno_id = user[0]
    nombre = user[1]
    idioma = db.obtener_idioma_usuario(alumno_id)

    # Crear ventana
    root.title("BioBookAR - Alumno")
    root.geometry("500x400")
    root.configure(bg="white")

    #Cambiar idioma de los tests
    def cambiar_idioma(user):
        nuevo_idioma = "en" if user[6] == "es" else "es"
        db.actualizar_idioma(user[0], nuevo_idioma)
        mensaje = "🌍 Idioma cambiado a Español" if nuevo_idioma == "es" else "🌍 Language changed to English"
        tk.messagebox.showinfo("Idioma", mensaje + "\nReinicia sesión para aplicar el cambio.")





    # Cabecera con nombre
    tk.Label(root, text=f" Bienvenido, {nombre}", font=("Helvetica", 14, "bold"), bg="white").pack(pady=20)

    # Botones de acción
    tk.Button(root, text="📊 Mis Notas", width=20, command=lambda: ver_notas(alumno_id, root, user)).pack(pady=10)
    tk.Button(root, text="📃 Realizar Test", width=20,command=lambda: realizar_test(alumno_id, root, user)).pack(pady=10)
    tk.Button(root, text="🩻 Iniciar Realidad Aumentada", width=25,command=lambda: ARventana(root, alumno_id, user)).pack(pady=10)
    tk.Button(root, text="🌐 Cambiar idioma", bg="#DDDDDD", command=lambda: cambiar_idioma(user)).pack(pady=10)
    tk.Button(root, text="🔒 Cerrar sesión", width=20, command=lambda: cerrar_sesion(root)).pack(pady=30)



