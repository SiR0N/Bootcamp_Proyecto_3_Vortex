import os
import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime
from services.retry_service import get_retry_session
from utils.helpers import calcular_distancia


class WeatherAPIService:
    def __init__(self):
        self.aemet_api_key      = os.getenv("AEMET_API_KEY")
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.logger  = logging.getLogger(__name__)
        self.session = get_retry_session() if self.aemet_api_key else None
        self.base_url = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"

        if not self.aemet_api_key:
            self.logger.warning("AEMET_API_KEY no encontrada en .env.")
        if not self.openweather_api_key:
            self.logger.warning("OPENWEATHER_API_KEY no encontrada en .env.")

    # ── AEMET: paso 1 y 2 ────────────────────────────────────────────────
    def _obtener_datos_crudos(self) -> list:
        """Descarga todas las observaciones de AEMET."""
        if not self.aemet_api_key:
            return []

        headers = {"api_key": self.aemet_api_key, "cache-control": "no-cache"}
        try:
            res_meta = self.session.get(self.base_url, headers=headers, timeout=20)
            res_meta.raise_for_status()

            datos_url = res_meta.json().get("datos")
            if not datos_url:
                return []

            res_datos = self.session.get(datos_url, timeout=20)
            res_datos.raise_for_status()
            return res_datos.json()

        except Exception as e:
            self.logger.error(f"Error al conectar con AEMET: {e}")
            return []

    # ── OpenWeather: fallback real ────────────────────────────────────────
    def _obtener_datos_openweather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Fallback a OpenWeather si AEMET falla. Datos reales, no sintéticos."""
        if not self.openweather_api_key:
            self.logger.warning("Sin OPENWEATHER_API_KEY, no hay fallback disponible.")
            return None

        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?lat={lat}&lon={lon}"
                f"&appid={self.openweather_api_key}"
                f"&units=metric"
            )
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            d = r.json()

            return {
                "estacion_id": f"OW-{d.get('id', 'unknown')}",
                "ubi":         d.get("name", "OpenWeather"),
                "lat":         d.get("coord", {}).get("lat", lat),
                "lon":         d.get("coord", {}).get("lon", lon),
                "temperatura": d.get("main", {}).get("temp"),
                "humedad":     d.get("main", {}).get("humidity"),
                "viento":      (d.get("wind", {}).get("speed", 0) or 0) * 3.6,
                "presion":     d.get("main", {}).get("pressure"),
                "lluvia":      d.get("rain", {}).get("1h", 0) if d.get("rain") else 0,
                "fecha":       datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "fuente":      "openweather",
            }

        except Exception as e:
            self.logger.error(f"Error OpenWeather: {e}")
            return None

    # ── Estación más cercana ──────────────────────────────────────────────
    def obtener_clima_por_coordenadas(self, user_lat: float, user_lon: float) -> Optional[Dict[str, Any]]:
        """
        Busca la estación AEMET más cercana.
        Si AEMET falla o está a más de 50km → OpenWeather.
        Si ambas fallan → None (no se inserta nada).
        """
        observaciones = self._obtener_datos_crudos()

        if not observaciones:
            self.logger.warning("AEMET no disponible. Intentando OpenWeather...")
            return self._obtener_datos_openweather(user_lat, user_lon)

        estacion_cercana  = None
        distancia_minima  = float('inf')

        for obs in observaciones:
            try:
                dist = calcular_distancia(
                    float(user_lat), float(user_lon),
                    float(obs['lat']), float(obs['lon'])
                )
                if dist < distancia_minima:
                    distancia_minima = dist
                    estacion_cercana = obs
            except (KeyError, ValueError, TypeError):
                continue

        if estacion_cercana:
            self.logger.info(
                f"Estación más cercana: {estacion_cercana.get('ubi')} "
                f"a {distancia_minima:.2f}km"
            )

        if distancia_minima > 50:
            self.logger.warning(
                f"Estación a {distancia_minima:.2f}km (>50km). Intentando OpenWeather..."
            )
            return self._obtener_datos_openweather(user_lat, user_lon)

        return estacion_cercana

    def obtener_clima_por_id(self, station_id: str):
        pass


# Función puente para compatibilidad con app.py
def obtener_clima_por_coordenadas(lat, lon):
    service = WeatherAPIService()
    return service.obtener_clima_por_coordenadas(lat, lon)