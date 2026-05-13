================================================================================
          PROYECTO 3: SISTEMA DE GESTIÓN DE INTELIGENCIA CLIMÁTICA (API & DB)
================================================================================
                    VERSIÓN DEFINITIVA: PostgreSQL + Supabase
================================================================================

================================================================================
                         FILOSOFÍA DE DESARROLLO
================================================================================

1. CADA PERSONA TRABAJA EN UN BLOQUE COMPLETO Y AISLADO
2. NO SE MEZCLAN SCRIPTS ENTRE DESARROLLADORES
3. CUANDO TERMINES, PUEDES AYUDAR A OTROS
4. EL PO DA COBERTURA Y COORDINA

================================================================================
                    DISTRIBUCIÓN EQUITATIVA (BLOQUES AISLADOS)
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│  JUAN (PO + Desarrollador) - PROYECTO COMPLETO                            │
│  ══════════════════════════════════════════════════════════════════════════│
│  Bloque: SUPABASE SETUP + DB + API MEDICIONES                              │
│  Archivos totales: 5                                                       │
│  ├── Crear proyecto en supabase.com                                       │
│  ├── .env (credenciales Supabase)                                          │
│  ├── db/models/zona.py (modelo SQLAlchemy)                                │
│  ├── db/models/medicion.py (modelo SQLAlchemy)                            │
│  └── api/routes/mediciones.py (CRUD completo)                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  HELEN (Desarrolladora)                                                     │
│  ══════════════════════════════════════════════════════════════════════════│
│  Bloque: ETL COMPLETO                                                       │
│  Archivos totales: 4                                                       │
│  ├── etl/extract.py (lee JSON)                                             │
│  ├── etl/transform.py (limpia con Pandas)                                  │
│  ├── etl/load.py (carga a Supabase)                                        │
│  └── etl/pipeline.py (orquestador)                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  JOSÉ MANUEL (SM + Desarrollador)                                          │
│  ══════════════════════════════════════════════════════════════════════════│
│  Bloque: API ZONAS + MAIN                                                   │
│  Archivos totales: 3                                                       │
│  ├── api/main.py (FastAPI + Swagger)                                       │
│  ├── api/routes/zonas.py (CRUD zonas)                                      │
│  └── api/routes/mediciones.py (integración con Juan)                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ELIZABETH (Desarrolladora)                                                │
│  ══════════════════════════════════════════════════════════════════════════│
│  Bloque: DB SETUP + SCHEMAS VALIDACIÓN                                     │
│  Archivos totales: 4                                                       │
│  ├── db/base.py (SQLAlchemy setup)                                        │
│  ├── db/session.py (conexión DB)                                           │
│  ├── api/schemas/medicion.py (Pydantic)                                    │
│  └── api/schemas/zona.py (Pydantic)                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  JOSÉ MELO (Desarrollador)                                                  │
│  ══════════════════════════════════════════════════════════════════════════│
│  Bloque: TESTS COMPLETOS                                                   │
│  Archivos totales: 2                                                       │
│  ├── tests/test_validators.py                                              │
│  └── tests/test_api.py                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  DAVID (Desarrollador)                                                      │
│  ══════════════════════════════════════════════════════════════════════════│
│  Bloque: TRAZABILIDAD + DOCUMENTACIÓN + DEPLOY                            │
│  Archivos totales: 3                                                       │
│  ├── etl/lineage.py (log de linaje)                                       │
│  ├── README.md (documentación completa)                                   │
│  └── deploy/supabase_deploy.md (guía despliegue)                          │
└─────────────────────────────────────────────────────────────────────────────┘


================================================================================
                    TAREA EXTRA: BASE DE DATOS Y DEPLOY
================================================================================

───────────────────────────────────────────────────────────────────────────────
SUPABASE: JUAN (como PO, hace el setup inicial)
───────────────────────────────────────────────────────────────────────────────
PASOS:
1. Ir a https://supabase.com y crear cuenta
2. Crear nuevo proyecto: "climapp-proyecto3"
3. Establecer contraseña de DB
4. Esperar a que-provisione (1-2 minutos)
5. Obtener credenciales del Settings → API:
   - Project URL
   - anon public key
   - service_role key (cuidado, no compartir)
