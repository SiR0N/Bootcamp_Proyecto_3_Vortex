import json
import os
from datetime import datetime as dt

try:
    from services.normalizer import NormalizerService
except ImportError:
    NormalizerService = None

try:
    from services import alert_service
    from services.alert_service import AlertService
except ImportError:
    alert_service = None
    AlertService = None


def normalizar_datos_aemet(data):
    """
    Normaliza datos de AEMET para el proyecto VORTEX.
    
    Args:
        data: dict o lista con datos crudos de AEMET
    Returns:
        dict con datos normalizados en formato compatible con el proyecto
    """
    if NormalizerService is None:
        return {"error": "No se pudo importar NormalizerService"}

    if data is None:
        return {"error": "Datos nulos"}

    if isinstance(data, list):
        if len(data) == 0:
            return {"error": "Lista vacía"}
        data = data[0]

    if not isinstance(data, dict):
        return {"error": "Formato de datos inválido"}

    try:
        normalizer = NormalizerService()
        resultado = normalizer.normalizar(data, fuente="aemet")

        estacion_raw = resultado.get("ciudad") or resultado.get("estacion") or resultado.get("ubi")
        estacion = estacion_raw if estacion_raw else "Ubicación Desconocida"

        fecha_raw = resultado.get("fecha")
        if fecha_raw:
            if "T" in str(fecha_raw):
                fecha_formato = str(fecha_raw).replace("T", " ")
            else:
                fecha_formato = str(fecha_raw)
        else:
            fecha_formato = "N/A"

        def safe_float(valor, default=0.0):
            try:
                return float(valor) if valor is not None else default
            except (ValueError, TypeError):
                return default

        resultado_final = {
            "estacion": estacion,
            "fecha": fecha_formato,
            "temperatura": safe_float(resultado.get("temperatura")),
            "humedad": safe_float(resultado.get("humedad")),
            "viento": safe_float(resultado.get("viento")),
            "presion": safe_float(resultado.get("presion")),
            "lluvia": safe_float(resultado.get("lluvia")),
            "alertas": []
        }

        if alert_service and hasattr(alert_service, 'evaluar_alertas'):
            try:
                string_alerts = alert_service.evaluar_alertas(resultado_final)
                resultado_final["alertas"] = string_alerts
            except Exception:
                pass

        return resultado_final

    except Exception as e:
        return {"error": str(e)}

