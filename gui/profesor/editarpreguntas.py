import tkinter as tk
from tkinter import ttk, messagebox
import json, os
import gui.profesor.profesor as profesor

RUTA_TESTS = os.path.join("test")

def mostrar_editor_preguntas(root, user):
    root.geometry("950x750")
    for widget in root.winfo_children():
        widget.destroy()

    # Scrollable canvas
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # CENTRAR el contenido horizontalmente en el canvas
    canvas.create_window((475, 0), window=scrollable_frame, anchor="n")  # 950 // 2
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Contenedor centrado dentro del scroll
    contenedor_centrado = tk.Frame(scrollable_frame)
    contenedor_centrado.pack(padx=20, pady=10)

    # Botón volver (esquina superior izquierda del contenido)
    tk.Button(contenedor_centrado, text="← Volver", bg="#CCCCCC",
              command=lambda: profesor.abrir_ventana(user, root)).pack(anchor="w", padx=10, pady=10)

    tk.Label(contenedor_centrado, text="📝 Editor de Preguntas", font=("Helvetica", 14, "bold")).pack(pady=10)

    temas = [f"Tema {i}" for i in range(1, 9)]
    tema_var = tk.StringVar(value=temas[0])

    combo = ttk.Combobox(contenedor_centrado, values=temas, textvariable=tema_var, state="readonly")
    combo.pack()

    lista_preguntas = tk.Listbox(contenedor_centrado, width=80, height=10)
    lista_preguntas.pack(pady=10)

    preguntas_actuales = []

    def cargar_preguntas():
        lista_preguntas.delete(0, tk.END)
        nonlocal preguntas_actuales
        archivo = os.path.join(RUTA_TESTS, f"tema{tema_var.get().split()[-1]}.json")
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                preguntas_actuales = json.load(f)
                for p in preguntas_actuales:
                    lista_preguntas.insert(tk.END, p["pregunta"]["es"])
        except FileNotFoundError:
            preguntas_actuales = []

    combo.bind("<<ComboboxSelected>>", lambda e: cargar_preguntas())
    cargar_preguntas()

    entrada_pregunta_es = tk.Entry(scrollable_frame, width=80)
    entrada_pregunta_en = tk.Entry(scrollable_frame, width=80)
    entrada_a_es = tk.Entry(scrollable_frame, width=80)
    entrada_a_en = tk.Entry(scrollable_frame, width=80)
    entrada_b_es = tk.Entry(scrollable_frame, width=80)
    entrada_b_en = tk.Entry(scrollable_frame, width=80)
    entrada_c_es = tk.Entry(scrollable_frame, width=80)
    entrada_c_en = tk.Entry(scrollable_frame, width=80)
    entrada_d_es = tk.Entry(scrollable_frame, width=80)
    entrada_d_en = tk.Entry(scrollable_frame, width=80)
    respuesta_var = tk.StringVar(value="a")

    campos = [
        ("Pregunta ES", entrada_pregunta_es),
        ("Pregunta EN", entrada_pregunta_en),
        ("Opción A ES", entrada_a_es),
        ("Opción A EN", entrada_a_en),
        ("Opción B ES", entrada_b_es),
        ("Opción B EN", entrada_b_en),
        ("Opción C ES", entrada_c_es),
        ("Opción C EN", entrada_c_en),
        ("Opción D ES", entrada_d_es),
        ("Opción D EN", entrada_d_en)
    ]

    for label, entry in campos:
        tk.Label(scrollable_frame, text=label).pack()
        entry.pack()

    tk.Label(scrollable_frame, text="Respuesta correcta:").pack()
    ttk.Combobox(scrollable_frame, textvariable=respuesta_var, values=["a", "b", "c", "d"], state="readonly").pack(pady=5)

    def rellenar_formulario(event):
        idx = lista_preguntas.curselection()
        if not idx:
            return
        p = preguntas_actuales[idx[0]]
        entrada_pregunta_es.delete(0, tk.END)
        entrada_pregunta_es.insert(0, p["pregunta"]["es"])
        entrada_pregunta_en.delete(0, tk.END)
        entrada_pregunta_en.insert(0, p["pregunta"]["en"])

        entrada_a_es.delete(0, tk.END)
        entrada_a_en.delete(0, tk.END)
        entrada_a_es.insert(0, p["a"]["es"])
        entrada_a_en.insert(0, p["a"]["en"])

        entrada_b_es.delete(0, tk.END)
        entrada_b_en.delete(0, tk.END)
        entrada_b_es.insert(0, p["b"]["es"])
        entrada_b_en.insert(0, p["b"]["en"])

        entrada_c_es.delete(0, tk.END)
        entrada_c_en.delete(0, tk.END)
        entrada_c_es.insert(0, p["c"]["es"])
        entrada_c_en.insert(0, p["c"]["en"])

        entrada_d_es.delete(0, tk.END)
        entrada_d_en.delete(0, tk.END)
        entrada_d_es.insert(0, p["d"]["es"])
        entrada_d_en.insert(0, p["d"]["en"])

        respuesta_var.set(p["respuesta"])

    lista_preguntas.bind("<<ListboxSelect>>", rellenar_formulario)

    def guardar_json():
        archivo = os.path.join(RUTA_TESTS, f"tema{tema_var.get().split()[-1]}.json")
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(preguntas_actuales, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("✅ Guardado", "Cambios guardados correctamente.")

    def agregar():
        nueva = {
            "pregunta": {"es": entrada_pregunta_es.get(), "en": entrada_pregunta_en.get()},
            "a": {"es": entrada_a_es.get(), "en": entrada_a_en.get()},
            "b": {"es": entrada_b_es.get(), "en": entrada_b_en.get()},
            "c": {"es": entrada_c_es.get(), "en": entrada_c_en.get()},
            "d": {"es": entrada_d_es.get(), "en": entrada_d_en.get()},
            "respuesta": respuesta_var.get()
        }
        preguntas_actuales.append(nueva)
        lista_preguntas.insert(tk.END, nueva["pregunta"]["es"])
        guardar_json()

    def actualizar():
        idx = lista_preguntas.curselection()
        if not idx:
            return
        index = idx[0]
        preguntas_actuales[index] = {
            "pregunta": {"es": entrada_pregunta_es.get(), "en": entrada_pregunta_en.get()},
            "a": {"es": entrada_a_es.get(), "en": entrada_a_en.get()},
            "b": {"es": entrada_b_es.get(), "en": entrada_b_en.get()},
            "c": {"es": entrada_c_es.get(), "en": entrada_c_en.get()},
            "d": {"es": entrada_d_es.get(), "en": entrada_d_en.get()},
            "respuesta": respuesta_var.get()
        }
        lista_preguntas.delete(index)
        lista_preguntas.insert(index, entrada_pregunta_es.get())
        guardar_json()

    def eliminar():
        idx = lista_preguntas.curselection()
        if not idx:
            return
        index = idx[0]
        if messagebox.askyesno("Eliminar", "¿Eliminar esta pregunta?"):
            lista_preguntas.delete(index)
            preguntas_actuales.pop(index)
            guardar_json()

    tk.Button(scrollable_frame, text="💾 Actualizar", command=actualizar).pack(pady=5)
    tk.Button(scrollable_frame, text="➕ Añadir", command=agregar).pack(pady=5)
    tk.Button(scrollable_frame, text="🗑️ Eliminar", command=eliminar).pack(pady=10)

