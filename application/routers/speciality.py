from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/speciality",
    tags=["Speciality management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.SpecialityResponse)
def create_a_speciality(speciality: schemas.SpecialityCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):  
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        speciality = models.Specialite(nom=speciality.nom, effectif=speciality.effectif, code_classe=speciality.code_classe)
        db.add(speciality)
        db.commit()
        db.refresh(speciality)
        return {"nom": speciality.nom,"effectif": speciality.effectif, "code_classe": speciality.code_classe}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("", response_model= List[schemas.SpecialityResponse])
def display_all_specialities(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):  
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        speciality = db.query(models.Specialite).all()
        return speciality
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/{nom}", response_model= schemas.SpecialityResponse)
def display_a_specific_speciality(nom: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        speciality = db.query(models.Specialite).filter(models.Specialite.nom == nom).first()
        if not speciality:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucune spécialité intitulée << {nom} >>")
        
        return speciality
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.delete("/{nom}")
def delete_a_speciality(nom: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        speciality = db.query(models.Specialite).filter(models.Specialite.nom == nom)
        if speciality.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucune spécialité intitulée << {nom} >>")
        else:
            speciality.delete(synchronize_session = False)
            db.commit()
            return {"message": f"la spécialité << {nom} >> est supprimé avec succes."}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")
