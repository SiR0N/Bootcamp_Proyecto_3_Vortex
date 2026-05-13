from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from db.models.medicion import Medicion
from db.models.zona import Zona
from api.schemas.medicion import MedicionCreate, MedicionResponse, MedicionUpdate

router = APIRouter(prefix="/mediciones", tags=["mediciones"])

@router.get("/", response_model=List[MedicionResponse])
def get_mediciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Medicion).offset(skip).limit(limit).all()

@router.post("/", response_model=MedicionResponse, status_code=status.HTTP_201_CREATED)
def create_medicion(medicion_in: MedicionCreate, db: Session = Depends(get_db)):
    # 1. Validar que la zona a la que se intenta asociar existe
    zona = db.query(Zona).filter(Zona.id == medicion_in.zona_id).first()
    if not zona:
        raise HTTPException(status_code=400, detail="La zona_id proporcionada no existe")

    # 2. Crear la medición
    nueva_medicion = Medicion(**medicion_in.model_dump())
    try:
        
        db.add(nueva_medicion)
        db.commit()
        db.refresh(nueva_medicion)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al guardar la medición")
    return nueva_medicion

@router.get("/{medicion_id}", response_model=MedicionResponse)
def get_medicion(medicion_id: int, db: Session = Depends(get_db)):
    medicion = db.query(Medicion).filter(Medicion.id == medicion_id).first()
    if not medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return medicion

@router.put("/{medicion_id}", response_model=MedicionResponse)
def update_medicion(medicion_id: int, medicion_update: MedicionUpdate, db: Session = Depends(get_db)):
    medicion = db.query(Medicion).filter(Medicion.id == medicion_id).first()
    if not medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    
    if medicion_update.zona_id is not None:
        zona = db.query(Zona).filter(Zona.id == medicion_update.zona_id).first()
        if not zona:
            raise HTTPException(status_code=400, detail="La zona_id proporcionada no existe")
    
    update_data = medicion_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(medicion, key, value)
    
    db.commit()
    db.refresh(medicion)
    return medicion

@router.delete("/{medicion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicion(medicion_id: int, db: Session = Depends(get_db)):
    medicion = db.query(Medicion).filter(Medicion.id == medicion_id).first()
    if not medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    
    db.delete(medicion)
    db.commit()
    return None