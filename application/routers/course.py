from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/course",
    tags=["Course management"]
)

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.CourseResponse)
def create_a_course(course: schemas.CourseCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        course = models.Cours(code=course.code, semestre=course.semestre, titre=course.titre, id_specialite=course.id_specialite, code_classe=course.code_classe, code_filiere=course.code_filiere, nom_seance=course.nom_seance, matricule_enseignant=course.matricule_enseignant)
        db.add(course)
        db.commit()
        db.refresh(course)
        return {"code":course.code,"semestre":course.semestre, "titre": course.titre, "id_specialite":course.id_specialite, "code_classe":course.code_classe, "code_filiere":course.code_filiere, "nom_seance":course.nom_seance, "matricule_enseignant":course.matricule_enseignant}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("/all", response_model= List[schemas.CourseResponse])
def display_all_courses(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):     
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        courses = db.query(models.Cours).all()
        return courses
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.get("", response_model= schemas.CourseResponse)
def display_a_specific_course(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        course = db.query(models.Cours).filter(models.Cours.code == code).first()
        if not course:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Le cours ayant pour code << {code} >> n'existe pas ")
        return course
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.delete("")
def delete_a_course(code: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)): 
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        user = db.query(models.Cours).filter(models.Cours.code == code)
        if user.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Le cours ayant pour code << {code} >> n'existe pas ")
        else:
            user.delete(synchronize_session = False)
            db.commit()
            return {"message": f"Le cours ayant pour code << {code} >> est supprimé avec succes"}
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un administrateur peut realiser cette tache.")

@router.put("", response_model=schemas.CourseResponse)
def update_a_course(code: str, course: schemas.CourseCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current User: ",type(current_user))
    if isinstance(current_user, models.Administrateur):
        response = db.query(models.Cours).filter(models.Cours.code == code)
        if response.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Il n'existe aucun cours ayant pour code << {code} >>")
        response.update(course.dict(),synchronize_session=False)
        db.commit()
        return course
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Désolé, seul un Administrateur peut realiser cette tache.")
