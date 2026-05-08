"""
Fallback Service - VORTEX EVOLUCIÓN
================================
Servicio de fallback dinámico basado en configuración JSON.
No hardcoded - todas las ubicaciones configurables.
"""

import json
import os
import logging

logger = logging.getLogger(__name__)


class FallbackService:
    """Servicio de fallback dinámico que lee configuración de JSON"""

    def __init__(self, config_path=None):
        if config_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(project_root, "config", "ubicaciones.json")

        self.config_path = config_path
        self.ubicaciones = []
        self.fallback_order = []
        self._cargar_config()

    def _cargar_config(self):
        """Carga la configuración de ubicaciones desde JSON"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            # Recoger todas las ubicaciones de todas las regiones
            for region_name, region_data in config.get("regiones", {}).items():
                if "ubicaciones" in region_data:
                    for ubi in region_data["ubicaciones"]:
                        ubi["region"] = region_name
                        self.ubicaciones.append(ubi)

            # Cargar orden de fallback
            self.fallback_order = config.get("fallback_orden", [])

            # Añadir ubicaciones del orden que no estén en la lista
            for nombre in self.fallback_order:
                if not any(u["nombre"] == nombre for u in self.ubicaciones):
                    logger.warning(f"Fallback '{nombre}' no encontrado en ubicaciones")

            logger.info(f"Fallback service cargado: {len(self.ubicaciones)} ubicaciones")

        except FileNotFoundError:
            logger.error(f"Archivo de configuración no encontrado: {self.config_path}")
            self.ubicaciones = []
            self.fallback_order = []

        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear config JSON: {e}")
            self.ubicaciones = []

    def get_fallback_locations(self):
        """Devuelve lista de ubicaciones de fallback ordenadas"""
        if self.fallback_order:
            ordered = []
            for nombre in self.fallback_order:
                ubi = next((u for u in self.ubicaciones if u["nombre"] == nombre), None)
                if ubi:
                    ordered.append(ubi)
            return ordered
        return self.ubicaciones

    def get_ubicacion_por_nombre(self, nombre):
        """Busca una ubicación por nombre"""
        return next((u for u in self.ubicaciones if u["nombre"] == nombre), None)

    def get_ubicacion_por_cod_ine(self, cod_ine):
        """Busca una ubicación por código INE"""
        return next((u for u in self.ubicaciones if u.get("cod_ine") == cod_ine), None)

    def get_ubicacion_cercana(self, lat, lon, radio_km=50):
        """Encuentra la ubicación más cercana a unas coordenadas"""
        from math import radians, sin, cos, sqrt, atan2

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Radio de la Tierra en km
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            return R * c

        mas_cercana = None
        distancia_min = float('inf')

        for ubi in self.ubicaciones:
            dist = haversine(lat, lon, ubi["lat"], ubi["lon"])
            if dist < distancia_min and dist <= radio_km:
                distancia_min = dist
                mas_cercana = ubi

        return mas_cercana, distancia_min

    def get_default_ubicacion(self):
        """Devuelve la ubicación por defecto (primera en el orden)"""
        if self.fallback_order:
            nombre_default = self.fallback_order[0]
            return self.get_ubicacion_por_nombre(nombre_default)
        return self.ubicaciones[0] if self.ubicaciones else None


# Instancia global para uso en la aplicación
_fallback_service = None


def get_fallback_service():
    """Obtiene la instancia global del servicio de fallback"""
    global _fallback_service
    if _fallback_service is None:
        _fallback_service = FallbackService()
    return _fallback_service


if __name__ == "__main__":
    # Test del servicio
    service = FallbackService()
    print(f"Total ubicaciones: {len(service.ubicaciones)}")
    print(f"Orden fallback: {service.fallback_order}")

    default = service.get_default_ubicacion()
    print(f"Ubicación por defecto: {default}")

    cercana, distancia = service.get_ubicacion_cercana(40.4167, -3.7033)
    print(f"Más cercana a Madrid centro: {cercana['nombre']} ({distancia:.2f} km)")