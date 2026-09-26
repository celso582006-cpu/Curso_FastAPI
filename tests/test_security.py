from api_py.security.token import create_access_token,SECRET_KEY,ALGORITHM
from jwt import decode
from http import HTTPStatus
def test_jwt():

    data={"test":"exemplo@gmail.com"}

    token=create_access_token(data)

    decoded=decode(token,SECRET_KEY,ALGORITHM)



    assert decoded["test"] == data["test"]
    assert "exp" in decoded

def test_jwt_invalid_token(client):
    res=client.delete("/delete_user/1",
        headers={"Authorization":f"Bearer TOKEN INVALIDO!"} ,
    )

    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.json() == {"detail":"Coul not validate credentail"}