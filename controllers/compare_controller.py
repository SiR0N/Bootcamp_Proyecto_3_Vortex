from datetime import datetime
from services.weather_api_service import obtener_clima_por_coordenadas
from services.normalizer import get_normalizer_service

def calculate_diff(v1, v2):
    try:
        return round(abs(float(v1 or 0) - float(v2 or 0)), 2)
    except:
        return 0

def get_comparison_data(municipio, manual_data):
    """
    Recibe los datos manuales del usuario y compara con AEMET actual.
    """
    normalizer = get_normalizer_service()
    
    # Obtener dato actual de AEMET
    # Usamos coordenadas por defecto de Madrid (esto debería venir del municipio)
    aemet_data = None
    try:
        raw_aemet = obtener_clima_por_coordenadas(40.4167, -3.7033)
        if raw_aemet:
            aemet_data = normalizer.normalizar(raw_aemet, fuente="aemet")
    except:
        pass
    
    # Calcular diferencias
    diffs = {}
    if aemet_data:
        diffs = {
            "temperatura": calculate_diff(manual_data.get("temperatura"), aemet_data.get("temperatura")),
            "humedad": calculate_diff(manual_data.get("humedad"), aemet_data.get("humedad")),
            "viento": calculate_diff(manual_data.get("viento"), aemet_data.get("viento")),
            "lluvia": calculate_diff(manual_data.get("lluvia"), aemet_data.get("lluvia"))
        }
    else:
        diffs = {"temperatura": 0, "humedad": 0, "viento": 0, "lluvia": 0}
    
    return {
        "success": True,
        "municipio": municipio,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "manual": manual_data,
        "aemet": aemet_data or {},
        "diferencias": diffs,
        "hay_discrepancia": (
            diffs["temperatura"] > 3 or
            diffs["humedad"] > 10 or
            diffs["viento"] > 10 or
            diffs["lluvia"] > 5
        )
    }


def get_aemet_current(municipio="Madrid"):
    """
    Obtiene solo el dato actual de AEMET para mostrar en pantalla.
    """
    normalizer = get_normalizer_service()
    try:
        raw = obtener_clima_por_coordenadas(40.4167, -3.7033)
        if raw:
            return normalizer.normalizar(raw, fuente="aemet")
    except:
        pass
    return None