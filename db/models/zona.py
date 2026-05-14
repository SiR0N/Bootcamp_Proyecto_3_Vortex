from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base

class Zona(Base):
    __tablename__ = "zonas"

    id = Column(Integer, primary_key=True, index=True)
    estacion_id = Column(String(50), unique=True, index=True)
    nombre = Column(String(100), nullable=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    mediciones = relationship("Medicion", back_populates="zona")