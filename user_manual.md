# 📖 Manual de Usuario – BioBookAR

## 🧠 ¿Qué es BioBookAR?

BioBookAR es una aplicación educativa interactiva que combina:

- Reconocimiento facial para inicio de sesión.
- Tests evaluativos orales o manuales.
- Realidad aumentada con marcadores ARUCO para visualizar contenido educativo.
- Acceso a notas y progreso del estudiante.

---

## 👥 Tipos de Usuarios

### 👨‍🏫 Profesor

- Usuario inicial: `admin / admin` (requiere cambio obligatorio de contraseña).

**Funcionalidades:**
- Ver y eliminar alumnos.
- Editar preguntas de test por tema.
- Consultar estadísticas globales y por tema.

### 👨‍🎓 Alumno

- Registro con nombre, usuario, contraseña e imagen facial.

**Funcionalidades:**
- Ver notas.
- Realizar tests (por voz o manualmente).
- Acceder a contenido AR.
- Cambiar idioma (ES/EN).

---

## 🖥️ Requisitos e Instalación

### 1. Requisitos

- Python 3.10 o superior
- Webcam y micrófono funcional

### 2. Instalación Automática (Recomendada)

1. Abre terminal en el directorio del proyecto.
2. Ejecuta:

```bash
chmod +x BIOBOOKAR.sh
./BIOBOOKAR.sh

```

Este script instala dependencias y lanza la aplicación (`main.py`).

## 🚀 Inicio Rápido

### Inicio del Programa
Al ejecutar `BIOBOOKAR.sh`, se abre una ventana con dos botones:

- Iniciar sesión
- Crear nuevo usuario

Se puede elegir o manualmente o mediante voz.
---

## 🔐 Iniciar Sesión

### Como Alumno:
- Opción 1: Usuario + Contraseña
- Opción 2: Reconocimiento Facial automatico.

### Como Profesor:
- Solo mediante usuario/contraseña (`admin / admin` al inicio).
- Se te pedirá cambiar la contraseña obligatoriamente al primer ingreso.

---

## 📝 Registro de Alumno

1. **"Crear nuevo usuario"**.
2. Introduce:
   - Nombre
   - Usuario único
   - Contraseña
   - Idioma preferido
3. Captura tu rostro automaticamente.
4. Si el usuario o rostro ya existen, recibirás una advertencia.

---

## 📚 Funcionalidades de Alumno

Una vez dentro, tendrás acceso a:

### 1. Mis Notas
Visualiza:
- Temas disponibles.
- Notas obtenidas.
- Número de intentos.
- Mejor nota.

### 2. Realizar Test
- Puedes contestar hablando ("opción A", "opción B", etc.) o seleccionando con el ratón.
- Solo se habilitan los temas vistos con RA.
- El sistema evalúa automáticamente y almacena tu resultado.

### 3. Iniciar Realidad Aumentada (RA)
- Pulsa “Iniciar Realidad Aumentada”.
- Apunta tu cámara al marcador ARUCO correspondiente (tema1, tema2...).
- Se mostrará un video educativo superpuesto.
- El tema queda registrado como “visto” tras cada visualización.

### 4. Cambiar idioma
- Cambia entre español e inglés.
- Se guarda en la base de datos y se aplica al reiniciar sesión.

---

## 👨‍🏫 Funcionalidades del Profesor

Después de cambiar la contraseña:

### 1. Ver Alumnos
- Lista con nombre, usuario, media, intentos y mejor nota.
- Posibilidad de eliminar alumno (y sus datos).

### 2. Editar Preguntas
- Elige un tema (Tema 1 a 8).
- Visualiza, edita, agrega o elimina preguntas.
- Traducción automática para ES/EN.

### 3. Ver Estadísticas
- Media, máxima y mínima nota por tema.
- Número de alumnos por test.
- Doble clic en un tema para ver histograma de notas.

---

## 📦 Estructura de Archivos Útiles

| Archivo                            | Función                                        |
|------------------------------------|------------------------------------------------|
| `BIOBOOKAR.sh`                     | Instalación y ejecución automática             |
| `main.py`                          | Entrada principal del programa                 |
| `reset_admin.sh`                   | Resetear el usuario admin                      |



---

## 🧩 Consejos Útiles

- Si se bloquea el acceso del profesor, puedes usar `reset_admin.sh` para restaurar el usuario `admin/admin`.
- Asegúrate de tener buena iluminación para el reconocimiento facial.
- Cierra sesión antes de cambiar el idioma para aplicarlo correctamente.
- Si un test no se habilita, asegúrate de haber visto el tema en AR primero.