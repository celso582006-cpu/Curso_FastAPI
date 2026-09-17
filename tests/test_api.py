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

def test_only_user(client):
    res=client.get("/only_user/1")
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {
        "id":1,
        "username": "Carlos",
        "email": "carlos@example.com"
    }



def test_all_ser(client):

    res=client.get("/all_user/")

    assert res.status_code ==HTTPStatus.OK
    assert res.json() == {
        "users": [
            {           
                "id":1,
                "username": "Carlos",
                "email": "carlos@example.com"
            }
        ]
    }

def test_update_user(client):
 
    res=client.put(
        "/update_user/1",
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


def test_delete_user(client):
    res=client.delete("/delete_user/1")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"message": "Usuario deletado com sucesso!"}