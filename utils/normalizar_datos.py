"""
Script de Normalización de Datos Climáticos - USANDO UMBRALES DEL PROYECTO
==========================================================================
Normaliza los registros del JSON usando los VALIDADORES EXISTENTES del proyecto.
Esto mantiene coherencia con validators.py y alert_service.py.

Umbrales usados (de utils/validators.py):
- Temperatura: -50 a 60
- Humedad: 0 a 100
- Viento: >= 0 (sin límite)
- Lluvia: >= 0 (sin límite)
"""

import sys
import os

# Añadir la raíz del proyecto al path para poder importar utils
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import json
import shutil
from datetime import datetime
from dateutil import parser as date_parser
import logging

# Importar validadores existentes del proyecto
from utils.validators import (
    validar_temperatura,
    validar_humedad,
    validar_viento,
    validar_lluvia,
    validar_fecha,
    validate_weather_data
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ValidadorRegistro:
    """Validador que usa los validadores existentes del proyecto"""

    @classmethod
    def validar_registro(cls, registro):
        """
        Valida un registro usando los validadores existentes.
        Returns: (valido, errores, registro_limpio)
        """
        errores = []

        # Usar validate_weather_data que ya integra todas las validaciones
        if not validate_weather_data(registro):
            errores.append("Registro no pasa validación completa")

        # Validación adicional de fecha (convierte a ISO)
        if 'fecha' in registro:
            fecha_original = str(registro['fecha'])
            # Limpiar y convertir a ISO
            fecha_limpia = fecha_original.replace("/", "-").replace("T", " ").split(" ")[0]
            try:
                fecha = date_parser.parse(fecha_limpia, dayfirst=True)
                registro['fecha'] = fecha.isoformat()
            except:
                # Si no se puede parsear, usar la original si validators.py la acepta
                if not validar_fecha(fecha_original):
                    errores.append(f"Fecha inválida: {fecha_original}")

        # Limpiar valores None
        registro_limpio = {k: v for k, v in registro.items() if v is not None}

        return len(errores) == 0, errores, registro_limpio


class NormalizadorRobusto:
    """Normalizador usando validadores existentes"""

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.backup_file = input_file + ".backup"
        self.stats = {
            "total": 0,
            "validos": 0,
            "invalidos": 0,
            "fechas_corregidas": 0,
            "duplicados": 0
        }

    def hacer_backup(self):
        """Crea backup del archivo original"""
        if os.path.exists(self.input_file):
            shutil.copy2(self.input_file, self.backup_file)
            logger.info(f"Backup creado: {self.backup_file}")
            return True
        return False

    def completar_campos(self, registro):
        """Añade campos faltantes con valores por defecto"""
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

        return registro

    def procesar_registro(self, registro):
        """Procesa un registro individual"""
        # Completar campos
        registro = self.completar_campos(registro)
        return registro

    def verificar_salida(self, datos):
        """Verifica que los datos normalizados son válidos"""
        logger.info("Verificando datos normalizados...")

        resultados = {
            "total": len(datos),
            "sin_fecha": 0,
            "sin_temperatura": 0,
            "sin_humedad": 0,
            "invalidos": 0
        }

        for reg in datos:
            if not validate_weather_data(reg):
                resultados["invalidos"] += 1

        return resultados

    def normalizar(self):
        """Ejecuta la normalización usando validadores del proyecto"""
        # 1. Crear backup
        self.hacer_backup()

        # 2. Cargar datos
        logger.info(f"Cargando datos de: {self.input_file}")
        with open(self.input_file, "r", encoding="utf-8") as f:
            datos = json.load(f)

        self.stats["total"] = len(datos)

        # 3. Validar cada registro con validadores existentes
        datos_validos = []
        registros_vistos = set()

        for idx, registro in enumerate(datos):
            es_valido, errores, registro_limpio = ValidadorRegistro.validar_registro(registro)

            if es_valido:
                resultado = self.procesar_registro(registro_limpio)

                # Check duplicados
                clave = f"{resultado.get('estacion_id', 'NA')}_{resultado.get('fecha', 'NA')}"
                if clave in registros_vistos:
                    self.stats["duplicados"] += 1
                    logger.debug(f"Duplicado: {clave}")
                else:
                    registros_vistos.add(clave)
                    datos_validos.append(resultado)
                    self.stats["validos"] += 1
            else:
                self.stats["invalidos"] += 1
                logger.debug(f"Registro {idx} inválido: {errores}")

        # 4. Guardar resultado
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(datos_validos, f, indent=4, ensure_ascii=False)

        logger.info(f"Datos normalizados guardados en: {self.output_file}")

        # 5. Verificar salida
        verificacion = self.verificar_salida(datos_validos)

        return self.stats, verificacion

    def generar_resumen(self):
        """Devuelve un resumen del procesamiento"""
        return f"""
=============================================
RESUMEN DE NORMALIZACION
(Usando validadores del proyecto)
=============================================
Total de registros:       {self.stats['total']}
Validados correctamente: {self.stats['validos']}
Descartados (invalid):   {self.stats['invalidos']}
Duplicados:              {self.stats['duplicados']}

Umbrales usados (de validators.py):
- Temperatura: -50 a 60
- Humedad: 0 a 100
- Viento: >= 0
- Lluvia: >= 0

Backup creado: {self.backup_file}
=============================================
"""


def generar_datos_sinteticos(cantidad=50):
    """Genera datos sintéticos válidos para pruebas"""
    import random

    estaciones = [
        "Madrid-Retiro", "Madrid-Cuarteles", "Alcala de Henares",
        "Getafe", "Barajas", "Tres Cantos", "Collado Villalb"
    ]

    municipios = [
        "Madrid", "Alcalá de Henares", "Getafe", "Fuenlabrada"
    ]

    datos = []
    for _ in range(cantidad):
        datos.append({
            "estacion_id": f"EST-{random.randint(1000, 9999)}",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "temperatura": round(random.uniform(-5, 40), 1),
            "humedad": random.randint(20, 95),
            "viento": round(random.uniform(0, 50), 1),
            "lluvia": round(random.uniform(0, 20), 1),
            "fuente": "synthetic",
            "municipio": random.choice(municipios),
            "ciudad": random.choice(estaciones)
        })

    return datos


if __name__ == "__main__":
    print("=" * 50)
    print("NORMALIZADOR - Usando validadores del proyecto")
    print("=" * 50)

    # Rutas absolutas basadas en la raíz del proyecto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, "data", "registros_climaticos.json")
    output_path = os.path.join(project_root, "data", "registros_climaticos_normalizados.json")

    # Verificar que existe el archivo
    if not os.path.exists(input_path):
        print(f"Archivo no encontrado: {input_path}")
        print("Generando datos de ejemplo...")

        datos_ejemplo = generar_datos_sinteticos(30)
        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(datos_ejemplo, f, indent=4, ensure_ascii=False)
        print(f"Archivo de ejemplo creado: {input_path}")

    print(f"\nInput: {input_path}")
    print(f"Output: {output_path}")

    # Ejecutar normalización
    print("\nIniciando normalización...")
    normalizador = NormalizadorRobusto(input_path, output_path)
    stats, verificacion = normalizador.normalizar()

    print(normalizador.generar_resumen())

    print("Verificación post-normalización:")
    print(f"  - Total registros: {verificacion['total']}")
    print(f"  - Inválidos: {verificacion['invalidos']}")

    # Generar datos sintéticos
    print("\nGenerando datos sintéticos...")
    sinteticos = generar_datos_sinteticos(10)
    sinteticos_path = os.path.join(project_root, "data", "registros_sinteticos.json")
    with open(sinteticos_path, "w", encoding="utf-8") as f:
        json.dump(sinteticos, f, indent=4, ensure_ascii=False)

    print(f"Datos sintéticos: {sinteticos_path}")
    print("\nProceso completado!")