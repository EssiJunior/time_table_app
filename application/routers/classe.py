from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, utils
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/class",
    tags=["Class management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.ClassResponse)
def create_a_class(classe: schemas.ClassCreate, db: Session = Depends(get_db) ):
    classe = models.Classe(code=classe.code, effectif=classe.effectif,  nom_specialite=classe.nom_specialite)
    db.add(classe)
    db.commit()
    db.refresh(classe)
    
    return {"code":classe.code,"effectif":classe.effectif, "nom_specialite":classe.nom_specialite}


@router.get("", response_model= List[schemas.ClassResponse])
def display_all_classes(db: Session = Depends(get_db)):    
    classes = db.query(models.Classe).all()
    
    return classes

@router.get("/{code}", response_model= schemas.ClassResponse)
def display_a_specific_class(code: str, db: Session = Depends(get_db)):
    classe = db.query(models.Classe).filter(models.Classe.code == code).first()
    if not classe:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La classe ayant pour code << {code} >> n'existe pas ")
    
    return classe

@router.delete("/{code}")
def delete_a_class(code: str, db: Session = Depends(get_db)):
    user = db.query(models.Classe).filter(models.Classe.code == code)
    if user.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La classe ayant pour code << {code} >> n'existe pas ")
    else:
        user.delete(synchronize_session = False)
        db.commit()
        return {"message": f"Le classe ayant pour code << {code} >> est supprimé avec succes"}
    