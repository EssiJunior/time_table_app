from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/day",
    tags=["Day management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.DayResponse)
def create_a_day(day: schemas.DayCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ):  
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        day = models.Jour(nom=day.nom, num=day.num)
        db.add(day)
        db.commit()
        db.refresh(day)
        return day
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")


@router.get("/all", response_model= List[schemas.DayResponse])
def display_all_days(db: Session = Depends(get_db)): 
    day = db.query(models.Jour).all()
    return day

@router.get("", response_model= schemas.DayResponse)
def display_a_specific_day(nom: str, db: Session = Depends(get_db)):
    day = db.query(models.Jour).filter(models.Jour.nom == nom).first()
    if not day:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucun jour intitulée << {nom} >>")
    return day

@router.delete("")
def delete_a_day(nom: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        day = db.query(models.Jour).filter(models.Jour.nom == nom)
        if day.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucun jour intitulée << {nom} >>")
        else:
            day.delete(synchronize_session = False)
            db.commit()
            return {"message": f"le jour << {nom} >> est supprimé avec succes."}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.put("", response_model=schemas.DayResponse)
def update_a_day(nom: str, day: schemas.DayCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        response = db.query(models.Jour).filter(models.Jour.nom == nom)
        if response.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"<< {nom} >> n'existe pas")
        response.update(day.dict(),synchronize_session=False)
        db.commit()
        return day
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Administrateur peut realiser cette tache.")
