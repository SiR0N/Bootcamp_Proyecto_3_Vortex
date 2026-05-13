"""
Normalizer Service - VORTEX EVOLUCIÓN
====================================
Normalizador automático que usa umbrales oficiales de AEMET.
Se integra en el flujo de la aplicación (no manual).
"""

import json
import os
import logging
from datetime import datetime
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)

# Mapeo de campos de AEMET a nombres estándar
AEMET_FIELD_MAP = {
    "ta": "temperatura",      # Temperatura actual
    "tamax": "temperatura_max",
    "tamin": "temperatura_min",
    "hr": "humedad",          # Humedad relativa
    "vv": "viento",           # Velocidad del viento
    "vmax": "viento_max",     # Ráfaga máxima
    "dv": "direccion_viento", # Dirección del viento (degrees)
    "prec": "lluvia",         # Precipitación
    "pres": "presion",        # Presión atmosférica
    "pres_nmar": "presion_nivel_mar",
    "ubi": "ciudad",          # Ubicación/Nombre estación
    "idema": "estacion_id",   # ID estación AEMET
    "fint": "fecha",          # Fecha/hora información
    "lat": "lat",
    "lon": "lon",
    "alt": "altitud",
    "tpr": "punto_rocio",     # Temperatura punto rocío
    "rviento": "racha_viento" # Racha de viento
}

# Importar validadores existentes del proyecto
try:
    from utils.validators import (
        validar_temperatura,
        validar_humedad,
        validar_viento,
        validar_lluvia,
        validar_fecha,
        validate_weather_data
    )
    USAR_VALIDADORES_PROYECTO = True
except ImportError:
    USAR_VALIDADORES_PROYECTO = False
    logger.warning("No se pudieron importar validadores del proyecto")


