from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Medicion(Base):
    __tablename__ = "mediciones"

    id = Column(Integer, primary_key=True, index=True)
    estacion_id = Column(Integer, ForeignKey("estaciones.id", ondelete="CASCADE"), nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    temperatura = Column(Float, nullable=True)
    humedad = Column(Float, nullable=True)
    viento = Column(Float, nullable=True)
    lluvia = Column(Float, nullable=True)
    presion = Column(Float, nullable=True)
    fuente_id = Column(Integer, ForeignKey("fuentes_dato.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('estacion_id', 'fecha', name='uq_medicion_estacion_fecha'),)

    estacion = relationship("Estacion", back_populates="mediciones")
    fuente = relationship("FuenteDato", back_populates="mediciones")
    alertas = relationship("Alerta", back_populates="medicion")