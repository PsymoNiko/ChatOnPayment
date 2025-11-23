"""
Tests for Basement Service Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO

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


def test_file_upload():
    """Test file upload endpoint."""
    # Create a simple test file
    file_content = b"Test file content"
    files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}
    
    response = client.post(
        "/files/upload",
        files=files,
        data={"file_tags": "test", "bucket_name": "test-bucket"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["file_name"] == "test.txt"
    assert "file_url" in data
    assert data["bucket_name"] == "test-bucket"
    assert data["file_tags"] == "test"


def test_get_file_info():
    """Test getting file info."""
    # First upload a file
    file_content = b"Test file content"
    files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}
    upload_response = client.post("/files/upload", files=files)
    file_id = upload_response.json()["file_id"]
    
    # Get file info
    response = client.get(f"/files/{file_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["file_name"] == "test.txt"


def test_get_file_not_found():
    """Test getting non-existent file."""
    response = client.get("/files/nonexistent-id")
    assert response.status_code == 404


def test_create_category():
    """Test creating a category."""
    response = client.post(
        "/categories",
        json={"title": "Test Category", "file_tags": "test"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "category_id" in data
    assert data["title"] == "Test Category"
    assert data["slug"] == "test-category"
    assert data["level"] == 0


def test_get_category():
    """Test getting a category."""
    # First create a category
    create_response = client.post(
        "/categories",
        json={"title": "Test Category"}
    )
    category_id = create_response.json()["category_id"]
    
    # Get category
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Category"


def test_list_categories():
    """Test listing categories."""
    response = client.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
