from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

#--------------------------------- Admin's Dashbord ---------------------------------#
class TeacherCreate(BaseModel):
    matricule: str
    nom: str

class TeacherResponse(BaseModel):
    nom: str
    login: str
    password: str
    created_at: datetime
    class Config:
        orm_mode = True
class CourseCreate(BaseModel):
    code: str 
    semester: str 
    title: bool
    
class CourseResponse(CourseCreate):
    ...
    class Config:
        orm_mode = True

class AdminCreate(BaseModel):
    login: str
    mot_de_passe: str

class AdminResponse(BaseModel):         
    login: str
    status: str
    class Config:
        orm_mode = True



#------------------------------------------------------------------------------------#
#--------------------------------- Teacher's Dashbord  ---------------------------------#
    
        
#--------------------------------------------------------------------------#

class UserLoginValidation(BaseModel):
    email: EmailStr
    
    class Config:
        orm_mode = True

#--------------------------------- Utils  ---------------------------------#

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: str

class TokenData(BaseModel):
    id: Optional[str] = None