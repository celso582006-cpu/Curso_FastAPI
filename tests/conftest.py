from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from api_py.models import table_registry, User
from api_py.app import app
from contextlib import contextmanager
from datetime import datetime
from api_py.database import get_session
import pytest
from sqlalchemy.pool import StaticPool

@pytest.fixture
def client(SessionDB):

    def get_session_overrides():
        return SessionDB
    with TestClient(app) as client:
        app.dependency_overrides[get_session]= get_session_overrides
        yield client
    app.dependency_overrides.clear()  

@pytest.fixture
def SessionDB():

    engine=create_engine("sqlite:///:memory:",
                         connect_args={"check_same_thread":False},
                         poolclass=StaticPool
                         )

    table_registry.metadata.create_all(engine)

    with Session(engine) as ss:
        yield ss

    table_registry.metadata.drop_all(engine)

@contextmanager
def _mock_db_time(model,time= datetime(2026,9,18)):

    def fake_time_hock(mapper ,connection,target):
        if hasattr(target,"created_a"):
            target.created_a = time

 

    event.listen(model, "before_insert", fake_time_hock)
    yield time
    event.remove(model, "before_insert", fake_time_hock)
    
@pytest.fixture
def mock_db_time():
    return _mock_db_time

@pytest.fixture
def new_user(SessionDB: Session):
    user=User(
            username= "Carlos",
            email= "carlos@example.com",
            password= "12345"
    )
    SessionDB.add(user)
    SessionDB.commit()
    SessionDB.refresh(user)

    return user
