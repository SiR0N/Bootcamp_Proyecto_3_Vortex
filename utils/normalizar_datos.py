"""
Script de Normalización de Datos Climáticos
=============================================
Normaliza los registros del JSON para eliminar inconsistencias:
- Formatos de fecha unificados a ISO 8601
- Campos faltantes completados
- Validación de rangos
"""

import json
import os
from datetime import datetime
from dateutil import parser as date_parser


class NormalizadorDatos:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.stats = {
            "total": 0,
            "procesados": 0,
            "fechas_corregidas": 0,
            "campos_anadidos": 0,
            "invalidos": 0
        }

    def normalizar_fecha(self, fecha_str):
        """
        Convierte diferentes formatos de fecha a ISO 8601
        Acepta: DD-MM-YYYY, YYYY-MM-DD, DD/MM/YYYY, etc.
        """
        if not fecha_str:
            return None

        fecha_str = str(fecha_str).strip()

        # Normalizar separadores
        fecha_str = fecha_str.replace("/", "-").replace("T", " ").split(" ")[0]

        # Intentar parsear
        try:
            fecha = date_parser.parse(fecha_str, dayfirst=True)
            return fecha.isoformat()
        except:
            return None

    def completar_campos(self, registro):
        """
        Añade campos faltantes con valores por defecto
        """
        campos_default = {
            "fuente": "unknown",
            "municipio": None,
            "alertas": [],
            "ciudad": None,
            "presion": None
        }

        for campo, valor in campos_default.items():
            if campo not in registro or registro.get(campo) is None:
                registro[campo] = valor
                self.stats["campos_anadidos"] += 1

        return registro

    def validar_rangos(self, registro):
        """
        Valida que los valores estén en rangos válidos
        """
        try:
            temp = float(registro.get("temperatura", 0))
            if temp < -50 or temp > 60:
                return False

            humedad = float(registro.get("humedad", 0))
            if humedad < 0 or humedad > 100:
                return False

            return True
        except:
            return False

    def procesar_registro(self, registro):
        """
        Procesa un registro individual
        """
        # Normalizar fecha
        if "fecha" in registro:
            fecha_normalizada = self.normalizar_fecha(registro["fecha"])
            if fecha_normalizada and fecha_normalizada != registro["fecha"]:
                registro["fecha"] = fecha_normalizada
                self.stats["fechas_corregidas"] += 1

        # Completar campos
        registro = self.completar_campos(registro)

        # Validar rangos
        if not self.validar_rangos(registro):
            return None

        return registro

    def normalizar(self):
        """
        Ejecuta la normalización completa
        """
        # Cargar datos
        with open(self.input_file, "r", encoding="utf-8") as f:
            datos = json.load(f)

        self.stats["total"] = len(datos)

        # Procesar cada registro
        datos_normalizados = []
        for registro in datos:
            resultado = self.procesar_registro(registro)
            if resultado:
                datos_normalizados.append(resultado)
                self.stats["procesados"] += 1
            else:
                self.stats["invalidos"] += 1

        # Guardar resultado
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(datos_normalizados, f, indent=4, ensure_ascii=False)

        return self.stats

    def generar_resumen(self):
        """
        Devuelve un resumen del procesamiento
        """
        return f"""
=============================================
RESUMEN DE NORMALIZACIÓN
=============================================
Total de registros:        {self.stats['total']}
Procesados correctamente: {self.stats['procesados']}
Fechas corregidas:        {self.stats['fechas_corregidas']}
Campos añadidos:          {self.stats['campos_anadidos']}
Registros inválidos:      {self.stats['invalidos']}

=============================================
"""


def generar_datos_sinteticos(cantidad=50):
    """
    Genera datos sintéticos válidos para pruebas
    """
    import random

    estaciones = [
        "Madrid-Retiro", "Madrid-Cuarteles", "Alcala de Henares",
        "Getafe", "Barajas", "Tres Cantos", "Collado Villalb",
        "El Escorial", "Alcobendas", "Fuenlabrada"
    ]

    municipio = [
        "Madrid", "Alcalá de Henares", "Getafe", "Fuenlabrada",
        "Móstoles", "Alcorcón", "Leganés", "Getafe", "Tres Cantos"
    ]

    datos_sinteticos = []
    for i in range(cantidad):
        datos_sinteticos.append({
            "estacion_id": f"EST-{random.randint(1000, 9999)}",
            "fecha": datetime.now().isoformat(),
            "temperatura": round(random.uniform(-5, 40), 1),
            "humedad": random.randint(20, 95),
            "viento": round(random.uniform(0, 50), 1),
            "lluvia": round(random.uniform(0, 20), 1),
            "fuente": "synthetic",
            "municipio": random.choice(municipio),
            "alertas": [],
            "ciudad": random.choice(estaciones)
        })

    return datos_sinteticos


if __name__ == "__main__":
    # Rutas
    input_path = os.path.join("data", "registros_climaticos.json")
    output_path = os.path.join("data", "registros_climaticos_normalizados.json")

    print("Iniciando normalización de datos...")

    # Ejecutar normalización
    normalizador = NormalizadorDatos(input_path, output_path)
    stats = normalizador.normalizar()

    # Mostrar resumen
    print(normalizador.generar_resumen())

    # Generar datos sintéticos de ejemplo
    print("Generando datos sintéticos de ejemplo...")
    datos_sinteticos = generar_datos_sinteticos(10)

    # Guardar datos sintéticos
    sinteticos_path = os.path.join("data", "registros_sinteticos.json")
    with open(sinteticos_path, "w", encoding="utf-8") as f:
        json.dump(datos_sinteticos, f, indent=4, ensure_ascii=False)

    print(f"Datos sintéticos guardados en: {sinteticos_path}")
    print("Proceso completado!")