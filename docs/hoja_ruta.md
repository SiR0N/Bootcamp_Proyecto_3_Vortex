================================================================================
             REPORTE 2: HOJA DE RUTA - PROYECTO 3
================================================================================

Fecha: 6 de mayo de 2026 | Deadline: 18 de mayo (9 días laborables)

================================================================================
                         FILOSOFÍA
================================================================================

- Cada persona trabaja en BLOQUES COMPLETOS y AISLADOS
- No se mezcal scripts entre desarrolladores
- Cuando termines, puedes ayudar a otros
- El PO da cobertura y coordina

================================================================================
                         DISTRIBUCIÓN EQUITATIVA (BLOQUES AISLADOS)
================================================================================

┌─────────────┬────────────────┬───────────────────────────────────────────────┐
│ PERSONA     │ BLOQUE         │ ARCHIVOS                                     │
├─────────────┼────────────────┼───────────────────────────────────────────────┤
│ Juan        │ DB Setup +    │ .env (credenciales), db/models/medicion.py, │
│             │ API Mediciones │ db/models/zona.py, api/routes/mediciones.py │
├─────────────┼────────────────┼───────────────────────────────────────────────┤
│ Helen       │ ETL Completo   │ etl/extract.py, etl/transform.py,           │
│             │                │ etl/load.py, etl/pipeline.py               │
├─────────────┼────────────────┼───────────────────────────────────────────────┤
│ José Manuel │ API Zonas +   │ api/main.py, api/routes/zonas.py            │
│             │ Main           │                                               │
├─────────────┼────────────────┼───────────────────────────────────────────────┤
│ Elizabeth   │ DB Base +     │ db/base.py, db/session.py,                  │
│             │ Validación     │ api/schemas/medicion.py, api/schemas/zona.py│
├─────────────┼────────────────┼───────────────────────────────────────────────┤
│ José Melo   │ Tests          │ tests/test_validators.py, tests/test_api.py │
├─────────────┼────────────────┼───────────────────────────────────────────────┤
│ David       │ Linaje + Docs  │ etl/lineage.py, README.md, deploy/           │
│             │ + Deploy      │                                               │
└─────────────┴────────────────┴───────────────────────────────────────────────┘


================================================================================
                         ESTRUCTURA FINAL
================================================================================

proyecto3/
├── api/
│   ├── main.py                           ← HELEN
│   ├── routes/
│   │   ├── mediciones.py                 ← JUAN
│   │   └── zonas.py                      ← HELEN
│   └── schemas/
│       ├── medicion.py                   ← ELIZABETH
│       └── zona.py                      ← ELIZABETH
├── db/
│   ├── base.py                           ← ELIZABETH
│   ├── session.py                        ← ELIZABETH
│   └── models/
│       ├── zona.py                       ← JUAN
│       └── medicion.py                   ← JUAN
├── etl/
│   ├── extract.py                       ← JOSÉ MANUEL
│   ├── transform.py                      ← JOSÉ MANUEL
│   ├── load.py                          ← JOSÉ MANUEL
│   ├── pipeline.py                      ← JOSÉ MANUEL
│   └── lineage.py                       ← DAVID
├── tests/
│   ├── test_validators.py                ← JOSÉ MELO
│   └── test_api.py                       ← JOSÉ MELO
├── deploy/                              ← DAVID
│   └── supabase_deploy.md
├── .env                                  ← JUAN (credenciales)
├── .env.example
├── requirements.txt
└── README.md                             ← DAVID


================================================================================
                         TAREA POR PERSONA (BLOQUE COMPLETO + EQUILIBRADO)
================================================================================

📋 JUAN (PO + Desarrollador)
└── CREAR PROYECTO SUPABASE + .env + db/models + api/routes/mediciones.py
    - Crear proyecto en supabase.com
    - Obtener credenciales (URL, KEY, DATABASE_URL)
    - Crear archivo .env con credenciales
    - db/models/zona.py (modelo SQLAlchemy)
    - db/models/medicion.py (modelo SQLAlchemy)
    - api/routes/mediciones.py (GET/POST/PUT/DELETE)

