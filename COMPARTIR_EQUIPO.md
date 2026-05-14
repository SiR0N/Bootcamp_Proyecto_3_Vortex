# VORTEX - Resumen del Proyecto

## 🏗️ Arquitectura
- **Backend**: FastAPI (puerto 8000)
- **Frontend**: Flask (puerto 5000)
- **Base de datos**: PostgreSQL ( Railway)
- **APIs externas**: AEMET (principal) + OpenWeather (fallback)

## ✅ Funcionalidades Implementadas

### ETL Automático
- Scheduler que ejecuta ETL cada hora
- Extrae datos de AEMET → Transforma → Carga en PostgreSQL
- Endpoint `/zonas/by_estacion` para consulta por estación

### Consultas
- `/consulta`: Lee de PostgreSQL (datos cacheados)
- Fallback automático a OpenWeather si AEMET falla

### Documentación
- `docs/bitacora.md`: Historial cronológico
- `docs/estado_proyecto.md`: Estado actual del proyecto
- `docs/guia_equipo.md`: Guía técnica
- `README.md`: Información general

## 🚀 Cómo ejecutar

### Opción 1 - Terminal
```bash
# Backend
uvicorn api.main:app --reload

# Frontend (otro terminal)
python app.py
```

### Opción 2 - Acceso directo
- Doble clic en `VORTEX.exe` en el escritorio
- Se abre automáticamente en http://localhost:5000

## 🔑 Variables requeridas (.env)
```
DATABASE_URL=postgresql://...
AEMET_API_KEY=...
OPENWEATHER_API_KEY=...
```

## 📊 Endpoints principales
- `GET /consulta?estacion=X` - Consulta meteorological
- `GET /zonas` - Lista de zonas
- `GET /zonas/{id}/mediciones` - Mediciones por zona
- `GET /docs` - Swagger UI (FastAPI)

## 👥 Equipo
- Juan (PM/Tech Lead)
- Helen (Frontend/API)
- Jose (Backend/DB)
- David (ETL/Data)
- Equipo anterior: Adriana, Isabela, Elena