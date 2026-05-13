from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

"""
Schemas Pydantic para zonas climaticas.
Un schema define la forma de los datos que entran o salen de la API.
"""

class ZonaBase(BaseModel):
    estacion_id: str = Field(..., min_length=1, max_length=50)
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    latitud: Optional[float] = Field(None, ge=-90, le=90)
    longitud: Optional[float] = Field(None, ge=-180, le=180)

    @field_validator("estacion_id", mode="before")
    @classmethod
    def normalizar_estacion_id(cls, v):
        return str(v).upper()

    @field_validator("nombre", mode="before")
    @classmethod
    def normalizar_nombre(cls, v):
        if v is None:
            return v
        return str(v).title()


class ZonaCreate(BaseModel):
    estacion_id: str = Field(..., min_length=1, max_length=50)
    nombre: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None


class ZonaResponse(BaseModel):
    id: int
    estacion_id: Optional[str] = None
    nombre: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True