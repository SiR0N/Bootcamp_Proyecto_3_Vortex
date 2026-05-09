# leemos JSON
import json
import os # Esto sirve para que el código buscar localizar el archivo .py donde sea que esté

def extract_data(relative_path):
    current_dir = os.path.dirname(__file__) # Esto busca la carpeta donde está este script (extract.py)
    full_path = os.path.join(current_dir, relative_path) # ruta absoluta al archivo JSON

    try:
        with open(full_path, 'r', encoding="utf-8") as file: # lee el archivo JSON
            data = json.load(file) # convierte el JSON en lenguaje Python (lista de diccionarios)
            print("✅ Extracción exitosa") 
            return data # devuelve los datos para que puedan ser usados por otros scripts
    except Exception as e: # si ocurre un error, lo captura y muestra un mensaje (e)
        print(f"❌ Error al leer el archivo: {e}")
        return None
    
# --- ESTO ES PARA PROBAR MANUALMENTE QUE FUNCIONA ---
if __name__ == "__main__":
    path = "../data/registros_climaticos_normalizados.json" # El '..' significa 'sal de la carpeta etl y busca fuera'
    data = extract_data(path)
    
    if data:
        print(f"He encontrado {len(data)} registros.")
        print(f"El primer registro es de: {data[0]['estacion_id']}") # la variable "estacion_id" queda pendiente de denominar

        