import tkinter as tk
from tkinter import simpledialog, messagebox
from base_datos import db

def cambiar_contraseña(user, root, forzado=False):
    nuevo_usuario = None  # variable a devolver

    def guardar():
        nonlocal nuevo_usuario

        nueva = entry_nueva.get()
        confirmar = entry_confirmar.get()

        if not nueva or not confirmar:
            messagebox.showwarning("Campos vacíos", "Debes rellenar ambos campos.")
            return

        if nueva != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        if nueva == "admin":
            messagebox.showwarning("Contraseña insegura", "Elige una contraseña distinta a 'admin'.")
            return

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contraseña = ? WHERE id = ?", (nueva, user[0]))
        conn.commit()
        conn.close()

        # 🔄 Recargar el usuario actualizado
        nuevo_usuario = db.obtener_usuario_por_credenciales(user[2], nueva)

        messagebox.showinfo("Contraseña cambiada", "✅ Contraseña actualizada correctamente.")
        ventana.destroy()

    ventana = tk.Toplevel(root)
    ventana.title("Cambiar Contraseña")
    ventana.geometry("400x300")
    ventana.transient(root)
    ventana.grab_set()

    if forzado:
        ventana.protocol("WM_DELETE_WINDOW", lambda: None)  # Bloquea cierre sin cambio
        label_info = "🔐 Es obligatorio cambiar la contraseña de administrador"
    else:
        label_info = "Introduce la nueva contraseña"

    tk.Label(ventana, text=label_info, wraplength=280, font=("Arial", 10, "bold")).pack(pady=10)

    tk.Label(ventana, text="Nueva contraseña:").pack()
    entry_nueva = tk.Entry(ventana, show="*")
    entry_nueva.pack(pady=5)

    tk.Label(ventana, text="Confirmar contraseña:").pack()
    entry_confirmar = tk.Entry(ventana, show="*")
    entry_confirmar.pack(pady=5)

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=15)

    if forzado:
        ventana.wait_window()

    return nuevo_usuario if nuevo_usuario else user  # si no cambió nada, se devuelve el original
