from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routes import zonas, mediciones

app = FastAPI(
    title='ClimApp API',
    description='API para la gestión de datos meteorológicos en la Comunidad de Madrid',
    version='1.0.0'
)



@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"message": "Lo sentimos, el recurso solicitado no existe."},
    )

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Error interno del servidor. Nuestro equipo técnico ha sido notificado."},
    )

# --- REGISTRO DE RUTAS (ROUTERS) ---
app.include_router(zonas.router)
app.include_router(mediciones.router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido a ClimApp API",
        "docs": "/docs",
        "status": "operacional"
    }