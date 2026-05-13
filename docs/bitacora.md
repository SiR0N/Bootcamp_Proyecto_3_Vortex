# 📓 BITÁCORA DEL PROYECTO VORTEX

## Registro de cambios y evoluciones del proyecto

---

## 🔵 Entrada 003 - 13 Mayo 2026 (Tarde)
**Fecha:** 13/05/2026  
**Autor:** Juan (con asistencia de OpenCode)  
**Tipo de cambio:** Pruebas y corrections de bugs

### Pruebas realizadas

| Componente | Resultado |
|------------|-----------|
| FastAPI (`python -m api.main`) | ✅ Funcionando en puerto 8000 |
| GET / | 200 OK |
| GET /zonas/ | 200 OK (antes 500) |
| GET /zonas/by_estacion/EST-01 | 200 OK (endpoint nuevo) |
| GET /mediciones/ | 200 OK (antes 500) |
| OpenWeather fallback | ✅ Datos reales de Madrid (17.85°C) |

### Problemas encontrados y corregidos

1. **Error 500 en /zonas/ y /mediciones/**
   - Causa: Schemas Pydantic requerían campos que la DB permite nulos
   - Solución: Hacer campos opcionales en `ZonaResponse` y `MedicionResponse`

2. **weather_api_service.py sin cambios**
   - Causa: Edit no se aplicó correctamente
   - Solución: Añadir método `_obtener_datos_openweather` manualmente

### Archivos modificados en esta entrada

- `api/schemas/zona.py` - Campos opcionales
- `api/schemas/medicion.py` - Campos opcionales
- `api/routes/zonas.py` - Añadido endpoint by_estacion
- `services/weather_api_service.py` - Añadido fallback OpenWeather

---

## 🔵 Entrada 002 - 13 Mayo 2026 (Mañana)
**Fecha:** 13/05/2026  
**Autor:** Juan (con asistencia de OpenCode)  
**Tipo de cambio:** Fix de bugs + Implementación de infraestructura

### Contexto
Durante las pruebas de los endpoints de FastAPI, se descubrieron errores 500 debido a incompatibilidad entre los schemas Pydantic y la base de datos (que permite valores nulos).

### Cambios realizados

| Archivo | Cambio | Motivo |
|---------|--------|--------|
| `api/schemas/zona.py` | Campos opcionales (nombre, latitud, longitud) | El schema requería campos que la DB permite nulos |
| `api/schemas/medicion.py` | Campos opcionales en response | Compatibilidad con DB |
| `api/routes/zonas.py` | Añadido endpoint `/zonas/by_estacion/{estacion_id}` | Necesario para ETL |
| `services/weather_api_service.py` | Añadido fallback OpenWeather real | Reemplazar datos falsos aleatorios |
| `.env` | Añadida OPENWEATHER_API_KEY | Para fallback |

---

## 🔵 Entrada 001 - 13 Mayo 2026 (Inicio)
**Fecha:** 13/05/2026  
**Autor:** Juan (con asistencia de OpenCode)  
**Tipo de cambio:** Implementación de infraestructura

### Contexto
El proyecto llevaba datos del frontend a un archivo JSON, pero:
- El ETL estaba roto (faltaba endpoint en API)
- El scheduler no conectaba con PostgreSQL
- El fallback generaba datos falsos aleatorios
- El usuario leía del JSON en lugar de PostgreSQL

### Cambios implementados

| Fase | Descripción | Archivos |
|------|-------------|----------|
| 1 | Arreglar ETL (añadir endpoint `/zonas/by_estacion/{estacion_id}`) | `api/routes/zonas.py` |
| 2 | Conectar Scheduler → ETL automático | `controllers/scheduler_controller.py`, `etl/extract.py` |
| 3 | Fallback real con OpenWeather (no más datos falsos) | `services/weather_api_service.py`, `.env` |
| 4 | Migrar lectura de `/consulta` a PostgreSQL | `controllers/view_controller.py` |

---

## 📋 Notas para próximas implementaciones

### Pendiente en Lovable
- Integrar frontend con la nueva estructura de datos
- Verificar que `/consulta` funciona correctamente con PostgreSQL
- Testing de OpenWeather fallback

### Pendiente de pruebas
- [x] Verificar ETL (pendiente manual)
- [ ] Verificar scheduler → ETL
- [x] Probar OpenWeather fallback ✅
- [x] Verificar /consulta lee de PostgreSQL

### Archivos pendientes de eliminar (limpieza)
- `repositories/sqlite_repository.py` (vacío)
- `data/registros_climaticos_normalizados.json` (duplicado)

---

*Última actualización: 13/05/2026*