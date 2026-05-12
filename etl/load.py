from sqlalchemy.orm import Session
from datetime import datetime
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from db.session import get_db
from db.models.medicion import Medicion
from db.models.zona import Zona



def load_data(df):
    """
    Load cleaned climate data directly into the database using SQLAlchemy,
    following the same logic as the FastAPI mediciones endpoint.
    """
    print("🔌 Conectando a la base de datos...")

    db: Session = next(get_db())  # Create SQLAlchemy session manually
    inserted = 0

    for _, row in df.iterrows():
        data = row.to_dict()

        # --- Validate zona_id ---
        zona_id = data.get("estacion_id")  # Your ETL uses estacion_id as the zone
        zona = db.query(Zona).filter(Zona.id == zona_id).first()

        if not zona:
            print(f"⚠️ Zona no válida para estacion_id={zona_id}. Registro omitido.")
            continue

        try:
            medicion = Medicion(
                zona_id=zona_id,
                fecha=data.get("fecha") if isinstance(data.get("fecha"), datetime)
                      else datetime.fromisoformat(str(data.get("fecha"))),
                temperatura=data.get("temperatura"),
                humedad=data.get("humedad"),
                viento=data.get("viento"),
                lluvia=data.get("lluvia"),
                fuente=data.get("fuente", "etl")
            )

            db.add(medicion)
            db.commit()
            db.refresh(medicion)

            inserted += 1

        except Exception as e:
            print(f"❌ Error insertando registro {zona_id}: {e}")
            db.rollback()

    db.close()
    print(f"📦 Inserción completada. Total insertado: {inserted}")
    return inserted


# --- Manual test ---
if __name__ == "__main__":
    import pandas as pd

    print("🔧 Test manual de load.py")

    df_test = pd.DataFrame([
        {
            "estacion_id": "EST-01",
            "fecha": "2026-01-01T00:00:00",
            "temperatura": 10,
            "humedad": 50,
            "viento": 2,
            "lluvia": 0,
            "fuente": "etl"
        }
    ])

    load_data(df_test)
