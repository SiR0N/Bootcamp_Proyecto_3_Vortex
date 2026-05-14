from flask_apscheduler import APScheduler
from services.weather_api_service import obtener_clima_por_coordenadas
from services.normalizer_service import normalizar_datos_aemet
from repositories.json_repository import JSONRepository
import logging
import sys
import os

# Instanciamos el scheduler
scheduler = APScheduler()
repo = JSONRepository('data/registros_climaticos.json')


def ejecutar_etl():
    """Ejecuta el pipeline ETL para cargar datos a PostgreSQL"""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        etl_path = os.path.join(project_root, "etl")
        sys.path.insert(0, etl_path)

        from extract import extract_data
        from transform import transform_data
        from load import load_data

        raw_data = extract_data("../data/registros_climaticos.json")
        if not raw_data:
            logging.warning("No hay datos en JSON para ETL")
            return 0

        df_clean = transform_data(raw_data)
        if df_clean.empty:
            logging.warning("ETL: no hay datos válidos para cargar")
            return 0

        inserted = load_data(df_clean)
        logging.info(f"ETL completado: {inserted} registros insertados en PostgreSQL")
        return inserted
    except Exception as e:
        logging.error(f"Error en ETL automático: {e}")
        return 0


def tarea_actualizar_clima():
    """Tarea automática: descarga el clima y dispara el ETL."""
    try:
        lat, lon = "40.4167", "-3.7033"

        raw_data = obtener_clima_por_coordenadas(lat, lon)
        if not raw_data:
            logging.warning("Scheduler: AEMET sin datos, abortando.")
            return

        data = normalizar_datos_aemet(raw_data)
        # 'aemet' EN MINÚSCULAS — cumple el CHECK constraint de PostgreSQL
        data["fuente"] = "aemet"

        repo.guardar(data)
        print(f"Datos guardados para {data.get('ciudad')}")

        ejecutar_etl() 🎯 AQUÍ DISPARA EL ETL

    except Exception as e:
        logging.error(f"Error en tarea automática: {e}")

def init_scheduler(app):
    """
    Configura e inicia el programador de tareas
    """
    # Configuración básica
    app.config['SCHEDULER_API_ENABLED'] = True
    
    scheduler.init_app(app)
    
    # Programamos la tarea: cada 2h
    scheduler.add_job(
        id='job_clima_auto', 
        func=tarea_actualizar_clima, 
        trigger='interval', 
        minutes=120
    )
    
    scheduler.start()