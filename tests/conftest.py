import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from main import app, get_db
from models import Base


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture()
def db(engine):
    with engine.connect() as connection:
        connection.begin()
        session = Session(bind=connection)
        yield session
        session.rollback()


@pytest.fixture()
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c
