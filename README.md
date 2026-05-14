<div align="center">
  <img src="static/logo_vortex_4.png" alt="Texto alternativo" width="50%">
  <br><br>
  <span style="font-size: 1.2em;">Plataforma ETL + API para la gestión, análisis y consulta de datos meteorológicos en la Comunidad de Madrid</span>
</div>

---

   ![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white)
   ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
   ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white)
   ![Supabase](https://img.shields.io/badge/Supabase-Cloud-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
   ![AEMET](https://img.shields.io/badge/API-AEMET-red?style=for-the-badge)
   ![Lineage](https://img.shields.io/badge/Lineage-Trazabilidad-8A2BE2?style=for-the-badge)
   ![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-success?style=for-the-badge)

## 📌 Descripción

**Vortex** es una plataforma completa para la **ingestión, transformación, almacenamiento y consulta de datos meteorológicos** en la Comunidad de Madrid.

Un sistema completo que combina:

* Un pipeline ETL que procesa datos normalizados y los carga en PostgreSQL a través de una API REST.
* Un **auditor de trazabilidad (Pipeline Auditor)** que descarga datos crudos desde la API oficial de [AEMET OpenData](https://opendata.aemet.es/centrodedescargas/inicio), los compara con los normalizados y genera informes detallados de linaje.
* Una API REST desarrollada con **FastAPI** para exponer zonas, mediciones y operaciones del ETL.
* Una base de datos **PostgreSQL** alojada en **Supabase** donde se almacenan las mediciones normalizadas.
* Un diseño modular que permite escalar el sistema fácilmente.
* Capacidad de geolocalización inteligente.

**Vortex** proporciona al usuario los siguientes datos:

- 🌡️ **Temperatura** (gestión de máximas y mínimas).
- 💧 **Humedad** relativa del aire.
- 💨 **Viento** (velocidad y dirección).
- 🌧️ **Precipitaciones** acumuladas.
- ⚠️ **Alertas meteorológicas** críticas.

## 🚀 Características Principales

# 🔄 ETL completo (Extract → Transform → Load)

- `Extract.py`: Descarga datos de AEMET mediante API Key.
- `Transform.py`: Limpieza, normalización, eliminación de duplicados, validación de campos.
- `Load.py`: Inserción en PostgreSQL con control de zonas y mediciones.

# 🌍 Gestión de Zonas

- Registro automático de zonas según estacion_id.
- Relación 1:N entre Zona y Mediciones.
- Endpoints para CRUD completo.

# 🌡️ Gestión de Mediciones

- Inserción automática desde el ETL.
- Validación de fuente (aemet o manual).
- Consulta por zona.

# ⚡ API REST con FastAPI

- Documentación automática en /docs.
- Endpoints para zonas, mediciones y ejecución del ETL.

# 🗄️ Persistencia en PostgreSQL

- Modelos ORM con SQLAlchemy.
- Relaciones normalizadas.
- Integridad garantizada.

## 🧱 Arquitectura del Proyecto
```
.
│
├── 📄 .env / .env.example          ← Credenciales (AEMET, Supabase)
├── 📄 requirements.txt              ← Dependencias Python
├── 🚀 api/main.py                   ← Arranque de la API FastAPI
│
├── 📁 api/                          ← API REST (FastAPI)
│   ├── routes/                      ← Endpoints de zonas y mediciones
│   │   ├── zonas.py
│   │   └── mediciones.py
│   └── schemas/                     ← Validación con Pydantic
│       ├── zona.py
│       └── medicion.py
│
├── 📁 etl/                          ← Pipeline ETL (Extract → Transform → Load)
│   ├── pipeline.py                  ← Orquestador principal
│   ├── extract.py                   ← Carga el JSON normalizado
│   ├── transform.py                 ← Limpieza y validación
│   ├── load.py                      ← Sube zonas/mediciones a la API
│   ├── lineage.py                   ← Trazabilidad básica
│   └── pipeline_log.py              ← Auditor completo de trazabilidad
│
├── 📁 logs/                         ← Logs y evidencias (se generan autom.)
│   ├── app.log                      ← Registro de actividad
│   ├── snapshots/                   ← Instantáneas de cada etapa
│   │   ├── normalized/
│   │   └── transformed/
│   └── lineage/                     ← Informes de linaje detallados
│
├── 📁 db/                           ← Base de datos (SQLAlchemy ORM)
│   ├── models/                      ← Modelos Zona y Medición
│   │   ├── zona.py
│   │   └── medicion.py
│   ├── base.py
│   ├── session.py                   ← Conexión a PostgreSQL (Supabase)
│   └── init_db.py                   ← Creación de tablas
│
├── 📁 services/                     ← Servicios compartidos
│   ├── weather_api_service.py       ← Cliente AEMET (API Key)
│   ├── normalizer.py                ← Normalización de datos crudos
│   ├── normalizer_service.py
│   ├── logging_service.py           ← Configuración de logs
│   └── fallback_service.py          ← Datos sintéticos de respaldo
│
├── 📁 controllers/                  ← Lógica de negocio (Flask legacy)
│   ├── api_controller.py
│   ├── auth_controller.py
│   ├── compare_controller.py
│   └── ...
│
├── 📁 static/ & templates/          ← Frontend Flask (web app)
│   ├── css/, js/
│   └── templates/ (Jinja2)
│
├── 📁 data/                         ← Datos locales (JSON)
│   ├── registros_climaticos.json
│   ├── registros_climaticos_normalizados.json
│   └── ...
│
├── 📁 tests/                        ← Tests automáticos (pytest)
│   ├── test_api.py
│   ├── test_validators.py
│   └── ...
│
├── 📁 docs/                         ← Documentación interna del equipo
│   ├── estado_actual.md
│   ├── guia_equipo.md
│   └── ...
│
└── 📁 utils/                        ← Funciones auxiliares
    ├── validators.py
    ├── helpers.py
    └── ...
```
---

## 📺 Demo del Proyecto

---

## 📚 Documentación completa

---

## 🔄 Flujo ETL

# 1️⃣ Extract

Obtiene datos de AEMET mediante doble petición (handshake):

- Solicitud inicial → AEMET devuelve URL temporal.
- Segunda petición → descarga del JSON real.

# 2️⃣ Transform

- Limpieza de campos.
- Conversión de tipos.
- Eliminación de duplicados.
- Validación de estacion_id.
- Normalización de fuente.

# 3️⃣ Load

- Inserta zonas nuevas si no existen.
- Inserta mediciones asociadas.
- Control de errores y rollback.

### 📡 API REST (FastAPI)

## 📍 Rutas principales

|Método |	Ruta |	Descripción|
| :--- | :--- | :--- |
|GET	| /zonas	| Listado de zonas|
|POST	| /zonas	| Crear zona|
|GET	| /zonas/{id} |	Obtener zona|
|GET	|/zonas/{id}/mediciones	| Mediciones por zona |
|GET	|/mediciones	| Listado de mediciones |
|POST	|/etl/run	| Ejecutar pipeline ETL |
|GET	|/docs	| Documentación Swagger |


### 🗄️ Modelos (SQLAlchemy)

## 🟦 Zona

- `id`
- `estacion_id`
- `nombre`
- `latitud`
- `longitud`
- `relación → mediciones`

## 🟥 Medicion

- `id`
- `zona_id`
- `fecha`
- `temperatura`
- `humedad`
- `viento`
- `lluvia`
- `presion`
- `fuente`

### ⚙️ Instalación y Configuración
## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-org/vortex.git
cd vortex
```

## 2️⃣ Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
.\venv\Scripts\activate    # Windows
```
## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
## 4️⃣ Configurar variables de entorno
Crear archivo .env:

Código
DATABASE_URL=postgresql://usuario:password@localhost:5432/vortex
AEMET_API_KEY=tu_api_key
```
## 5️⃣ Iniciar FastAPI
```bash
uvicorn main:app --reload
```
## 🧪 Ejecutar el ETL
```bash
python etl/pipeline.py
```

   **Salida esperada:**

      ✔ Datos transformados: 26

      ✔ Filas insertadas: 25

      🎉 Pipeline completado

## 🧪 Testing
```bash
pytest -v
```
---

## 👩‍💻 Autores

| Miembro | Rol | Contacto |
| :--- | :--- | :--- |
| **Jose Manuel** | Scrum Master | [@SiRON](https://github.com/SiR0N) |
| **Juan Manuel de la Fuente** | Product Manager | [@juandelaf1](https://github.com/juandelaf1) |
| **Eli** | Desarrolladora | [@adryeli](https://github.com/adryeli) |
| **José Melo** | Desarrollador | [@GregDev08](https://github.com/GregDev08) |
| **David** | Desarrollador | [@drojas-7u7](https://github.com/drojas-7u7) |
| **Helen** | Desarrolladora | [@HelenDiMo](https://github.com/HelenDiMo) |

---

## 🧾 Licencia
Proyecto educativo desarrollado en el Bootcamp de Somos F5 en IA, Data Science & Programación — 2026.

*Uso libre para fines formativos y demostrativos.*
