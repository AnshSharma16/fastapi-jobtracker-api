from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/docs")
    assert response.status_code == 200

def test_register_user():
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200

def test_login_user():
    response = client.post(
        "/users/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_me_unauthorized():
    response = client.get(
        "/users/me"
    )
    assert response.status_code == 401