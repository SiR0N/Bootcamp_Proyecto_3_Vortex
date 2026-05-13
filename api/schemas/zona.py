from pydantic import BaseModel, Field
from datetime import datetime

"""
Schemas Pydantic para zonas climaticas.
Un schema define la forma de los datos que entran o salen de la API.
"""

class ZonaBase(BaseModel):
    estacion_id: str = Field(..., min_length=1, max_length=50)
    nombre: str | None = Field(default=None, min_length=0, max_length=100)
    latitud: float | None = Field(default=None, ge=-90, le=90)
    longitud: float | None = Field(default=None, ge=-180, le=180)


class ZonaCreate(BaseModel):
    estacion_id: str = Field(..., min_length=1, max_length=50)
    nombre: str | None = None
    latitud: float | None = None
    longitud: float | None = None


class ZonaResponse(BaseModel):
    id: int
    estacion_id: str | None = None
    nombre: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True