import pandas as pd

def transform_data(raw_data):
    """
    Limpiar, validar y normalizar el conjunto de datos climáticos.

    Modelo simple: Zonas + Mediciones
    - Campos en BD: zona_id, fecha, temperatura, humedad, viento, lluvia, presion, fuente
    """
    print("🔧 Iniciando transformación de datos...")

    df = pd.DataFrame(raw_data)
    print("Columnas detectadas:", df.columns.tolist())

    df = df.dropna(how='all')
    print("✅ Filas vacías eliminadas.")

    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        print("✅ Campo 'fecha' transformado a formato datetime.")

    numeric_cols = ['temperatura', 'humedad', 'viento', 'lluvia', 'presion']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    print("✅ Campos numéricos convertidos a tipo numérico.")

    df = df.drop(columns=['municipio', 'ciudad', 'alertas', 'station_name', 'estacion'], errors='ignore')
    print("🗑️ Columnas irrelevantes eliminadas.")

    if 'zona_id' not in df.columns and 'estacion_id' in df.columns:
        df = df.rename(columns={'estacion_id': 'zona_id'})

    df = df.drop_duplicates()
    before = len(df)
    after = len(df)
    print(f"✅ Duplicados eliminados: {before - after}")

    print("🔧 Transformación de datos completada.")
    print("Columnas finales:", df.columns.tolist())
    return df


if __name__ == "__main__":
    from extract import extract_data

    data = extract_data("../data/registros_climaticos_normalizados.json")
    df_clean = transform_data(data)
    print(df_clean.head())