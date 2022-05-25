from fastapi import status, Depends , HTTPException, APIRouter
from .. import models, schemas, utils
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/teacher",
    tags=["Teachers management"]
)



@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.TeacherCreateResponse)
def create_a_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db) ):
    password = utils.password_generated()
    login = utils.login_generated(teacher.matricule)
    utils.store_teachers_in_file(teacher.nom, login, password)
    
    hashed_password = utils.hashed(password)
    password = hashed_password
    teacher = models.Enseignant(matricule=teacher.matricule, nom=teacher.nom, mot_de_passe=password, login=login)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    
    return {"nom":teacher.nom, "login":login, "password": password, "created_at": datetime.now()}


@router.get("", response_model= List[schemas.TeacherResponse])
def display_all_teachers(db: Session = Depends(get_db)):    
    teachers = db.query(models.Enseignant).all()
    
    return teachers

@router.get("/{matricule}", response_model= schemas.TeacherResponse)
def display_a_specific_teacher(matricule: str, db: Session = Depends(get_db)):
    teacher = db.query(models.Enseignant).filter(models.Enseignant.matricule == matricule).first()
    if not teacher:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucun enseignant immatriculé << {matricule} >>")
    
    return teacher

@router.delete("/{matricule}")
def delete_a_teacher(matricule: str, db: Session = Depends(get_db)):
    user = db.query(models.Enseignant).filter(models.Enseignant.matricule == matricule)
    if user.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Aucun enseignant immatriculé << {matricule} >>")
    else:
        user.delete(synchronize_session = False)
        db.commit()
        return {"message": f"L'enseignant ayant comme matricule: {matricule} est supprimé avec succes"}
    