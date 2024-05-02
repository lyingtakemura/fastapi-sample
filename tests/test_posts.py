from fastapi.testclient import TestClient

from config.database import Base, get_session
from config.test import get_test_session, test_engine
from main import app

Base.metadata.create_all(bind=test_engine)
app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


def test_should_create_post():
    response = client.post("/api/v1/posts", json={"title": "test title", "body": "test body"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "test title", "body": "test body"}


def test_should_get_all_posts():
    response = client.get("/api/v1/posts")
    assert response.status_code == 200
    obj = response.json()[0]
    assert obj["id"] == 1
    assert obj["title"] == "test title"
    assert obj["body"] == "test body"


def test_should_get_post():
    response = client.get("/api/v1/posts/1")
    assert response.status_code == 200
    obj = response.json()
    assert obj["id"] == 1
    assert obj["title"] == "test title"
    assert obj["body"] == "test body"


def test_should_update_post():
    response = client.put("/api/v1/posts/1", params={"title": "updated", "body": "updated"})
    assert response.status_code == 200
    obj = response.json()
    assert obj["id"] == 1
    assert obj["title"] == "updated"
    assert obj["body"] == "updated"


def test_should_delete_post():
    response = client.delete("/api/v1/posts/1")
    assert response.status_code == 200
    obj = response.json()
    assert obj["id"] == 1
    assert obj["title"] == "updated"
    assert obj["body"] == "updated"


def test_should_return_not_found_post():
    response = client.get("/api/v1/posts/1")
    assert response.status_code == 404
