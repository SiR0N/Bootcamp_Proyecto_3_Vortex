from flask import Blueprint, request, jsonify
from models.registro_climatico import RegistroClimatico
from repositories.json_repository import JSONRepository
from services.normalizer import get_normalizer_service
import json

manual_bp = Blueprint('manual', __name__)

# Instancias globales
repo = JSONRepository('data/registros_climaticos.json')
normalizer = get_normalizer_service()

@manual_bp.route('/api/registrar', methods=['POST'])
def registrar_datos_manuales():
    """
    Recibe datos JSON, los valida, los guarda y evalúa alertas climáticas.
    """
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

        # 1. Crear el objeto de registro (Persona 2)
        nuevo_registro = RegistroClimatico(
            datos.get("estacion_id"),
            datos.get("fecha"),
            float(datos.get("temperatura", 0)),
            float(datos.get("humedad", 0)),
            float(datos.get("viento", 0)),
            float(datos.get("lluvia", 0))
        )

        # 2. Preparar el diccionario final
        registro_dict = nuevo_registro.to_dict()
        registro_dict["municipio"] = datos.get("municipio", "Desconocido")
        registro_dict["fuente"] = "manual"

        # 3. NORMALIZAR con VORTEX (incluye alertas AEMET)
        registro_normalizado = normalizer.normalizar(registro_dict, fuente="manual")
        lista_alertas = registro_normalizado.get("alertas", [])

        # 4. Guardar en el JSON de datos (el registro ya normalizado)
        exito = repo.guardar(registro_normalizado)

        if exito:
            # Devolver respuesta completa con todos los campos normalizados
            return jsonify({
                "status": "success",
                "message": "Registro guardado con éxito",
                "estacion_id": registro_normalizado.get("estacion_id"),
                "temperatura": registro_normalizado.get("temperatura"),
                "humedad": registro_normalizado.get("humedad"),
                "viento": registro_normalizado.get("viento"),
                "lluvia": registro_normalizado.get("lluvia"),
                "ciudad": registro_normalizado.get("ciudad") or registro_normalizado.get("municipio"),
                "municipio": registro_normalizado.get("municipio"),
                "fecha": registro_normalizado.get("fecha"),
                "fuente": registro_normalizado.get("fuente"),
                "alertas": lista_alertas
            }), 201
        
        return jsonify({"status": "error", "message": "Error al escribir en el repositorio"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error interno: {str(e)}"}), 500