from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/to_program",
    tags=["To program (association) management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.ToProgramCreateResponse)
def create_a_programmation(programmation: schemas.ToProgramCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmation = models.Programmer(code_classe=programmation.code_classe,code_cours=programmation.code_cours,
                matricule_enseignant=programmation.matricule_enseignant, id_plage=programmation.id_plage,
                code_salle=programmation.code_salle, nom_jour=programmation.nom_jour)
        db.add(programmation)
        db.commit()
        db.refresh(programmation)
        return {"code_classe":programmation.code_classe,"code_cours":programmation.code_cours,
                "matricule_enseignant":programmation.matricule_enseignant, "id_plage":programmation.id_plage,
                "code_salle":programmation.code_salle, "nom_jour":programmation.nom_jour,"created_at": datetime.now()}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/all", response_model= List[schemas.ToProgramResponse])
def display_all_programmations(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):    
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmations = db.query(models.Programmer).all()
        return programmations
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/{matricule_enseignant}", response_model= schemas.ToProgramResponse)
def display_a_specific_programmation(matricule_enseignant: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmation = db.query(models.Programmer).filter(models.Programmer.matricule_enseignant == matricule_enseignant).first()
        
        if not programmation:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La programmation ayant pour enseignant << {matricule_enseignant} >> n'existe pas ")
        
        return programmation
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.delete("/{matricule_enseignant}")
def delete_a_programmation(matricule_enseignant: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmation = db.query(models.Programmer).filter(models.Programmer.matricule_enseignant == matricule_enseignant)
        if programmation.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"La programmation ayant pour enseignant << {matricule_enseignant} >> n'existe pas ")
        else:
            programmation.delete(synchronize_session = False)
            db.commit()
            return {"message": f"la programmation ayant pour enseignant << {matricule_enseignant} >> est supprimé avec succes."}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")
