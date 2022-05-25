from pydantic import BaseModel, EmailStr
from datetime import datetime, time
from typing import Optional

#---------------------------------- Main operations ----------------------------------#
class AdminCreate(BaseModel):
    login: str
    mot_de_passe: str

class AdminResponse(BaseModel):         
    login: str
    status: str
    class Config:
        orm_mode = True
        
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None
#---------------------------------------------------------------------------------------#
#--------------------------------- Teacher management  ---------------------------------#
class TeacherCreate(BaseModel):
    matricule: str
    nom: str

class TeacherCreateResponse(BaseModel):
    nom: str
    login: str
    password: str
    created_at: datetime
    class Config:
        orm_mode = True

class TeacherResponse(TeacherCreate):
    ...
    class Config:
        orm_mode = True
        
#--------------------------------------------------------------------------------------#
#--------------------------------- Room management  ---------------------------------#
class RoomCreate(BaseModel):
    code: str 
    effectif: int 
    
class RoomCreateResponse(RoomCreate):
    created_at: datetime
    class Config:
        orm_mode = True

class RoomResponse(RoomCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Course's hour management  ---------------------------------#
class CoursePeriodCreate(BaseModel):
    heure_debut: time 
    heure_fin: time 
    
class CoursePeriodResponse(CoursePeriodCreate):
    id_plage: int
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Speciality management  ---------------------------------#
class SpecialityCreate(BaseModel):
    nom: str 
    effectif: int 
    
class SpecialityResponse(SpecialityCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Course management  ---------------------------------#
class CourseCreate(BaseModel):
    code: str 
    semester: str 
    title: bool
    
class CourseResponse(CourseCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
class UserLoginValidation(BaseModel):
    email: EmailStr
    
    class Config:
        orm_mode = True

#--------------------------------- Utils  ---------------------------------#
