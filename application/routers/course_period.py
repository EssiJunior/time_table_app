from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/course_period",
    tags=["Course period management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.CoursePeriodResponse)
def create_a_course_period(period: schemas.CoursePeriodCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        period = models.PlageHoraire(heure_debut=period.heure_debut, heure_fin=period.heure_fin)
        db.add(period)
        db.commit()
        db.refresh(period)
        return {"id_plage": period.id_plage,"heure_debut": period.heure_debut, "heure_fin":period.heure_fin}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")


@router.get("/all", response_model= List[schemas.CoursePeriodResponse])
def display_all_course_period(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):    
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        period = db.query(models.PlageHoraire).all()
        return period
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")


@router.get("", response_model= schemas.CoursePeriodResponse)
def display_a_specific_course_period(id_plage: int, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        period = db.query(models.PlageHoraire).filter(models.PlageHoraire.id_plage == id_plage).first()
        if not period:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucune plage horaire identifié par << {id_plage} >>")
        
        return period
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")


@router.delete("")
def delete_a_course_period(id_plage: int, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        period = db.query(models.PlageHoraire).filter(models.PlageHoraire.id_plage == id_plage)
        if period.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucune plage horaire identifié par << {id_plage} >>")
        else:
            period.delete(synchronize_session = False)
            db.commit()
            return {"message": f"la plage horaire identifiée << {id_plage} >> est supprimé avec succes."}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.put("", response_model=schemas.CoursePeriodResponse)
def update_a_course_period(id_plage: int, course_period: schemas.CoursePeriodCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        response = db.query(models.PlageHoraire).filter(models.PlageHoraire.id_plage == id_plage)
        if response.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Il n'existe aucune plage horaire identifié par << {id_plage} >>")
        response.update(course_period.dict(),synchronize_session=False)
        db.commit()
        return course_period
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Administrateur peut realiser cette tache.")
