from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Estacion(Base):
    __tablename__ = "estaciones"

    id = Column(Integer, primary_key=True, index=True)
    indicativo = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    provincia = Column(String(100))
    lat = Column(Numeric)
    lon = Column(Numeric)
    municipio_id = Column(Integer, ForeignKey("municipios.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)

    municipio = relationship("Municipio", back_populates="estaciones")
    mediciones = relationship("Medicion", back_populates="estacion")