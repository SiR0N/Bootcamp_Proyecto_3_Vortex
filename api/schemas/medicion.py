from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import datetime, timezone
from typing import Literal

"""
Schemas Pydantic para mediciones climaticas.
Validan que los datos climaticos tengan tipos correctos y rangos razonables.
"""

class MedicionBase(BaseModel):
    zona_id: int = Field(..., gt=0)
    fecha: Union[str, datetime] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    temperatura: float = Field(..., ge=-50, le=60)
    humedad: float = Field(..., ge=0, le=100)
    viento: float = Field(..., ge=0)
    lluvia: float = Field(..., ge=0)
    presion: float = Field(..., ge=800, le=1100)
    fuente: Literal["AEMET", "manual", "api_aemet"] = Field(...)


class MedicionCreate(MedicionBase):
    pass


class MedicionResponse(MedicionBase):
    id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class MedicionUpdate(BaseModel):
    zona_id: Optional[int] = None
    fecha: Optional[Union[str, datetime]] = None
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    viento: Optional[float] = None
    lluvia: Optional[float] = None
    presion: Optional[float] = None
    fuente: Optional[Literal["AEMET", "manual", "api_aemet"]] = None