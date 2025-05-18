# 📘 BioBookAR

**BioBookAR** es una aplicación educativa interactiva desarrollada como proyecto académico para la asignatura de **CUIA** (Curso de Interfaces de Usuario Avanzadas) en la **Universidad de Granada, España**. Diseñada por **Francisco José Ramos Moya**, estudiante del **Doble Grado en Ingeniería Informática y Administración y Dirección de Empresas (ADE)**, esta aplicación ofrece una experiencia innovadora para el aprendizaje del cuerpo humano mediante el uso de tecnologías como realidad aumentada, reconocimiento facial y procesamiento de lenguaje natural.

---

## 🎯 Objetivo del Proyecto

BioBookAR busca transformar la forma en que los estudiantes de secundaria aprenden sobre el cuerpo humano, ofreciendo una plataforma donde puedan:

- Interactuar con contenido educativo mediante marcadores físicos ARUCO.
- Realizar tests orales evaluados automáticamente.
- Acceder a sus notas y progreso individual.
- Iniciar sesión mediante usuario o reconocimiento facial.

---

## 👤 Roles del Sistema

### 👨‍🏫 Profesor (rol único)

- Usuario por defecto: `admin / admin`.
- Al iniciar por primera vez, debe cambiar la contraseña.
- Accede a:
  - Lista de alumnos, estadísticas básicas y posibilidad de eliminar alumno.
  - Edición avanzada de preguntas de test por tema.
  - Visualización detallada del rendimiento global y estadísticas de los alumnos.

### 👨‍🎓 Alumnos

- Se registran con nombre, usuario, contraseña y captura facial.
- No pueden registrarse con un nombre de usuario ya existente ni con un rostro ya registrado previamente.
- Inician sesión mediante usuario o reconocimiento facial (con fallback en caso de error).
- Acceden a:
  - “Mis notas”: ver notas por tema, intentos, mejor nota y media.
  - “Realizar test”: por voz o manualmente, repetirlos según disponibilidad.
  - “Iniciar AR”: escanear marcadores ARUCO y ver videos educativos relacionados con el tema, desbloqueando los test de cada tema correspondiente.
  - Cambio de idioma (ES/EN) de los test.

---

## 💻 Tecnologías Utilizadas

- Python 3.10+
- Tkinter – Interfaz gráfica.
- OpenCV + face_recognition – Reconocimiento facial (vectores codificados, no imágenes).
- OpenCV + ARUCO – Realidad aumentada con marcadores.
- SQLite3 – Base de datos local.
- SpeechRecognition, transformers o nltk – Procesamiento de voz/NLP.
- Pillow – Visualización de imágenes.
- JSON – Almacenamiento de tests y configuración.
- pickle/json – Serialización de vectores de rostros.

---

## 🗂️ Estructura del Proyecto

```plaintext
BioBookAR/
├── main.py                            # Punto de entrada principal.
├── BIOBOOKAR.sh                       # Script de instalación y ejecución automática.
├── gui/                               # Interfaces gráficas con Tkinter.
│   ├── login.py                       # Login + Registro de usuarios.
│   ├── alumno/                        # Módulo alumno.
│   │   ├── alumno.py
│   │   ├── AR.py
│   │   ├── misnotas.py
│   │   └── realizartest.py
│   ├── profesor/                      # Módulo profesor.
│   │   ├── profesor.py
│   │   ├── cambiarcontrasena.py
│   │   ├── editarpreguntas.py
│   │   ├── estadisticas.py
│   │   └── veralumnos.py
├── reconocimiento/
│   └── facial.py                      # Captura y verificación de rostros con OpenCV.
├── base_datos/
│   ├── db.py                          # Funciones CRUD: usuarios, resultados, estadísticas.
│   └── biobookar.db                   # Base de datos.
├── realidad_aumentada/
│   └── detector.py                    # Escaneo de marcadores y reproducción de video.
├── test/
│   ├── tema1.json
│   ├── tema2.json
│   ├── tema3.json
│   ├── tema4.json
│   ├── tema5.json
│   ├── tema6.json
│   ├── tema7.json
│   └── tema8.json
├── recursos/
│   ├── logof2.ico
│   ├── logof2.png
│   └── videos/                        # Videos didácticos vinculados a marcadores ARUCO.
└── README.md                          # Descripción técnica del proyecto.
```

---

## 💡 Créditos

- Autor: Francisco José Ramos Moya.
- Universidad: Universidad de Granada, España.
- Asignatura: Curso de Interfaces de Usuario Avanzadas (CUIA).

---

Además, el proyecto incluye un script `BIOBOOKAR.sh` que instala automáticamente las dependencias necesarias y ejecuta la aplicación.

---
