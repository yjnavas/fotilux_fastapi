#!/bin/bash
# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté lista..."
sleep 5

# Ejecutar migraciones
echo "Ejecutando migraciones..."
alembic upgrade head

# Iniciar la aplicación
echo "Iniciando la aplicación..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
