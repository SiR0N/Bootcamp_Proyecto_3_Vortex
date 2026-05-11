from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base


class FuenteDato(Base):
    __tablename__ = "fuentes_dato"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100))
    url = Column(String(255))
    cobertura = Column(String(100))

    mediciones = relationship("Medicion", back_populates="fuente")