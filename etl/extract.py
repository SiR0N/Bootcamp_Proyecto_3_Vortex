# lee JSON
import json

def extraer_datos(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as file:
            datos = json.load(file)
            print("✅ Extracción exitosa")
            return datos
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")