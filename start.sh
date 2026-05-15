#!/bin/bash
echo "============================================"
echo "  VORTEX - Arranque completo (WSL)"
echo "============================================"
echo

# Activar entorno virtual
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
    echo "✓ Entorno virtual .venv activado"
else
    echo "[WARN] No se encontro .venv, usando Python global"
fi

# Liberar puertos por si quedaron procesos huérfanos
echo "Liberando puertos 8000 y 5000 por si acaso..."
fuser -k 8000/tcp 2>/dev/null
fuser -k 5000/tcp 2>/dev/null
sleep 1

# Arrancar FastAPI en background
echo "Arrancando FastAPI (puerto 8000)..."
uvicorn api.main:app --reload --port 8000 > fastapi.log 2>&1 &
FASTAPI_PID=$!

# Esperar a que FastAPI cargue
sleep 5

# Arrancar Flask en background
echo "Arrancando Flask (puerto 5000)..."
python app.py > flask.log 2>&1 &
FLASK_PID=$!

# Esperar a que Flask cargue
sleep 3

echo
echo "============================================"
echo "  SERVIDORES ARRANCADOS"
echo "  - Flask:   http://localhost:5000"
echo "  - FastAPI: http://localhost:8000/docs"
echo "============================================"
echo
echo "PIDs: FastAPI=$FASTAPI_PID, Flask=$FLASK_PID"
echo "Logs en: fastapi.log y flask.log"
echo "Pulsa Ctrl+C para parar ambos servidores."
echo

# Atrapar Ctrl+C para parar limpio
trap "echo; echo 'Parando servidores...'; kill $FASTAPI_PID $FLASK_PID 2>/dev/null; fuser -k 8000/tcp 5000/tcp 2>/dev/null; exit 0" INT

# Mantener vivo el script mostrando logs combinados
tail -f fastapi.log flask.log