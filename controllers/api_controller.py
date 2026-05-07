from flask import Blueprint, jsonify, request
import json
import os
from services.weather_api_service import obtener_clima_por_coordenadas
from services.normalizer import get_normalizer_service
from repositories.json_repository import guardar_registro 

api_bp = Blueprint('api', __name__)

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
            return jsonify({"error": "No se pudieron obtener datos de AEMET", "fallback": True}), 503

        # Usar el nuevo normalizador VORTEX
        normalizer = get_normalizer_service()
        data = normalizer.normalizar(raw_data, fuente="aemet")

        # Mantenemos tu lógica de seguridad para la ciudad
        if 'ciudad' not in data or not data['ciudad']:
            data['ciudad'] = data.get('municipio', 'Ubicación Detectada')

        # Añadimos la fuente para que tus filtros (manual/aemet) funcionen después
        data['fuente'] = 'aemet'

        # Llamamos a tu repositorio JSON
        guardar_registro(data) 

        return jsonify(data), 200

    except Exception as e:
        print(f"Error en api_controller: {e}")
        return jsonify({
            "error": str(e),
            "temperatura": 0,
            "ciudad": "Error de conexión",
            "humedad": 0
        }), 500