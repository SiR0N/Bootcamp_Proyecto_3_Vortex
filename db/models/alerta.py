from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    medicion_id = Column(Integer, ForeignKey("mediciones.id", ondelete="CASCADE"), nullable=False)
    umbral_id = Column(Integer, ForeignKey("umbrales_alerta.id", ondelete="SET NULL"))
    tipo = Column(String(50))
    nivel = Column(String(50))
    mensaje = Column(Text)
    valor_detectado = Column(Numeric)
    umbral = Column(Numeric)
    created_at = Column(DateTime, default=datetime.utcnow)

    medicion = relationship("Medicion", back_populates="alertas")
    umbral = relationship("UmbralAlerta")