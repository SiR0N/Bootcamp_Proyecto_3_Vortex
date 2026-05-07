from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Medicion(Base):
    __tablename__ = "mediciones"

    id = Column(Integer, primary_key=True, index=True)
    zona_id = Column(Integer, ForeignKey("zonas.id"), nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    temperatura = Column(Float, nullable=True)
    humedad = Column(Integer, nullable=True)
    viento = Column(Float, nullable=True)
    lluvia = Column(Float, nullable=True)
    fuente = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    zona = relationship("Zona", back_populates="mediciones")