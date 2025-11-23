"""
Resume Microservice - FastAPI Application

Provides resume management endpoints.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(title="Resume Service", version="0.1.0")


class ResumeCreate(BaseModel):
    """Resume creation request model."""
    user_id: str
    title: str
    summary: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[str] = None
    education: Optional[str] = None


class ResumeResponse(BaseModel):
    """Resume response model."""
    resume_id: str
    user_id: str
    title: str
    summary: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    created_at: str
    updated_at: str


class ResumeUpdate(BaseModel):
    """Resume update request model."""
    title: Optional[str] = None
    summary: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[str] = None
    education: Optional[str] = None


# In-memory storage for demonstration (replace with database in production)
resumes = {}


@app.get("/healthz")
async def health_check():
    """Health check endpoint for liveness probe."""
    return {"status": "ok"}


@app.get("/readyz")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready"}


@app.post("/resumes", response_model=ResumeResponse)
async def create_resume(resume: ResumeCreate):
    """Create a new resume."""
    resume_id = str(uuid.uuid4())
    
    # Check if user already has a resume
    for existing_resume in resumes.values():
        if existing_resume["user_id"] == resume.user_id:
            raise HTTPException(
                status_code=400,
                detail="User already has a resume. Use PUT to update."
            )
    
    now = datetime.utcnow().isoformat()
    resumes[resume_id] = {
        "user_id": resume.user_id,
        "title": resume.title,
        "summary": resume.summary,
        "skills": resume.skills or [],
        "experience": resume.experience,
        "education": resume.education,
        "created_at": now,
        "updated_at": now
    }
    
    return ResumeResponse(
        resume_id=resume_id,
        **resumes[resume_id]
    )


@app.get("/resumes/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: str):
    """Get resume by ID."""
    if resume_id not in resumes:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return ResumeResponse(
        resume_id=resume_id,
        **resumes[resume_id]
    )


@app.get("/resumes/user/{user_id}", response_model=ResumeResponse)
async def get_resume_by_user(user_id: str):
    """Get resume by user ID."""
    for resume_id, resume in resumes.items():
        if resume["user_id"] == user_id:
            return ResumeResponse(
                resume_id=resume_id,
                **resume
            )
    
    raise HTTPException(status_code=404, detail="Resume not found for this user")


@app.put("/resumes/{resume_id}", response_model=ResumeResponse)
async def update_resume(resume_id: str, resume_update: ResumeUpdate):
    """Update an existing resume."""
    if resume_id not in resumes:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume = resumes[resume_id]
    
    # Update only provided fields
    if resume_update.title is not None:
        resume["title"] = resume_update.title
    if resume_update.summary is not None:
        resume["summary"] = resume_update.summary
    if resume_update.skills is not None:
        resume["skills"] = resume_update.skills
    if resume_update.experience is not None:
        resume["experience"] = resume_update.experience
    if resume_update.education is not None:
        resume["education"] = resume_update.education
    
    resume["updated_at"] = datetime.utcnow().isoformat()
    
    return ResumeResponse(
        resume_id=resume_id,
        **resume
    )


@app.delete("/resumes/{resume_id}")
async def delete_resume(resume_id: str):
    """Delete a resume."""
    if resume_id not in resumes:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    del resumes[resume_id]
    return {"message": "Resume deleted successfully"}


@app.get("/resumes", response_model=List[ResumeResponse])
async def list_resumes():
    """List all resumes."""
    return [
        ResumeResponse(
            resume_id=resume_id,
            **resume
        )
        for resume_id, resume in resumes.items()
    ]
