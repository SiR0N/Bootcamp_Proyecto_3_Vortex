from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from db.models.zona import Zona
from db.models.medicion import Medicion

router = APIRouter(prefix="/zonas", tags=["zonas"])


@router.get("/", response_model=List[dict])
def get_zonas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    zonas = db.query(Zona).offset(skip).limit(limit).all()
    return [
        {
            "id": z.id,
            "nombre": z.nombre,
            "lat": z.lat,
            "lon": z.lon,
            "created_at": z.created_at.isoformat() if z.created_at else None
        }
        for z in zonas
    ]


@router.get("/{zona_id}", response_model=dict)
def get_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona no encontrada")
    return {
        "id": zona.id,
        "nombre": zona.nombre,
        "lat": zona.lat,
        "lon": zona.lon,
        "created_at": zona.created_at.isoformat() if zona.created_at else None
    }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_zona(data: dict, db: Session = Depends(get_db)):
    zona = Zona(
        nombre=data.get("nombre"),
        lat=data.get("lat"),
        lon=data.get("lon")
    )
    db.add(zona)
    db.commit()
    db.refresh(zona)

    return {
        "id": zona.id,
        "nombre": zona.nombre,
        "lat": zona.lat,
        "lon": zona.lon
    }


@router.put("/{zona_id}", response_model=dict)
def update_zona(zona_id: int, data: dict, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona no encontrada")

    if "nombre" in data:
        zona.nombre = data["nombre"]
    if "lat" in data:
        zona.lat = data["lat"]
    if "lon" in data:
        zona.lon = data["lon"]

    db.commit()
    db.refresh(zona)

    return {
        "id": zona.id,
        "nombre": zona.nombre,
        "lat": zona.lat,
        "lon": zona.lon
    }


@router.delete("/{zona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona no encontrada")

    db.delete(zona)
    db.commit()
    return None


@router.get("/{zona_id}/mediciones", response_model=List[dict])
def get_zona_mediciones(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona no encontrada")

    mediciones = db.query(Medicion).filter(Medicion.zona_id == zona_id).all()
    return [
        {
            "id": m.id,
            "fecha": m.fecha.isoformat() if m.fecha else None,
            "temperatura": m.temperatura,
            "humedad": m.humedad,
            "viento": m.viento,
            "lluvia": m.lluvia,
            "fuente": m.fuente
        }
        for m in mediciones
    ]