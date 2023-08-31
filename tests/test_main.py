def test_signup(client):
    response = client.post(
        "/signup/",
        json={"username": "test", "email": "test@example.com", "password": "0"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "test"

    assert "id" in data
    user_id = data["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200


def test_duplicate_user(client):
    response = client.post(
        "/signup/",
        json={"username": "test", "email": "test@example.com", "password": "0"},
    )
    assert response.status_code == 200
    response = client.post(
        "/signup/",
        json={"username": "test", "email": "test@example.com", "password": "0"},
    )
    assert response.status_code == 400