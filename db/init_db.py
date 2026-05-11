"""
Inicialización de base de datos PostgreSQL/Supabase.

Este script:
1. Comprueba conexión con la base de datos.
2. Crea las tablas del proyecto si no existen.
"""

from sqlalchemy import text
from db.session import engine


with engine.connect() as connection:

    # 1. Comprobar conexión
    result = connection.execute(text("SELECT NOW();"))
    row = result.fetchone()

    print("Conexión correcta con Supabase/PostgreSQL.")
    print(f"Fecha/hora BD: {row[0]}")

    # 2. Crear tabla zonas
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS public.estaciones (
                id SERIAL PRIMARY KEY,
                indicativo VARCHAR(50) NOT NULL UNIQUE,
                municipio VARCHAR(100),
                provincia VARCHAR(100),
                lat NUMERIC,
                lon NUMERIC,
                estacion_id VARCHAR(50)
            );
            """
        )
    )

    print("Tabla zonas creada o verificada correctamente.")

    # 3. Crear tabla mediciones
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS public.mediciones (
                id SERIAL PRIMARY KEY,
                FOREIGN KEY(zona_id)
                REFERENCES public.zonas(id)
                fecha TIMESTAMP NOT NULL,
                temperatura NUMERIC,
                humedad NUMERIC,
                viento NUMERIC,
                lluvia NUMERIC,
                presion NUMERIC,
                fuente VARCHAR(100),

                CONSTRAINT fk_zona
                    FOREIGN KEY(zona_id)
                    REFERENCES public.zonas(id)
                    ON DELETE CASCADE
            );
            """
        )
    )

    print("Tabla mediciones creada.")

    # 4. Crear tabla alertas
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS public.alertas (
                id SERIAL PRIMARY KEY,
                medicion_id INTEGER NOT NULL,
                tipo VARCHAR(50),
                nivel VARCHAR(50),
                mensaje TEXT,
                valor_detectado NUMERIC,
                umbral NUMERIC,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_medicion
                    FOREIGN KEY(medicion_id)
                    REFERENCES public.mediciones(id)
                    ON DELETE CASCADE
            );
            """
        )
    )

    print("Tabla alertas creada.")

    # Confirmar cambios
    connection.commit()

    print("\nBase de datos inicializada correctamente.")
