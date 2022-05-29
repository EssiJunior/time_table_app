from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, oauth2
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/course_type",
    tags=["Course type management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.CourseTypeResponse)
def create_a_course_type(course_type: schemas.CourseTypeCreate, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user) ):  
    course_type = models.TypeSeance(nom=course_type.nom, duree=course_type.duree)
    db.add(course_type)
    db.commit()
    db.refresh(course_type)
    
    print("Current Administrator: ",current_user.login)
    return {"nom": course_type.nom, "duree": course_type.duree}


@router.get("", response_model= List[schemas.CourseTypeResponse])
def display_all_course_types(db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):    
    course_type = db.query(models.TypeSeance).all()
    
    print("Current Administrator: ",current_user.login)
    return course_type

@router.get("/{nom}", response_model= schemas.CourseTypeResponse)
def display_a_specific_course_type(nom: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current Administrator: ",current_user.login)
    
    course_type = db.query(models.TypeSeance).filter(models.TypeSeance.nom == nom).first()
    if not course_type:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucun  type de seance intitulée << {nom} >>")
    
    return course_type

@router.delete("/{nom}")
def delete_a_course_type(nom: str, db: Session = Depends(get_db),
        current_user: models.Administrateur=Depends(oauth2.get_current_user)):
    print("Current Administrator: ",current_user.login)
    
    course_type = db.query(models.TypeSeance).filter(models.TypeSeance.nom == nom)
    if course_type.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucun  type de seance intitulée << {nom} >>")
    else:
        course_type.delete(synchronize_session = False)
        db.commit()
        return {"message": f"le type de seance << {nom} >> est supprimé avec succes."}
    