6. Crear archivo .env:
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   DATABASE_URL=postgresql://postgres:TU_PASSWORD@db.xxxxx.supabase.co:5432/postgres
7. Crear .env.example (sin valores reales) y subirlo
8. Compartir .env con el equipo (NO subir a Git)

NOTA: Sin este paso, nadie puede trabajar.


───────────────────────────────────────────────────────────────────────────────
DEPLOY: DAVID (añadido a su bloque)
───────────────────────────────────────────────────────────────────────────────
Crear deploy/supabase_deploy.md con:
- Cómo conectar Supabase al proyecto
- Variables de entorno necesarias
- Verificar conexión desde código
- Comandos para despliegue (uvicorn, gunicorn, etc.)
- Notas para producción


================================================================================
                         DETALLE DE BLOQUES COMPLETOS
================================================================================

═══════════════════════════════════════════════════════════════════════════════
BLOQUE 1: JUAN (PO + Desarrollador)
═══════════════════════════════════════════════════════════════════════════════

PASO 0 - CREAR SUPABASE:
- Crear proyecto en supabase.com
- Obtener credenciales
- Crear .env

1. db/models/zona.py
   - class Zona(Base): id, nombre, lat, lon, created_at
   - relationship("Medicion", back_populates="zona")

2. db/models/medicion.py
   - class Medicion(Base): id, zona_id (FK), fecha, temperatura, humedad, viento, lluvia, fuente, created_at
   - relationship("Zona", back_populates="mediciones")

3. api/routes/mediciones.py
   - GET /mediciones (lista, 200)
   - GET /mediciones/{id} (detalle, 404 si no existe)
   - POST /mediciones (crear, 201 Created)
   - PUT /mediciones/{id} (editar, 200/404)
   - DELETE /mediciones/{id} (borrar, 204/404)


═══════════════════════════════════════════════════════════════════════════════
BLOQUE 2: HELEN (Desarrolladora)
═══════════════════════════════════════════════════════════════════════════════

1. etl/extract.py
   - read_json("data/registros_climaticos.json")
   - return DataFrame

2. etl/transform.py
   - drop_duplicates() por clave compuesta (fecha + zona)
   - dropna() y fillna()
   - normalize_types: temp float, humedad int, etc.
   - validate_ranges: temp[-50,60], humedad[0,100]

3. etl/load.py
   - to_sql() con SQLAlchemy
   - bulk_insert_mappings()

4. etl/pipeline.py
   - orchestrator: extract → transform → load


═══════════════════════════════════════════════════════════════════════════════
BLOQUE 3: JOSÉ MANUEL (SM + Desarrollador)
═══════════════════════════════════════════════════════════════════════════════

1. api/main.py
   - app = FastAPI(title="VORTEX API")
   - config DB connection
   - Swagger UI (/docs)
   - exception handlers (404, 500)

2. api/routes/zonas.py
   - GET /zonas (lista, 200)
   - GET /zonas/{id} (detalle, 404)
   - POST /zonas (crear, 201)
   - PUT /zonas/{id} (editar, 200/404)
   - DELETE /zonas/{id} (borrar, 204/404)
   - GET /zonas/{id}/mediciones


═══════════════════════════════════════════════════════════════════════════════
BLOQUE 4: ELIZABETH (Desarrolladora)
═══════════════════════════════════════════════════════════════════════════════

1. db/base.py
   - from sqlalchemy.orm import declarative_base
   - Base = declarative_base()

2. db/session.py
   - create_engine(DATABASE_URL) [usa variable de .env de Juan]
   - SessionLocal = sessionmaker(...)
   - def get_db(): yield SessionLocal()

3. api/schemas/medicion.py
   - MedicionCreate: zona_id, fecha, temp, humedad, viento, lluvia
   - Validación: temp[-50,60], humedad[0,100], viento≥0, lluvia≥0
   - MedicionResponse: +id

4. api/schemas/zona.py
   - ZonaCreate: nombre, lat, lon
   - ZonaResponse: +id


═══════════════════════════════════════════════════════════════════════════════
BLOQUE 5: JOSÉ MELO (Desarrollador)
═══════════════════════════════════════════════════════════════════════════════

1. tests/test_validators.py
   - test temp rango válido
   - test temp fuera rango → error
   - test humedad 0-100
   - test datos inválidos rechazados

