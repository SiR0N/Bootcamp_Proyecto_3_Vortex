"""
db/base.py

Este archivo define la Base común de SQLAlchemy.

La Base es necesaria para que todos los modelos ORM del proyecto
puedan heredar de ella y SQLAlchemy pueda reconocerlos como tablas
de la base de datos.

Ejemplo de uso en un modelo:

    from db.base import Base

    class Zona(Base):
        ...
"""

# Importamos declarative_base desde SQLAlchemy.
# Esta función crea una clase base para definir modelos ORM.
from sqlalchemy.orm import declarative_base

# Creamos la Base común del proyecto.
# Todos los modelos de db/models/ deberán heredar de esta Base.
Base = declarative_base()