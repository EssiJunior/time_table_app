from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime, time
from sqlalchemy import distinct

router = APIRouter(
    prefix="/timetable/course",
    tags=["To program (association) management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.ToProgramCreateResponse)
def create_a_programmation(programmation: schemas.ToProgramCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        requete = db.query(models.Programmer).join(models.PlageHoraire).filter(
                models.Programmer.code_salle == programmation.code_salle,
                models.Programmer.nom_jour == programmation.nom_jour,
                models.PlageHoraire.heure_debut == programmation.heure_debut
                )
        print(requete)
        if requete.first() == None:
            id_plage = db.query(models.PlageHoraire).filter(models.PlageHoraire.heure_debut 
                == programmation.heure_debut, models.PlageHoraire.heure_fin 
                == programmation.heure_fin).with_entities(
                    distinct(models.PlageHoraire.id_plage)).first()
            if id_plage == None:
                raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail="La plage horaire specifiée n'existe pas")
            else:
                programmation = models.Programmer(code_cours=programmation.code_cours,id_plage=id_plage[0],
                code_salle=programmation.code_salle, nom_jour=programmation.nom_jour)
                db.add(programmation)
                db.commit()
                db.refresh(programmation)
                return {"code_cours":programmation.code_cours, "id_plage":programmation.id_plage,
                "code_salle":programmation.code_salle, "nom_jour":programmation.nom_jour,"created_at": datetime.now()}
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Programmation impossible")
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/all", status_code = status.HTTP_200_OK, response_model= List[schemas.ToProgramResponse])
def display_all_programmations(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):    
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmations = db.query(models.Programmer).all()
        return programmations
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/{code_cours}", status_code = status.HTTP_200_OK, response_model= schemas.ToProgramResponse)
def display_a_specific_programmation(code_cours: str, id_plage:int, code_salle:str
        ,nom_jour:str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmation = db.query(models.Programmer).filter(models.Programmer.code_cours == code_cours
        , models.Programmer.id_plage == id_plage , models.Programmer.code_salle == code_salle
        , models.Programmer.nom_jour == nom_jour)
        if not programmation:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"""la programmation ayant pour code << {code_cours} >> 
                    dans la salle << {code_salle} >> {nom_jour} est supprimé avec succes.""")
        
        return programmation
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.delete("/{code_cours}", status_code = status.HTTP_200_OK)
def delete_a_programmation(code_cours: str, id_plage:int, code_salle:str
        ,nom_jour:str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmation = db.query(models.Programmer).filter(models.Programmer.code_cours == code_cours
        , models.Programmer.id_plage == id_plage , models.Programmer.code_salle == code_salle
        , models.Programmer.nom_jour == nom_jour)
        if programmation.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"""la programmation ayant pour code << {code_cours} >> 
                    dans la salle << {code_salle} >> {nom_jour} est supprimé avec succes.""")
        else:
            programmation.delete(synchronize_session = False)
            db.commit()
            return {"message": f"""la programmation ayant pour code << {code_cours} >> 
                    dans la salle << {code_salle} >> {nom_jour} est supprimé avec succes."""}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.put("", response_model=schemas.ToProgramResponse)
def update_a_programmation(code_cours: str, heure_debut:time, heure_fin:time, code_salle:str
        ,nom_jour:str, programmation: schemas.ToProgramCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        id_plage = db.query(models.PlageHoraire).filter(models.PlageHoraire.heure_debut 
                == programmation.heure_debut, models.PlageHoraire.heure_fin 
                == programmation.heure_fin).with_entities(
                    distinct(models.PlageHoraire.id_plage)).first()
        if id_plage == None:
            raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail="La plage horaire specifiée n'existe pas")
        else:
            response = db.query(models.Programmer).filter(models.Programmer.code_cours == code_cours
            , models.Programmer.id_plage == id_plage , models.Programmer.code_salle == code_salle
            , models.Programmer.nom_jour == nom_jour)
        
            if response.first() == None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Il n'existe aucun cours ayant pour code << {code_cours} >>")
            
            response.update(programmation.dict(),synchronize_session=False)
            db.commit()
            return programmation
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Administrateur peut realiser cette tache.")

@router.get("/teacher/all/{matricule}", response_model= List[schemas.ToProgramCourseResponse])
def display_all_programmations_for_specific_teacher(matricule:str, 
    db: Session = Depends(get_db),current_user: models.Administrateur=Depends(oauth2.get_current_user)):    
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmations = db.query(models.Programmer).join(models.Cours).filter(
            models.Programmer.code_cours == models.Cours.code,
            models.Cours.matricule_enseignant == matricule).all()
        return programmations
    
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/room/all/{code}", response_model= List[schemas.ToProgramRoomResponse])
def display_all_programmations_for_specific_room(code:str, 
    db: Session = Depends(get_db),current_user: models.Administrateur=Depends(oauth2.get_current_user)):    
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmations = db.query(models.Programmer).join(models.Salle).filter(
            models.Programmer.code_salle == models.Salle.code,models.Salle.code == code).all()
        print(db.query(models.Programmer).join(models.Salle).filter(models.Salle.code == code))
        return programmations
    
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")
