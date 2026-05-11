from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base

class Medicion(Base):
    __tablename__ = "mediciones"

    # Definición de la estructura de la tabla
    id = Column(Integer, primary_key=True, index=True)
    zona_id = Column(Integer, ForeignKey("zonas.id"), nullable=False)
    
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    temperatura = Column(Float, nullable=True)
    humedad = Column(Float, nullable=True)
    viento = Column(Float, nullable=True)
    lluvia = Column(Float, nullable=True)
    presion = Column(Float, nullable=True) # Este es el que faltaba
    fuente = Column(String(50), nullable=True)
    
    # Campo administrativo para saber cuándo se guardó el dato
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación lógica: "Esta medición pertenece a una Zona"
    zona = relationship("Zona", back_populates="mediciones")