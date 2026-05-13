"""
db/init_db.py

Inicialización de la base de datos PostgreSQL/Supabase — Proyecto Vortex.

Este script:
1. Comprueba la conexión con la base de datos.
2. Crea las tablas del modelo relacional en el orden correcto:
      zonas → mediciones
   (zonas primero porque mediciones tiene una clave foránea hacia ella)
"""

from sqlalchemy import text
from db.session import engine


with engine.connect() as connection:

    # ── 1. Comprobar conexión ─────────────────────────────────────────────
    result = connection.execute(text("SELECT NOW();"))
    row = result.fetchone()
    print("✅ Conexión correcta con Supabase/PostgreSQL.")
    print(f"   Fecha/hora BD: {row[0]}\n")


    # ── 2. TABLA: ZONAS ───────────────────────────────────────────────────
    #
    # Representa una estación meteorológica o punto de medición.
    # Es la tabla "padre": cada medición pertenece a una zona.
    #
    # Campos:
    #   estacion_id → identificador textual de la fuente (ej. "EST-01")
    #   nombre      → nombre descriptivo de la zona
    #   latitud     → coordenada geográfica (puede ser NULL si no se conoce)
    #   longitud    → coordenada geográfica (puede ser NULL si no se conoce)
    # ─────────────────────────────────────────────────────────────────────
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.zonas (

            id          SERIAL PRIMARY KEY,

            estacion_id VARCHAR(50)  NOT NULL UNIQUE,

            nombre      VARCHAR(100),

            latitud     FLOAT,

            longitud    FLOAT,

            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))
    print("✅ Tabla 'zonas' creada (o ya existía).")


    # ── 3. TABLA: MEDICIONES ──────────────────────────────────────────────
    #
    # Almacena cada registro meteorológico recogido.
    # Está vinculada a zonas mediante zona_id (clave foránea).
    #
    # Regla de integridad:
    #   No pueden existir mediciones sin zona asociada.
    #   Si se intenta borrar una zona con mediciones, la BD lo impide.
    #
    # Campos climáticos: temperatura, humedad, viento, lluvia, presion
    #   → todos FLOAT y nullable (puede haber sensores sin datos)
    #   → presion en particular siempre llega como NULL en los datos actuales
    #
    # fuente → quién generó el dato: 'aemet' o 'manual'
    # ─────────────────────────────────────────────────────────────────────
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.mediciones (

            id          SERIAL PRIMARY KEY,

            zona_id     INTEGER NOT NULL
                            REFERENCES public.zonas(id)
                            ON DELETE RESTRICT,

            fecha       TIMESTAMP NOT NULL,

            temperatura FLOAT,

            humedad     FLOAT,

            viento      FLOAT,

            lluvia      FLOAT,

            presion     FLOAT,

            fuente      VARCHAR(20) NOT NULL
                            CHECK (fuente IN ('aemet', 'manual', 'openweather')),

            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))
    print("✅ Tabla 'mediciones' creada (o ya existía).")


    # Confirmamos todos los cambios en la base de datos
    connection.commit()
    print("\n✅ Base de datos inicializada correctamente.")