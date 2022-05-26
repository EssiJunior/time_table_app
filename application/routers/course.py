from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, utils
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/course",
    tags=["Course management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.CourseResponse)
def create_a_course(course: schemas.CourseCreate, db: Session = Depends(get_db) ):
    course = models.Cours(code=course.code, semestre=course.semestre, titre=course.titre, nom_seance=course.nom_seance, code_filiere=course.code_filiere)
    db.add(course)
    db.commit()
    db.refresh(course)
    
    return {"code":course.code,"semestre":course.semestre, "nom_seance":course.nom_seance, "titre": course.titre, "code_filiere":course.code_filiere}


@router.get("", response_model= List[schemas.CourseResponse])
def display_all_courses(db: Session = Depends(get_db)):    
    courses = db.query(models.Cours).all()
    
    return courses

@router.get("/{code}", response_model= schemas.CourseResponse)
def display_a_specific_course(code: str, db: Session = Depends(get_db)):
    course = db.query(models.Cours).filter(models.Cours.code == code).first()
    if not course:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Le cours ayant pour code << {code} >> n'existe pas ")
    
    return course

@router.delete("/{code}")
def delete_a_course(code: str, db: Session = Depends(get_db)):
    user = db.query(models.Cours).filter(models.Cours.code == code)
    if user.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Le cours ayant pour code << {code} >> n'existe pas ")
    else:
        user.delete(synchronize_session = False)
        db.commit()
        return {"message": f"Le cours ayant pour code << {code} >> est supprimé avec succes"}
    