#!/bin/bash

echo "Instalando dependencias necesarias para BioBookAR..."

# Asegura que pip esté actualizado
python3 -m pip install --upgrade pip

# Instala las dependencias necesarias
pip install dlib cmake opencv-python face_recognition pillow SpeechRecognition transformers nltk matplotlib
pip uninstall opencv-python
pip install opencv-contrib-python


# Ejecuta el archivo principal
echo "Ejecutando BioBookAR."
python3 main.py
