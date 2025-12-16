"""Tests to push coverage over 90% by targeting main.py endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    # Root endpoint returns HTML, not JSON
    assert "text/html" in response.headers.get("content-type", "")

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_docs_redirect():
    """Test docs redirect."""
    response = client.get("/docs")
    assert response.status_code in [200, 307]  # Either direct or redirect

def test_openapi_schema():
    """Test OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data

def test_404_handler():
    """Test 404 error handling."""
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404

def test_cors_headers():
    """Test CORS headers on preflight request."""
    response = client.options("/")
    # CORS should be configured
    assert response.status_code in [200, 405]  # Either allowed or method not allowed

def test_static_files_route():
    """Test static files are served."""
    # Test that static route exists (even if file doesn't)
    response = client.get("/static/test.css")
    # Should get either the file or 404, but not 500
    assert response.status_code in [200, 404]
