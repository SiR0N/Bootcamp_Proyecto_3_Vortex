"""
Test temporal de conexión con Supabase/PostgreSQL usando la tabla zonas.

Este script:
1. Comprueba la conexión con SELECT NOW().
2. Crea la tabla zonas si no existe.
3. Inserta una zona de prueba.
4. Lee las zonas guardadas.
"""

from sqlalchemy import text

from db.session import engine


with engine.connect() as connection:
    # 1. Comprobar conexión básica
    result = connection.execute(text("SELECT NOW();"))
    row = result.fetchone()

    print("Conexión correcta con Supabase/PostgreSQL.")
    print("Fecha/hora de la base de datos:")
    print(row)

    # 2. Crear tabla zonas si no existe
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS public.zonas (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE
            );
            """
        )
    )

    print("\nTabla public.zonas comprobada o creada correctamente.")

    # 3. Insertar una zona de prueba
    connection.execute(
        text(
            """
            INSERT INTO public.zonas (nombre)
            VALUES ('Madrid')
            ON CONFLICT (nombre) DO NOTHING;
            """
        )
    )

    # 4. Confirmar cambios
    connection.commit()

    print("Zona de prueba insertada correctamente o ya existente.")

    # 5. Leer zonas
    result_zonas = connection.execute(
        text(
            """
            SELECT id, nombre
            FROM public.zonas
            ORDER BY id;
            """
        )
    )

    zonas = result_zonas.fetchall()

    print("\nZonas encontradas en Supabase:")
    for zona in zonas:
        print(zona)
