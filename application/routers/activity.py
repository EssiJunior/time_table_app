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
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        activity = models.Activite(nom=activity.nom, date_act=activity.date_act, matricule_enseignant=activity.matricule_enseignant,
                id_plage=activity.id_plage, code_salle=activity.code_salle, nom_jour=activity.nom_jour)
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return {"nom":activity.nom, "date_act": activity.date_act,"matricule_enseignant":activity.matricule_enseignant, "id_plage":activity.id_plage,
                "code_salle":activity.code_salle, "nom_jour":activity.nom_jour,"created_at": datetime.now()}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Enseignant peut realiser cette tache.")


@router.get("/all", response_model= List[schemas.ActivityResponse])
def display_all_activities(db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        activitys = db.query(models.Activite).all()
        return activitys
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Enseignant peut realiser cette tache.")

@router.get("", response_model= schemas.ActivityResponse)
def display_a_specific_activity(nom: str, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        activity = db.query(models.Activite).filter(models.Activite.nom == nom).first()
        if not activity:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"L'activité << {nom} >> n'existe pas ")
        
        return activity
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Enseignant peut realiser cette tache.")

@router.delete("")
def delete_a_activity(nom: str, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        activity = db.query(models.Activite).filter(models.Activite.nom == nom)
        if activity.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"L'activité  << {nom} >> n'existe pas ")
        else:
            activity.delete(synchronize_session = False)
            db.commit()
            return {"message": f"l'activité ayant << {nom} >> est supprimé avec succes."}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Enseignant peut realiser cette tache.")

@router.put("", response_model=schemas.ActivityResponse)
def update_an_activity(nom: str, activity: schemas.ActivityCreate, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        response = db.query(models.Activite).filter(models.Activite.nom == nom)
        if response.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucune activité intitulée << {nom} >>")
        response.update(activity.dict(),synchronize_session=False)
        db.commit()
        return activity
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Enseignant peut realiser cette tache.")
