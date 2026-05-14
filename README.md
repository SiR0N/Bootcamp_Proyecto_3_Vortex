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
   ![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-success?style=for-the-badge)

---

## Contenidos

> Este README se encuentra en fase de redacción. Las secciones completadas están listas para revisión del equipo; el resto se incorporarán progresivamente.

| Sección | Estado |
|---------|--------|
| 1. Título y badges | Completado |
| 2. Tabla de contenidos | Completado |
| 3. Resumen del proyecto | Completado |
| 4. Arquitectura general | Completado |
| 5. Tecnologías utilizadas | Completado |
| 6. Requisitos previos | Completado |
| 7. Instalación y configuración | Completado |
| 8. Uso del sistema | Completado |
| 9. Flujo de datos y trazabilidad | Completado |
| 10. Base de datos | Completado |
| 11. Despliegue | Completado |
| 12. Testing | Pendiente |
| 13. Equipo | Pendiente |
| 14. Licencia | Pendiente |

---

## Resumen del proyecto

**Vortex** es una plataforma de gestión de inteligencia climática orientada a la Comunidad de Madrid. Su objetivo es automatizar la obtención, validación y exposición de datos meteorológicos fiables, combinando un pipeline ETL, una API REST y una capa de trazabilidad integrada.

El sistema resuelve la necesidad de disponer de datos climáticos estructurados y auditables, eliminando procesos manuales y garantizando la procedencia de cada registro.

**Funcionalidades principales**

* Ingesta automatizada de observaciones meteorológicas desde fuentes oficiales.
* Normalización, limpieza y validación de datos con reglas configurables.
* Almacenamiento en PostgreSQL con integridad referencial (zonas y mediciones).
* API REST documentada con FastAPI para consulta y carga de datos.
* Trazabilidad completa del dato: registro del origen, transformaciones y destino final.
* Gestión de zonas geográficas por estación meteorológica.

**Datos disponibles**

* Temperatura (máxima y mínima)
* Humedad relativa
* Viento (velocidad y dirección)
* Precipitaciones acumuladas
* Alertas meteorológicas críticas

---

## Arquitectura general

Vortex sigue una arquitectura modular con tres capas diferenciadas:

- **Capa de datos**: base de datos PostgreSQL alojada en Supabase, con modelos relacionales para zonas y mediciones.
- **Capa de negocio**: pipeline ETL que normaliza, transforma y carga los datos; servicios de trazabilidad que documentan cada etapa.
- **Capa de exposición**: API REST con FastAPI que sirve los datos validados y permite la operación del pipeline.

A nivel de directorios, el proyecto se organiza de la siguiente manera:

```
Vortex/
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
│   └── pipeline_log.py              ← Auditor de trazabilidad
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

## Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
|------------|--------------------|
| Python 3.12+ | Lenguaje principal del sistema |
| FastAPI | API REST con documentación automática |
| PostgreSQL | Almacenamiento relacional de datos |
| Supabase | Infraestructura cloud de la base de datos |
| SQLAlchemy | ORM para definición y consulta de modelos |
| Pydantic | Validación de esquemas en la API |
| AEMET OpenData | Fuente oficial de observaciones meteorológicas |
| pytest | Framework de testing automatizado |

---

## Requisitos previos

Antes de instalar y ejecutar Vortex, asegúrate de disponer de lo siguiente:

* Python 3.12 o superior
* Git
* Una cuenta gratuita en [Supabase](https://supabase.com/)
* Una clave de API de [AEMET OpenData](https://opendata.aemet.es/) (gratuita)

Se recomienda el uso de un entorno virtual (Conda, venv o similar) para aislar las dependencias del proyecto.

---

## Instalación y configuración

### 1. Clonar el repositorio

```
git clone https://github.com/SiR0N/Bootcamp_Proyecto_3_Vortex.git
cd Bootcamp_Proyecto_3_Vortex
```

### 2. Crear y activar un entorno virtual

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
.\venv\Scripts\activate    # Windows
```

### 3. Instalar las dependencias

```
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
DATABASE_URL=postgresql://user:password@host:port/dbname
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
AEMET_API_KEY=your-aemet-api-key
```