💻 HELEN (Desarrolladora)
└── etl/extract.py + etl/transform.py + etl/load.py + etl/pipeline.py
    - etl/extract.py (leer JSONs)
    - etl/transform.py (limpiar Pandas)
    - etl/load.py (cargar a Supabase)
    - etl/pipeline.py (orquestador)

🔧 JOSÉ MANUEL (SM + Desarrollador)
└── api/main.py + api/routes/zonas.py
    - api/main.py (FastAPI + Swagger)
    - api/routes/zonas.py (CRUD)

📝 ELIZABETH (Desarrolladora)
└── db/base.py + db/session.py + api/schemas/medicion.py + api/schemas/zona.py
    - db/base.py (SQLAlchemy declarative)
    - db/session.py (conexión DB)
    - api/schemas/medicion.py (Pydantic)
    - api/schemas/zona.py (Pydantic)

🧪 JOSÉ MELO (Desarrollador)
└── tests/test_validators.py + tests/test_api.py
    - tests/test_validators.py
    - tests/test_api.py

📚 DAVID (Desarrollador)
└── etl/lineage.py + README.md + deploy/
    - etl/lineage.py (trazabilidad)
    - README.md (documentación)
    - deploy/supabase_deploy.md (guía deploy)


================================================================================
                         TAREA EXTRA: BASE DE DATOS Y DEPLOY
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│ BASE DE DATOS: JUAN (como PO)                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ - Crear cuenta en https://supabase.com                                    │
│ - Crear nuevo proyecto (New Project)                                      │
│ - Nombre: climapp-proyecto3                                               │
│ - Obtener credenciales:                                                    │
│   * Project URL (https://xxxxx.supabase.co)                               │
│   * anon public key                                                        │
│   * service_role key                                                       │
│ - Crear archivo .env con todas las variables                              │
│ - Compartir .env.example (sin valores reales) con el equipo              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ DEPLOY: DAVID (añadido a su bloque)                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ - deploy/supabase_deploy.md:                                              │
│   * Cómo conectar Supabase al proyecto                                     │
│   * Variables de entorno necesarias                                        │
│   * Verificar conexión desde código                                       │
│   * Posibles comandos de despliegue                                        │
│ - README.md incluir sección de deploy                                     │
└─────────────────────────────────────────────────────────────────────────────┘


================================================================================
                         CRONOGRAMA (9 DÍAS)
================================================================================

D1 (6-may):  Juan crea proyecto Supabase + .env
D2 (7-may):  Elizabeth → db/base.py + session.py
D3 (8-may):  Juan → db/models + Elizabeth → schemas Pydantic
D4 (9-may):  José Manuel → ETL extract + transform
D5 (12-may): José Manuel → ETL load + pipeline
D6 (13-may): Helen → api/main.py + routes zonas
D7 (14-may): Juan → routes mediciones
D8 (15-may): José Melo → tests + David → lineage + deploy
D9 (18-may): David → README + Presentación


================================================================================
                         REGLAS
================================================================================

1. Cada uno termina su bloque antes de ayudar
2. Juan (PO) crea Supabase al inicio para que todos tengan DB
3. David incluye deploy en su documentación


================================================================================
                         CRITERIOS DE ÉXITO
================================================================================

□ Proyecto Supabase creado y funcional
□ Integridad referencial
□ Duplicados eliminados
□ Linaje ETL
□ API REST (POST→201, GET/DELETE→404)
□ Pydantic rechaza malformados
□ Tests funcionan
□ README + deploy docs


================================================================================
                         DEPENDENCIAS
================================================================================

- fastapi, uvicorn, sqlalchemy, pandas, pydantic, psycopg2-binary, pytest, httpx


================================================================================