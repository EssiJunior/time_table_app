from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/class",
    tags=["Class management"]
)

@router.get("/generate_classes", status_code = status.HTTP_201_CREATED)
def create_classes(db: Session = Depends(get_db) ): 
    code_filieres = db.query(models.Filiere).with_entities(distinct(models.Filiere.code)).all()
    code_niveaux = db.query(models.Niveau).with_entities(distinct(models.Niveau.code)).all()
    liste_filieres = []
    liste_niveaux = []
    liste_codes = []
    for i in code_filieres:
        liste_filieres.append(i[0])
    for i in code_niveaux:
        liste_niveaux.append(i[0])
    
    for i in liste_filieres:
        for j in liste_niveaux:
            liste_codes.append(i+j)
            enreg = models.Classe(code=i+j, effectif=0,  niveau=j, code_filiere=i)
            db.add(enreg)
            db.commit()
            db.refresh(enreg)
            
    print(liste_filieres)
    print(liste_niveaux)
    print(liste_codes)
    
    return {"message":"generated"}

@router.get("/all", response_model= List[schemas.ClassResponse])
def display_all_classes(db: Session = Depends(get_db)): 
    classes = db.query(models.Classe).all()
    return classes
    
@router.get("", response_model= schemas.ClassResponse)
def display_a_specific_class(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        classe = db.query(models.Classe).filter(models.Classe.code == code).first()
        if not classe:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La classe ayant pour code << {code} >> n'existe pas ")
        
        return classe
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.delete("")
def delete_a_class(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        user = db.query(models.Classe).filter(models.Classe.code == code)
        if user.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La classe ayant pour code << {code} >> n'existe pas ")
        else:
            user.delete(synchronize_session = False)
            db.commit()
            return {"message": f"Le classe ayant pour code << {code} >> est supprimé avec succes"}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.put("", response_model=schemas.ClassResponse)
def update_a_class(code: str, activity: schemas.ClassCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        response = db.query(models.Classe).filter(models.Classe.code == code)
        if response.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Il n'existe aucune classe ayant pour code << {code} >>")
        response.update(activity.dict(),synchronize_session=False)
        db.commit()
        return activity
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Administrateur peut realiser cette tache.")

@router.get("/all/{code_filiere}", response_model= List[schemas.ClassResponse])
def display_all_classes_of_specified_filiere(code_filiere: str, db: Session = Depends(get_db)): 
    classes = db.query(models.Classe).filter(models.Classe.code_filiere == code_filiere).all()
    return classes

