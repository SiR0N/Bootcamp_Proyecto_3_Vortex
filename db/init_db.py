"""
Inicialización de base de datos PostgreSQL/Supabase — Proyecto Vortex.

Este script:
1. Comprueba conexión con la base de datos.
2. Crea todas las tablas normalizadas con sus relaciones correctas.

Modelo de datos:
    zonas → municipios → estaciones → mediciones → alertas
    fuentes_dato (catálogo)
    umbrales_alerta (catálogo AEMET)
    usuarios
"""

from sqlalchemy import text
from db.session import engine


with engine.connect() as connection:

    # ── 1. Comprobar conexión ──────────────────────────────────────────────────
    result = connection.execute(text("SELECT NOW();"))
    row = result.fetchone()
    print("Conexión correcta con Supabase/PostgreSQL.")
    print(f"Fecha/hora BD: {row[0]}\n")


    # ── 2. ZONAS ──────────────────────────────────────────────────────────────
    # Representa las regiones geográficas del proyecto (capital, norte, sur…).
    # Datos de origen: config/ubicaciones.json → regiones
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.zonas (
            id         SERIAL       PRIMARY KEY,
            codigo     VARCHAR(50)  NOT NULL UNIQUE,   -- ej: "capital", "norte"
            nombre     VARCHAR(100) NOT NULL,           -- ej: "Madrid Capital"
            es_default BOOLEAN      DEFAULT FALSE
        );
    """))
    print("✔️ Tabla zonas creada.")


    # ── 3. MUNICIPIOS ─────────────────────────────────────────────────────────
    # Municipios de la Comunidad de Madrid.
    # Datos de origen: config/municipios.json y config/ubicaciones.json
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.municipios (
            id       SERIAL       PRIMARY KEY,
            cod_ine  VARCHAR(10)  UNIQUE,               -- código INE del municipio
            nombre   VARCHAR(100) NOT NULL,
            lat      NUMERIC,
            lon      NUMERIC,
            zona_id  INTEGER      REFERENCES public.zonas(id) ON DELETE SET NULL
        );
    """))
    print("✔️ Tabla municipios creada.")


    # ── 4. ESTACIONES ─────────────────────────────────────────────────────────
    # Estaciones meteorológicas (AEMET u otras fuentes).
    # Se añade municipio_id para la relación estacion → municipio → zona.
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.estaciones (
            id            SERIAL       PRIMARY KEY,
            indicativo    VARCHAR(50)  NOT NULL UNIQUE,  -- ej: "3195", "3194U"
            nombre        VARCHAR(100) NOT NULL,
            provincia     VARCHAR(100),
            lat           NUMERIC,
            lon           NUMERIC,
            municipio_id  INTEGER      REFERENCES public.municipios(id) ON DELETE SET NULL
        );
    """))
    print("✔️ Tabla estaciones creada.")


    # ── 5. FUENTES_DATO ───────────────────────────────────────────────────────
    # Catálogo de fuentes de datos (aemet, manual, unknown…).
    # Datos de origen: config/aemet_thresholds.json → fuentes_datos
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.fuentes_dato (
            id       SERIAL       PRIMARY KEY,
            codigo   VARCHAR(50)  NOT NULL UNIQUE,       -- ej: "aemet", "manual"
            nombre   VARCHAR(100),
            url      VARCHAR(255),
            cobertura VARCHAR(100)
        );
    """))
    print("✔️ Tabla fuentes_dato creada.")


    # ── 6. MEDICIONES ─────────────────────────────────────────────────────────
    # Una medición por estación y fecha/hora.
    # fuente_id reemplaza la columna VARCHAR fuente → FK normalizada.
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.mediciones (
            id           SERIAL    PRIMARY KEY,
            estacion_id  INTEGER   NOT NULL
                             REFERENCES public.estaciones(id) ON DELETE CASCADE,
            fecha        TIMESTAMP NOT NULL,
            temperatura  NUMERIC,       -- °C
            humedad      NUMERIC,       -- %
            viento       NUMERIC,       -- km/h
            lluvia       NUMERIC,       -- mm
            presion      NUMERIC,       -- hPa
            fuente_id    INTEGER
                             REFERENCES public.fuentes_dato(id) ON DELETE SET NULL,

            UNIQUE (estacion_id, fecha)  -- una medición por estación/instante
        );
    """))
    print("✔️ Tabla mediciones creada.")


    # ── 7. UMBRALES_ALERTA ────────────────────────────────────────────────────
    # Catálogo de umbrales AEMET (amarillo/naranja/rojo por variable).
    # Datos de origen: config/aemet_thresholds.json → alertas
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.umbrales_alerta (
            id          SERIAL       PRIMARY KEY,
            variable    VARCHAR(50)  NOT NULL,   -- temperatura, viento, lluvia…
            nivel       VARCHAR(20)  NOT NULL,   -- amarillo, naranja, rojo
            valor       NUMERIC      NOT NULL,   -- umbral numérico
            descripcion VARCHAR(200),
            color_hex   VARCHAR(7),
            icono       VARCHAR(10),

            UNIQUE (variable, nivel)
        );
    """))
    print("✔️ Tabla umbrales_alerta creada.")


    # ── 8. ALERTAS ────────────────────────────────────────────────────────────
    # Alertas generadas para una medición concreta.
    # umbral_id enlaza con el catálogo de umbrales en lugar de duplicar datos.
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.alertas (
            id              SERIAL    PRIMARY KEY,
            medicion_id     INTEGER   NOT NULL
                                REFERENCES public.mediciones(id) ON DELETE CASCADE,
            umbral_id       INTEGER
                                REFERENCES public.umbrales_alerta(id) ON DELETE SET NULL,
            tipo            VARCHAR(50),   -- calor, viento, lluvia…
            nivel           VARCHAR(50),   -- amarillo, naranja, rojo
            mensaje         TEXT,
            valor_detectado NUMERIC,
            umbral          NUMERIC,       -- valor en el momento (desnormalizado para histórico)
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))
    print("✔️ Tabla alertas creada.")


    # ── 9. USUARIOS ───────────────────────────────────────────────────────────
    # Usuarios de la aplicación.
    # Datos de origen: data/usuarios.json
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS public.usuarios (
            id           SERIAL       PRIMARY KEY,
            email        VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
            activo       BOOLEAN      DEFAULT TRUE
        );
    """))
    print("✔️ Tabla usuarios creada.")


    # ── 10. INDICES DE RENDIMIENTO ────────────────────────────────────────────
    connection.execute(text("CREATE INDEX IF NOT EXISTS idx_mediciones_estacion_fecha ON public.mediciones(estacion_id, fecha);"))
    connection.execute(text("CREATE INDEX IF NOT EXISTS idx_alertas_medicion ON public.alertas(medicion_id);"))
    connection.execute(text("CREATE INDEX IF NOT EXISTS idx_estaciones_municipio ON public.estaciones(municipio_id);"))
    connection.execute(text("CREATE INDEX IF NOT EXISTS idx_municipios_zona ON public.municipios(zona_id);"))
    print("✔️ Índices creados.")


    # ── Confirmar cambios ─────────────────────────────────────────────────────
    connection.commit()
    print("\n✅ Base de datos inicializada")
    connection.commit()

    print("\nBase de datos inicializada correctamente.")
