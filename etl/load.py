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

        estacion_id = data["estacion_id"]

        # VALIDAR estacion_id: evitar NaN, None o valores inválidos
        if not estacion_id or (isinstance(estacion_id, float) and str(estacion_id) == 'nan'):
            print("[WARN] estacion_id inválido, omitiendo registro")
            continue

        # --- Validate zona_id ---
        
        zona = db.query(Zona).filter(Zona.estacion_id == estacion_id).first()

        if not zona:
            zona = Zona(
                estacion_id=estacion_id,
                nombre=None,
                latitud=None,
                longitud=None
            )
            db.add(zona)
            db.commit()
            db.refresh(zona)
            print(f"ℹ️ Nueva zona creada para estacion_id={estacion_id}")
            
            # Normalizar fuente
        fuente = str(data.get("fuente", "manual"))
        if fuente not in ("aemet", "manual"):
            fuente = "manual"

        medicion = Medicion(
            zona_id=zona.id,
            fecha=data["fecha"], 
            temperatura=data.get("temperatura"),
            humedad=data.get("humedad"),
            viento=data.get("viento"),
            lluvia=data.get("lluvia"),
            presion=data.get("presion"),
            fuente=fuente   
        )
        try:
            db.add(medicion)
            db.commit()
            inserted += 1
        except Exception as e:
            print(f"❌ Error insertando registro {estacion_id}: {e}")
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
            "fecha": datetime.now(),
            "temperatura": 10,
            "humedad": 50,
            "viento": 2,
            "lluvia": 0,
            "fuente": "manual"
        }
    ])

    load_data(df_test)
