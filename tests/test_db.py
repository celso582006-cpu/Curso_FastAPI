from api_py.models import User
from sqlalchemy import select
from dataclasses import asdict


def test_create_user_db(SessionDB, mock_db_time):

    with mock_db_time(model=User) as time:
        
        new_user=User(
            username="Celso Manuel",
            email="celso@gmail.com",
            password="123"
        )

        SessionDB.add(new_user)
        SessionDB.commit()

        user=SessionDB.scalar(
            select(User).where(User.username == "Celso Manuel")
        )

    print(user)

    assert asdict(user) == {
        "id": 1,
        "username":"Celso Manuel",
        "email":"celso@gmail.com",
        "password":"123",
        'created_a':time,
        "update_a":time
    }
