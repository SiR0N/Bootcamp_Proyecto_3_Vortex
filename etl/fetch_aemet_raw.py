import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv

# Ruta absoluta a la raíz del proyecto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Añadir la raíz al PYTHONPATH
sys.path.append(ROOT_DIR)

# Cargar el .env desde la raíz del proyecto
load_dotenv(os.path.join(ROOT_DIR, ".env"))

from services.weather_api_service import WeatherAPIService


def fetch_and_save_raw_data():
    """
    Obtiene datos crudos de AEMET usando WeatherAPIService
    y los guarda en /data/raw/aemet_raw_YYYYMMDD.json

    EN:    
    Fetch raw weather data from AEMET using WeatherAPIService
    and save it into /data/raw/aemet_raw_YYYYMMDD.json
    """

    print("📡 Obteniendo datos crudos desde AEMET...")

    # 1. Llamar al servicio original del proyecto
    service = WeatherAPIService()
    raw_data = service._obtener_datos_crudos()

    if not raw_data:
        print("⚠️ No se recibieron datos crudos de AEMET.")
        return None

    # 2. Crear carpeta /data/raw si no existe
    raw_dir = os.path.join("data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    # 3. Crear nombre de archivo con fecha
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join(raw_dir, f"aemet_raw_{date_str}.json")

    # 4. Guardar datos crudos
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Datos crudos guardados en: {file_path}")
    print(f"📊 Registros descargados: {len(raw_data)}")

    return file_path


if __name__ == "__main__":
    fetch_and_save_raw_data()