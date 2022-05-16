from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed(password: str):
    return password_context.hash(password)

def verified(password: str, db_password: str):
    return password_context.verify(password, db_password)