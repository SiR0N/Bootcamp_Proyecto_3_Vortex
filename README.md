
<p align="center">
<img src="static/logo_vortex_4.png" alt="Texto alternativo" width="50%">
</p>

# Vortex

### Plataforma ETL + API para la gestión, análisis y consulta de datos meteorológicos en la Comunidad de Madrid

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastApi](https://img.shields.io/badge/FastAPI-Backend-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![AEMET](https://img.shields.io/badge/API-AEMET-red)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-success)


![Flask](https://img.shields.io/badge/Flask-Web%20App-black) ????

## 📌 Descripción

**Vortex** es una plataforma completa para la **ingestión, transformación, almacenamiento y consulta de datos meteorológicos** en la Comunidad de Madrid.

Un sistema completo que combina:

* Un ETL propio que obtiene datos de la API oficial de [AEMET OpenData](https://opendata.aemet.es/centrodedescargas/inicio).
* Una API REST desarrollada con FastAPI para exponer zonas, mediciones y operaciones del ETL.
* Una base de datos PostgreSQL donde se almacenan las mediciones normalizadas.
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
├── api
│   ├── routes
│   │   ├── __init__.py
│   │   ├── mediciones.py
│   │   └── zonas.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── main.py
│   ├── config
│   │   ├── aemet_thresholds.json
│   │   ├── estaciones_madrid.json
│   │   ├── municipios.json
│   │   └── ubicaciones.json
│   └── controllers
│       ├── __init__.py
│       ├── api_controller.py
│       ├── auth_controller.py
│       ├── compare_controller.py
│       └── (otros controllers: manual, scheduler, view)
│
├── controllers
│   ├── __init__.py
│   ├── api_controller.py
│   ├── auth_controller.py
│   ├── compare_controller.py
│   ├── manual_controller.py
│   ├── scheduler_controller.py
│   └── view_controller.py
│
├── db
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   └── __pycache__
│
├── etl
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── services
│   └── static
│       ├── css
│       │   ├── auth.css
│       │   ├── compare.css
│       │   ├── historico.css
│       │   ├── index.css
│       │   ├── registro_styles.css
│       │   └── style.css
│       └── js
│           ├── app.js
│           ├── auth.js
│           ├── index.js
│           └── estacion_por_municipio.json
│
├── utils
│   ├── __init__.py
│   ├── datetime_utils.py
│   ├── generar_estaciones.py
│   ├── helpers.py
│   ├── normalizar_datos.py
│   └── validators.py
│
├── data
│   ├── registros_climaticos_normalizados.json
│   ├── registros_climaticos.json
│   ├── registros_climaticos.json.backup
│   ├── registros_sinteticos.json
│   └── usuarios.json
│
├── docs
│   ├── estado_actual.md
│   ├── guia_equipo.md
│   └── hoja_ruta.md
│
├── tests
│   └── test_validators.py
│
├── .env
├── .env.example
├── .gitignore
├── app.py
├── main.py
├── clima.db
├── README.md
└── requirements.txt
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
| **Elena D.** | Desarrolladora | [@HelenDiMo](https://github.com/HelenDiMo) |

---

## 🧾 Licencia
Proyecto educativo desarrollado en el Bootcamp de Somos F5 en IA, Data Science & Programación — 2026.

*Uso libre para fines formativos y demostrativos.*