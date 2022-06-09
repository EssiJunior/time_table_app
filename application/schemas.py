from pydantic import BaseModel, EmailStr
from datetime import datetime, time, date
from typing import Optional, List
from sqlalchemy.orm.query import Query
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
    matricule: str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None
#---------------------------------------------------------------------------------------#
#--------------------------------- Speciality management  ---------------------------------#
class SpecialityCreate(BaseModel):
    nom: str 
    effectif: int 
    code_classe: str
    
class SpecialityResponse(SpecialityCreate):
    id: int
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Class management  ---------------------------------#
class ClassCreate(BaseModel):
    code: str 
    effectif: int 
    niveau: str
    code_filiere: str
    
class ClassResponse(ClassCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Level management  ---------------------------------#
class LevelCreate(BaseModel):
    code: str
    
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
    
    class Config:
        orm_mode = True

class FiliereAllResponse(FiliereCreate):
    ...
    class Config:
        orm_mode = True
#--------------------------------------------------------------------------------------#
#--------------------------------- Course management  ---------------------------------#
class CourseCreate(BaseModel):
    code: str 
    semestre: int 
    titre: str
    id_specialite: int
    code_classe: str
    code_filiere: str
    nom_seance: str
    matricule_enseignant: str
    
class CourseResponse(CourseCreate):
    id: int
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
#--------------------------------- To Program (association) management  ---------------------------------#
class ToProgramCreate(BaseModel):
    id_cours: int 
    heure_debut: time
    code_salle: str
    nom_jour: str

class ToProgramResponse(BaseModel):
    id_cours: int 
    id_plage: int
    code_salle: str
    nom_jour: str
    class Config:
        orm_mode = True    
class ToProgramCreateResponse(ToProgramCreate):
    heure_fin: time
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Day management  ---------------------------------#
class DayCreate(BaseModel):
    nom: str 
    num: int
    
class DayResponse(DayCreate):
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
#--------------------------------- Course type management  ---------------------------------#
class CourseTypeCreate(BaseModel):
    nom: str 
    duree: time 
    
class CourseTypeResponse(CourseTypeCreate):
    ...
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Activity (association) management  ---------------------------------#
class ActivityCreate(BaseModel):
    nom: str
    date_act: date
    matricule_enseignant: str
    heure_debut: time
    heure_fin: time
    code_salle: str
    nom_jour: str

class ActivityResponse(ActivityCreate):
    ...
    class Config:
        orm_mode = True
class ActivityCreateResponse(ActivityCreate):
    created_at: datetime
    class Config:
        orm_mode = True

#--------------------------------------------------------------------------------------#
#--------------------------------- Teacher management  ---------------------------------#
class TeacherCreate(BaseModel):
    matricule: str
    nom: str
    email: EmailStr
    code_filiere: str

class TeacherCreateResponse(BaseModel):
    nom: str
    email: EmailStr
    matricule: str
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
#--------------------------------- Utils  ---------------------------------#
class RoomClassResponse(BaseModel):
    Salle: RoomResponse
    Classe: ClassResponse
    class Config:
        orm_mode = True

class ToProgramCourseResponse(BaseModel):
    course: CourseCreate
    programmation: ToProgramCreate
    class Config:
        orm_mode = True

class ToProgramRoomResponse(BaseModel):
    room: RoomCreate
    programmation: ToProgramCreate
    class Config:
        orm_mode = True
        
class UserLoginValidation(BaseModel):
    email: EmailStr
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    token: str
    expire_time: int
    class Config:
        orm_mode = True