# limpia con Pandas
import pandas as pd

def transformar_datos(datos_crudos):
    df = pd.DataFrame(datos_crudos)
    
    # 1. Limpieza: Quitar filas vacías
    df = df.dropna()
    
    # 2. Tipado: Asegurar que la temperatura sea número
    df['temperatura'] = pd.to_numeric(df['temperatura'], errors='coerce')
    
    return df