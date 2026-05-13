================================================================================
             REPORTE 2: HOJA DE RUTA - PROYECTO 3 (VORTEX)
================================================================================

Fecha Actualización: 12 de mayo de 2026 | Deadline: 18 de mayo (6 días laborables)
Progreso General: ████████░░ 80% completado | 3 componentes pendientes

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

┌─────────────┬────────────────┬───────────────────────────────────────────────┬─────────┐
│ PERSONA     │ BLOQUE         │ ARCHIVOS                                     │ ESTADO  │
├─────────────┼────────────────┼───────────────────────────────────────────────┼─────────┤
│ Juan (PO)   │ DB Setup +    │ .env ✅, db/models/medicion.py ✅,           │ ✅ 95%  │
│             │ API Mediciones │ db/models/zona.py ✅, api/routes/med. ✅    │         │
├─────────────┼────────────────┼───────────────────────────────────────────────┼─────────┤
│ Helen       │ ETL Completo   │ etl/extract.py ✅, etl/transform.py ✅,     │ ✅ 100% │
│             │                │ etl/load.py ✅, etl/pipeline.py ✅          │         │
├─────────────┼────────────────┼───────────────────────────────────────────────┼─────────┤
│ José Manuel │ API Zonas +   │ api/main.py ✅, api/routes/zonas.py ✅       │ ✅ 100% │
│ (SM)        │ Main           │ Swagger integrado ✅                          │         │
├─────────────┼────────────────┼───────────────────────────────────────────────┼─────────┤
│ Elizabeth   │ DB Base +     │ db/base.py ✅, db/session.py ✅,             │ ✅ 100% │
│             │ Validación     │ api/schemas/medicion.py ✅ (ajustes),        │         │
│             │                │ api/schemas/zona.py ✅                       │         │
├─────────────┼────────────────┼───────────────────────────────────────────────┼─────────┤
│ José Melo   │ Tests          │ test_validators.py ⏳, test_api.py ⏳        │ ⏳ 30%  │
├─────────────┼────────────────┼───────────────────────────────────────────────┼─────────┤
│ David       │ Linaje + Docs  │ etl/lineage.py ⏳, README.md ⏳,             │ ⏳ 20%  │
│             │ + Deploy       │ deploy/supabase_deploy.md ⏳                  │         │
└─────────────┴────────────────┴───────────────────────────────────────────────┴─────────┘

LEYENDA: ✅ Completado | ⏳ En progreso | ❌ Pendiente


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
                    CRONOGRAMA ACTUALIZADO (6 DÍAS RESTANTES)
================================================================================

✅ COMPLETADO:
├─ D1 (6-may):  Juan crea proyecto Supabase + .env
├─ D2 (7-may):  Elizabeth → db/base.py + session.py
├─ D3 (8-may):  Juan → db/models + Elizabeth → schemas Pydantic
├─ D4 (9-may):  José Manuel → api/main.py + zonas.py
├─ D5 (10-11):  Helen → ETL completo (extract, transform, load, pipeline)
└─ D6 (12-may): Juan → routes mediciones + Merge PR #54, #55

⏳ EN PROGRESO:
├─ D7 (12-13):  José Melo → Ampliar cobertura tests (⏳ 30%)
└─ D8 (13-14):  David → etl/lineage.py + deploy docs (⏳ 20%)

📅 PENDIENTE (ANTES DEL 18 MAY):
├─ D9 (15-16):  Revisión y fixes de tests
├─ D10 (17):    QA final + documentación README
└─ D11 (18):    Deploy staging + Presentación


================================================================================
                         REGLAS
================================================================================
CRITERIOS DE ÉXITO - ESTADO ACTUAL
================================================================================

✅ Proyecto Supabase creado y funcional
✅ Integridad referencial (FK zona_id)
✅ Duplicados eliminados en ETL
⏳ Linaje ETL (David en progreso)
✅ API REST (POST→201, GET/DELETE→404)
✅ Pydantic rechaza malformados
⏳ Tests funcionan (José Melo expandiendo cobertura)
⏳ README + deploy docs (David)

PENDIENTE CRÍTICO:
├─ José Melo: Completar tests/ (30% listo)
└─ David: etl/lineage.py + deploy/ (20% listo)eado y funcional
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