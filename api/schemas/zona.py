from pydantic import BaseModel, Field

<<<<<<< HEAD
# Esquema base con los campos comunes 
# - HELEN - ESTO LO MODIFICO PARA QUE NO ME DEJARA FUERA LOS REGISTROS QUE NO TENIAN NOMBRE, LATITUD O LONGITUD, YA QUE MUCHOS DATOS DE AEMET VIENEN ASÍ
class ZonaBase(BaseModel):
    #estacion_id: str = Field(..., example="EST-001")
    #nombre: str = Field(..., example="Madrid-Retiro")
    #latitud: float = Field(..., ge=-90, le=90, example=40.4167)
    #longitud: float = Field(..., ge=-180, le=180, example=-3.7033)

    estacion_id: str
    nombre: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
=======
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

>>>>>>> c208530eb32cc03e014d68488a45685936c635d8

class ZonaCreate(ZonaBase):
    # Hereda todos los campos y validaciones de ZonaBase
    pass


class ZonaResponse(ZonaBase):
    # Campo que genera la base de datos automaticamente
    id: int

    class Config:
        # Permite que Pydantic lea objetos SQLAlchemy directamente
        from_attributes = True