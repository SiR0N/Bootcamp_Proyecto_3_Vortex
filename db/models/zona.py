from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Zona(Base):
    __tablename__ = "zonas"

    id = Column(Integer, primary_key=True, index=True)
    estacion_id = Column(String, unique=True, index=True)
    nombre = Column(String)
    latitud = Column(Float)
    longitud = Column(Float)

    # Relación lógica: "Una zona tiene muchas mediciones"
    mediciones = relationship("Medicion", back_populates="zona")