import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from base_datos import db
from reconocimiento import facial

# Asegúrate de que las tablas existen

db.crear_tablas()

class LoginApp:
    def __init__(self, root):
        self.root = root
        icono_img = Image.open("recursos/logof2.ico")
        self.icono_tk = ImageTk.PhotoImage(icono_img)
        self.root.iconphoto(False, self.icono_tk)

        self.root.title("BioBookAR")
        self.root.geometry("400x300")
        self.root.configure(bg="white")  # Fondo blanco

        # Cargar logo y colocarlo en esquina superior izquierda
        logo_path = "recursos/logof2.png"  
        image = Image.open(logo_path).resize((60, 60)) # Cambia el tamaño al necesario
        self.logo_tk = ImageTk.PhotoImage(image)
        self.logo_label = tk.Label(self.root, image=self.logo_tk, bg="white", borderwidth=0)
        self.logo_label.place(x=10, y=10)

        # Inicializa la pantalla principal
        self.frame_actual = None
        self.mostrar_pantalla_inicio()

    def limpiar_frame(self):
        if self.frame_actual:
            self.frame_actual.destroy()

    def mostrar_pantalla_inicio(self):
        self.limpiar_frame()
        self.frame_actual = tk.Frame(self.root, bg="white")
        self.frame_actual.pack(expand=True)

        tk.Label(self.frame_actual, text="Bienvenido a BioBookAR", font=("Helvetica", 14, "bold"), bg="white").pack(pady=20)
        tk.Button(self.frame_actual, text="Iniciar sesión", width=20, bg="#4CAF50", fg="white",
                  command=self.mostrar_login).pack(pady=10)
        tk.Button(self.frame_actual, text="Crear nuevo usuario", width=20, bg="#2196F3", fg="white",
                  command=self.mostrar_registro).pack(pady=10)

    def mostrar_login(self):
        self.limpiar_frame()
        self.frame_actual = tk.Frame(self.root, bg="white")
        self.frame_actual.pack(expand=True)

        tk.Label(self.frame_actual, text="Usuario", bg="white").pack()
        self.usuario_entry = tk.Entry(self.frame_actual)
        self.usuario_entry.pack()

        tk.Label(self.frame_actual, text="Contraseña", bg="white").pack()
        self.contraseña_entry = tk.Entry(self.frame_actual, show="*")
        self.contraseña_entry.pack()

        tk.Button(self.frame_actual, text="Iniciar sesión", bg="#4CAF50", fg="white",
                  command=self.login_manual).pack(pady=5)
        tk.Button(self.frame_actual, text="Iniciar con rostro", command=self.login_facial).pack(pady=5)
        tk.Button(self.frame_actual, text="← Volver", command=self.mostrar_pantalla_inicio).pack(pady=10)

    def mostrar_registro(self):
        self.limpiar_frame()
        self.frame_actual = tk.Frame(self.root, bg="white")
        self.frame_actual.pack(expand=True)

        tk.Label(self.frame_actual, text="Nombre completo", bg="white").pack()
        self.nombre_entry = tk.Entry(self.frame_actual)
        self.nombre_entry.pack()

        tk.Label(self.frame_actual, text="Usuario", bg="white").pack()
        self.usuario_reg = tk.Entry(self.frame_actual)
        self.usuario_reg.pack()

        tk.Label(self.frame_actual, text="Contraseña", bg="white").pack()
        self.contraseña_reg = tk.Entry(self.frame_actual, show="*")
        self.contraseña_reg.pack()

        tk.Label(self.frame_actual, text="Idioma preferido", bg="white").pack()
        self.idioma_var = tk.StringVar(value="es")
        tk.OptionMenu(self.frame_actual, self.idioma_var, "es", "en").pack()

        tk.Button(self.frame_actual, text="Registrar", bg="#2196F3", fg="white",
                  command=self.registrar_usuario).pack(pady=10)
        tk.Button(self.frame_actual, text="← Volver", command=self.mostrar_pantalla_inicio).pack(pady=5)

    def login_manual(self):
        usuario = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()
        user = db.obtener_usuario_por_credenciales(usuario, contraseña)
        if user:
            self.redirigir_por_rol(user)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas", parent=self.root)

    def login_facial(self):
        encoding_nuevo = facial.capturar_y_codificar_rostro()
        if encoding_nuevo is None:
            messagebox.showwarning("Rostro no detectado", "No se detectó exactamente un rostro", parent=self.root)
            return

        encodings_guardados = db.obtener_todos_los_encodings()
        usuario_id = facial.comparar_encoding_con_base(encoding_nuevo, encodings_guardados)

        if usuario_id is not None:
            user = self.obtener_usuario_por_id(usuario_id)
            self.redirigir_por_rol(user)
        else:
            messagebox.showwarning("Error", "Reconocimiento facial fallido. Intente con usuario y contraseña.", parent=self.root)

    def registrar_usuario(self):
        nombre = self.nombre_entry.get().strip()
        usuario = self.usuario_reg.get().strip()
        contraseña = self.contraseña_reg.get().strip()
        idioma = self.idioma_var.get()

        # Validar campos vacíos
        if not nombre or not usuario or not contraseña:
            messagebox.showwarning("Campos vacíos", "Debes completar todos los campos: nombre, usuario y contraseña.", parent=self.root)
            return

        # Captura facial
        encoding = facial.capturar_y_codificar_rostro()
        if encoding is None:
            messagebox.showwarning("Error", "No se detectó un rostro válido", parent=self.root)
            return

        # Obtener encodings existentes
        encodings_guardados = db.obtener_todos_los_encodings()

        # Comprobar si el rostro ya está registrado
        usuario_existente = facial.comparar_encoding_con_base(encoding, encodings_guardados)

        if usuario_existente is not None:
            messagebox.showerror("Error de Registro", 
                                "Este rostro ya está registrado en el sistema. "
                                "Por favor, inicia sesión o contacta con el administrador.", 
                                parent=self.root)
            return

        # Proceder al registro si no existe coincidencia
        exito = db.insertar_usuario(nombre, usuario, contraseña, "alumno", encoding, idioma)
        if exito:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente", parent=self.root)
            self.mostrar_pantalla_inicio()
        else:
            messagebox.showerror("Error", "Ese nombre de usuario ya existe", parent=self.root)



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
        messagebox.showinfo("Bienvenido", f"Hola, {nombre} ({rol})", parent=self.root)

        if rol == "alumno":
            from gui.alumno import alumno
            alumno.abrir_ventana(user, self.root)
        elif rol == "profesor":
            from gui.profesor import profesor
            profesor.abrir_ventana(user, self.root)


        # Aquí se redirigiría a gui.alumno o gui.profesor

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

