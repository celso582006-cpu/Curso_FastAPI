from pwdlib import PasswordHash

pwd_context=PasswordHash.recommended()

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, password_hash:str):
    return pwd_context.verify(plain_password,password_hash)

