from pydantic import BaseModel, Field
from typing import Optional

"""
Schemas Pydantic para zonas climaticas.
Un schema define la forma de los datos que entran o salen de la API.
"""

class ZonaBase(BaseModel):
    # Identificador de la estacion meteorologica - REQUERIDO
    estacion_id: str = Field(..., min_length=2, max_length=50)

    # Nombre de la zona, opcional porque algunos datos de AEMET vienen incompletos
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)

    # Latitud valida: entre -90 y 90 (limites reales del planeta), opcional
    latitud: Optional[float] = Field(None, ge=-90, le=90)

    # Longitud valida: entre -180 y 180, opcional
    longitud: Optional[float] = Field(None, ge=-180, le=180)

class ZonaCreate(ZonaBase):
    # Hereda todos los campos y validaciones de ZonaBase
    pass


class ZonaResponse(ZonaBase):
    # Campo que genera la base de datos automaticamente
    id: int

    class Config:
        # Permite que Pydantic lea objetos SQLAlchemy directamente
        from_attributes = True