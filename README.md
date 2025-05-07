# 📘 BioBookAR

**BioBookAR** es una aplicación educativa interactiva desarrollada como proyecto académico para la asignatura de **CUIA** (Curso de Interfaces de Usuario Avanzadas) en la **Universidad de Granada, España**.  

Diseñada por **Francisco José Ramos Moya**, estudiante del **Doble Grado en Ingeniería Informática y Administración y Dirección de Empresas (ADE)**,esta aplicación ofrece una experiencia innovadora para el aprendizaje del cuerpo humano mediante el uso de tecnologías como realidad aumentada, reconocimiento facial, y procesamiento de lenguaje natural.

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
  - Cambio de idioma (ES/EN), que se guarda como preferencia en la base de datos.


### 👨‍🎓 Alumnos

- Se registran con nombre, usuario, contraseña y captura facial
- Inician sesión mediante usuario o reconocimiento facial (con fallback en caso de error)
- Acceden a:
  - “Mis notas”: ver notas por tema, intentos, mejor nota y media
  - “Realizar test”: responder tests por voz, repetirlos según disponibilidad
  - “Iniciar AR”: escanear marcadores ARUCO y ver videos educativos
  - Cambio de idioma (ES/EN), que se guarda como preferencia en la base de datos.


---

## 💻 Tecnologías Utilizadas

- **Python 3.10+**
- **Tkinter** – Interfaz gráfica
- **OpenCV** + `face_recognition` – Reconocimiento facial (usando vectores codificados, no imágenes)
- **OpenCV** + ARUCO – Realidad aumentada con marcadores
- **SQLite3** – Base de datos local
- **SpeechRecognition**, `transformers` o `nltk` – Procesamiento de voz/NLP
- **Pillow** – Visualización de imágenes
- **JSON** – Almacenamiento de tests y configuración
- **pickle / json** – Serialización de vectores de rostros


---

## 🗂️ Estructura del Proyecto

```plaintext
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
│   ├── videos/                        # Videos didácticos vinculados a marcadores ARUCO
│   └── logo.png                       # Imagen para pantalla de inicio
│
└── README.md                          # Descripción técnica del proyecto

---

## 🧾 Estructura de la Base de Datos

### Tabla `usuarios`
| Campo         | Tipo       | Descripción                                         |
|---------------|------------|-----------------------------------------------------|
| id            | INTEGER    | ID del usuario                                      |
| nombre        | TEXT       | Nombre completo                                     |
| usuario       | TEXT       | Nombre de usuario                                   |
| contraseña    | TEXT       | Contraseña en texto plano o hash                    |
| rol           | TEXT       | 'alumno' o 'profesor'                               |
| encoding      | BLOB       | Vector codificado del rostro (no imagen)            |
| idioma        | TEXT       | Preferencia de idioma del usuario ('es', 'en')      |


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
- Esta preferencia se guarda en la base de datos por usuario.
- Al iniciar sesión, la app carga el idioma seleccionado previamente.
- El usuario puede cambiar el idioma manualmente en cualquier momento, y se actualizará la base.

---

## 🔐 Inicio de Sesión y Registro

## 🔐 Inicio de Sesión y Registro

### Métodos de acceso:
- Usuario + contraseña
- Reconocimiento facial con `face_recognition`
- Si falla, muestra mensaje: `"Reconocimiento facial fallido"` y permite acceso manual

### Registro de nuevo usuario:
- Captura facial con webcam
- La imagen se convierte en un **vector facial codificado (encoding)**
- Ese vector se serializa y se guarda en la base de datos
- **No se almacena ninguna imagen del rostro**


---

## 🛠️ Requisitos del Sistema

- Python 3.10 o superior

### Instalación de dependencias:

```bash
pip install dlib cmake opencv-python face_recognition pillow sqlite3 SpeechRecognition transformers nltk
