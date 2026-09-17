from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from api_py.models import table_registry, User
from api_py.app import app
from contextlib import contextmanager
from datetime import datetime
import pytest

@pytest.fixture
def client():

    return TestClient(app)

@pytest.fixture
def SessionDB():

    engine=create_engine("sqlite:///:memory:")

    table_registry.metadata.create_all(engine)

    with Session(engine) as ss:
        yield ss

    table_registry.metadata.drop_all(engine)

@contextmanager
def _mock_db_time(model,time= datetime(2026,9,18)):

    def fake_time_hock(mapper ,connection,target):
        if hasattr(target,"created_a") and hasattr(target, "update_a"):
            target.created_a = time
            target.update_a = time
 

    event.listen(model, "before_insert", fake_time_hock)
    yield time
    event.remove(model, "before_insert", fake_time_hock)
    
@pytest.fixture
def mock_db_time():
    return _mock_db_time