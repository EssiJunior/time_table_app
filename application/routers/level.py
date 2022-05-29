from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/level",
    tags=["Level management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.LevelResponse)
def create_a_level(level: schemas.LevelCreate, db: Session = Depends(get_db) ,
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        level = models.Niveau(numero=level.numero)
        db.add(level)
        db.commit()
        db.refresh(level)
        return {"numero":level.numero}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")


@router.get("", response_model= List[schemas.LevelResponse])
def display_all_levels(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):   
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        levels = db.query(models.Niveau).all()
        return levels
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/{numero}", response_model= schemas.LevelResponse)
def display_a_specific_level(numero: int, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        level = db.query(models.Niveau).filter(models.Niveau.numero == numero).first()
        if not level:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La niveau << {numero} >> n'existe pas ")
        
        return level
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.delete("/{numero}")
def delete_a_level(numero: int, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        level = db.query(models.Niveau).filter(models.Niveau.numero == numero)
        if level.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La niveau << {numero} >> n'existe pas ")
        else:
            level.delete(synchronize_session = False)
            db.commit()
            return {"message": f"Le niveau << {numero} >> est supprimé avec succes"}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")