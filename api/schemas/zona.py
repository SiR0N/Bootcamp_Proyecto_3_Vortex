from pydantic import BaseModel, Field

"""
Schemas Pydantic para zonas climaticas.
Un schema define la forma de los datos que entran o salen de la API.
"""

class ZonaBase(BaseModel):
    # Identificador de la estacion meteorologica
    # min_length/max_length ---> evita textos vacios o demasiado largos
    estacion_id: str = Field(..., min_length=2, max_length=50)

    # Nombre de la zona, minimo 2 caracteres y maximo 100
    nombre: str = Field(..., min_length=2, max_length=100)

    # Latitud valida: entre -90 y 90 (limites reales del planeta)
    latitud: float = Field(..., ge=-90, le=90)

    # Longitud valida: entre -180 y 180
    longitud: float = Field(..., ge=-180, le=180)


class ZonaCreate(ZonaBase):
    # Hereda todos los campos y validaciones de ZonaBase
    pass


class ZonaResponse(ZonaBase):
    # Campo que genera la base de datos automaticamente
    id: int

    class Config:
        # Permite que Pydantic lea objetos SQLAlchemy directamente
        from_attributes = True