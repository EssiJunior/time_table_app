from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/class",
    tags=["Class management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.ClassResponse)
def create_a_class(classe: schemas.ClassCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user_if_teacher) ):
    classe = models.Classe(code=classe.code, effectif=classe.effectif,  niveau=classe.niveau, code_filiere=classe.code_filiere)
    db.add(classe)
    db.commit()
    db.refresh(classe)
    
    print("Current Administrator: ",current_user.login)
    return {"code":classe.code,"effectif":classe.effectif, "niveau":classe.niveau, "code_filiere":classe.code_filiere}


@router.get("", response_model= List[schemas.ClassResponse])
def display_all_classes(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user_if_teacher)):    
    classes = db.query(models.Classe).all()
    
    print("Current Administrator: ",current_user.login)
    return classes

@router.get("/{code}", response_model= schemas.ClassResponse)
def display_a_specific_class(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user_if_teacher)):
    print("Current Administrator: ",current_user.login)
    
    classe = db.query(models.Classe).filter(models.Classe.code == code).first()
    if not classe:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La classe ayant pour code << {code} >> n'existe pas ")
    
    return classe

@router.delete("/{code}")
def delete_a_class(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user_if_teacher)):
    print("Current Administrator: ",current_user.login)
    
    user = db.query(models.Classe).filter(models.Classe.code == code)
    if user.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La classe ayant pour code << {code} >> n'existe pas ")
    else:
        user.delete(synchronize_session = False)
        db.commit()
        return {"message": f"Le classe ayant pour code << {code} >> est supprimé avec succes"}
    