from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
import api_py.schemas as schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from api_py.database import get_session
from api_py.models import User
from sqlalchemy import select
from api_py.security.encryption import get_password_hash,verify_password
from fastapi.security import OAuth2PasswordRequestForm
from api_py.security.token import create_access_token,get_current_user

app = FastAPI()


DataBase=[]

@app.get('/hello/',status_code=HTTPStatus.OK)
def Hello():
    return {'message':'Ola como vai'}


@app.post(
        '/create/',
        status_code=HTTPStatus.CREATED,
        response_model= schemas.UserPublic
)
def Create_User(user:schemas.User, session : Session =Depends(get_session)):

    db_user= session.scalar(
        select(User).where(
        (User.username==user.username) | (User.email==user.email)
                           )
    )

    if db_user:
        raise HTTPException(
            detail="Usuario existente",
            status_code=HTTPStatus.CONFLICT
        )
    else:
        db_user=User(
            username=user.username,
            email=user.email,
            password= get_password_hash(user.password) 
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

@app.get(
        "/all_user/",
        response_model=schemas.ListUser,
        status_code=HTTPStatus.OK
)
def All_User(
    limit=10,
    offset=0,
    session : Session = Depends(get_session),
    curret_user: User =Depends(get_current_user)
    ):

    all_user=session.scalars(
        select(User).limit(limit).offset(offset)
    )
    return {"users": all_user}


@app.get(
        "/only_user/{user_id}",
        status_code=HTTPStatus.OK,
        response_model=schemas.UserPublic,
)
def Only_User(user_id: int,session:Session=Depends(get_session),
              curret_user: User =Depends(get_current_user)
):
    user_exist=session.scalar(
        select(User).where(
            (User.id==user_id)
        )
    )

    if user_exist:
        return user_exist
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuario não encontrado...!"
        )




@app.put(
    "/update_user/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=schemas.UserPublic
    
)
def Update_User(user_id:int, user:schemas.User,session:Session=Depends(get_session),
                curret_user: User =Depends(get_current_user)
):


    if curret_user.id!=user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough Permissions!"
        )

    try:
        curret_user.email=user.email
        curret_user.username=user.username
        curret_user.password=get_password_hash(user.password)

        session.add(curret_user)
        session.commit()
        session.refresh(curret_user)
        return curret_user
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Dados existentes!"
        )


@app.delete(
    "/delete_user/{user_id}",
    status_code=HTTPStatus.OK, response_model=schemas.Message,
)
def Delete_User(user_id:int, session:Session=Depends(get_session),
                curret_user: User = Depends(get_current_user)
):

    if curret_user.id!=user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough Permissions!"
        )

    session.delete(curret_user)
    session.commit()
    return {"message": "Usuario deletado com sucesso!"}


@app.post("/token/", response_model=schemas.Token)
def login_access_token(form_date:OAuth2PasswordRequestForm=Depends(),session:Session=Depends(get_session)):
    user_exist=session.scalar(
       select(User).where(User.email==form_date.username)
    )

    if not user_exist or not verify_password(form_date.password,user_exist.password):

        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect E-mail or password"

        )

    access_token= create_access_token(
        {"sub":user_exist.email}
    )



    return {"access_token":access_token, "type_token":"Bearer"}
 


    




