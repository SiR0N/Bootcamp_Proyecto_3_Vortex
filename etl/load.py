import os
import sys
import requests
from datetime import datetime


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

API_URL = os.getenv("VORTEX_API_URL", "http://localhost:8000")
FUENTES_VALIDAS = {"aemet", "manual", "openweather"}


# -----------------------------
#  ZONAS
# -----------------------------
def crear_o_obtener_zona(datos_zona):
    """Crea una zona o devuelve su ID si ya existe."""
    response = requests.post(f"{API_URL}/zonas/", json=datos_zona, timeout=10)

    if response.status_code == 201:
        print(f"✔ Zona creada: {datos_zona['estacion_id']}")
        return response.json()["id"]

    if response.status_code == 409:
        print(f"ℹ Zona ya existente: {datos_zona['estacion_id']}")
        r = requests.get(
            f"{API_URL}/zonas/by_estacion/{datos_zona['estacion_id']}",
            timeout=10,
        )
        if r.status_code == 200:
            return r.json()["id"]

    print(f"❌ Error creando zona: {response.status_code} - {response.text}")
    return None


# -----------------------------
#  MEDICIONES
# -----------------------------
def subir_mediciones(lista_mediciones):
    """Envía mediciones a la API una por una."""
    for medicion in lista_mediciones:
        response = requests.post(f"{API_URL}/mediciones/", json=medicion, timeout=10)

        if response.status_code == 201:
            print(f"✔ Medición subida: {medicion['fecha']}")
        else:
            print(f"❌ Error subiendo medición: {response.status_code} - {response.text}")



# -----------------------------
#  LOAD PRINCIPAL DEL ETL
# -----------------------------
def load_data(df):
    """
    Load final del ETL: envía zonas y mediciones a la API.
    No toca la base de datos directamente.
    """
    print("📡 Enviando datos a la API...")

    inserted = 0

    for _, row in df.iterrows():
        data = row.to_dict()

        estacion_id = data.get("estacion_id")

        # Validación básica
        if not estacion_id or str(estacion_id).lower() == "nan":
            print("[WARN] estacion_id inválido, omitiendo registro")
            continue

        # Crear/obtener zona
        zona_payload = {
            "estacion_id": str(estacion_id),
            "nombre": data.get("nombre") or data.get("ciudad") or "Desconocido",
            "latitud": data.get("latitud") or 0.0,
            "longitud": data.get("longitud") or 0.0,
        }

        zona_id = crear_o_obtener_zona(zona_payload)
        if not zona_id:
            continue

        # Normalizar fuente (siempre minúsculas para cumplir CHECK constraint)
        fuente = str(data.get("fuente", "manual")).lower()
        if fuente not in FUENTES_VALIDAS:
            fuente = "manual"

        # Normalizar fecha a ISO 8601
        fecha_val = data.get("fecha")
        if isinstance(fecha_val, datetime):
            fecha_iso = fecha_val.isoformat()
        elif hasattr(fecha_val, "isoformat"):  # pd.Timestamp
            fecha_iso = fecha_val.isoformat()
        else:
            fecha_iso = str(fecha_val) if fecha_val else datetime.utcnow().isoformat()

        # Crear medición
        medicion_payload = {
            "zona_id": zona_id,
            "fecha": fecha_iso,
            "temperatura": data.get("temperatura"),
            "humedad": data.get("humedad"),
            "viento": data.get("viento"),
            "lluvia": data.get("lluvia"),
            "presion": data.get("presion"),
            "fuente": fuente,
        }

        response = requests.post(f"{API_URL}/mediciones/", json=medicion_payload, timeout=10)

        if response.status_code == 201:
            inserted += 1
        else:
            print(f"❌ Error insertando medición: {response.status_code} - {response.text}")

    print(f"📦 Inserción completada. Total insertado: {inserted}")
    return inserted


# -----------------------------
#  TEST MANUAL
# -----------------------------
if __name__ == "__main__":
    import pandas as pd
    from datetime import datetime
    import random
    import string

    print("🔧 Test manual de load.py")

    def generar_estacion_id():
        return "EST-test-" + "".join(random.choices(string.digits, k=2))

    df_test = pd.DataFrame([
        {
            "estacion_id": generar_estacion_id(),
            "fecha": datetime.now(),
            "temperatura": 10,
            "humedad": 50,
            "viento": 2,
            "lluvia": 0,
            "presion": 1012,
            "fuente": "manual",
        }
    ])

    load_data(df_test)