# Guía de despliegue en Supabase

Esta guía te llevará desde cero hasta tener la base de datos de Vortex funcionando en Supabase y conectada con la API.

## Contenido

- [1. Requisitos previos](#1-requisitos-previos)
- [2. Crear un proyecto en Supabase](#2-crear-un-proyecto-en-supabase)
  - [2.1 Acceder al panel](#21-acceder-al-panel)
  - [2.2 Configurar el proyecto](#22-configurar-el-proyecto)
  - [2.3 Esperar a que el proyecto esté listo](#23-esperar-a-que-el-proyecto-este-listo)
- [3. Obtener las credenciales de conexión](#3-obtener-las-credenciales-de-conexión)
  - [3.1 SUPABASE_URL y SUPABASE_KEY](#31-supabase_url-y-supabase_key)
  - [3.2 DATABASE_URL](#32-database_url)
  - [3.3 Dónde encontrar cada valor (referencia visual)](#33-donde-encontrar-cada-valor-referencia-visual)
- [4. Configurar el archivo .env](#4-configurar-el-archivo-env)
- [5. Inicializar la base de datos](#5-inicializar-la-base-de-datos)
- [6. Verificar la conexión](#6-verificar-la-conexión)
- [7. Solución de problemas frecuentes](#7-solución-de-problemas-frecuentes)
- [8. Siguientes pasos](#8-siguientes-pasos)

---

## 1. Requisitos previos

Antes de empezar, asegúrate de tener:

- Una cuenta gratuita en [Supabase](https://supabase.com/). Puedes registrarte con GitHub, GitLab o correo electrónico.
- El repositorio de Vortex clonado en tu máquina local.
- Python 3.12+ y el entorno virtual del proyecto preparado (consulta el README principal).
- Un editor de texto para modificar el archivo `.env`.
- Conexión a internet para acceder al panel de Supabase y para que la API pueda conectarse a la base de datos remota.

> Si aún no tienes el proyecto configurado, vuelve al README y sigue los pasos de instalación antes de continuar.

## 2. Crear un proyecto en Supabase

Supabase organiza tus bases de datos en "proyectos". Cada proyecto incluye una instancia de PostgreSQL, autenticación, almacenamiento y APIs automáticas.

Sigue estos pasos desde el panel de control de Supabase:

### 2.1 Acceder al panel

1. Ve a [https://supabase.com/dashboard](https://supabase.com/dashboard) e inicia sesión con tu cuenta.
2. Si es la primera vez que entras, verás un botón **"New project"**. Si ya tienes proyectos, aparecerá en la esquina superior derecha de la pantalla.

### 2.2 Configurar el proyecto

Pulsa **"New project"** y rellena los siguientes campos:

| Campo | Qué poner |
|-------|-----------|
| **Name** | `vortex-db` (o el nombre que prefieras) |
| **Database Password** | Elige una contraseña segura. **Guárdala en un lugar seguro**; la necesitarás para conectar desde Python. |
| **Region** | `eu-central-1` (Fráncfort) para cumplir con regulaciones europeas y tener baja latencia desde España. |
| **Pricing Plan** | `Free` (incluye 500 MB de base de datos y 2 proyectos gratuitos). |

> La contraseña de base de datos no es la misma que la de tu cuenta de Supabase. Es exclusiva para este proyecto.

### 2.3 Esperar a que el proyecto esté listo

Pulsa **"Create new project"**. Supabase tardará entre 1 y 2 minutos en aprovisionar la base de datos. Mientras tanto, verás una animación de carga.

Cuando el proyecto esté listo, serás redirigido automáticamente al **panel de administración** del proyecto (Table Editor, SQL Editor, etc.).

## 3. Obtener las credenciales de conexión

Una vez creado el proyecto, necesitas tres valores para que Vortex pueda conectarse a la base de datos:

- `SUPABASE_URL` – la dirección HTTP de tu proyecto.
- `SUPABASE_KEY` – la clave anónima (permite consultas desde la API).
- `DATABASE_URL` – la cadena de conexión directa a PostgreSQL.

Los tres se obtienen desde el panel de Supabase.

### 3.1 SUPABASE_URL y SUPABASE_KEY

1. En el menú lateral izquierdo, pulsa el icono de ajustes (⚙️ **Project Settings**).
2. Dentro de Project Settings, haz clic en **API**.
3. Verás dos valores destacados:
   - **Project URL** → copia este valor. Será tu `SUPABASE_URL`.
   - **anon public** → copia este valor. Será tu `SUPABASE_KEY`.

> Ejemplo:  
> `SUPABASE_URL=https://rzygsdeigyfgyzktqrne.supabase.co`  
> `SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### 3.2 DATABASE_URL

1. En el menú lateral izquierdo, pulsa el icono de ajustes (⚙️ **Project Settings**).
2. Haz clic en **Database**.
3. Busca la sección **Connection string**.
4. Selecciona la pestaña **URI**.
5. Copia la cadena que aparece. Tiene este formato:  

   `postgresql://postgres.[ID_PROYECTO]:[TU_CONTRASEÑA]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres`

6. Sustituye `[TU_CONTRASEÑA]` por la contraseña de base de datos que elegiste al crear el proyecto (paso 2.2).

> **Importante**: no uses la contraseña de tu cuenta de Supabase,  
> sino la contraseña específica de la base de datos que pusiste  
> al crear el proyecto.

Guarda bien estos tres valores. Los necesitarás en la siguiente sección para configurar el archivo `.env`.

### 3.3 Dónde encontrar cada valor (referencia visual)

Cuando estés en **Project Settings > API** verás algo similar a esto:

    ┌─────────────────────────────────────────────────────────┐
    │  Project Settings  >  API                               │
    │                                                         │
    │  Project URL                                            │
    │  ┌───────────────────────────────────────────────────┐  │
    │  │ https://xxxxxxxxxxxx.supabase.co                  │  │
    │  └───────────────────────────────────────────────────┘  │
    │                                                         │
    │  Project API keys                                       │
    │  ┌───────────────────────────────────────────────────┐  │
    │  │ anon public                                        │  │
    │  │ eyJhbGciOiJIUzI1NiIs... (clave larga)             │  │
    │  │ ^-- Esta es tu SUPABASE_KEY                       │  │
    │  └───────────────────────────────────────────────────┘  │
    │                                                         │
    │  (La SUPABASE_URL es el Project URL)                    │
    └─────────────────────────────────────────────────────────┘

Y en **Project Settings > Database**:

    ┌─────────────────────────────────────────────────────────┐
    │  Project Settings  >  Database                          │
    │                                                         │
    │  Connection string                                      │
    │  ┌───────────────────────────────────────────────────┐  │
    │  │ URI                                                │  │
    │  │ postgresql://postgres.xxxx:[YOUR-PASSWORD]@...     │  │
    │  └───────────────────────────────────────────────────┘  │
    │                                                         │
    │  Sustituye [YOUR-PASSWORD] por la contraseña            │
    │  que pusiste al crear el proyecto.                      │
    └─────────────────────────────────────────────────────────┘

## 4. Configurar el archivo .env

El proyecto Vortex lee la configuración de base de datos desde un archivo `.env` ubicado en la raíz. Ya tienes uno creado durante la instalación; ahora debes completarlo con los valores que obtuviste en la sección 3.

### 4.1 Abrir el archivo .env

En la raíz del proyecto, abre el archivo `.env` con tu editor de texto o IDE.

### 4.2 Completar las variables

Asegúrate de que las siguientes líneas existan y contengan tus datos reales:

```
DATABASE_URL=postgresql://postgres.xxxx:[TU-CONTRASEÑA]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
AEMET_API_KEY=tu_clave_de_aemet
```

> La variable `AEMET_API_KEY` no es necesaria para el despliegue
> de la base de datos, pero sí para el pipeline ETL. Déjala como
> está si ya la tenías configurada.

### 4.3 Precauciones de seguridad

- **Nunca subas el archivo `.env` a GitHub.** El proyecto ya incluye una regla en `.gitignore` para evitarlo.
- Si compartes pantalla o haces una demo, oculta los valores de las claves.
- Si crees que una clave ha quedado expuesta, regenérala desde el panel de Supabase (Project Settings > API > JWT Settings).

## 5. Inicializar la base de datos

Con las credenciales configuradas, ya puedes crear las tablas
en PostgreSQL. El proyecto incluye un script que se encarga de
esto automáticamente.

### 5.1 Verificar el entorno

Abre una terminal en la raíz del proyecto y activa tu entorno virtual:

```
# Si usas venv
source venv/bin/activate

# Si usas Conda
conda activate vortex
```

Asegúrate de que el archivo `.env` está correctamente configurado (sección 4).

### 5.2 Ejecutar el script de inicialización

Ejecuta el siguiente comando:

```
python db/init_db.py
```

**¿Qué hace este script?**
- Lee las variables `DATABASE_URL`, `SUPABASE_URL` y `SUPABASE_KEY` desde `.env`.
- Conecta con PostgreSQL en Supabase usando SQLAlchemy.
- Crea las tablas `zonas` y `mediciones` con sus relaciones, exactamente como están definidas en `db/models/`.

### 5.3 Salida esperada

Si todo funciona correctamente, verás un mensaje similar a este:

```
Tablas creadas exitosamente.
```

Si no hay errores, las tablas ya existen en tu base de datos de Supabase y están listas para recibir datos.

### 5.4 Verificación visual en Supabase

Puedes confirmar la creación de las tablas desde el panel de Supabase:

1. En el menú lateral, pulsa **Table Editor**.
2. Verás dos tablas: `zonas` y `mediciones`.
3. Si pulsas en cualquiera de ellas, podrás ver su estructura (columnas, tipos de datos, claves foráneas).

> Si no ves las tablas, espera unos segundos y pulsa el botón de refresco del Table Editor. La sincronización puede tardar unos instantes.

### 5.5 Posible error de conexión

Si el script muestra un error como `could not translate host name` o `connection refused`, comprueba:

- Que las variables en `.env` son correctas (sin espacios, sin comillas extra).
- Que la contraseña en `DATABASE_URL` es la de la base de datos, no la de tu cuenta de Supabase.
- Que tienes conexión a internet.

Para soluciones más detalladas, consulta la sección 7 (Solución de problemas frecuentes).

## 6. Verificar la conexión

Una vez creadas las tablas, confirma que la API es capaz de conectarse a la base de datos y que todo el flujo funciona.

### 6.1 Iniciar la API

En la raíz del proyecto, con el entorno virtual activado, lanza el servidor:

```
uvicorn api.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

### 6.2 Probar un endpoint de lectura

Abre un navegador o una herramienta como Postman y visita:

```
http://localhost:8000/zonas
```

Si la conexión es correcta, recibirás una respuesta JSON vacía (porque aún no has insertado datos):

```json
[]
```

Si obtienes un error 500, un mensaje de conexión rechazada o una pantalla en blanco, detén el servidor y revisa la sección 7 (Solución de problemas frecuentes).

### 6.3 Explorar la documentación interactiva

FastAPI genera automáticamente documentación Swagger. Visita:

```
http://localhost:8000/docs
```

Allí podrás ver todos los endpoints disponibles, probarlos directamente desde el navegador y confirmar que la API responde correctamente.

### 6.4 Prueba rápida desde la terminal (opcional)

Si prefieres no usar el navegador, ejecuta:

```
curl http://localhost:8000/zonas
```

El resultado esperado es también `[]`.

> Si la respuesta contiene datos, es que el pipeline ETL ya ha sido ejecutado previamente. Eso también indica que la conexión funciona sin problemas.

## 7. Solución de problemas frecuentes

Durante el despliegue pueden aparecer algunos errores. Aquí tienes los más comunes y cómo resolverlos.

### Error: "could not translate host name to address"

- **Causa probable:** el valor de `DATABASE_URL` en `.env` es incorrecto o tienes problemas de conectividad.

- **Soluciones:**
    - Verifica que la URL comienza exactamente con `postgresql://postgres.xxxxxxxxx:...`
    - Comprueba que no hay espacios en blanco alrededor del signo `=` en el archivo `.env`.
    - Asegúrate de que tu conexión a internet funciona y no hay un firewall bloqueando el puerto 5432.

### Error: "password authentication failed"

- **Causa probable:** la contraseña en `DATABASE_URL` no coincide con la que pusiste al crear el proyecto en Supabase.

- **Soluciones:**
    - Recuerda que la contraseña es la de la base de datos, **no** la de tu cuenta de Supabase.
    - Si no estás seguro, puedes restablecer la contraseña en **Project Settings > Database > Database Password**.

### Error: "relation 'zonas' does not exist"

- **Causa probable:** el script `db/init_db.py` no se ha ejecutado o falló sin que lo notaras.

- **Soluciones:**
    - Vuelve a ejecutar `python db/init_db.py` y revisa la salida.
    - En el panel de Supabase, ve a **SQL Editor** y ejecuta: `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';` Si no ves las tablas, repite el paso 5.

### La API inicia pero al visitar /zonas no responde

- **Causa probable:** el servidor Uvicorn está detenido o el  
puerto 8000 está ocupado.

- **Soluciones:**
    - Asegúrate de que el comando `uvicorn api.main:app --reload` sigue en ejecución en la terminal.
    - Si el puerto está ocupado, usa otro: `uvicorn api.main:app --reload --port 8001`
    - Revisa que el archivo `.env` contiene las tres variables de Supabase (`SUPABASE_URL`, `SUPABASE_KEY`, `DATABASE_URL`).

### Error: "ModuleNotFoundError: No module named 'sqlalchemy'"

- **Causa probable:** no has instalado las dependencias del proyecto o el entorno virtual no está activado.

- **Soluciones:**
    - Asegúrate de haber ejecutado `pip install -r requirements.txt`.
    - Verifica que el entorno virtual está activo (debe aparecer `(venv)` o `(vortex)` en la terminal).

> Si tras aplicar estas soluciones el problema persiste, contacta con el equipo o revisa los logs en `logs/app.log` para obtener más detalles del error.

## 8. Siguientes pasos

Con la base de datos operativa y la API respondiendo, puedes pasar a utilizar el sistema en su conjunto.

### 8.1 Poblar la base de datos

Para insertar datos reales en las tablas `zonas` y `mediciones`, tienes dos opciones:

**Ejecutar el pipeline completo**  
Esto descargará datos crudos de AEMET, los normalizará,
transformará y cargará en la base de datos:

```
python etl/pipeline.py
```

**Usar el auditor de trazabilidad**  
Si deseas ejecutar el pipeline con informes de linaje detallados:

```
python etl/pipeline_log.py
```

Ambos comandos requieren que el archivo `.env` tenga una clave válida en `AEMET_API_KEY`.

### 8.2 Insertar datos de prueba manualmente

Si quieres verificar rápidamente la funcionalidad, puedes insertar algunos registros desde la documentación interactiva:

1. Visita `http://localhost:8000/docs`
2. Usa el endpoint `POST /zonas` para crear una estación.
3. Usa el endpoint `POST /mediciones` para añadir una observación.

### 8.3 Consultar los endpoints disponibles

Recuerda que la API ofrece estos recursos:

| Método | Ruta                      | Descripción                    |
|--------|---------------------------|--------------------------------|
| GET    | `/zonas`                  | Listar todas las zonas         |
| POST   | `/zonas`                  | Crear una nueva zona           |
| GET    | `/zonas/{id}`             | Obtener una zona por ID        |
| GET    | `/zonas/{id}/mediciones`  | Mediciones de una zona         |
| GET    | `/mediciones`             | Listar todas las mediciones    |
| POST   | `/mediciones`             | Insertar una nueva medición    |

### 8.4 Siguientes lecturas

- **README.md**: descripción completa de la arquitectura, flujo de datos y estructura del proyecto.
- **logs/lineage/**: informes generados tras ejecutar el auditor.
- **deploy/supabase_deploy.md**: este mismo documento, que puedes consultar siempre que necesites desplegar de nuevo.

### 8.5 Posibles ampliaciones

Este despliegue cubre la capa de datos. Si en el futuro queréis exponer la API en producción, podéis considerar:

- Desplegar la API en [Render](https://render.com), [Railway](https://railway.app) o [Deta](https://deta.sh).
- Configurar un dominio personalizado.
- Añadir autenticación a los endpoints con las políticas de Supabase.

Por ahora, la base de datos está lista para el desarrollo y las pruebas del proyecto Vortex.