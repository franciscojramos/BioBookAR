import tkinter as tk
import json
import speech_recognition as sr
import os
from tkinter import messagebox
from gui.alumno import alumno
from base_datos import db


def realizar_test(usuario_id, root, user):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Realizar Test")
    root.configure(bg="white")
    tk.Button(root, text="🔙 Volver al Menú", bg="#cccccc",
              command=lambda: alumno.abrir_ventana(user, root)).place(x=10, y=10)

    tk.Label(root, text="🧪 Selecciona un tema", font=("Helvetica", 12, "bold"), bg="white").pack(pady=10)

    temas_vistos = db.obtener_temas_vistos(usuario_id)

    for i in range(1, 9):
        estado = "normal" if i in temas_vistos else "disabled"
        tk.Button(root, text=f"Tema {i}", width=20, state=estado,
                  command=lambda tema=i: empezar_test_tema(usuario_id, tema, root, user)).pack(pady=5)


def cargar_preguntas_por_tema(tema):
    ruta = os.path.join("test", f"tema{tema}.json")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)



def empezar_test_tema(usuario_id, tema, root, user, indice=0, aciertos=0):
    preguntas = cargar_preguntas_por_tema(tema)

    if indice >= len(preguntas):
        for widget in root.winfo_children():
            widget.destroy()
        nota = round((aciertos / len(preguntas)) * 10, 2) if preguntas else 0
        db.guardar_resultado(usuario_id, tema, nota)
        tk.Label(root, text=f"✅ Test finalizado\nNota: {nota}/10", font=("Helvetica", 14), bg="white").pack(pady=30)
        tk.Button(root, text="← Volver a Temas", command=lambda: realizar_test(usuario_id, root, user),
                  bg="#cccccc").pack(pady=20)
        return

    pregunta = preguntas[indice]
    idioma = user[6] if isinstance(user, (list, tuple)) else user.get("idioma", "es")

    for widget in root.winfo_children():
        widget.destroy()

    root.title(f"Test Tema {tema}")
    root.configure(bg="white")

    tk.Label(root, text=f"Pregunta {indice + 1}: {pregunta['pregunta'][idioma]}", wraplength=400,
             font=("Helvetica", 12), bg="white").pack(pady=10)

    respuesta_var = tk.StringVar()
    radio_buttons = {}

    for opcion in ['a', 'b', 'c', 'd']:
        texto = f"{opcion.upper()}) {pregunta[opcion][idioma]}"
        rb = tk.Radiobutton(root, text=texto, variable=respuesta_var, value=opcion, bg="white")
        rb.pack(anchor="w", padx=40)
        radio_buttons[opcion] = rb

    # Instrucción de voz multilingüe
    instruccion = {
        "es": "🎙 Di 'opción A', 'opción B', etc. para seleccionar una respuesta",
        "en": "🎙 Di 'opción A', 'opción B', etc. para seleccionar una respuesta",
    }
    tk.Label(root, text=instruccion.get(idioma, instruccion["es"]), font=("Helvetica", 10), bg="white", fg="gray").pack(pady=5)

    feedback = tk.Label(root, text="", bg="white")
    feedback.pack()

    def enviar_respuesta():
        seleccion = respuesta_var.get()
        if not seleccion:
            feedback.config(text="⚠️ Selecciona una opción antes de continuar" if idioma == "es" else "⚠️ Please select an option before continuing")
            return
        correcto = seleccion.lower() == pregunta["respuesta"].lower()
        nuevo_aciertos = aciertos + 1 if correcto else aciertos
        empezar_test_tema(usuario_id, tema, root, user, indice + 1, nuevo_aciertos)

    def reconocer_y_seleccionar():
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone(device_index=0) as source:
                print("🎙 Escuchando...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            texto = recognizer.recognize_google(audio, language="es-ES").lower()
            print("📝 Texto reconocido:", texto)

            for opcion in ['a', 'b', 'c', 'd']:
                if f"opcion {opcion}" in texto or f"opción {opcion}" in texto:
                    respuesta_var.set(opcion)
                    feedback.config(text=f"✅ Seleccionada opción {opcion.upper()}")
                    return

            feedback.config(text="❌ No se reconoció ninguna opción válida. Diga por ejemplo: 'opción A'")
        except sr.WaitTimeoutError:
            feedback.config(text="⏱ Tiempo agotado. Intenta de nuevo.")
        except sr.UnknownValueError:
            feedback.config(text="❌ No se entendió el audio. Intenta de nuevo.")
        except sr.RequestError as e:
            feedback.config(text=f"🌐 Error de conexión: {e}")
        except Exception as e:
            feedback.config(text=f"🚨 Error inesperado: {str(e)}")

    tk.Button(root, text="Enviar", bg="#4CAF50", fg="white", command=enviar_respuesta).pack(pady=10)
    tk.Button(root, text="🎤 Hablar", bg="#FF9800", fg="white", command=reconocer_y_seleccionar).pack(pady=5)
