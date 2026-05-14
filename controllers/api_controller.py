import json
import os
import requests
from flask import Blueprint, jsonify, request
from services.weather_api_service import obtener_clima_por_coordenadas
from services.normalizer import get_normalizer_service
from repositories.json_repository import guardar_registro

api_bp = Blueprint('api', __name__)

FASTAPI_URL = "http://localhost:8000"

@api_bp.route("/api/config/fallback")
def api_config_fallback():
    """Devuelve la configuración de ubicaciones para el fallback"""
    try:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config", "ubicaciones.json"
        )
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Devolver solo las ubicaciones necesarias para el frontend
        ubicaciones = []
        for region_name, region_data in config.get("regiones", {}).items():
            if "ubicaciones" in region_data:
                for ubi in region_data["ubicaciones"]:
                    ubicaciones.append({
                        "nombre": ubi.get("nombre"),
                        "lat": ubi.get("lat"),
                        "lon": ubi.get("lon")
                    })

        return jsonify({
            "ubicaciones": ubicaciones,
            "fallback_order": config.get("fallback_orden", [])
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/api/clima")
def api_clima():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Faltan coordenadas"}), 400

    try:
        raw_data = obtener_clima_por_coordenadas(lat, lon)

        if not raw_data:
            return jsonify({
                "error": "No se pudieron obtener datos de ninguna fuente",
                "temperatura": None,
                "humedad": None,
                "ciudad": "Sin datos",
                "fuente": "ninguna",
                "_fallback": True
            }), 503

        # Detectar fuente real y stale ANTES de normalizar
        fuente_real = raw_data.get('fuente', 'aemet')
        es_fallback = raw_data.get('_fallback', False)
        es_stale = raw_data.get('_stale', False)
        horas_sin_actualizar = raw_data.get('_horas_sin_actualizar', 0)

        # Usar el normalizador VORTEX
        normalizer = get_normalizer_service()
        data = normalizer.normalizar(raw_data, fuente=fuente_real)

        # Mantenemos tu lógica de seguridad para la ciudad
        if 'ciudad' not in data or not data['ciudad']:
            data['ciudad'] = data.get('municipio', 'Ubicación Detectada')

        # IMPORTANTE: Usar la fuente REAL detectada (no sobreescribir)
        data['fuente'] = fuente_real
        data['_fallback'] = es_fallback
        data['_stale'] = es_stale
        data['_horas_sin_actualizar'] = horas_sin_actualizar

        # Llamamos a tu repositorio JSON
        guardar_registro(data)

        # 2. Guardar en PostgreSQL via FastAPI
        try:
            zona_payload = {
                "estacion_id": data.get("estacion_id", "DESCONOCIDO"),
                "nombre": data.get("ciudad", data.get("municipio", "Desconocido")),
                "latitud": float(data.get("lat", data.get("latitud", 0))) or 0.0,
                "longitud": float(data.get("lon", data.get("longitud", 0))) or 0.0
            }
            r_zona = requests.post(f"{FASTAPI_URL}/zonas/", json=zona_payload, timeout=5)
            if r_zona.status_code == 201:
                zona_id = r_zona.json()["id"]
            elif r_zona.status_code == 400:
                r_zona2 = requests.get(f"{FASTAPI_URL}/zonas/by_estacion/{zona_payload['estacion_id']}", timeout=5)
                zona_id = r_zona2.json().get("id") if r_zona2.status_code == 200 else None
            else:
                zona_id = None

            if zona_id:
                med_payload = {
                    "zona_id": zona_id,
                    "fecha": data.get("fecha", ""),
                    "temperatura": data.get("temperatura", 0),
                    "humedad": data.get("humedad", 0),
                    "viento": data.get("viento", 0),
                    "lluvia": data.get("lluvia", 0),
                    "presion": data.get("presion", 0),
                    "fuente": data.get("fuente", "aemet").lower()
                }
                requests.post(f"{FASTAPI_URL}/mediciones/", json=med_payload, timeout=5)
        except Exception:
            pass

        return jsonify(data), 200

    except Exception as e:
        print(f"Error en api_controller: {e}")
        return jsonify({
            "error": str(e),
            "temperatura": 0,
            "ciudad": "Error de conexión",
            "humedad": 0
        }), 500