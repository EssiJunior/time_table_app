from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from .database import engine, get_db
from . import models, schemas, oauth2, utils
from .routers import (teacher, room, course_period, speciality, day,
        course_type, course, classe, level, filiere, to_program, activity)

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

#from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
#from starlette.requests import Request
#from starlette.responses import JSONResponse
#from typing import List
#from pydantic import EmailStr, BaseModel

models.Base.metadata.create_all(bind=engine) # Creation de la base de donnees

origins = ["*"]
app = FastAPI()
def custom_openapi(): #     Swagger UI customization
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="time-table-app",
        version="1.0",
        description="INF 3036 group 14 project",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"] 
)
app.include_router(filiere.router)
app.include_router(day.router)
app.include_router(level.router)
app.include_router(course_period.router)
app.include_router(room.router)
app.include_router(course_type.router)
app.include_router(classe.router)
app.include_router(teacher.router)
app.include_router(activity.router)
app.include_router(speciality.router)
app.include_router(course.router)
app.include_router(to_program.router)


@app.get("/")
def root():
    return {"message": "Hello world, by the BI-deployer... Lock functionality OK!"}

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

#@app.post("/logout")
# def logout(token: TokenData)
@app.post("/admin", status_code = status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
def create_an_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hashed(admin.mot_de_passe)
    admin.mot_de_passe = hashed_password
    admin = models.Administrateur(**admin.dict())
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    return {"login":admin.login, "status": "Registered"}

#class EmailSchema(BaseModel):
#    email: List[EmailStr]

#conf = ConnectionConfig(
#    MAIL_FROM="essijunior19@gmail.com",
#    MAIL_USERNAME="Junior Essi",
#    MAIL_PASSWORD="jr192020",
#    MAIL_PORT=587,
#    MAIL_SERVER="smtp.gmail.com",
#    MAIL_TLS=True,
#    MAIL_SSL=False,
#    USE_CREDENTIALS = True,
#    VALIDATE_CERTS = True
#)

#@app.post("/send_mail")
#async def send_mail(email: EmailSchema):
#	template = """
#		<html>
#		<body>
##		

#<p>Hi !!!
#		<br>Thanks for using fastapi mail, keep using it..!!!</p>
#

#		</body>
#		</html>
#		"""

#	message = MessageSchema(
#		subject="Fastapi-Mail module",
#		recipients=email.dict().get("email"), # List of recipients, as many as you can pass
#		body=template,
#		subtype="html"
#		)

#	fm = FastMail(conf)
#	await fm.send_message(message)
#	print(message)

	

#	return JSONResponse(status_code=200, content={"message": "email has been sent"})