class AEMETThresholds:
    """Gestor de umbrales oficiales de AEMET"""

    def __init__(self, config_path=None):
        if config_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(project_root, "config", "aemet_thresholds.json")

        self.config_path = config_path
        self.validacion = {}
        self.alertas = {}
        self._cargar_config()

    def _cargar_config(self):
        """Carga los umbrales de AEMET desde JSON"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            self.validacion = config.get("validacion", {})
            self.alertas = config.get("alertas", {})
            logger.info(f"Umbrales AEMET cargados: {len(self.validacion)} campos")

        except FileNotFoundError:
            logger.error(f"Archivo de umbrales no encontrado: {self.config_path}")
            self._usar_por_defecto()

        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear umbrales: {e}")
            self._usar_por_defecto()

    def _usar_por_defecto(self):
        """Usa umbrales por defecto si no se puede cargar el config"""
        self.validacion = {
            "temperatura": {"min": -50, "max": 60},
            "humedad": {"min": 0, "max": 100},
            "viento": {"min": 0, "max": 200},
            "lluvia": {"min": 0, "max": 300},
            "presion": {"min": 900, "max": 1050}
        }
        self.alertas = {
            "temperatura": {
                "roja_alta": {"valor": 40, "color": "#ef4444"},
                "naranja_alta": {"valor": 35, "color": "#f97316"}
            }
        }

    def validar_campo(self, campo, valor):
        """Valida un campo específico"""
        if campo not in self.validacion:
            return True

        rango = self.validacion[campo]
        min_val = rango.get("min", float('-inf'))
        max_val = rango.get("max", float('inf'))

        try:
            val_num = float(valor)
            return min_val <= val_num <= max_val
        except (ValueError, TypeError):
            return False

    def obtener_alertas(self, data):
        """Genera alertas según los umbrales de AEMET"""
        alertas_result = []

        # Temperatura
        temp = data.get("temperatura")
        if temp is not None:
            temp = float(temp)
            if "temperatura" in self.alertas:
                if "roja_alta" in self.alertas["temperatura"] and temp >= self.alertas["temperatura"]["roja_alta"]["valor"]:
                    alertas_result.append({"tipo": "temperatura", "nivel": "roja", "valor": temp, **self.alertas["temperatura"]["roja_alta"]})
                elif "naranja_alta" in self.alertas["temperatura"] and temp >= self.alertas["temperatura"]["naranja_alta"]["valor"]:
                    alertas_result.append({"tipo": "temperatura", "nivel": "naranja", "valor": temp, **self.alertas["temperatura"]["naranja_alta"]})

        # Viento
        viento = data.get("viento")
        if viento is not None:
            viento = float(viento)
            if "viento" in self.alertas and self.alertas["viento"]:
                for nivel, config in self.alertas["viento"].items():
                    if viento >= config["valor"]:
                        alertas_result.append({"tipo": "viento", "nivel": nivel, "valor": viento, **config})

        # Lluvia
        lluvia = data.get("lluvia")
        if lluvia is not None:
            lluvia = float(lluvia)
            if "lluvia" in self.alertas and self.alertas["lluvia"]:
                for nivel, config in self.alertas["lluvia"].items():
                    if lluvia >= config["valor"]:
                        alertas_result.append({"tipo": "lluvia", "nivel": nivel, "valor": lluvia, **config})

        # Humedad
        humedad = data.get("humedad")
        if humedad is not None:
            humedad = float(humedad)
            if "humedad" in self.alertas and self.alertas["humedad"]:
                for nivel, config in self.alertas["humedad"].items():
                    if humedad >= config["valor"]:
                        alertas_result.append({"tipo": "humedad", "nivel": nivel, "valor": humedad, **config})

        # Si no hay alertas, añadir verde
        if not alertas_result:
            alertas_result.append({"tipo": "estado", "nivel": "verde", "descripcion": "Sin alertas", "color": "#22c55e"})

        return alertas_result


class NormalizerService:
    """Normalizador automático con umbrales de AEMET"""

    def __init__(self):
        self.thresholds = AEMETThresholds()

    def normalizar(self, data, fuente="unknown"):
        """
        Normaliza un registro de datos.
        Args:
            data: dict con los datos a normalizar
            fuente: str fuente de los datos (AEMET, MANUAL, SCHEDULER, etc.)
        Returns:
            dict con los datos normalizados
        """
        resultado = {}

        # 0. MAPEAR CAMPOS AEMET si es necesario
        for key, value in data.items():
            if key in AEMET_FIELD_MAP:
                mapped_key = AEMET_FIELD_MAP[key]
                resultado[mapped_key] = value
            else:
                resultado[key] = value

        # 1. Normalizar fecha a ISO 8601
        fecha_campo = resultado.get("fecha") or resultado.get("fint")
        if fecha_campo:
            fecha_original = str(fecha_campo)
            try:
                fecha_dt = date_parser.parse(fecha_original)
                resultado["fecha"] = fecha_dt.isoformat()
            except:
                if not validar_fecha(fecha_original):
                    resultado["fecha"] = datetime.now().isoformat()

        # 2. Normalizar tipos numéricos
        campos_numericos = ["temperatura", "humedad", "viento", "lluvia", "presion"]
        for campo in campos_numericos:
            if campo in resultado and resultado[campo] is not None:
                try:
                    resultado[campo] = float(resultado[campo])
                except (ValueError, TypeError):
                    resultado[campo] = None

        # 3. Normalizar y añadir campos faltantes con valores por defecto

        # fuente ---> SIEMPRE en MINÚSCULAS (la BD tiene CHECK con minúsculas)
        # 'aemet' | 'manual' | 'openweather'
        VALORES_VALIDOS = {"aemet", "manual", "openweather"}

        if "fuente" not in resultado or resultado["fuente"] is None:
            fuente_norm = str(fuente).lower()
        else:
            fuente_norm = str(resultado["fuente"]).lower()

        if fuente_norm not in VALORES_VALIDOS:
            fuente_norm = "manual"  # fallback seguro

        resultado["fuente"] = fuente_norm

        # estacion_id ---> mayúsculas
        if "estacion_id" in resultado and resultado["estacion_id"] is not None:
            resultado["estacion_id"] = str(resultado["estacion_id"]).upper()

        # ciudad ---> title case y sin espacios dobles
        # "MADRID  C. UNIVERSITARIA" → "Madrid C. Universitaria"
        if "ciudad" in resultado and resultado["ciudad"] is not None:
            resultado["ciudad"] = " ".join(str(resultado["ciudad"]).title().split())
        else:
            resultado["ciudad"] = None

        if "municipio" not in resultado or resultado["municipio"] is None:
            resultado["municipio"] = None

        if "alertas" not in resultado or resultado["alertas"] is None:
            resultado["alertas"] = []

        # 4. Generar alertas usando umbrales de AEMET
        resultado["alertas"] = self.thresholds.obtener_alertas(resultado)

        # 5. Añadir metadata
        resultado["normalizado_en"] = datetime.now().isoformat()
        resultado["version_normalizador"] = "vortex-1.0"

        # 6. Validar campos críticos
        if not self._es_valido(resultado):
            pass  # Silencioso - el normalizador ya añadió valores por defecto

        return resultado

    def _es_valido(self, data):
        """Verifica si el registro tiene los campos críticos válidos"""
        campos_criticos = ["temperatura", "humedad"]

        for campo in campos_criticos:
            valor = data.get(campo)
            if valor is not None:
                try:
                    val_num = float(valor)
                    if campo == "temperatura" and (val_num < -50 or val_num > 60):
                        return False
                    if campo == "humedad" and (val_num < 0 or val_num > 100):
                        return False
                except (ValueError, TypeError):
                    return False

        return True

    def normalizar_lote(self, datos, fuente="unknown"):
        """Normaliza un lote de registros"""
        resultados = []
        for registro in datos:
            try:
                normalizado = self.normalizar(registro, fuente)
                resultados.append(normalizado)
            except Exception as e:
                logger.error(f"Error normalizando registro: {e}")
                continue

        logger.info(f"Normalizados {len(resultados)} de {len(datos)} registros")
        return resultados


# Instancia global
_normalizer_service = None


def get_normalizer_service():
    """Obtiene la instancia global del normalizador"""
    global _normalizer_service
    if _normalizer_service is None:
        _normalizer_service = NormalizerService()
    return _normalizer_service


if __name__ == "__main__":
    service = NormalizerService()

    test_data = {
        "estacion_id": "EST-1234",
        "fecha": "29/05/2026 15:30",
        "temperatura": 38.5,
        "humedad": 65,
        "viento": 25,
        "lluvia": 0,
        "fuente": "aemet"
    }

    resultado = service.normalizar(test_data, "AEMET")

    print("=== RESULTADO NORMALIZACIÓN ===")
    print(f"Fecha: {resultado['fecha']}")
    print(f"Temperatura: {resultado['temperatura']}")
    print(f"Fuente: {resultado['fuente']}")
    print(f"Alertas: {resultado['alertas']}")
    print(f"Normalizado en: {resultado['normalizado_en']}")