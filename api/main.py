import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Importamos las rutas
from api.routes import zonas, mediciones
# Importamos la base de datos para inicializarla
from db.session import engine
from db.base import Base

# 1. CARGAR VARIABLES DE ENTORNO
# Esto es vital para que reconozca DATABASE_URL, SECRET_KEY, etc.
load_dotenv()

#NUEVO AÑADIDO 13/04/2026 - - -
# Importamos modelos para que SQLAlchemy los registre en Base.metadata
from db.base import Base
from db.session import engine
import db.models  # ← REGISTRA Zona y Medicion en Base.metadata

# Routers
from api.routes import zonas, mediciones
#NUEVO AÑADIDO 13/04/2026 - - -

app = FastAPI(
    title='VORTEX API',
    description='API para la gestión de datos meteorológicos en la Comunidad de Madrid',
    version='1.0.0'
)

#NUEVO AÑADIDO 13/04/2026 - - -
# CORS — necesario si el frontend Flask llama directo al puerto 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# - - -

# 2. CREAR LAS TABLAS EN LA BASE DE DATOS
# Esto hace que, al arrancar la App, se cree el archivo clima.db o se conecte a Postgres
# Si las tablas ya existen, no hace nada.
Base.metadata.create_all(bind=engine)

# --- MANEJO DE EXCEPCIONES ---

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"message": "Lo sentimos, el recurso solicitado no existe."},
    )
#@app.exception_handler(500)
#async def server_error_exception_handler(request: Request, exc: Exception):
    #return JSONResponse(
        #status_code=500,
        #content={"message": "Error interno del servidor. Nuestro equipo técnico ha sido notificado."},
            #)

# --- REGISTRO DE RUTAS (ROUTERS) ---
app.include_router(zonas.router)
app.include_router(mediciones.router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido a Vortex API",
        "docs": "/docs",
        "status": "operacional"
    }

# --- EJECUCIÓN ---
if __name__ == "__main__":
    # Esto permite ejecutar la API escribiendo simplemente: python api/main.py
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)