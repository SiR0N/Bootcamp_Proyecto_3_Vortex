# limpia con Pandas
import pandas as pd

def transform_data(raw_data):
    """
    Limpiar, validar y normalizar el conjunto de datos climáticos.

    EN:
    Clean, validate and normalize the climate dataset.
    """
    print("🔧 Iniciando transformación de datos...")

    # convertir a DataFrame para facilitar la manipulación
    df = pd.DataFrame(raw_data)

    print("Columnas detectadas:", df.columns.tolist())
    
    # --- 1. Rename unexpected column 'estacion' to 'station_name' ---
    if "estacion" in df.columns:
        df.rename(columns={"estacion": "station_name"}, inplace=True)
        print("ℹ️ Columna 'estacion' renombrada a 'station_name'.")

    # 1. Limpieza: Quitar filas vacías
    df = df.dropna(how='all')
    print("✅ Filas vacías eliminadas.")

    # 2. Convetir "fecha" a formato datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    print("✅ Campo 'fecha' transformado a formato datetime.")

    # 3. Tipado: Asegurar que los campos numéricos sean números
    numeric_cols = ['temperatura', "humedad", "viento", "lluvia", "presion"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print("✅ Campos numéricos convertidos a tipo numérico.")
    
    # 4. Reemplazar valores nulos en "municipio/ciudad" con "Desconocido"
    df['municipio'] = df['municipio'].fillna("Desconocido")
    df["ciudad"] = df["ciudad"].fillna("Desconocido")
    df["station_name"] = df["station_name"].fillna("Desconocido")

    print("✅ Campos de municipio/ciudad normalizados")

    # 5. Asegurar que "alertas" sea una lista (si no lo es, convertirlo)
    df["alertas"] = df["alertas"].apply(lambda x: x if isinstance(x, list) else [])
    print("✅ Campo 'alertas' validado.")

    # 6. Eliminar duplicados
    before = len(df)
    cols_for_duplicates = [col for col in df.columns if col != "alertas"]
    df = df.drop_duplicates(subset=cols_for_duplicates)
    after = len(df)
    print(f"✅ Duplicados eliminados: {before - after}")
    
    print("🔧 Transformación de datos completada.")
    return df

# --- MANUAL TEST ---
if __name__ == "__main__":
    from extract import extract_data

    data = extract_data("../data/registros_climaticos_normalizados.json")
    df_clean = transform_data(data)

    print(df_clean.head())


    