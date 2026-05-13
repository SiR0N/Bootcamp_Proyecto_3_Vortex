import os
import logging
from typing import Dict, Any, Optional
from services.retry_service import get_retry_session
from services.fallback_service import get_fallback_service
from utils.helpers import calcular_distancia
import requests

class WeatherAPIService:
    def __init__(self):
        self.aemet_api_key = os.getenv("AEMET_API_KEY")
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

        if not self.aemet_api_key:
            self.logger = logging.getLogger(__name__)
            self.logger.warning("AEMET_API_KEY no encontrada en .env.")

        self.session = get_retry_session() if self.aemet_api_key else None
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"

    def _obtener_datos_openweather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Obtiene datos de OpenWeather API como fallback"""
        if not self.openweather_api_key:
            return None
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.openweather_api_key}&units=metric"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            d = r.json()
            return {
                "estacion_id": f"OW-{d.get('id', 'unknown')}",
                "ubi": d.get("name", "OpenWeather"),
                "lat": d.get("coord", {}).get("lat", lat),
                "lon": d.get("coord", {}).get("lon", lon),
                "municipio": d.get("name"),
                "temperatura": d.get("main", {}).get("temp"),
                "humedad": d.get("main", {}).get("humidity"),
                "viento": (d.get("wind", {}).get("speed", 0) or 0) * 3.6,
                "presion": d.get("main", {}).get("pressure"),
                "lluvia": d.get("rain", {}).get("1h", 0) if d.get("rain") else 0,
                "fecha": self._obtener_fecha_actual(),
                "fuente": "openweather",
                "_fallback": True
            }
        except Exception as e:
            self.logger.error(f"Error OpenWeather: {e}")
            return None

    def _obtener_datos_crudos(self) -> list:
        """Método interno para bajar todas las observaciones de AEMET."""
        if not self.aemet_api_key:
            self.logger.warning("Sin AEMET API key, devolviendo lista vacía para fallback.")
            return []

        headers = {"api_key": self.aemet_api_key, "cache-control": "no-cache"}
        try:
            # Usamos la sesión con reintentos de la arquitectura original
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

    # 2. TU MEJORA: Búsqueda por coordenadas integrada
    def obtener_clima_por_coordenadas(self, user_lat: float, user_lon: float) -> Optional[Dict[str, Any]]:
        """
        Lógica de Juan: Localiza la estación más cercana y devuelve sus datos RAW.
        Si falla AEMET, usa fallback_service con ubicaciones predefinidas.
        """
        observaciones = self._obtener_datos_crudos()

        if not observaciones:
            # Intentar OpenWeather primero
            ow_data = self._obtener_datos_openweather(user_lat, user_lon)
            if ow_data:
                return ow_data
            self.logger.warning("AEMET y OpenWeather fallaron.")
            return None

        estacion_cercana = None
        distancia_minima = float('inf')

        for obs in observaciones:
            try:
                # Extraemos y validamos coordenadas de la estación
                obs_lat = float(obs['lat'])
                obs_lon = float(obs['lon'])

                dist = calcular_distancia(
                    float(user_lat),
                    float(user_lon),
                    obs_lat,
                    obs_lon
                )

                if dist < distancia_minima:
                    distancia_minima = dist
                    estacion_cercana = obs

            except (KeyError, ValueError, TypeError):
                continue # Saltamos estaciones con datos corruptos

        if estacion_cercana:
            self.logger.info(f"Estación más cercana hallada: {estacion_cercana.get('ubi')} a {distancia_minima:.2f}km")

        # Si la estación más cercana está a más de 50km, usar OpenWeather
        if distancia_minima > 50:
            self.logger.warning(f"Estación a {distancia_minima:.2f}km (>50km). Intentando OpenWeather...")
            ow_data = self._obtener_datos_openweather(user_lat, user_lon)
            if ow_data:
                return ow_data
            return None

        return estacion_cercana

    def _generar_datos_fallback(self, lat: float, lon: float, estacion_cercana=None) -> Dict[str, Any]:
        """
        Genera datos de fallback usando ubicaciones predefinidas.
        Se usa cuando AEMET falla o la estación está muy lejos.
        """
        try:
            fallback_service = get_fallback_service()

            # Buscar la ubicación más cercana en las predefinidas
            ubicacion = None
            distancia = 0

            try:
                ubicacion, distancia = fallback_service.get_ubicacion_cercana(lat, lon, radio_km=100)
            except Exception:
                pass

            if not ubicacion:
                # Usar la ubicación por defecto
                try:
                    ubicacion = fallback_service.get_default_ubicacion()
                except Exception:
                    pass

            if not ubicacion:
                # Último recurso: datos de emergencia
                return {
                    "estacion_id": "FALLBACK-EMERGENCIA",
                    "ubi": "Datos de emergencia",
                    "lat": float(lat),
                    "lon": float(lon),
                    "municipio": "Emergencia",
                    "temperatura": 20,
                    "humedad": 50,
                    "viento": 0,
                    "presion": 1015,
                    "lluvia": 0,
                    "fuente": "fallback"
                }

            # Generar datos sintéticos realistas basados en la ubicación
            lat_val = float(ubicacion.get("lat", lat))
            lon_val = float(ubicacion.get("lon", lon))

            return {
                "estacion_id": f"FALLBACK-{ubicacion.get('nombre', 'UNKNOWN').replace(' ', '-')}",
                "ubi": ubicacion.get("nombre", "Ubicación Fallback"),
                "lat": lat_val,
                "lon": lon_val,
                "municipio": ubicacion.get("municipio", ubicacion.get("nombre")),
                # Datos sintéticos razonables
                "temperatura": round(random.uniform(15, 28), 1),
                "humedad": random.randint(40, 70),
                "viento": round(random.uniform(0, 15), 1),
                "presion": random.randint(1010, 1025),
                "lluvia": 0,
                "fecha": self._obtener_fecha_actual(),
                "fuente": "fallback",
                "_fallback": True,
                "_distancia_fallback": round(distancia, 2) if distancia else 0
            }
        except Exception as e:
            self.logger.error(f"Error en fallback: {e}")
            # Devolver datos mínimo como último recurso
            return {
                "estacion_id": "FALLBACK-EMERGENCIA",
                "ubi": "Datos de emergencia",
                "lat": float(lat),
                "lon": float(lon),
                "municipio": "Emergencia",
                "temperatura": 20,
                "humedad": 50,
                "fuente": "fallback"
            }

    def _obtener_fecha_actual(self) -> str:
        """Devuelve la fecha actual en formato AEMET"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # 3. MANTENEMOS: Los métodos originales que ellas ya tuvieran (ej: por ID)
    def obtener_clima_por_id(self, station_id: str):
        # Aquí iría el código que ellas ya escribieron (puedes completarlo si es necesario)
        pass

# --- FUNCIÓN PUENTE PARA COMPATIBILIDAD CON APP.PY ---
def obtener_clima_por_coordenadas(lat, lon):
    """
    Permite que app.py siga llamando a esta función directamente 
    mientras nosotros usamos la lógica de la clase por debajo.
    """
    service = WeatherAPIService()
    return service.obtener_clima_por_coordenadas(lat, lon)