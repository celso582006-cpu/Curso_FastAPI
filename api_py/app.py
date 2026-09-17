from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
import api_py.schemas as schemas


app = FastAPI()


DataBase=[]

@app.post(
        '/create/',
        status_code=HTTPStatus.CREATED,
        response_model= schemas.UserPublic
)
def Create_User(user:schemas.User):
    new_user= schemas.UserDB(
        **user.model_dump(),
        id=len(DataBase)+1
    )
 
    DataBase.append(new_user)
    return new_user


@app.get(
        "/only_user/{user_id}",
        status_code=HTTPStatus.OK,
        response_model=schemas.UserPublic
)
def Only_User(user_id: int):
    if user_id < 1 or user_id > len(DataBase):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuario não encontrado...!"
        )
    
    return DataBase[int(user_id)-1]


@app.get(
        "/all_user/",
        response_model=schemas.ListUser,
        status_code=HTTPStatus.OK
)
def All_User():
    return {"users": DataBase}


@app.put(
    "/update_user/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=schemas.UserPublic
)
def Update_User(user_id:int, user:schemas.User):

    new_user= schemas.UserDB(
        **user.model_dump(),
        id=user_id
    )

    if user_id < 1 or user_id > len(DataBase):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuario não encontrado...!"
        )

    DataBase[int(user_id)-1]=new_user


    return DataBase[int(user_id)-1]


@app.delete(
    "/delete_user/{user_id}",
    status_code=HTTPStatus.OK, response_model=schemas.Message

)
def Delete_User(user_id:int):

    if user_id < 1 or user_id > len(DataBase):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuario não encontrado...!"
        )
    del DataBase[int(user_id)-1]
    return {"message": "Usuario deletado com sucesso!"}



