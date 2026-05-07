from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes import mediciones, zonas

app = FastAPI(
    title="Vortex API - Proyecto 3",
    description="API para gestión de inteligencia climática",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error interno: {str(exc)}"}
    )


@app.get("/")
def root():
    return {"message": "Vortex API - Proyecto 3", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(mediciones.router)
app.include_router(zonas.router)