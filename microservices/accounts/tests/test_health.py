"""
Tests for Accounts Service Health Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint returns status ok."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_endpoint():
    """Test the readiness check endpoint returns status ready."""
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_jwks_endpoint():
    """Test the JWKS endpoint returns empty keys array."""
    response = client.get("/.well-known/jwks.json")
    assert response.status_code == 200
    assert response.json() == {"keys": []}


def test_users_me_stub():
    """Test the /users/me stub endpoint."""
    response = client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "username" in data
    assert "message" in data
