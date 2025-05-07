import tkinter as tk
from tkinter import messagebox
from base_datos import db
from reconocimiento import facial

# Llamamos a crear tablas si aún no existen
db.crear_tablas()

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioBookAR - Login")
        self.root.geometry("800x600")

        tk.Label(root, text="Usuario").pack()
        self.usuario_entry = tk.Entry(root)
        self.usuario_entry.pack()

        tk.Label(root, text="Contraseña").pack()
        self.contraseña_entry = tk.Entry(root, show="*")
        self.contraseña_entry.pack()

        tk.Button(root, text="Iniciar sesión", command=self.login_manual).pack(pady=5)
        tk.Button(root, text="Iniciar con rostro", command=self.login_facial).pack(pady=5)
        tk.Button(root, text="Registrar nuevo alumno", command=self.registrar_usuario).pack(pady=5)

    def login_manual(self):
        usuario = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()
        user = db.obtener_usuario_por_credenciales(usuario, contraseña)
        if user:
            self.redirigir_por_rol(user)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def login_facial(self):
        encoding_nuevo = facial.capturar_y_codificar_rostro()
        if encoding_nuevo is None:
            messagebox.showwarning("Rostro no detectado", "No se detectó exactamente un rostro")
            return

        encodings_guardados = db.obtener_todos_los_encodings()
        usuario_id = facial.comparar_encoding_con_base(encoding_nuevo, encodings_guardados)

        if usuario_id is not None:
            user = self.obtener_usuario_por_id(usuario_id)
            self.redirigir_por_rol(user)
        else:
            messagebox.showwarning("Error", "Reconocimiento facial fallido. Intente con usuario y contraseña.")

    def registrar_usuario(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registro de Alumno")

        tk.Label(ventana, text="Nombre").pack()
        nombre = tk.Entry(ventana)
        nombre.pack()

        tk.Label(ventana, text="Usuario").pack()
        usuario = tk.Entry(ventana)
        usuario.pack()

        tk.Label(ventana, text="Contraseña").pack()
        contraseña = tk.Entry(ventana, show="*")
        contraseña.pack()

        def registrar():
            encoding = facial.capturar_y_codificar_rostro()
            if encoding is None:
                messagebox.showwarning("Error", "No se detectó un rostro válido")
                return
            exito = db.insertar_usuario(nombre.get(), usuario.get(), contraseña.get(), "alumno", encoding)
            if exito:
                messagebox.showinfo("Éxito", "Alumno registrado correctamente")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Ese nombre de usuario ya existe")

        tk.Button(ventana, text="Registrar", command=registrar).pack(pady=5)

    def obtener_usuario_por_id(self, usuario_id):
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def redirigir_por_rol(self, user):
        rol = user[4]
        nombre = user[1]
        messagebox.showinfo("Bienvenido", f"Hola, {nombre} ({rol})")
        # Aquí podrías hacer: import alumno o profesor y abrir su ventana
        # Ejemplo:
        # if rol == "alumno":
        #     import gui.alumno as alumno
        #     alumno.abrir_ventana(user)
        # elif rol == "profesor":
        #     import gui.profesor as profesor
        #     profesor.abrir_ventana(user)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
