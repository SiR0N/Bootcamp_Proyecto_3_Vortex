# VORTEX - Guía de Ejecución desde Cero

## ¿Qué es VORTEX?

VORTEX es una aplicación web de **seguimiento meteorológico** con dos servidores:

| Servidor | Puerto | Tecnología | Función |
|----------|--------|------------|---------|
| **Frontend** | 5000 | Flask + Jinja2 + HTML/CSS/JS | Sirve las páginas web (index, login, registro, etc.) |
| **Backend API** | 8000 | FastAPI + SQLAlchemy + PostgreSQL | CRUD de zonas/mediciones en base de datos |

## Arquitectura y Flujo de Datos

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  NAVEGADOR  │────▶│  FLASK (5000)     │────▶│  AEMET API   │
│  (localhost)│◀────│  /api/clima       │◀────│  OpenWeather │
└─────────────┘     │                  │     └──────────────┘
        │           │  POST /zonas/    │
        │           │  POST /mediciones│     ┌──────────────┐
        │           │  GET /zonas/     │────▶│  PostgreSQL  │
        │           │  GET /mediciones/│     │  (Supabase)  │
        ▼           └──────────────────┘     └──────────────┘
   HTML + JS                       
```

**Paso a paso cuando abres la web:**

1. Navegas a `http://localhost:5000/` → Flask sirve `index.html`
2. El JavaScript (`index.js`) ejecuta `actualizarClima()` automáticamente
3. JS llama a `GET /api/clima?lat=40.4167&lon=-3.7033` (Flask)
4. Flask llama a **AEMET API** (principal) → si falla, llama a **OpenWeather** (fallback)
5. Los datos se **normalizan** (servicio normalizer.py) → se guardan en JSON y en PostgreSQL
6. Flask devuelve los datos normalizados al frontend
7. JS actualiza la interfaz con temperatura, humedad, viento, lluvia...

## Requisitos Previos

Necesitas tener instalado:
- **Python 3.12+** (descargar de python.org)
- **Git** (opcional, para clonar)

## Ejecución Paso a Paso (PRIMERA VEZ)

### PASO 1: Abrir terminal en la carpeta del proyecto

Abre PowerShell o CMD y navega a:
```
cd C:\Users\JUAN\Desktop\Proyectos\Bootcamp_Proyecto_3_Vortex
```

### PASO 2: Verificar que tienes el archivo .env

Necesitas un archivo `.env` en la raíz del proyecto con estas claves:
```
SUPABASE_URL=https://rzygsdeigyfgyzktqrne.supabase.co
SUPABASE_KEY=tu_clave_supabase
DATABASE_URL=postgresql://postgres:tupassword@db.rzygsdeigyfgyzktqrne.supabase.co:5432/postgres
OPENWEATHER_API_KEY=tu_clave_openweather
AEMET_API_KEY=tu_clave_aemet
```

### PASO 3: Instalar dependencias (solo la primera vez)

```
pip install -r requirements.txt
```

### PASO 4: Arranque rápido (elige uno)

**OPCIÓN A — Con el script (RECOMENDADO):**

Ejecuta el archivo `INICIAR.bat` haciendo doble clic, O desde terminal:
```
.\INICIAR.bat
```

Esto arranca ambos servidores y abre el navegador automáticamente.

**OPCIÓN B — Manual (dos terminales):**

Terminal 1 — FastAPI:
```
python -c "import uvicorn; uvicorn.run('api.main:app', host='0.0.0.0', port=8000)"
```

Terminal 2 — Flask:
```
python -c "from app import app; app.run(host='0.0.0.0', port=5000)"
```

### PASO 5: Abrir el navegador

Ve a: **http://localhost:5000/**

Ahí verás el dashboard principal con los datos meteorológicos.

## ¿Por qué no hay EXE?

No hemos creado un `.exe` todavía porque:
- Necesita **ambos servidores corriendo simultáneamente**
- Hay que incluir las credenciales `.env` de forma segura
- El empaquetado con PyInstaller es posible pero aún no se ha configurado
- El `build/` que existía anteriormente era de pruebas y se ha eliminado

Si quieres un EXE en el futuro, se puede hacer con PyInstaller o auto-py-to-exe.

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| Página en blanco | Revisa que ambos servidores estén corriendo (puertos 5000 y 8000) |
| Datos no cargan | Verifica que tienes internet y las API keys funcionan |
| Error 500 | Puede ser que la tabla no exista en Supabase → regenerar |
| Flask no arranca | Verifica que el puerto 5000 no esté en uso |
| FastAPI no arranca | Verifica que el puerto 8000 no esté en uso |
| "Sin datos disponibles" | AEMET y OpenWeather han fallado — revisa API keys |

## Estructura del Proyecto

```
📁 Vortex/
├── api/                    # Servidor FastAPI
│   ├── main.py             # Punto de entrada FastAPI
│   ├── routes/             # Endpoints (zonas, mediciones)
│   └── schemas/            # Modelos Pydantic
├── app.py                  # Servidor Flask (frontend)
├── controllers/            # Lógica de negocio Flask
├── services/               # Servicios (normalizer, weather, fallback)
├── etl/                    # Pipeline ETL (extract, transform, load)
├── db/                     # Modelos SQLAlchemy, conexión
├── static/                 # CSS, JS, imágenes
│   ├── css/                # Archivos CSS (6 archivos)
│   ├── js/                 # JavaScript (index.js, auth.js, etc.)
│   └── img/                # Logo y recursos
├── templates/              # HTML (6 páginas)
├── data/                   # Datos meteorológicos (JSON)
├── config/                 # Configuración (ubicaciones, umbrales)
├── tests/                  # Tests unitarios
├── requirements.txt        # Dependencias Python
├── .env                    # Variables de entorno (NO SUBIR)
└── .gitignore              # Archivos a ignorar en Git
```