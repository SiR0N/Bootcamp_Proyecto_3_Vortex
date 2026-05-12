from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Esquema base con los campos comunes
class ZonaBase(BaseModel):
    estacion_id: str = Field(..., example="EST-001")
    nombre: str = Field(..., example="Madrid-Retiro")
    latitud: float = Field(..., ge=-90, le=90, example=40.4167)
    longitud: float = Field(..., ge=-180, le=180, example=-3.7033)

# Esquema para crear (POST)
class ZonaCreate(ZonaBase):
    pass

# Esquema para la respuesta (GET)
class ZonaResponse(ZonaBase):
    id: int

    class Config:
        from_attributes = True  # Esto permite que Pydantic lea modelos de SQLAlchemy