# 📘 BioBookAR

**BioBookAR** es una aplicación educativa interactiva desarrollada como proyecto académico para la asignatura de **CUIA** (Curso de Interfaces de Usuario Avanzadas) en la **Universidad de Granada, España**.  

Diseñada por **Francisco José Ramos Moya**, estudiante del **Doble Grado en Ingeniería Informática y Administración y Dirección de Empresas (ADE)**, esta aplicación ofrece una experiencia innovadora para el aprendizaje del cuerpo humano mediante el uso de tecnologías como realidad aumentada, reconocimiento facial, y procesamiento de lenguaje natural.

---

## 🎯 Objetivo del Proyecto

BioBookAR busca transformar la forma en que los estudiantes de secundaria aprenden sobre el cuerpo humano, ofreciendo una plataforma donde puedan:

- Interactuar con contenido educativo mediante marcadores físicos ARUCO
- Realizar tests orales evaluados automáticamente
- Acceder a sus notas y progreso individual
- Iniciar sesión mediante usuario o reconocimiento facial

---

## 👤 Roles del Sistema

### 👨‍🏫 Profesor (rol único)

- Usuario por defecto: `admin / admin`
- Al iniciar por primera vez, **debe cambiar nombre de usuario y contraseña**
- Accede a:
  - Lista de alumnos y sus estadísticas
  - Edición de preguntas de test por tema
  - Visualización del rendimiento global de la clase
  - Opción para cambiar el idioma (Español/Inglés)

### 👨‍🎓 Alumnos

- Se registran con nombre, usuario, contraseña y captura facial
- Inician sesión mediante usuario o reconocimiento facial (con fallback en caso de error)
- Acceden a:
  - “Mis notas”: ver notas por tema, intentos, mejor nota y media
  - “Realizar test”: responder tests por voz, repetirlos según disponibilidad
  - “Iniciar AR”: escanear marcadores ARUCO y ver videos educativos
  - Cambio de idioma (ES/EN)

---

## 💻 Tecnologías Utilizadas

- **Python 3.10+**
- **Tkinter** – Interfaz gráfica
- **OpenCV** + `face_recognition` – Reconocimiento facial
- **OpenCV** + ARUCO – Realidad aumentada con marcadores
- **SQLite3** – Base de datos local
- **SpeechRecognition**, `transformers` o `nltk` – Procesamiento de voz/NLP
- **Pillow** – Visualización de imágenes
- **JSON** – Almacenamiento de tests y configuración

---

## 🗂️ Estructura de carpetas del Proyecto

BioBookAR/
├── main.py                            # Punto de entrada principal
│
├── gui/                               # Interfaces gráficas con Tkinter
│   ├── login.py                       # Login + Registro de usuarios
│   ├── alumno.py                      # Vista principal del alumno
│   ├── profesor.py                    # Vista principal del profesor
│   └── componentes.py                 # Widgets reutilizables: idioma, menú, etc.
│
├── reconocimiento/                    # Módulo de reconocimiento facial
│   └── facial.py                      # Captura y verificación de rostros con OpenCV
│
├── base_datos/                        # Módulo de base de datos SQLite
│   └── db.py                          # Funciones CRUD: usuarios, resultados, estadísticas
│
├── realidad_aumentada/               # Módulo de RA con ARUCO
│   └── ar_aruco.py                    # Escaneo de marcadores y reproducción de video
│
├── tests/                             # Banco de preguntas
│   └── preguntas.json                 # Preguntas clasificadas por tema (editable por profesor)
│
├── recursos/                          # Recursos multimedia y de usuarios
│   ├── alumnos/                       # Imágenes de rostros capturados
│   ├── videos/                        # Videos didácticos vinculados a marcadores ARUCO
│   └── logo.png                       # Imagen para pantalla de inicio
│
└── README.md                          # Descripción técnica del proyecto

---

## 🧾 Estructura de la Base de Datos

### Tabla `usuarios`
| Campo         | Tipo       | Descripción                          |
|---------------|------------|--------------------------------------|
| id            | INTEGER    | ID del usuario                       |
| nombre        | TEXT       | Nombre completo                      |
| usuario       | TEXT       | Nombre de usuario                    |
| contraseña    | TEXT       | Contraseña en texto plano o hash     |
| rol           | TEXT       | 'alumno' o 'profesor'                |
| imagen_path   | TEXT       | Ruta a la imagen facial              |

### Tabla `resultados`
| Campo         | Tipo       | Descripción                          |
|---------------|------------|--------------------------------------|
| id            | INTEGER    | ID del resultado                     |
| usuario_id    | INTEGER    | Relación con usuario                 |
| tema          | TEXT       | Tema asociado al test                |
| nota          | FLOAT      | Nota obtenida                        |
| intentos      | INTEGER    | Número de intentos realizados        |

---

## 🧪 Sistema de Tests

- Las preguntas se cargan desde `tests/preguntas.json`.
- Cada tema contiene:
  - Pregunta
  - Opciones de respuesta
  - Respuesta correcta
- El alumno responde **por voz** usando el micrófono o manual.
- El sistema evalúa automáticamente y muestra:
  - Corrección inmediata.
  - Nota obtenida.
  - Posibilidad de repetir el test.
- Los resultados se guardan en la base de datos.

---

## 🧬 Módulo de Realidad Aumentada

- Utiliza marcadores ARUCO físicos colocados en un libro.
- El alumno accede a este modo desde su menú.
- Instrucciones en pantalla:
  - “Pulsa ESC para salir”
  - “Pulsa ENTER para iniciar cámara”
- Al escanear un marcador, se reproduce un **video educativo** vinculado al contenido escaneado.
- Los videos están almacenados en `recursos/videos/`.

---

## 🌍 Gestión de Idiomas

- La interfaz puede cambiarse entre **Español** e **Inglés**.
- Esta opción está disponible tanto para alumnos como para el profesor desde sus respectivos menús.
- Se puede guardar como preferencia del usuario si se desea.

---

## 🔐 Inicio de Sesión y Registro

### Métodos de acceso:
- Usuario + contraseña
- Reconocimiento facial con `face_recognition`
  - Si falla, muestra mensaje: `"Reconocimiento facial fallido"` y permite acceso manual

### Registro de nuevo usuario:
- Captura facial con webcam
- Datos guardados:
  - Imagen en `recursos/alumnos/`
  - Información en base de datos SQLite (`usuarios`)

---

## 🛠️ Requisitos del Sistema

- Python 3.10 o superior

### Instalación de dependencias:

```bash
pip install dlib cmake opencv-python face_recognition pillow sqlite3 SpeechRecognition transformers nltk
