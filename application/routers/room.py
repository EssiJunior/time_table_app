from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/room",
    tags=["Room management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.RoomCreateResponse)
def create_a_room(room: schemas.RoomCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ):  
    room = models.Salle(code=room.code, effectif=room.effectif)
    db.add(room)
    db.commit()
    db.refresh(room)
    
    print("Current Administrator: ",current_user.login)
    return {"code": room.code, "effectif":room.effectif,"created_at": datetime.now()}


@router.get("", response_model= List[schemas.RoomResponse])
def display_all_rooms(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):    
    rooms = db.query(models.Salle).all()
    
    print("Current Administrator: ",current_user.login)
    return rooms

@router.get("/{code}", response_model= schemas.RoomResponse)
def display_a_specific_room(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current Administrator: ",current_user.login)
    
    room = db.query(models.Salle).filter(models.Salle.code == code).first()
    if not room:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La salle << {code} >> n'existe pas ")
    
    return room

@router.delete("/{code}")
def delete_a_room(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current Administrator: ",current_user.login)
    
    room = db.query(models.Salle).filter(models.Salle.code == code)
    if room.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La salle << {code} >> n'existe pas ")
    else:
        room.delete(synchronize_session = False)
        db.commit()
        return {"message": f"la salle << {code} >> est supprimé avec succes."}
    