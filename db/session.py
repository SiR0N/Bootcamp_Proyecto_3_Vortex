"""
db/session.py

Este archivo configura la conexión entre la aplicación FastAPI
y la base de datos PostgreSQL alojada en Supabase.

Aquí se definen tres elementos principales:

1. engine:
   Motor de conexión con la base de datos.

2. SessionLocal:
   Fábrica de sesiones para consultar o modificar datos.

3. get_db:
   Función que FastAPI usa para abrir y cerrar una sesión
   de base de datos en cada petición.
"""

# Importamos os para leer variables de entorno del sistema o del archivo .env
import os

# load_dotenv permite cargar las variables guardadas en el archivo .env
from dotenv import load_dotenv

# create_engine crea el motor de conexión con PostgreSQL
from sqlalchemy import create_engine

# sessionmaker crea sesiones de base de datos
from sqlalchemy.orm import sessionmaker

# Cargamos las variables definidas en el archivo .env
# Por ejemplo: DATABASE_URL=postgresql://...
load_dotenv()

# Leemos la URL de conexión desde el archivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Validación defensiva:
# Si DATABASE_URL no existe, detenemos el programa con un mensaje claro.
# Esto evita errores confusos más adelante.
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL no está definida. Revisa que exista el archivo .env "
        "y que contenga la variable DATABASE_URL."
    )

# Creamos el engine de SQLAlchemy.
# El engine es el objeto que sabe cómo conectarse a PostgreSQL/Supabase.
engine = create_engine(DATABASE_URL)

# Creamos SessionLocal.
# SessionLocal NO es una sesión todavía.
# Es una fábrica que crea sesiones cuando las necesitamos.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Crea una sesión de base de datos y la cierra al terminar.

    Esta función se usa en las rutas de FastAPI con Depends(get_db).

    Ejemplo de uso en una ruta:

        def get_zonas(db: Session = Depends(get_db)):
            zonas = db.query(Zona).all()
            return zonas

    Funcionamiento:
    1. Abre una sesión.
    2. Entrega esa sesión a la ruta con yield.
    3. Cuando la ruta termina, cierra la sesión en finally.
    """

    # Creamos una nueva sesión de base de datos
    db = SessionLocal()

    try:
        # yield entrega la sesión a FastAPI
        yield db

    finally:
        # finally se ejecuta siempre, incluso si ocurre un error
        # Cerramos la sesión para no dejar conexiones abiertas
        db.close()