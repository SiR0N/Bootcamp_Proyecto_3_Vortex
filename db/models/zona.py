from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Zona(Base):
    __tablename__ = "zonas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    mediciones = relationship("Medicion", back_populates="zona")