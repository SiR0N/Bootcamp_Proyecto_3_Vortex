import os
from datetime import datetime as dt

try:
    from services.normalizer import NormalizerService
except ImportError:
    NormalizerService = None


def normalizar_datos_aemet(data, fuente="aemet"):
    """
    Normaliza datos de AEMET para el proyecto VORTEX.

    Args:
        data:   dict o lista con datos crudos de AEMET
        fuente: origen del dato ('aemet' o 'manual')
    Returns:
        dict con datos normalizados listos para la BD
    """
    if NormalizerService is None:
        return {"error": "No se pudo importar NormalizerService"}

    if data is None:
        return {"error": "Datos nulos"}

    # Si llega una lista, procesamos solo el primero
    if isinstance(data, list):
        if len(data) == 0:
            return {"error": "Lista vacía"}
        data = data[0]

    if not isinstance(data, dict):
        return {"error": "Formato de datos inválido"}

    try:
        normalizer = NormalizerService()
        resultado = normalizer.normalizar(data, fuente=fuente)

        def safe_float(valor):
            """Devuelve float o None. Nunca inventa un 0.0."""
            try:
                return float(valor) if valor is not None else None
            except (ValueError, TypeError):
                return None

        return {
            "estacion_id": resultado.get("estacion_id"),
            "fecha":       resultado.get("fecha"),
            "temperatura": safe_float(resultado.get("temperatura")),
            "humedad":     safe_float(resultado.get("humedad")),
            "viento":      safe_float(resultado.get("viento")),
            "presion":     safe_float(resultado.get("presion")),
            "lluvia":      safe_float(resultado.get("lluvia")),
            # fuente siempre en minúsculas para cumplir el CHECK constraint
            "fuente":      str(resultado.get("fuente", fuente)).lower(),
        }

    except Exception as e:
        return {"error": str(e)}