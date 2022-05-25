from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, utils
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/course_period",
    tags=["Course period management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.CoursePeriodResponse)
def create_a_course_period(period: schemas.CoursePeriodCreate, db: Session = Depends(get_db) ):  
    period = models.PlageHoraire(heure_debut=period.heure_debut, heure_fin=period.heure_fin)
    db.add(period)
    db.commit()
    db.refresh(period)
    
    return {"id_plage": period.id_plage,"heure_debut": period.heure_debut, "heure_fin":period.heure_fin}


@router.get("", response_model= List[schemas.CoursePeriodResponse])
def display_all_course_period(db: Session = Depends(get_db)):    
    period = db.query(models.PlageHoraire).all()
    
    return period

@router.get("/{id_plage}", response_model= schemas.CoursePeriodResponse)
def display_a_specific_course_period(id_plage: int, db: Session = Depends(get_db)):
    period = db.query(models.PlageHoraire).filter(models.PlageHoraire.id_plage == id_plage).first()
    if not period:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucune plage horaire identifié par << {id_plage} >>")
    
    return period

@router.delete("/{id_plage}")
def delete_a_course_period(id_plage: int, db: Session = Depends(get_db)):
    period = db.query(models.PlageHoraire).filter(models.PlageHoraire.id_plage == id_plage)
    if period.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucune plage horaire identifié par << {id_plage} >>")
    else:
        period.delete(synchronize_session = False)
        db.commit()
        return {"message": f"la plage horaire identifiée << {id_plage} >> est supprimé avec succes."}
    