"""
Tests for Chat Service Endpoints
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


def test_room_info_endpoint():
    """Test the room info endpoint."""
    response = client.get("/rooms/test-room/info")
    assert response.status_code == 200
    data = response.json()
    assert "room_name" in data
    assert data["room_name"] == "test-room"
    assert "active_connections" in data
    assert data["active_connections"] == 0


def test_websocket_connection():
    """Test WebSocket connection to a chat room."""
    with client.websocket_connect("/ws/test-room") as websocket:
        # Send a message
        websocket.send_json({
            "message": "Hello, World!",
            "phone_number": "1234567890",
            "avatar": "http://example.com/avatar.jpg"
        })
        # Receive the broadcast message
        data = websocket.receive_json()
        assert data["message"] == "Hello, World!"
        assert data["phone_number"] == "1234567890"
        assert data["avatar"] == "http://example.com/avatar.jpg"
