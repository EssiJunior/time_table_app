from fastapi import APIRouter

from datetime import datetime
from fastapi import status, Depends , HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from application import models, utils, oauth2, schemas
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/login",
    tags=["Authentification"]
)

@router.post("/", response_model=schemas.Token)
def login(user_log: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Utilisateur).filter(models.Utilisateur.email == user_log.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vous n'avez pas de compte")

    if not utils.verified(user_log.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mot de passe incorrect")

    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer", "date": datetime.now()}