2. tests/test_api.py
   - test GET /mediciones → 200
   - test GET /mediciones/{id} inexistente → 404
   - test POST /mediciones → 201
   - test PUT /mediciones/{id} → 200
   - test DELETE /mediciones/{id} → 204


═══════════════════════════════════════════════════════════════════════════════
BLOQUE 6: DAVID (Desarrollador)
═══════════════════════════════════════════════════════════════════════════════

1. etl/lineage.py
   - generar_linaje(df_original, df_limpio):
     * original_count = len(df_original)
     * limpio_count = len(df_limpio)
     * descartadas = original_count - limpio_count
   - guardar_log(lineage) → JSON/CSV

2. README.md
   - Descripción proyecto
   - Estructura carpetas (diagrama)
   - Diagrama DB (Draw.io)
   - pip install -r requirements.txt
   - Config .env
   - python etl/pipeline.py
   - uvicorn api.main:app
   - curl examples

3. deploy/supabase_deploy.md
   - Conexión Supabase al proyecto
   - Variables de entorno
   - Verificación de conexión
   - Notas de producción


================================================================================
                         CONEXIONES (CÓMO SE UNEN LOS BLOQUES)
================================================================================

                    ┌────────────────────────────────────────┐
                    │         ELIZABETH                      │
                    │  db/base.py + session.py              │
                    │  schemas/ (validación)                │
                    └─────────────────┬──────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
         ▼                           ▼                           ▼
  ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
  │    JUAN     │            │    HELEN    │            │   JOSÉ     │
  │  Supabase   │            │  API main   │            │   MANUEL    │
  │  DB models  │            │  routes     │            │   ETL       │
  │  routes     │            │             │            │             │
  └─────────────┘            └─────────────┘            └─────────────┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     ▼
                          ┌────────────────────┐
                          │   SUPABASE (DB)    │
                          └──────────┬─────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
  ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
  │  JOSÉ MELO  │            │   DAVID     │            │   EQUIPO    │
  │   Tests     │            │  Linaje     │            │   Ayudas    │
  │             │            │  README     │            │             │
  │             │            │  Deploy     │            │             │
  └─────────────┘            └─────────────┘            └─────────────┘


================================================================================
                         REGLAS DE COLABORACIÓN
================================================================================

1. JUAN CREA SUPABASE EL DÍA 1 (sin esto nadie puede trabajar)
2. CADA UNO TRABAJA SU BLOQUE HASTA TERMINAR
3. SI TERMINAS ANTES, PUEDES AYUDAR A OTROS
4. EL PO (JUAN) DA COBERTURA Y COORDINA
5. NO HAY CONFLICTOS SI CADA UNO TRABAJA EN SU BLOQUE


================================================================================
                         CRONOGRAMA (9 DÍAS)
================================================================================

SEMANA 1 (FUNDAMENTOS):
- D1 (6-may): JUAN crea proyecto Supabase + .env + estructura
- D2 (7-may): Elizabeth → db/base.py + session.py
- D3 (8-may): Juan → db/models + Elizabeth → schemas Pydantic
- D4 (9-may): José Manuel ETL extract + transform
- D5 (12-may): José Manuel ETL load + pipeline

SEMANA 2 (INTEGRACIÓN):
- D6 (13-may): Helen api/main.py + routes zonas
- D7 (14-may): Juan routes mediciones
- D8 (15-may): José Melo tests + David lineage + deploy
- D9 (18-may): David README + Presentación


================================================================================
                         CRITERIOS DE ÉXITO
================================================================================

□ Proyecto Supabase creado y funcional
□ Integridad referencial: zona_id válido
□ Duplicados eliminados por clave compuesta
□ Linaje ETL: log con descartadas/modificadas/insertadas
□ API REST: POST→201, GET/DELETE→404
□ Pydantic rechaza datos malformados
□ Tests funcionan
□ README completo
□ Documentación de deploy


================================================================================
                         RECURSOS
================================================================================

Tech: FastAPI + PostgreSQL/Supabase + SQLAlchemy + Pandas + Pydantic
Dependencias: fastapi, uvicorn, sqlalchemy, pandas, pydantic, psycopg2-binary, pytest, httpx
Deadline: 18 de mayo (9 días laborables)


================================================================================