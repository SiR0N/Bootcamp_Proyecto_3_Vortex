# 📓 BITÁCORA DEL PROYECTO VORTEX

## Registro cronológico de cambios y evoluciones

---

## 🔵 ENTRADA 013 - 13 Mayo 2026 (FINAL)
**Fecha:** 13/05/2026  
**Rama:** `feat/implementations` → PR a `main`  
**Estado:** ✅ IMPLEMENTACIONES COMPLETAS - PR EN REVISIÓN

### Cambios implementados

| # | Cambio | Archivo | Descripción |
|---|--------|---------|--------------|
| 1 | **Scheduler → ETL automático** | `scheduler_controller.py` | Cada 2h ejecuta ETL automáticamente |
| 2 | **Fallback OpenWeather** | `weather_api_service.py` | Datos reales si AEMET falla |
| 3 | **Consulta desde PostgreSQL** | `view_controller.py` | /consulta lee de DB via FastAPI |
| 4 | **Endpoint ETL** | `api/routes/zonas.py` | `/zonas/by_estacion/{estacion_id}` |
| 5 | **Merge PR #63 Beth** | `api/schemas/*.py` | Normalizers y validators |

### Pruebas realizadas

- FastAPI: http://localhost:8000 ✅
- Flask: http://localhost:5000 ✅
- GET /zonas/ → 200 OK (8 zonas)
- GET /mediciones/ → 200 OK (100 mediciones)
- /api/clima → 200 OK (Madrid, 18.2°C)

### Archivos relevantes en docs
- `bitacora.md` (esta)
- `estado_actual.md`
- `hoja_ruta.md`
- `guia_equipo.md`
- `informe_proyecto.md`

---

## 🔵 ENTRADA 012 - 13 Mayo 2026 (Tarde)
**Fecha:** 13/05/2026  
**Rama:** `feat/implementations`  
**Estado:** PR #63 mergeado a main + fix de conflicts

### Merge PR #63 (Elizabeth - fix/normalizer)
- Resolución de conflictos en schemas
- Código de Beth integrado: validators, normalización, campos opcionales

---

## 🔵 ENTRADA 011 - 12 Mayo 2026
**Fecha:** 12/05/2026  
**Rama:** `main`  
**Estado:** PR #62 Merge - Pipeline Log

### Cambios
- `etl/pipeline_log.py` añadido
- Auditoría pasiva del ETL

---

## 🔵 ENTRADA 010 - 11 Mayo 2026
**Fecha:** 11/05/2026  
**Rama:** `main`  
**Estado:** PR #60 Merge - Test Refactor

### Cambios
- Suite de tests refactorizada
- Mejoras en coverage

---

## 🔵 ENTRADA 009 - 10 Mayo 2026
**Fecha:** 10/05/2026  
**Rama:** `main`  
**Estado:** PR #58 Merge - ETL Load

### Cambios
- `etl/load.py` refactorizado
- Normalización de fuente (manual/aemet)

---

## 🔵 ENTRADA 008 - 9 Mayo 2026
**Fecha:** 09/05/2026  
**Rama:** `main`  
**Estado:** PR #56 Merge - README completo

### Cambios
- README.md completo creado
- Logo del proyecto
- Estructura de carpetas documentada
- Guía de instalación

---

## 🔵 ENTRADA 007 - 8 Mayo 2026
**Fecha:** 08/05/2026  
**Rama:** `main`  
**Estado:** PR #55 Merge - Scheduler

### Cambios
- Fix en scheduler: fuente value coincide con Pydantic schema

---

## 🔵 ENTRADA 006 - 7 Mayo 2026
**Fecha:** 07/05/2026  
**Rama:** `main`  
**Estado:** PR #54 Merge - Fix title

### Cambios
- Título cambiado a "VORTEX API"

---

## 🔵 ENTRADA 005 - 6 Mayo 2026
**Fecha:** 06/05/2026  
**Rama:** `main`  
**Estado:** PR #52 - Schemas Refactor

### Cambios
- Pydantic validations en MedicionBase
- Validaciones de longitud en zona.py

---

## 🔵 ENTRADA 004 - 5 Mayo 2026
**Fecha:** 05/05/2026  
**Rama:** `main`  
**Estado:** PR #51 - ETL Load

### Cambios
- Refactor de load.py
- Conexión con Vortex API

---

## 🔵 ENTRADA 003 - 4 Mayo 2026
**Fecha:** 04/05/2026  
**Rama:** `main`  
**Estado:** PR #49 - Sync Init DB

### Cambios
- Sincronización de init_db con modelos
- Fix en imports

---

## 🔵 ENTRADA 002 - 3 Mayo 2026
**Fecha:** 03/05/2026  
**Rama:** `main`  
**Estado:** README básico

### Cambios
- README.md básico creado
- Descripción del proyecto
- Estructura de carpetas

---

## 🔵 ENTRADA 001 - Inicio del proyecto
**Fecha:** Abril 2026  
**Rama:** `main` (inicio)  
**Estado:** Creación del proyecto

### Origen del proyecto
- Inicio como proyecto Weather API (frontend Flask)
- Evolución a VORTEX con FastAPI + PostgreSQL
- Integración con API AEMET
- Pipeline ETL con Pandas

---

## 📋 GLOSARIO DE RAMAS

| Rama | Descripción |
|------|-------------|
| `main` | Rama estable/producción |
| `feat/implementations` | Nuevas implementaciones (esta) |
| `fix/normalizer` | PR #63 - Normalizers de Beth |
| `feature/etl-load` | PR #58 - Carga ETL |
| `docs/readme` | Documentación README |

---

## 📋 PRs IMPORTANTES MERGEADOS

| #PR | Rama | Descripción | Fecha |
|-----|------|-------------|-------|
| #63 | fix/normalizer | Normalizers y validators | 13/05 |
| #62 | feature/pipeline-log | Pipeline Log | 12/05 |
| #60 | refactor/test | Tests | 11/05 |
| #58 | feature/etl-load | ETL Load | 10/05 |
| #56 | docs/readme | README completo | 09/05 |
| #55 | refactor/scheduler | Scheduler fix | 08/05 |
| #54 | fix/vortex-api-title | Título API | 07/05 |

---

*Última actualización: 13/05/2026*
*Bitácora coherente - Desde el inicio del proyecto*