Los valores de `DATABASE_URL`, `SUPABASE_URL` y `SUPABASE_KEY` se obtienen desde el panel de control de Supabase (Project Settings > API). La `AEMET_API_KEY` se solicita gratuitamente en [AEMET OpenData](https://opendata.aemet.es/).

### 5. Iniciar la API

```
uvicorn api.main:app --reload
```

La API estará disponible en `http://localhost:8000`. La documentación interactiva (Swagger) se encuentra en `http://localhost:8000/docs`.

---

## Uso del sistema

### 1 Iniciar la API

```
uvicorn api.main:app --reload
```

La API estará disponible en `http://localhost:8000`. La documentación interactiva se encuentra en `http://localhost:8000/docs`.

### 2 Ejecutar el Pipeline ETL

El pipeline principal procesa el archivo de datos normalizados, los transforma y los carga en la base de datos a través de la API.

```
python etl/pipeline.py
```

Salida esperada (ejemplo):

```
Datos transformados: 26
Filas insertadas: 25
Pipeline completado
```

### 3 Ejecutar el Auditor de Trazabilidad

El sistema incluye un módulo de auditoría que descarga datos crudos desde AEMET, los compara con el archivo normalizado existente y genera informes de linaje sin modificar el flujo de producción.

```
python etl/pipeline_log.py
```

Los informes y snapshots se almacenan en `logs/snapshots/` y `logs/lineage/`.

### 4 Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/zonas` | Listar todas las zonas |
| POST | `/zonas` | Crear una nueva zona |
| GET | `/zonas/{id}` | Obtener una zona por ID |
| GET | `/zonas/{id}/mediciones` | Obtener mediciones de una zona |
| GET | `/mediciones` | Listar todas las mediciones |
| POST | `/mediciones` | Insertar una nueva medición |
| POST | `/etl/run` | Ejecutar el pipeline ETL |

---

## Flujo de datos y trazabilidad

El sistema implementa un ciclo de vida del dato en tres etapas, desde la fuente original hasta su almacenamiento definitivo:

**1. Obtención de datos crudos**

Las observaciones meteorológicas se descargan desde la API de AEMET OpenData. Esta fuente proporciona miles de registros diarios en formato JSON, correspondientes a estaciones distribuidas por todo el territorio nacional.

**2. Normalización y transformación**

Los datos crudos pasan por un proceso de filtrado, limpieza y validación. En esta etapa se descartan registros incompletos o fuera de rango, se unifican formatos de fecha y se convierten los tipos de datos numéricos. El resultado es un conjunto reducido de registros normalizados, preparados para su carga en la base de datos.

**3. Carga en base de datos**

Los registros transformados se insertan en PostgreSQL a través de la API REST. Cada medición queda vinculada a una zona geográfica identificada por su estación meteorológica de origen.

**Trazabilidad**

Cada ejecución del pipeline deja constancia documental de todo el proceso. El sistema genera automáticamente informes de linaje que registran:

- Cuántos registros se obtuvieron en cada etapa.
- Cuántos fueron descartados y por qué motivos.
- Qué transformaciones se aplicaron a los datos.

Estos informes, junto con las instantáneas de cada fase, se almacenan en `logs/snapshots/` y `logs/lineage/`, permitiendo auditar el recorrido de cualquier dato desde su origen hasta su destino final.

---

## Base de datos

El sistema utiliza **PostgreSQL** alojado en **Supabase** como motor de almacenamiento principal. La capa de acceso a datos se implementa mediante **SQLAlchemy ORM**, que permite definir y consultar los modelos de forma tipada y segura.

### Modelo de datos

**Zona**

Representa una estación meteorológica o ubicación geográfica de la cual se registran mediciones.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | Identificador único (autogenerado) |
| `estacion_id` | string | Código identificador de la estación |
| `nombre` | string | Nombre de la zona o estación |
| `latitud` | float | Coordenada de latitud |
| `longitud` | float | Coordenada de longitud |

Relación: una zona tiene múltiples mediciones (1:N).

**Medicion**

Representa una observación meteorológica puntual asociada a una zona.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | Identificador único (autogenerado) |
| `zona_id` | integer | Clave foránea hacia Zona |
| `fecha` | datetime | Fecha y hora de la observación |
| `temperatura` | float | Temperatura registrada |
| `humedad` | float | Porcentaje de humedad relativa |
| `viento` | float | Velocidad del viento |
| `lluvia` | float | Precipitación acumulada |
| `presion` | float | Presión atmosférica |
| `fuente` | string | Origen del dato (aemet, manual) |

### Conexión

Los parámetros de conexión se configuran en el archivo `.env` mediante las variables `DATABASE_URL`, `SUPABASE_URL` y `SUPABASE_KEY`. La configuración de la sesión se encuentra en `db/session.py`.

---

## Despliegue

El despliegue de la base de datos se realiza sobre **Supabase**, que proporciona PostgreSQL en la nube junto con herramientas de administración.

### 1. Crear un proyecto en Supabase

Accede a [supabase.com](https://supabase.com/), inicia sesión y crea un nuevo proyecto. Anota la contraseña de base de datos que establezcas durante la creación.

### 2. Obtener las credenciales de conexión

Una vez creado el proyecto, ve a **Project Settings > API** y copia:

- `Project URL` → será `SUPABASE_URL`
- `anon public` → será `SUPABASE_KEY`

En **Project Settings > Database** copia la cadena de conexión bajo `Connection string` → será `DATABASE_URL`. Sustituye `[YOUR-PASSWORD]` por la contraseña que configuraste en el paso 1.

### 3. Configurar las variables de entorno

Asegúrate de que tu archivo `.env` contiene los valores copiados:

```
DATABASE_URL=postgresql://postgres.xxxx:password@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=exxxxxxxxxxxxxxxxxxxxVCJ9...
```

### 4. Crear las tablas en la base de datos

Con el entorno virtual activado, ejecuta el script de inicialización:

```
python db/init_db.py
```

Este script crea las tablas `zonas` y `mediciones` con sus relaciones, utilizando los modelos definidos en `db/models/`.

### 5. Verificar el despliegue

Inicia la API y realiza una petición de prueba:

```
uvicorn api.main:app --reload
```

Abre `http://localhost:8000/zonas` en el navegador. Si la base de datos está correctamente configurada, recibirás una respuesta JSON vacía (`[]`) en lugar de un error.

Para instrucciones más detalladas, consulta `deploy/supabase_deploy.md`.

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
