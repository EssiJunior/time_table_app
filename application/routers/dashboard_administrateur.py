from fastapi import status, Depends , HTTPException, Response, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from datetime import datetime
from typing import List 
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="",
    tags=["Admin's Dashbord"]
)

@router.post("/create_admin", status_code = status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
def createAdmin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hashed(admin.mot_de_passe)
    admin.mot_de_passe = hashed_password
    admin = models.Administrateur(**admin.dict())
    db.add(admin)
    db.commit()
    print(admin)
    db.refresh(admin)
    print(admin)
    message = f"Administrator: {admin} /nStatus: Registered"
    return {"message": message}
    
@router.post("/login_admin", response_model=schemas.TokenResponse)
def login(user_log: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Administrateur).filter(models.Administrateur.login == user_log.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vous n'avez pas de compte")

    if not utils.verified(user_log.password, user.mot_de_passe):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mot de passe incorrect")

    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "Bearer", "date": datetime.now()}


@router.post("/registerTeacher", status_code = status.HTTP_201_CREATED, response_model=schemas.TeacherResponse)
def createUser(teacher: schemas.TeacherCreate,db: Session = Depends(get_db) ):
    #hash the password
    
    hashed_password = utils.hashed(teacher.password)
    teacher.password = hashed_password
    user = models.Enseignant(**teacher.dict())
    db.add(user)
    db.commit()
    print(user)
    db.refresh(user)
    print(user)
    return user


@router.get("/showTeachers", response_model= List[schemas.TeacherResponse])
def getUsers(db: Session = Depends(get_db)):    
    users = db.query(models.Enseignant).all()
    
    return users

@router.get("/showUser/{identifier}", response_model= schemas.TeacherResponse)
def getSpecificUser(identifier: int, db: Session = Depends(get_db)):
    user = db.query(models.Enseignant).filter(models.Enseignant.id == identifier).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"L'utilisateur ayant comme identifiant << {identifier} >> n'existe pas ")
    
    return user

@router.delete("/deleteUser/{identifier}")
def deleteUser(identifier: int, db: Session = Depends(get_db)):
    user = db.query(models.Enseignant).filter(models.Enseignant.id == identifier).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"L'utilisateur ayant comme identifiant << {identifier} >> n'existe pas ")
    else:
        user.delete()
        return {"message": f"user with id: {identifier} deleted!"}