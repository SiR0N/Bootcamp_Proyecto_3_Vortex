from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Municipio(Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, index=True)
    cod_ine = Column(String(10), unique=True)
    nombre = Column(String(100), nullable=False)
    lat = Column(Numeric)
    lon = Column(Numeric)
    zona_id = Column(Integer, ForeignKey("zonas.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)

    zona = relationship("Zona", back_populates="municipios")
    estaciones = relationship("Estacion", back_populates="municipio")