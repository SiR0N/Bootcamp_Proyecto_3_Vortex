from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
from typing import Literal

"""
Schemas Pydantic para mediciones climaticas.
Validan que los datos climaticos tengan tipos correctos y rangos razonables.
"""

class MedicionBase(BaseModel):
    # La medicion debe estar asociada a una zona existente
    # gt=0 significa mayor que 0, el 0 no pasa
    zona_id: int = Field(..., gt=0)

    # Fecha y hora de la medicion. FastAPI puede leer strings ISO.
    # Optional ---> el campo no es obligatorio
    # default_factory=lambda ---> si no viene, usa la fecha y hora actual
    fecha: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Campos climaticos — rangos basados en limites fisicos reales
    temperatura: Optional[float] = Field(..., ge=-50, le=60)   # grados Celsius
    humedad: Optional[float] = Field(..., ge=0, le=100)         # porcentaje
    viento: Optional[float] = Field(..., ge=0)                  # no puede ser negativo
    lluvia: Optional[float] = Field(..., ge=0)                  # no puede ser negativa

    # Solo se aceptan estos tres valores — siempre en mayusculas
    # "aemet" → "AEMET", "manual" → "MANUAL", "scheduler" → "SCHEDULER"
    fuente: Literal["AEMET", "MANUAL", "SCHEDULER"] = Field(...)

    @field_validator("fuente", mode="before")
    @classmethod
    def normalizar_fuente(cls, v):
        # mode="before" ---> convierte ANTES de validar el Literal
        return str(v).upper()


class MedicionCreate(MedicionBase):
    # Hereda todos los campos y validaciones de MedicionBase
    pass


class MedicionResponse(MedicionBase):
    # Campos que genera la base de datos automaticamente
    id: int
    created_at: datetime

    class Config:
        # Permite que Pydantic lea objetos SQLAlchemy directamente
        from_attributes = True