from pydantic import BaseModel, Field, field_validator
from typing import Optional

"""
Schemas Pydantic para zonas climaticas.
Un schema define la forma de los datos que entran o salen de la API.
"""

class ZonaBase(BaseModel):
    # Identificador de la estacion meteorologica
    # min_length/max_length ---> evita textos vacios o demasiado largos
    estacion_id: str = Field(..., min_length=2, max_length=50)

    # Nombre de la zona, minimo 2 caracteres y maximo 100
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)

    # Latitud valida: entre -90 y 90 (limites reales del planeta)
    latitud: Optional[float] = Field(None, ge=-90, le=90)

    # Longitud valida: entre -180 y 180
    longitud: Optional[float] = Field(None, ge=-180, le=180)

    @field_validator("estacion_id", mode="before")
    @classmethod
    def normalizar_estacion_id(cls, v):
        # "est-001" → "EST-001"
        return str(v).upper()

    @field_validator("nombre", mode="before")
    @classmethod
    def normalizar_nombre(cls, v):
        # "madrid-retiro" → "Madrid-Retiro"
        # None ---> lo dejamos pasar sin cambios
        if v is None:
            return v
        return str(v).title()


class ZonaCreate(ZonaBase):
    # Hereda todos los campos y validaciones de ZonaBase
    pass


class ZonaResponse(ZonaBase):
    # Campo que genera la base de datos automaticamente
    id: int

    class Config:
        # Permite que Pydantic lea objetos SQLAlchemy directamente
        from_attributes = True