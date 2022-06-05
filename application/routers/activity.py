from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy import distinct
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/timetable/activity",
    tags=["Activity (association) management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.ActivityCreateResponse)
def create_an_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user) ):  
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        id_plage = db.query(models.PlageHoraire).filter(models.PlageHoraire.heure_debut 
                == activity.heure_debut, models.PlageHoraire.heure_fin 
                == activity.heure_fin ).with_entities(distinct(models.PlageHoraire.id_plage)).first()
        
        if id_plage == None:
            raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail="La plage horaire specifiée n'existe pas")
        else:
            activity = models.Activite(nom=activity.nom, date_act=activity.date_act, matricule_enseignant=activity.matricule_enseignant,
                id_plage=id_plage, code_salle=activity.code_salle, nom_jour=activity.nom_jour)
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
def display_a_specific_activity(matricule_enseignant: str, id_plage:int, code_salle:str
        ,nom_jour:str, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        activity = db.query(models.Activite).filter(models.Activite.matricule_enseignant == matricule_enseignant
        and models.Activite.id_plage == id_plage and models.Activite.code_salle == code_salle and
        models.Activite.nom_jour == nom_jour)
        if not activity:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"L'activité programmé {nom_jour} à {code_salle} par {matricule_enseignant} n'existe pas ")
        
        return activity
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Enseignant peut realiser cette tache.")

@router.delete("")
def delete_a_activity(matricule_enseignant: str, id_plage:int, code_salle:str
        ,nom_jour:str, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        activity = db.query(models.Activite).filter(models.Activite.matricule_enseignant == matricule_enseignant
        and models.Activite.id_plage == id_plage and models.Activite.code_salle == code_salle and
        models.Activite.nom_jour == nom_jour)
        if activity.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"L'activité programmé {nom_jour} à {code_salle} par {matricule_enseignant} n'existe pas ")
        else:
            activity.delete(synchronize_session = False)
            db.commit()
            return {"message": f"L'activité programmé {nom_jour} à {code_salle} par {matricule_enseignant} est supprimé avec succes."}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Enseignant peut realiser cette tache.")

@router.put("", response_model=schemas.ActivityResponse)
def update_an_activity(matricule_enseignant: str, id_plage:int, code_salle:str
        ,nom_jour:str, activity: schemas.ActivityCreate, db: Session = Depends(get_db),
        current_user: models.Enseignant=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Enseignant):
        response = db.query(models.Activite).filter(models.Activite.matricule_enseignant == matricule_enseignant
        and models.Activite.id_plage == id_plage and models.Activite.code_salle == code_salle and
        models.Activite.nom_jour == nom_jour)
        if response.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucune activité programmé {nom_jour} à {code_salle} par {matricule_enseignant}")
        response.update(activity.dict(),synchronize_session=False)
        db.commit()
        return activity
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Enseignant peut realiser cette tache.")
