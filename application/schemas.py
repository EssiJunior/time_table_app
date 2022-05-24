from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

#--------------------------------- Admin's Dashbord ---------------------------------#
class CourseCreate(BaseModel):
    code: str 
    semester: str 
    title: bool
    
class CourseResponse(CourseCreate):
    ...

class AdminCreate(BaseModel):
    login: str
    mot_de_passe: str

class AdminResponse(BaseModel):
    message: str
    class Config:
        orm_mode = True
        
class AdminLogin(BaseModel):
    login: str
    password: str
#--------------------------------- Teacher's Dashbord  ---------------------------------#
class TeacherCreate(BaseModel):
    matricule: str
    nom: str
    password: str
    login: str
    
class TeacherResponse(BaseModel):
    nom: str
    login: str
    created_at: datetime
    class Config:
        orm_mode = True
        
class TeacherLogin(BaseModel):
    login: str
    password: str
#--------------------------------------------------------------------------#

class UserLoginValidation(BaseModel):
    email: EmailStr
    
    class Config:
        orm_mode = True

#--------------------------------- Utils  ---------------------------------#

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: str

class TokenData(BaseModel):
    id: Optional[str] = None