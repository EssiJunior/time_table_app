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
    code_filiere: str

class TeacherCreateResponse(BaseModel):
    nom: str
    login: str
    password: str
    code_filiere: str
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
    code_classe: str
    
class SpecialityResponse(SpecialityCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Day management  ---------------------------------#
class DayCreate(BaseModel):
    nom: str 
    
class DayResponse(DayCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Course type management  ---------------------------------#
class CourseTypeCreate(BaseModel):
    nom: str 
    duree: time 
    
class CourseTypeResponse(CourseTypeCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Course management  ---------------------------------#
class CourseCreate(BaseModel):
    code: str 
    semestre: int 
    titre: str
    nom_seance: str
    code_filiere: str
    
class CourseResponse(CourseCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Class management  ---------------------------------#
class ClassCreate(BaseModel):
    code: str 
    effectif: int 
    niveau: int
    code_filiere: str
    
class ClassResponse(ClassCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Class management  ---------------------------------#
class LevelCreate(BaseModel):
    numero: int
    
class LevelResponse(LevelCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Filiere management  ---------------------------------#
class FiliereCreate(BaseModel):
    code: str 
    nom: str 
    
class FiliereCreateResponse(FiliereCreate):
    created_at: datetime
    class Config:
        orm_mode = True

class FiliereResponse(FiliereCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- To Program (association) management  ---------------------------------#
class ToProgramCreate(BaseModel):
    code_classe: str 
    code_cours: str 
    matricule_enseignant: str
    id_plage: int
    code_salle: str
    nom_jour: str
    
class ToProgramCreateResponse(ToProgramCreate):
    created_at: datetime
    class Config:
        orm_mode = True

class ToProgramResponse(ToProgramCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Activity (association) management  ---------------------------------#
class ActivityCreate(BaseModel):
    nom: str 
    matricule_enseignant: str
    id_plage: int
    code_salle: str
    nom_jour: str
    
class ActivityCreateResponse(ActivityCreate):
    created_at: datetime
    class Config:
        orm_mode = True

class ActivityResponse(ActivityCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
class UserLoginValidation(BaseModel):
    email: EmailStr
    
    class Config:
        orm_mode = True

#--------------------------------- Utils  ---------------------------------#
