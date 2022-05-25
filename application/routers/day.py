from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/day",
    tags=["Day management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.DayResponse)
def create_a_day(day: schemas.DayCreate, db: Session = Depends(get_db) ):  
    day = models.Jour(nom=day.nom)
    db.add(day)
    db.commit()
    db.refresh(day)
    
    return {"nom": day.nom}


@router.get("", response_model= List[schemas.DayResponse])
def display_all_days(db: Session = Depends(get_db)):    
    day = db.query(models.Jour).all()
    
    return day

@router.get("/{nom}", response_model= schemas.DayResponse)
def display_a_specific_day(nom: str, db: Session = Depends(get_db)):
    day = db.query(models.Jour).filter(models.Jour.nom == nom).first()
    if not day:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucun jour intitulée << {nom} >>")
    
    return day

@router.delete("/{nom}")
def delete_a_day(nom: str, db: Session = Depends(get_db)):
    day = db.query(models.Jour).filter(models.Jour.nom == nom)
    if day.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucun jour intitulée << {nom} >>")
    else:
        day.delete(synchronize_session = False)
        db.commit()
        return {"message": f"le jour << {nom} >> est supprimé avec succes."}
    