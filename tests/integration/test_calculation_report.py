import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def user_token(db_session):
    reg_data = {
        "first_name": "Report",
        "last_name": "User",
        "email": "reportuser@example.com",
        "username": "reportuser",
        "password": "ReportPass123!",
        "confirm_password": "ReportPass123!"
    }
    client.post("/auth/register", json=reg_data)
    login = client.post("/auth/login", json={"username": "reportuser", "password": "ReportPass123!"})
    return login.json()["access_token"]

def test_report_empty(user_token):
    res = client.get("/calculations/report", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["total_calculations"] == 0
    assert data["average_operands"] == 0.0
    assert data["most_common_type"] == "N/A"
    assert data["last_calculation_at"] is None

def test_report_with_calculations(user_token):
    # Add calculations
    client.post("/calculations", json={"type": "addition", "inputs": [1, 2]}, headers={"Authorization": f"Bearer {user_token}"})
    client.post("/calculations", json={"type": "addition", "inputs": [3, 4]}, headers={"Authorization": f"Bearer {user_token}"})
    client.post("/calculations", json={"type": "multiplication", "inputs": [2, 2]}, headers={"Authorization": f"Bearer {user_token}"})
    res = client.get("/calculations/report", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["total_calculations"] == 3
    assert abs(data["average_operands"] - 2.0) < 1e-6
    assert data["most_common_type"] == "addition"
    assert data["last_calculation_at"] is not None
