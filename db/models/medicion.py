from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Medicion(Base):
    __tablename__ = "mediciones"

    id = Column(Integer, primary_key=True, index=True)
    zona_id = Column(Integer, ForeignKey("zonas.id", ondelete="CASCADE"), nullable=False)
    fecha = Column(String(255), nullable=False)  # Almacenar como string
    temperatura = Column(Float, nullable=True)
    humedad = Column(Float, nullable=True)
    viento = Column(Float, nullable=True)
    lluvia = Column(Float, nullable=True)
    presion = Column(Float, nullable=True)
    fuente = Column(String(50), nullable=True)
    created_at = Column(String(255), default=lambda: datetime.utcnow().isoformat())

    zona = relationship("Zona", back_populates="mediciones")