# orquestador
import time
from extract import extract_data
from transform import transform_data
from load import load_data


def run_pipeline():
    """
    Orchestrates the full ETL pipeline: extract → transform → load.
    """
    print("🚀 Iniciando pipeline ETL...")
    start_time = time.time()

    # --- 1. Extract ---
    print("\n📥 [1/3] Extrayendo datos...")
    try:
        raw_data = extract_data("../data/registros_climaticos_normalizados.json")
    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")
        return

    if not raw_data:
        print("❌ No se encontraron datos para extraer. Pipeline detenido.")
        return

    print(f"✔ Datos extraídos: {len(raw_data)} registros.")

    # --- 2. Transform ---
    print("\n🧹 [2/3] Transformando datos...")
    try:
        df_clean = transform_data(raw_data)
    except Exception as e:
        print(f"❌ Error durante la transformación: {e}")
        return

    if df_clean.empty:
        print("❌ La transformación produjo un DataFrame vacío. Pipeline detenido.")
        return

    print(f"✔ Datos transformados: {len(df_clean)} registros limpios.")

    # --- 3. Load ---
    print("\n📤 [3/3] Cargando datos en la base de datos...")
    try:
        inserted_rows = load_data(df_clean)
    except Exception as e:
        print(f"❌ Error durante la carga: {e}")
        inserted_rows = 0

    print(f"✔ Filas insertadas en la base de datos: {inserted_rows}")

    # --- Summary ---
    total_time = round(time.time() - start_time, 2)
    print(f"\n🎉 Pipeline completado en {total_time} segundos.")
    print("--------------------------------------------------")
    print("Resumen del pipeline:")
    print(f"  - Registros extraídos: {len(raw_data)}")
    print(f"  - Registros transformados: {len(df_clean)}")
    print(f"  - Registros cargados: {inserted_rows}")
    print("--------------------------------------------------")


if __name__ == "__main__":
    run_pipeline()