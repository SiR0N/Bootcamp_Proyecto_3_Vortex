from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union, Literal
from datetime import datetime, timezone

"""
Schemas Pydantic para mediciones climaticas.
Validan que los datos climaticos tengan tipos correctos y rangos razonables.
"""

class MedicionBase(BaseModel):
    zona_id:     int                  = Field(..., gt=0)
    fecha:       Union[str, datetime] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    temperatura: Optional[float]      = Field(None, ge=-50, le=60)
    humedad:     Optional[float]      = Field(None, ge=0, le=100)
    viento:      Optional[float]      = Field(None, ge=0)
    lluvia:      Optional[float]      = Field(None, ge=0)
    presion:     Optional[float]      = Field(None, ge=800, le=1100)
    fuente:      Literal["aemet", "manual"] = Field(...)  # ← minúsculas, sin SCHEDULER

    @field_validator("fuente", mode="before")
    @classmethod
    def normalizar_fuente(cls, v):
        return str(v).lower()  # ← era .upper()


class MedicionCreate(MedicionBase):
    pass


class MedicionResponse(BaseModel):
    id:          int
    zona_id:     int | None      = None
    fecha:       datetime | None = None
    temperatura: float | None    = None
    humedad:     float | None    = None
    viento:      float | None    = None
    lluvia:      float | None    = None
    presion:     float | None    = None
    fuente:      str | None      = None
    created_at:  datetime | None = None

    class Config:
        from_attributes = True


class MedicionUpdate(BaseModel):
    zona_id:     Optional[int]                        = None
    fecha:       Optional[Union[str, datetime]]        = None
    temperatura: Optional[float]                       = None
    humedad:     Optional[float]                       = None
    viento:      Optional[float]                       = None
    lluvia:      Optional[float]                       = None
    presion:     Optional[float]                       = None
    fuente:      Optional[Literal["aemet", "manual"]] = None  # ← minúsculas, sin SCHEDULER