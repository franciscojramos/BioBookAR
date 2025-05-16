#!/bin/bash

# Ruta absoluta o relativa al script SQL temporal
SQL_SCRIPT="delete_admin.sql"
DB_PATH="./base_datos/biobookar.db"

# Crear archivo SQL temporal para eliminar al usuario admin
echo "DELETE FROM usuarios WHERE usuario = 'admin';" > $SQL_SCRIPT

# Ejecutar el SQL sobre la base de datos
echo "🗑️ Eliminando usuario admin..."
sqlite3 "$DB_PATH" < $SQL_SCRIPT

# Eliminar archivo temporal
rm $SQL_SCRIPT

# Ejecutar la app
echo "🚀 Iniciando BioBookAR..."
python3 main.py
