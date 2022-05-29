from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/activity",
    tags=["Activity (association) management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.ActivityCreateResponse)
def create_an_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user) ):  
    activity = models.Activite(nom=activity.nom,matricule_enseignant=activity.matricule_enseignant,
            id_plage=activity.id_plage, code_salle=activity.code_salle, nom_jour=activity.nom_jour)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    print("Current Teacher: ",current_user.nom)
    return {"nom":activity.nom, "matricule_enseignant":activity.matricule_enseignant, "id_plage":activity.id_plage,
            "code_salle":activity.code_salle, "nom_jour":activity.nom_jour,"created_at": datetime.now()}


@router.get("", response_model= List[schemas.ActivityResponse])
def display_all_activities(db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):    
    activitys = db.query(models.Activite).all()
    
    print("Current Teacher: ",current_user.nom)
    return activitys

@router.get("/{nom}", response_model= schemas.ActivityResponse)
def display_a_specific_activity(nom: str, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):
    print("Current Teacher: ",current_user.nom)
    
    activity = db.query(models.Activite).filter(models.Activite.nom == nom).first()
    if not activity:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"L'activité << {nom} >> n'existe pas ")
    
    return activity

@router.delete("/{nom}")
def delete_a_activity(nom: str, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):
    print("Current Teacher: ",current_user.nom)
    
    activity = db.query(models.Activite).filter(models.Activite.nom == nom)
    if activity.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"L'activité  << {nom} >> n'existe pas ")
    else:
        activity.delete(synchronize_session = False)
        db.commit()
        return {"message": f"l'activité ayant << {nom} >> est supprimé avec succes."}
    