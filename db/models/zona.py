from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Zona(Base):
    __tablename__ = "zonas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    es_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    municipios = relationship("Municipio", back_populates="zona")