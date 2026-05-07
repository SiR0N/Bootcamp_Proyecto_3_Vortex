from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from db.session import get_db
from db.models.zona import Zona
from db.models.medicion import Medicion

router = APIRouter(prefix="/mediciones", tags=["mediciones"])


@router.get("/", response_model=List[dict])
def get_mediciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    mediciones = db.query(Medicion).offset(skip).limit(limit).all()
    return [
        {
            "id": m.id,
            "zona_id": m.zona_id,
            "fecha": m.fecha.isoformat() if m.fecha else None,
            "temperatura": m.temperatura,
            "humedad": m.humedad,
            "viento": m.viento,
            "lluvia": m.lluvia,
            "fuente": m.fuente,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        for m in mediciones
    ]


@router.get("/{medicion_id}", response_model=dict)
def get_medicion(medicion_id: int, db: Session = Depends(get_db)):
    medicion = db.query(Medicion).filter(Medicion.id == medicion_id).first()
    if not medicion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medición no encontrada")
    return {
        "id": medicion.id,
        "zona_id": medicion.zona_id,
        "fecha": medicion.fecha.isoformat() if medicion.fecha else None,
        "temperatura": medicion.temperatura,
        "humedad": medicion.humedad,
        "viento": medicion.viento,
        "lluvia": medicion.lluvia,
        "fuente": medicion.fuente,
        "created_at": medicion.created_at.isoformat() if medicion.created_at else None
    }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_medicion(data: dict, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == data.get("zona_id")).first()
    if not zona:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Zona no válida")

    medicion = Medicion(
        zona_id=data.get("zona_id"),
        fecha=datetime.fromisoformat(data.get("fecha")) if data.get("fecha") else datetime.utcnow(),
        temperatura=data.get("temperatura"),
        humedad=data.get("humedad"),
        viento=data.get("viento"),
        lluvia=data.get("lluvia"),
        fuente=data.get("fuente", "manual")
    )
    db.add(medicion)
    db.commit()
    db.refresh(medicion)

    return {
        "id": medicion.id,
        "zona_id": medicion.zona_id,
        "fecha": medicion.fecha.isoformat() if medicion.fecha else None,
        "temperatura": medicion.temperatura,
        "humedad": medicion.humedad,
        "viento": medicion.viento,
        "lluvia": medicion.lluvia,
        "fuente": medicion.fuente
    }


@router.put("/{medicion_id}", response_model=dict)
def update_medicion(medicion_id: int, data: dict, db: Session = Depends(get_db)):
    medicion = db.query(Medicion).filter(Medicion.id == medicion_id).first()
    if not medicion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medición no encontrada")

    if "zona_id" in data:
        zona = db.query(Zona).filter(Zona.id == data["zona_id"]).first()
        if not zona:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Zona no válida")
        medicion.zona_id = data["zona_id"]

    if "fecha" in data:
        medicion.fecha = datetime.fromisoformat(data["fecha"])
    if "temperatura" in data:
        medicion.temperatura = data["temperatura"]
    if "humedad" in data:
        medicion.humedad = data["humedad"]
    if "viento" in data:
        medicion.viento = data["viento"]
    if "lluvia" in data:
        medicion.lluvia = data["lluvia"]

    db.commit()
    db.refresh(medicion)

    return {
        "id": medicion.id,
        "zona_id": medicion.zona_id,
        "fecha": medicion.fecha.isoformat() if medicion.fecha else None,
        "temperatura": medicion.temperatura,
        "humedad": medicion.humedad,
        "viento": medicion.viento,
        "lluvia": medicion.lluvia,
        "fuente": medicion.fuente
    }


@router.delete("/{medicion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicion(medicion_id: int, db: Session = Depends(get_db)):
    medicion = db.query(Medicion).filter(Medicion.id == medicion_id).first()
    if not medicion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medición no encontrada")

    db.delete(medicion)
    db.commit()
    return None