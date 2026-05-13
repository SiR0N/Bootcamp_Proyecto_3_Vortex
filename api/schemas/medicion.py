from pydantic import BaseModel, Field
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
    # Optional --> el campo no es obligatorio
    # lambda --> cada vez que se crea una medicion, genera una fecha nueva
    fecha: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Campos climaticos — rangos basados en limites fisicos reales
    temperatura: float = Field(..., ge=-50, le=60)   # grados Celsius
    humedad: float = Field(..., ge=0, le=100)         # porcentaje
    viento: float = Field(..., ge=0)                  # no puede ser negativo
    lluvia: float = Field(..., ge=0)                  # no puede ser negativa
    presion: float = Field(..., ge=800, le=1100)      # hPa, rango atmosferico normal

    # Solo se aceptan estas dos fuentes de datos
    fuente: Literal["AEMET", "manual"] = Field(...)


class MedicionCreate(MedicionBase):
    # Hereda todos los campos y validaciones de MedicionBase
    pass


class MedicionResponse(BaseModel):
    id: int
    zona_id: int | None = None
    fecha: datetime | None = None
    temperatura: float | None = None
    humedad: float | None = None
    viento: float | None = None
    lluvia: float | None = None
    presion: float | None = None
    fuente: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class MedicionUpdate(BaseModel):
    # Para actualizaciones parciales - todos los campos opcionales
    zona_id: Optional[int] = None
    fecha: Optional[datetime] = None
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    viento: Optional[float] = None
    lluvia: Optional[float] = None
    presion: Optional[float] = None
    fuente: Optional[Literal["AEMET", "manual"]] = None