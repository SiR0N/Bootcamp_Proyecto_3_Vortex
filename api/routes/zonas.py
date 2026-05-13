from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from db.models.zona import Zona
from db.models.medicion import Medicion
from api.schemas.zona import ZonaCreate, ZonaResponse
from api.schemas.medicion import MedicionResponse

router = APIRouter(prefix="/zonas", tags=["zonas"])


@router.get("/", response_model=List[ZonaResponse])
def get_zonas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Zona).offset(skip).limit(limit).all()


# ⚠️ Este endpoint debe ir ANTES de /{id} para que FastAPI no lo confunda
@router.get("/by_estacion/{estacion_id}", response_model=ZonaResponse)
def get_zona_by_estacion(estacion_id: str, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.estacion_id == estacion_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return zona


@router.get("/{id}", response_model=ZonaResponse)
def get_zona(id: int, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return zona


@router.post("/", response_model=ZonaResponse, status_code=status.HTTP_201_CREATED)
def create_zona(zona: ZonaCreate, db: Session = Depends(get_db)):
    # Si ya existe → 409 Conflict
    existing = db.query(Zona).filter(Zona.estacion_id == zona.estacion_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="La zona ya existe")

    # Crear nueva → 201 Created
    nueva_zona = Zona(**zona.model_dump())
    db.add(nueva_zona)
    db.commit()
    db.refresh(nueva_zona)
    return nueva_zona


@router.put("/{id}", response_model=ZonaResponse)
def update_zona(id: int, zona_in: ZonaCreate, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    for key, value in zona_in.model_dump().items():
        setattr(zona, key, value)

    db.commit()
    db.refresh(zona)
    return zona


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zona(id: int, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    db.delete(zona)
    db.commit()
    return None


@router.get("/{id}/mediciones", response_model=List[MedicionResponse])
def get_mediciones_por_zona(id: int, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    return db.query(Medicion).filter(Medicion.zona_id == id).all()