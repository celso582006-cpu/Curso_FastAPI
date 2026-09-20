from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
import api_py.schemas as schemas
from sqlalchemy.orm import Session
from api_py.database import get_session
from api_py.models import User
from sqlalchemy import select


app = FastAPI()


DataBase=[]

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
            password=user.password
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
    session : Session = Depends(get_session)):

    all_user=session.scalars(
        select(User).limit(limit).offset(offset)
    )
    return {"users": all_user}


@app.get(
        "/only_user/{user_id}",
        status_code=HTTPStatus.OK,
        response_model=schemas.UserPublic
)
def Only_User(user_id: int,session:Session=Depends(get_session)):
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
def Update_User(user_id:int, user:schemas.User,session:Session=Depends(get_session)):

    user_exist=session.scalar(
        select(User).where(
            User.id==user_id
        )
    )

    if user_exist:

        same_data=session.scalar(
        select(User).where(
           ( (User.username==user.username) | (User.email==user.email)) & (User.id!=user_id)
        )
        )

        if same_data:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Dados existentes!"
            )

        
        user_exist.email=user.email
        user_exist.username=user.username
        user_exist.password=user.password

        session.add(user_exist)
        session.commit()
        session.refresh(user_exist)
        return user_exist
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuario não encontrado...!"
        )



   


@app.delete(
    "/delete_user/{user_id}",
    status_code=HTTPStatus.OK, response_model=schemas.Message
)
def Delete_User(user_id:int, session:Session=Depends(get_session)):

    user_exist=session.scalar(
        select(User).where(
            User.id==user_id
        )
    )

    if user_exist:
        session.delete(user_exist)
        session.commit()
        return {"message": "Usuario deletado com sucesso!"}
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuario não encontrado...!"
        )
    



