import tkinter as tk
from tkinter import ttk
import subprocess
from gui.alumno import alumno

class ARventana(tk.Frame):
    def __init__(self, root, usuario_id, user, *args, **kwargs):
        for widget in root.winfo_children():
            widget.destroy()

        super().__init__(root, *args, **kwargs)
        self.usuario_id = usuario_id
        self.user = user
        self.root = root

        self.root.title("Realidad Aumentada - BioBookAR")
        self.pack(fill="both", expand=True)
        self.root.configure(bg="white")

        label = tk.Label(self, text="Pulsa el botón para iniciar la Realidad Aumentada.\nPulsa ESC o Q para salir de la ventana de RA.",
                         font=("Arial", 14), bg="white", justify="center")
        label.pack(pady=20)

        boton_ra = tk.Button(self, text="Iniciar Realidad Aumentada", command=self.iniciar_ra)
        boton_ra.pack(pady=10)

        boton_volver = tk.Button(self, text="← Volver", command=self.volver, bg="#cccccc")
        boton_volver.pack(pady=10)

    def iniciar_ra(self):
        subprocess.Popen(["python", "realidad_aumentada/detector.py", str(self.usuario_id)])

    def volver(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        alumno.abrir_ventana(self.user, self.root)

if __name__ == "__main__":
    def dummy_user():
        return [1, "Alumno Demo", None, None, None, None, "es"]  # Simulación estructura user

    root = tk.Tk()
    user_data = dummy_user()
    app = ARventana(root, usuario_id=user_data[0], user=user_data)
    app.mainloop()
