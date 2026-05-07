# leemos JSON
import json
import os # Esto sirve para que el código buscar localizar el archivo .py donde sea que esté

def extraer_datos(ruta_archivo):
    directorio_actual = os.path.dirname(__file__) # Esto busca la carpeta donde está este script (extract.py)
    ruta_completa = os.path.join(directorio_actual, ruta_archivo) # ruta absoluta al archivo JSON

    try:
        with open(ruta_completa, 'r') as file: # lee el archivo JSON
            datos = json.load(file) # convierte el JSON en lenguaje Python (lista de diccionarios)
            print("✅ Extracción exitosa") 
            return datos # devuelve los datos para que puedan ser usados por otros scripts
    except Exception as e: # si ocurre un error, lo captura y muestra un mensaje (e)
        print(f"❌ Error al leer el archivo: {e}")

# --- ESTO ES PARA PROBAR QUE FUNCIONA ---
if __name__ == "__main__":
    ruta = "../data/registros_climaticos.json" # El '..' significa 'sal de la carpeta etl y busca fuera'
    mis_datos = extraer_datos(ruta)
    
    if mis_datos:
        print(f"He encontrado {len(mis_datos)} registros.")
        print(f"El primer registro es de: {mis_datos[0]['estacion_id']}") # la variable "estacion_id" queda pendiente de denominar

        