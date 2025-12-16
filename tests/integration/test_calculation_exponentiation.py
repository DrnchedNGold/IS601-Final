import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def user_token(db_session):
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    username = f"expuser_{unique_id}"
    email = f"expuser_{unique_id}@example.com"
    
    reg_data = {
        "first_name": "Exp",
        "last_name": "User",
        "email": email,
        "username": username,
        "password": "ExpPass123!",
        "confirm_password": "ExpPass123!"
    }
    reg_response = client.post("/auth/register", json=reg_data)
    if reg_response.status_code != 201:
        raise Exception(f"Registration failed with status {reg_response.status_code}: {reg_response.json()}")
        
    login = client.post("/auth/login", json={"username": username, "password": "ExpPass123!"})
    if login.status_code != 200:
        raise Exception(f"Login failed with status {login.status_code}: {login.json()}")
    return login.json()["access_token"]

def test_create_exponentiation_calculation(user_token):
    payload = {
        "type": "exponentiation",
        "inputs": [2, 8]
    }
    res = client.post("/calculations", json=payload, headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 201
    data = res.json()
    assert data["type"] == "exponentiation"
    assert data["inputs"] == [2, 8]
    assert data["result"] == 256

def test_exponentiation_invalid_inputs(user_token):
    payload = {
        "type": "exponentiation",
        "inputs": [2]
    }
    res = client.post("/calculations", json=payload, headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 400
    assert "requires exactly two numbers" in res.json()["detail"]
