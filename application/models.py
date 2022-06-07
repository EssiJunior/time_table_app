from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date
from sqlalchemy.sql.expression import text

class Administrateur(Base):
    __tablename__ = "admin"
    
    login = Column(String(50), primary_key = True, nullable=False, unique=True)
    mot_de_passe = Column(String(100),  nullable = False)

class Specialite(Base):
    __tablename__ = "specialite"
    
    id = Column(Integer, primary_key = True, nullable = False )
    nom = Column(String(50), nullable = False)
    effectif = Column(Integer, nullable = False)
    code_classe = Column(String(10), ForeignKey("classe.code", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)

class Classe(Base):
    __tablename__ = "classe"
    
    id = Column(Integer,primary_key = True , nullable = False) 
    code = Column(String(10), nullable = False)
    effectif = Column(Integer, nullable = False)   
    niveau = Column(String(6), ForeignKey("niveau.code", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)
    code_filiere = Column(String(6), ForeignKey("filiere.code", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)

class Niveau(Base):
    __tablename__ = "niveau"
    
    code = Column(String(6), primary_key = True, nullable = False)

class Filiere(Base):
    __tablename__ = "filiere"
    
    code = Column(String(6), primary_key = True, nullable = False)
    nom = Column(String(25), nullable = False)

class Cours(Base):
    __tablename__ = "cours"
    
    code = Column(String(10), primary_key = True, nullable = False)
    semestre = Column(Integer, nullable = False)
    titre = Column(String(50), nullable = False)
    id_specialite = Column(Integer, ForeignKey("specialite.id", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)
    id_classe = Column(String(10), ForeignKey("classe.id", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)
    code_filiere = Column(String(6), ForeignKey("filiere.code", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)
    nom_seance = Column(String(10), ForeignKey("type_seance.nom", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)
    matricule_enseignant = Column(String(10), ForeignKey("enseignant.matricule", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)

class PlageHoraire(Base):
    __tablename__ = "plage_horaire"
    
    id_plage = Column(Integer, primary_key = True, nullable = False)
    heure_debut = Column(Time(timezone=False), nullable=False, server_default= text("now()"))
    heure_fin = Column(Time(timezone=False),  nullable=False, server_default= text("now()"))

class Programmer(Base): 
    __tablename__ = "programmer"

    code_cours = Column(String(10), ForeignKey("cours.code", ondelete="CASCADE", onupdate="CASCADE"), primary_key = True, nullable = False)
    id_plage = Column(Integer, ForeignKey("plage_horaire.id_plage", ondelete="CASCADE", onupdate="CASCADE"), primary_key = True, nullable = False)
    code_salle= Column(String(50), ForeignKey("salle.code", ondelete="CASCADE", onupdate="CASCADE"), primary_key = True, nullable = False)
    nom_jour = Column(String(10), ForeignKey("jour.nom", ondelete="CASCADE", onupdate="CASCADE"), primary_key = True, nullable = False)

class Jour(Base):
    __tablename__ = "jour"
    
    nom = Column(String(10), primary_key = True, nullable = False)
    num = Column(Integer, nullable = False)

class Salle(Base):
    __tablename__ = "salle"
    
    code = Column(String(10), primary_key = True, nullable = False)
    effectif = Column(Integer, nullable = False)
    
class TypeSeance(Base):
    __tablename__ = "type_seance"
    
    nom = Column(String(10), primary_key = True, nullable = False)
    duree = Column(Time(timezone=False), nullable=False, server_default= text("now()"))

class Activite(Base): # ------------  Not yet okay !!!  ------------
    __tablename__ = "activite"
    
    nom = Column(String(50), nullable = False)
    date_act = Column(Date, nullable = False, server_default= text("now()"))
    matricule_enseignant = Column(String(10), ForeignKey("enseignant.matricule", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable = False)
    id_plage = Column(Integer, ForeignKey("plage_horaire.id_plage", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable = False)
    code_salle = Column(String(10), ForeignKey("salle.code", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable = False)
    nom_jour = Column(String(10), ForeignKey("jour.nom", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable = False)
    
class Enseignant(Base):
    __tablename__ = "enseignant"
    
    matricule = Column(String(10), primary_key = True, nullable = False)
    nom = Column(String(50), nullable = False)
    mot_de_passe = Column(String(100),  nullable = False)
    email = Column(String(50), nullable=False, unique=True)
    login = Column(String(50), nullable=False, unique=True)
    code_filiere = Column(String(6), ForeignKey("filiere.code", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)

