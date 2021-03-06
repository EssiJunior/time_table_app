from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy import insert
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/filiere",
    tags=["Filiere management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.FiliereCreateResponse)
def create_a_filiere(filiere: schemas.FiliereCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ):   
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        filiere = models.Filiere(code=filiere.code, nom=filiere.nom)
        db.add(filiere)
        db.commit()
        db.refresh(filiere)
        
        return {"code": filiere.code, "nom":filiere.nom,
                "created_at": datetime.now()}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")


@router.get("/all", response_model= List[schemas.FiliereAllResponse], status_code=status.HTTP_200_OK)
def display_all_filieres(db: Session = Depends(get_db)):  
    filieres = db.query(models.Filiere).all()
    return filieres

@router.get("", response_model= schemas.FiliereResponse, status_code=status.HTTP_200_OK)
def display_a_specific_filiere(code: str, db: Session = Depends(get_db)): 
    filiere = db.query(models.Filiere).filter(models.Filiere.code == code).first()
    if not filiere:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La Filiere codée << {code} >> n'existe pas ")
        
    return {"code": filiere.code, "nom":filiere.nom}

@router.delete("", status_code=status.HTTP_200_OK)
def delete_a_filiere(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        filiere = db.query(models.Filiere).filter(models.Filiere.code == code)
        if filiere.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La filiere codée << {code} >> n'existe pas ")
        else:
            filiere.delete(synchronize_session = False)
            db.commit()
            return {"message": f"la filiere codée << {code} >> est supprimé avec succes.",
            }
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.put("", response_model=schemas.FiliereResponse, status_code=status.HTTP_200_OK)
def update_a_filiere(code: str, filiere: schemas.FiliereCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        response = db.query(models.Filiere).filter(models.Filiere.code == code)
        if response.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Il n'existe aucune Filiere ayant pour code << {code} >>")
        response.update(filiere.dict(),synchronize_session=False)
        db.commit()
        return {"code": filiere.code, "nom":filiere.nom,
                "created_at": datetime.now()}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Administrateur peut realiser cette tache.")
