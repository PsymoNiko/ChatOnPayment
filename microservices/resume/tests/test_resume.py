"""
Tests for Resume Service Endpoints
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


def test_create_resume():
    """Test creating a resume."""
    resume_data = {
        "user_id": "user-123",
        "title": "Software Engineer",
        "summary": "Experienced developer",
        "skills": ["Python", "FastAPI", "Docker"],
        "experience": "5 years at Tech Corp",
        "education": "BS in Computer Science"
    }
    
    response = client.post("/resumes", json=resume_data)
    assert response.status_code == 200
    data = response.json()
    assert "resume_id" in data
    assert data["user_id"] == "user-123"
    assert data["title"] == "Software Engineer"
    assert data["skills"] == ["Python", "FastAPI", "Docker"]


def test_create_duplicate_resume():
    """Test that creating a duplicate resume for the same user fails."""
    resume_data = {
        "user_id": "user-456",
        "title": "Data Scientist"
    }
    
    # Create first resume
    response1 = client.post("/resumes", json=resume_data)
    assert response1.status_code == 200
    
    # Try to create second resume for same user
    response2 = client.post("/resumes", json=resume_data)
    assert response2.status_code == 400


def test_get_resume():
    """Test getting a resume by ID."""
    # First create a resume
    resume_data = {
        "user_id": "user-789",
        "title": "DevOps Engineer"
    }
    create_response = client.post("/resumes", json=resume_data)
    resume_id = create_response.json()["resume_id"]
    
    # Get the resume
    response = client.get(f"/resumes/{resume_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "DevOps Engineer"


def test_get_resume_not_found():
    """Test getting a non-existent resume."""
    response = client.get("/resumes/nonexistent-id")
    assert response.status_code == 404


def test_get_resume_by_user():
    """Test getting a resume by user ID."""
    # First create a resume
    resume_data = {
        "user_id": "user-999",
        "title": "Product Manager"
    }
    client.post("/resumes", json=resume_data)
    
    # Get resume by user ID
    response = client.get("/resumes/user/user-999")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user-999"
    assert data["title"] == "Product Manager"


def test_update_resume():
    """Test updating a resume."""
    # First create a resume
    resume_data = {
        "user_id": "user-111",
        "title": "Frontend Developer",
        "skills": ["JavaScript", "React"]
    }
    create_response = client.post("/resumes", json=resume_data)
    resume_id = create_response.json()["resume_id"]
    
    # Update the resume
    update_data = {
        "title": "Senior Frontend Developer",
        "skills": ["JavaScript", "React", "TypeScript", "Vue.js"]
    }
    response = client.put(f"/resumes/{resume_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Senior Frontend Developer"
    assert len(data["skills"]) == 4


def test_delete_resume():
    """Test deleting a resume."""
    # First create a resume
    resume_data = {
        "user_id": "user-222",
        "title": "Backend Developer"
    }
    create_response = client.post("/resumes", json=resume_data)
    resume_id = create_response.json()["resume_id"]
    
    # Delete the resume
    response = client.delete(f"/resumes/{resume_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Resume deleted successfully"
    
    # Verify it's deleted
    get_response = client.get(f"/resumes/{resume_id}")
    assert get_response.status_code == 404


def test_list_resumes():
    """Test listing all resumes."""
    response = client.get("/resumes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
