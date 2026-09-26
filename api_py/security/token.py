from jwt import encode, decode, DecodeError
from  datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from sqlalchemy import select
from api_py.database import get_session
from fastapi import Depends, HTTPException
from http import HTTPStatus
from fastapi.security import OAuth2PasswordBearer
from api_py.models import User

SECRET_KEY="minha_chave_secreta_super_segura_com_mais_de_32_caracteres"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPERI_TIME=30

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode=data.copy()

    experi=datetime.now(tz=ZoneInfo("Africa/Luanda"))+timedelta(
        minutes=ACCESS_TOKEN_EXPERI_TIME   
    )

    to_encode.update({"exp":experi})

    encode_jwt= encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encode_jwt

def get_current_user(
    session:Session= Depends(get_session),
    token: str= Depends(oauth2_scheme)
):
    credentials_exception= HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Coul not validate credentail",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload=decode(token,SECRET_KEY,ALGORITHM)
        subject_email=payload.get("sub")

        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user=session.scalar(
        select(User).where(User.email==subject_email)
    )

    if not user:
        raise credentials_exception
    return user

    
