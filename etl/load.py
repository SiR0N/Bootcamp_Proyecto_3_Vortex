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
    print("📤 Iniciando carga de datos en la base de datos...")

    db: Session = next(get_db())
    inserted = 0

    for _, row in df.iterrows():
        data = row.to_dict()

        zona_id = data.get("zona_id")
        zona = db.query(Zona).filter(Zona.id == zona_id).first()

        if not zona:
            print(f"⚠️ Zona no válida: {zona_id}. Registro omitido.")
            continue

        fecha = data.get("fecha")
        try:
            fecha = datetime.fromisoformat(str(fecha)) if not isinstance(fecha, datetime) else fecha
        except Exception:
            print(f"⚠️ Fecha inválida: {fecha}. Registro omitido.")
            continue

        try:
            medicion = Medicion(
                zona_id=zona_id,
                fecha=fecha,
                temperatura=data.get("temperatura"),
                humedad=data.get("humedad"),
                viento=data.get("viento"),
                lluvia=data.get("lluvia"),
                presion=data.get("presion"),
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
    print(f"✔ Carga completada. Registros insertados: {inserted}")
    return inserted


if __name__ == "__main__":
    import pandas as pd

    df_test = pd.DataFrame([{
        "zona_id": 1,
        "fecha": "2026-01-01T00:00:00",
        "temperatura": 10,
        "humedad": 50,
        "viento": 2,
        "lluvia": 0,
        "presion": 1013,
        "fuente": "etl"
    }])

    load_data(df_test)