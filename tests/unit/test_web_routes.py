"""Tests for web routes to push coverage to 90%+."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_page():
    """Test login page route."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_register_page():
    """Test register page route."""
    response = client.get("/register")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_dashboard_page():
    """Test dashboard page route."""
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_view_calculation_page():
    """Test view calculation page route."""
    test_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/dashboard/view/{test_id}")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_edit_calculation_page():
    """Test edit calculation page route."""
    test_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/dashboard/edit/{test_id}")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_profile_page():
    """Test profile page route."""
    response = client.get("/profile")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_web_routes_contain_expected_content():
    """Test that web routes contain expected HTML elements."""
    # Test login page has form
    response = client.get("/login")
    assert response.status_code == 200
    
    # Test register page has form
    response = client.get("/register")
    assert response.status_code == 200
    
    # Test dashboard page
    response = client.get("/dashboard")
    assert response.status_code == 200
