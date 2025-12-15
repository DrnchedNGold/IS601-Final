import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_web_routes():
    for path in ["/", "/login", "/register", "/dashboard"]:
        resp = client.get(path)
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

def test_register_invalid():
    # Missing required fields
    resp = client.post("/auth/register", json={})
    assert resp.status_code == 422

def test_login_invalid():
    # Invalid credentials or schema
    resp = client.post("/auth/login", json={"username": "nouser", "password": "bad"})
    assert resp.status_code == 422 or resp.status_code == 401

def test_list_calculations_unauth():
    resp = client.get("/calculations")
    assert resp.status_code in (401, 403)

def test_register_login_and_calculation_crud():
    # Register a user
    reg_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    }
    resp = client.post("/auth/register", json=reg_data)
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    # Login
    login_data = {"username": "testuser", "password": "TestPass123!"}
    resp = client.post("/auth/login", json=login_data)
    assert resp.status_code == 200
    tokens = resp.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create calculation
    calc_data = {"type": "addition", "inputs": [1, 2]}
    resp = client.post("/calculations", json=calc_data, headers=headers)
    assert resp.status_code == 201
    calc_id = resp.json()["id"]

    # List calculations
    resp = client.get("/calculations", headers=headers)
    assert resp.status_code == 200
    assert any(c["id"] == calc_id for c in resp.json())

    # Get calculation
    resp = client.get(f"/calculations/{calc_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == calc_id

    # Update calculation
    update_data = {"inputs": [5, 7]}
    resp = client.put(f"/calculations/{calc_id}", json=update_data, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["inputs"] == [5, 7]

    # Delete calculation
    resp = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert resp.status_code == 204

    # Confirm deletion
    resp = client.get(f"/calculations/{calc_id}", headers=headers)
    assert resp.status_code == 404
