from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, Time
from sqlalchemy.sql.expression import text
#from sqlalchemy.types import Time
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)

class Utilisateur(Base):
    __tablename__ = "utilisateur"
    
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable = False, server_default= "TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text("now()"))
    
class Enseignant(Base):
    __tablename__ = "enseignant"
    
    matricule = Column(String(10), primary_key = True, nullable = False)
    nom = Column(String(50), nullable = False)

class Salle(Base):
    __tablename__ = "salle"
    
    code = Column(String(50), primary_key = True, nullable = False)
    effectif = Column(Integer, nullable = False)

class PlageHoraire(Base):
    __tablename__ = "plage_horaire"
    
    heure_debut = Column(Time(timezone=False), primary_key = True, nullable=False, server_default= text("now()"))
    heure_fin = Column(Time(timezone=False), primary_key = True, nullable=False, server_default= text("now()"))

class Specialite(Base):
    __tablename__ = "specialite"
    
    nom = Column(String(50), primary_key = True, nullable = False)
    effectif = Column(Integer, nullable = False)

class Jour(Base):
    __tablename__ = "jour"
    
    nom = Column(String(10), primary_key = True, nullable = False)

class TypeSeance(Base):
    __tablename__ = "type_seance"
    
    nom = Column(String(50), primary_key = True, nullable = False)
    duree = Column(Time(timezone=False), nullable=False, server_default= text("now()"))

class Cours(Base):
    __tablename__ = "cours"
    
    code = Column(String(10), primary_key = True, nullable = False)
    semestre = Column(Integer, nullable = False)
    titre = Column(String(50), nullable = False)
    nom_seance = Column(String(50), ForeignKey("type_seance.nom", ondelete="CASCADE"), nullable = False)

class Classe(Base):
    __tablename__ = "classe"
    
    code = Column(String(10), primary_key = True, nullable = False)
    effectif = Column(Integer, nullable = False)   
    nom_specialite = Column(String(50), ForeignKey("specialite.nom", ondelete="CASCADE"), nullable = False)

class Niveau(Base):
    __tablename__ = "niveau"
    
    numero = Column(String(6), primary_key = True, nullable = False)
    code_classe = Column(String(10), ForeignKey("classe.code", ondelete="CASCADE"), nullable = False)

class Filiere(Base):
    __tablename__ = "filiere"
    
    code = Column(String(6), primary_key = True, nullable = False)
    nom = Column(String(25), nullable = False)
    code_classe = Column(String(10), ForeignKey("classe.code", ondelete="CASCADE"), nullable = False)
    code_cours = Column(String(10), ForeignKey("cours.code", ondelete="CASCADE"), nullable = False)
    matricule_enseignant = Column(String(10), ForeignKey("enseignant.matricule", ondelete="CASCADE"), nullable = False)

class Programmer(Base):
    __tablename__ = "programmer"

    code_classe = Column(String(10), ForeignKey("classe.code", ondelete="CASCADE"), primary_key = True, nullable = False)
    code_cours = Column(String(10), ForeignKey("cours.code", ondelete="CASCADE"), primary_key = True, nullable = False)
    matricule_enseignant = Column(String(10), ForeignKey("enseignant.matricule", ondelete="CASCADE"), primary_key = True, nullable = False)
    heure_debut = Column(Time(timezone=False), ForeignKey("plage_horaire.heure_debut", ondelete="CASCADE"), primary_key = True, nullable = False)
    heure_fin = Column(Time(timezone=False), ForeignKey("plage_horaire.heure_fin", ondelete="CASCADE"), primary_key = True, nullable = False)
    code_salle= Column(String(50), ForeignKey("salle.code", ondelete="CASCADE"), primary_key = True, nullable = False)
    nom_jour = Column(String(10), ForeignKey("jour.nom", ondelete="CASCADE"), primary_key = True, nullable = False)

class Activite(Base):
    __tablename__ = "activite"
    
    nom = Column(String(50), primary_key = True, nullable = False)
    matricule_enseignant = Column(String(10), ForeignKey("enseignant.matricule", ondelete="CASCADE"), nullable = False)
    heure_debut = Column(Time(timezone=False), ForeignKey("plage_horaire.heure_debut", ondelete="CASCADE"), nullable = False)
    heure_fin = Column(Time(timezone=False), ForeignKey("plage_horaire.heure_fin", ondelete="CASCADE"), nullable = False)
    code_salle= Column(String(50), ForeignKey("salle.code", ondelete="CASCADE"), nullable = False)
    nom_jour = Column(String(10), ForeignKey("jour.nom", ondelete="CASCADE"), nullable = False)
