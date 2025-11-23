"""
Tests for Accounts Service User and Account Management
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    """Test creating a new user."""
    response = client.post(
        "/users",
        json={
            "phone_number": "1234567890",
            "password": "testpass123",
            "date_of_birth": "1990-01-01"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["phone_number"] == "1234567890"
    assert data["is_active"] is True
    assert data["is_admin"] is False


def test_create_duplicate_user():
    """Test creating a user with duplicate phone number."""
    # Create first user
    client.post(
        "/users",
        json={
            "phone_number": "9999999999",
            "password": "testpass123"
        }
    )
    
    # Try to create duplicate
    response = client.post(
        "/users",
        json={
            "phone_number": "9999999999",
            "password": "testpass456"
        }
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_user():
    """Test getting a user by ID."""
    # Create user
    create_response = client.post(
        "/users",
        json={
            "phone_number": "5555555555",
            "password": "testpass123"
        }
    )
    user_id = create_response.json()["user_id"]
    
    # Get user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["phone_number"] == "5555555555"


def test_get_account_by_user():
    """Test getting account for a user."""
    # Create user (account is created automatically)
    create_response = client.post(
        "/users",
        json={
            "phone_number": "7777777777",
            "password": "testpass123"
        }
    )
    user_id = create_response.json()["user_id"]
    
    # Get account
    response = client.get(f"/accounts/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "account_id" in data
    assert data["user_id"] == user_id
    assert data["balance"] == "0.00"


def test_create_transaction_insufficient_balance():
    """Test creating a transaction with insufficient balance."""
    # Create sender and receiver
    sender_response = client.post(
        "/users",
        json={"phone_number": "1111111111", "password": "test"}
    )
    receiver_response = client.post(
        "/users",
        json={"phone_number": "2222222222", "password": "test"}
    )
    
    sender_id = sender_response.json()["user_id"]
    receiver_id = receiver_response.json()["user_id"]
    
    # Get account IDs
    sender_account = client.get(f"/accounts/user/{sender_id}").json()
    receiver_account = client.get(f"/accounts/user/{receiver_id}").json()
    
    # Create transaction (should fail due to insufficient balance)
    response = client.post(
        "/transactions",
        json={
            "sender_id": sender_account["account_id"],
            "receiver_id": receiver_account["account_id"],
            "amount": "100.00"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "FAILED"
