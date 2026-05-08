# leemos JSON
import json
import os # Esto sirve para que el código buscar localizar el archivo .py donde sea que esté

RAW_DIR = os.path.join("data", "raw")

def _list_raw_files():
    """
    Devuelve una lista de archivos RAW disponibles en /data/raw/
    
    EN:
    Return a list of available RAW files inside /data/raw/
    """
    if not os.path.exists(RAW_DIR):
        return []

    return [
        f for f in os.listdir(RAW_DIR)
        if f.startswith("aemet_raw_") and f.endswith(".json")
    ]

def _latest_raw_file():
    """
    Detecta automáticamente el archivo RAW más reciente.
    """
    files = _list_raw_files()

    if not files:
        print("⚠️ No hay archivos RAW en /data/raw/. Ejecuta primero fetch_aemet_raw.py")
        return None

    # Ordenar por fecha dentro del nombre del archivo (descendente)
    files.sort(reverse=True)

    return os.path.join(RAW_DIR, files[0])

def extract_data(raw_file=None):
    """
    Extrae datos crudos desde un archivo RAW.
    Si no se especifica archivo, usa el más reciente.

    EN:
    Extract raw data from a RAW JSON file.
    If no file is provided, the most recent RAW file is used.
    """

    # 1. Determinar qué archivo usar
    if raw_file is None:
        raw_file = _latest_raw_file()

    if raw_file is None or not os.path.exists(raw_file):
        print(f"❌ No se encontró el archivo RAW: {raw_file}")
        return None

    print(f"📥 Leyendo datos crudos desde: {raw_file}")

    # 2. Leer el archivo JSON
    try:
        with open(raw_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"✅ Extracción completada. Registros encontrados: {len(data)}")
        return data

    except Exception as e:
        print(f"❌ Error leyendo el archivo RAW: {e}")
        return None


# --- PRUEBA MANUAL ---
if __name__ == "__main__":
    data = extract_data()
    if data:
        print(f"Primer registro:\n{data[0]}")
        print(f"He encontrado {len(data)} registros.")
        
