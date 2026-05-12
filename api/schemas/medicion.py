from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MedicionBase(BaseModel):
    zona_id: int = Field(..., example=1)
    fecha: datetime = Field(..., example="2024-03-20T12:00:00")
    # Campos climáticos del diagrama
    temperatura: float = Field(..., ge=-50, le=60, example=22.5)
    humedad: float = Field(..., ge=0, le=100, example=45.0)
    viento: float = Field(..., ge=0, example=12.5)
    lluvia: float = Field(..., ge=0, example=0.0)
    presion: float = Field(..., ge=800, le=1100, example=1013.2) # Faltaba este campo
    fuente: str = Field(..., example="AEMET")

class MedicionCreate(BaseModel):
    # En la creación, permitimos que la fecha sea opcional 
    # y usamos los mismos campos que el base
    zona_id: int
    fecha: Optional[datetime] = Field(default_factory=datetime.utcnow)
    temperatura: float
    humedad: float
    viento: float
    lluvia: float
    presion: float
    fuente: str = "AEMET"

class MedicionResponse(MedicionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MedicionUpdate(BaseModel):
    zona_id: Optional[int] = None
    fecha: Optional[datetime] = None
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    viento: Optional[float] = None
    lluvia: Optional[float] = None
    presion: Optional[float] = None
    fuente: Optional[str] = None