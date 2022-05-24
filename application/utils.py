from passlib.context import CryptContext
from string import ascii_letters, digits
from random import choice

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed(password: str):
    return password_context.hash(password)

def verified(password: str, db_password: str):
    return password_context.verify(password, db_password)

def incorrect_pass():
    return "Mot de passe incorrect"

def no_account():
    return "Vous n'avez pas de compte"

def password_generated():
    password = ''.join(choice(ascii_letters + digits) for _ in range(10))
    return password

def login_generated(matricule: str):
    generated = ''.join(choice(ascii_letters + digits) for _ in range(6))
    login = matricule + "_" + generated
    return login

def store_teachers_in_file(nom, login, password):
    file = open("teachers.txt", "a+")
    file.write(f"|Nom: {nom} \t\t| Login: {login} \t\t| Mot de passe: {password}\t\t|")
    file.close()
