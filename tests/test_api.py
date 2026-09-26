from http import HTTPStatus

def test_create_user(client):
    res=client.post(
        "/create/",
        json={
            "username": "Carlos",
            "email": "carlos@example.com",
            "password": "12345"
        }
    )

    assert res.status_code== HTTPStatus.CREATED
    assert res.json()=={
        "id":1,
        "username": "Carlos",
        "email": "carlos@example.com"
    }

    


def test_all_user_cheio(client,token):
    res=client.get("/all_user/",
    headers={"Authorization":f"Bearer {token}"}               
    )
    assert res.json()=={
        "users": [
            {
        "id":1,
        "username": "Carlos",
        "email": "carlos@example.com"
    }
        ]
    }


def test_only_user(client,token):
    res=client.get("/only_user/1",
        headers={"Authorization":f"Bearer {token}"} 
    )
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {
        "id":1,
        "username": "Carlos",
        "email": "carlos@example.com"
    }



def test_update_user(client,token):
 
    res=client.put(
        "/update_user/1",
        headers={"Authorization":f"Bearer {token}"} ,
        json={
            "username": "Manuel",
            "email": "Manuel@example.com",
            "password": "54321",
           
        }
    )


    assert res.status_code== HTTPStatus.OK
    assert res.json() == {
            "username": "Manuel",
            "email": "Manuel@example.com",
            "id":1
    }


def test_delete_user(client,token):
    res=client.delete("/delete_user/1",
        headers={"Authorization":f"Bearer {token}"} ,
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"message": "Usuario deletado com sucesso!"}


def test_get_acsess_token(client,new_user):

    res=client.post(
        "/token/",
        data={"username":new_user.email,"password":"123"}
    )

    res_json=res.json()
    assert res.status_code==HTTPStatus.OK
    assert res_json["type_token"]=="Bearer"
    assert "access_token" in res_json
    
