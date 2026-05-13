from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Medicion(Base):
    __tablename__ = "mediciones"
    __table_args__ = (
        CheckConstraint(
            "fuente IN ('aemet', 'manual', 'openweather')",
            name="ck_mediciones_fuente",
        ),
    )

    id          = Column(Integer, primary_key=True, index=True)
    zona_id     = Column(Integer, ForeignKey("zonas.id", ondelete="RESTRICT"), nullable=False)
    fecha       = Column(DateTime, nullable=False)
    temperatura = Column(Float, nullable=True)
    humedad     = Column(Float, nullable=True)
    viento      = Column(Float, nullable=True)
    lluvia      = Column(Float, nullable=True)
    presion     = Column(Float, nullable=True)
    fuente      = Column(String(20), nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    zona = relationship("Zona", back_populates="mediciones")