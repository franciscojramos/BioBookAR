from tkinter import Tk
from gui.login import LoginApp
from base_datos import db

if __name__ == "__main__":
    db.crear_tablas()  # asegúrate de que las tablas existen

    root = Tk()
    app = LoginApp(root)
    root.mainloop()
