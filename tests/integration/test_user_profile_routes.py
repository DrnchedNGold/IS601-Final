import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.database import get_db

client = TestClient(app)

@pytest.fixture
def user_token_and_id(db_session):
    # Register and login a user, return token and user id
    reg_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    }
    client.post("/auth/register", json=reg_data)
    login = client.post("/auth/login", json={"username": "testuser", "password": "TestPass123!"})
    token = login.json()["access_token"]
    user_id = login.json()["user_id"]
    return token, user_id

def test_get_profile(user_token_and_id):
    token, _ = user_token_and_id
    res = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

def test_update_profile(user_token_and_id):
    token, _ = user_token_and_id
    update = {"first_name": "Updated", "email": "updated@example.com"}
    res = client.put("/users/me", json=update, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["first_name"] == "Updated"
    assert data["email"] == "updated@example.com"

def test_change_password(user_token_and_id):
    token, _ = user_token_and_id
    pw_data = {
        "current_password": "TestPass123!",
        "new_password": "NewPass456!",
        "confirm_new_password": "NewPass456!"
    }
    res = client.post("/users/me/change-password", json=pw_data, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 204
    # Login with new password should succeed
    login = client.post("/auth/login", json={"username": "testuser", "password": "NewPass456!"})
    assert login.status_code == 200
    # Login with old password should fail
    login2 = client.post("/auth/login", json={"username": "testuser", "password": "TestPass123!"})
    assert login2.status_code == 401
