from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from db.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)