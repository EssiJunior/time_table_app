from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from .database import engine, get_db
from . import models, schemas, oauth2, utils
from .routers import dashboard_administrateur, dashboard_teacher 

models.Base.metadata.create_all(bind=engine)

origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"]
)
app.include_router(dashboard_administrateur.router)
app.include_router(dashboard_teacher.router)

@app.get("/")
def root():
    return {"message": "Hello world, by a deployer"}

@app.post("/login", response_model=schemas.LoginResponse)
def login(user_log: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(models.Administrateur).filter(models.Administrateur.login == user_log.username).first()
    user: str
    
    if not admin:
        teacher = db.query(models.Enseignant).filter(models.Enseignant.login == user_log.username).first()
        if not teacher:    
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=utils.no_account())
        else:
            if not utils.verified(user_log.password, teacher.mot_de_passe):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=utils.incorrect_pass())
            access_token = oauth2.create_access_token(data= {"user_id": teacher.login})
            user = "Enseignant"
            return {"access_token": access_token, "token_type": "Bearer", "user": user}
    else:    
        if not utils.verified(user_log.password, admin.mot_de_passe):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=utils.incorrect_pass())
        access_token = oauth2.create_access_token(data= {"user_id": admin.login})
        user = "Administrateur"
        return {"access_token": access_token, "token_type": "Bearer", "user": user}

