from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime, time
from sqlalchemy import distinct, text

router = APIRouter(
    prefix="/timetable/course",
    tags=["To program (association) management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.ToProgramCreateResponse)
def create_a_programmation(programmation: schemas.ToProgramCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        requete = db.query(models.Programmer).join(models.PlageHoraire).join(models.Salle).filter(models.Programmer.nom_jour==programmation.nom_jour, models.PlageHoraire.heure_debut == programmation.heure_debut, models.Salle.code == programmation.code_salle)
        print(requete)
        if requete.first() == None:
            duree = db.query(models.Cours).join(models.TypeSeance).filter(models.Cours.id == programmation.id_cours).with_entities(
                    distinct(models.TypeSeance.duree)).first()
            print(duree[0])
            t1 = datetime.strptime(str(programmation.heure_debut), '%H:%M:%S')
            t2 = datetime.strptime(str(duree[0]), '%H:%M:%S')
            time_zero = datetime.strptime('00:00:00', '%H:%M:%S')
            heureF = (t1 - time_zero + t2).time() 
            print(heureF)
            creation_de_plage = models.PlageHoraire(heure_debut=programmation.heure_debut,
                            heure_fin=heureF)
            db.add(creation_de_plage)
            db.commit()
            db.refresh(creation_de_plage)
            requete = models.Programmer(id_cours=programmation.id_cours,id_plage=creation_de_plage.id_plage,
            code_salle=programmation.code_salle, nom_jour=programmation.nom_jour)
            db.add(requete)
            db.commit()
            db.refresh(requete)
            
            return {"id_cours":programmation.id_cours, "heure_debut":programmation.heure_debut, "heure_fin":creation_de_plage.heure_fin,
                "code_salle":programmation.code_salle, "nom_jour":programmation.nom_jour,"created_at": datetime.now()}
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Programmation impossible car un cours la possède déjà")
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/all", status_code = status.HTTP_200_OK, response_model= List[schemas.ToProgramResponse])
def display_all_programmations(db: Session = Depends(get_db)): 
    programmations = db.query(models.Programmer).all()
    return programmations

@router.get("/", status_code = status.HTTP_200_OK, response_model= schemas.ToProgramResponse)
def display_a_specific_programmation(id_cours: str, id_plage:int, code_salle:str
        ,nom_jour:str, db: Session = Depends(get_db)):
    programmation = db.query(models.Programmer).filter(models.Programmer.id_cours == id_cours
        , models.Programmer.id_plage == id_plage , models.Programmer.code_salle == code_salle
        , models.Programmer.nom_jour == nom_jour)
    if not programmation:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"""la programmation ayant pour code << {id_cours} >> 
                dans la salle << {code_salle} >> {nom_jour} est supprimé avec succes.""")
        
    return programmation

@router.delete("/", status_code = status.HTTP_200_OK)
def delete_a_programmation(id_cours: str, id_plage:int, code_salle:str
        ,nom_jour:str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        programmation = db.query(models.Programmer).filter(models.Programmer.id_cours == id_cours
        , models.Programmer.id_plage == id_plage , models.Programmer.code_salle == code_salle
        , models.Programmer.nom_jour == nom_jour)
        if programmation.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"""la programmation ayant pour code << {id_cours} >> 
                    dans la salle << {code_salle} >> {nom_jour} est supprimé avec succes.""")
        else:
            programmation.delete(synchronize_session = False)
            db.commit()
            return {"message": f"""la programmation ayant pour code << {id_cours} >> 
                    dans la salle << {code_salle} >> {nom_jour} est supprimé avec succes."""}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.put("", response_model=schemas.ToProgramResponse)
def update_a_programmation(id_cours: str, heure_debut:time, heure_fin:time, code_salle:str
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
            response = db.query(models.Programmer).filter(models.Programmer.id_cours == id_cours
            , models.Programmer.id_plage == id_plage[0] , models.Programmer.code_salle == code_salle
            , models.Programmer.nom_jour == nom_jour)
        
            if response.first() == None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Il n'existe aucun cours ayant pour code << {id_cours} >>")
            
            response.update(programmation.dict(),synchronize_session=False)
            db.commit()
            return programmation
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Administrateur peut realiser cette tache.")

@router.get("/teacher/all")
def display_all_programmations_for_specific_teacher(matricule:str, semestre:int,
    db: Session = Depends(get_db)):    

    #requete = db.query(models.Enseignant).join(models.Cours).join(models.Programmer).join(models.#Salle).join(models.Jour).join(models.PlageHoraire)
    #requete = db.query(models.Programmer, models.Classe, models.Cours, models.PlageHoraire, models.#Jour, models.Salle).filter( models.Programmer.id_cours == .id, models.Programmer.id_plage == #models.PlageHoraire.id_plage, models.Programmer.code_salle == models.Salle.code, models.Cours.#code_classe == models.Classe.code, models.Cours.matricule_enseignant == matricule)
    #print(requete)
    
    statement = text("""SELECT *
                        FROM enseignant, cours
                        WHERE matricule = matricule_enseignant
                """)
    results = db.execute(statement)
    #programmations = requete.all()
    return results


@router.get("/room/all", response_model= List[schemas.TimeTableResponse])
def display_all_programmations_for_specific_room(code:str, db: Session = Depends(get_db)):    
    requete = db.query(models.Programmer, models.Classe, models.Cours, models.PlageHoraire, models.Jour, models.Salle).filter( models.Programmer.id_cours == models.Cours.id, models.Programmer.id_plage == models.PlageHoraire.id_plage, models.Programmer.code_salle == models.Salle.code, models.Cours.code_classe == models.Classe.code, models.Salle.code == code)
    print(requete)
    programmations = requete.all()
    return programmations
    
