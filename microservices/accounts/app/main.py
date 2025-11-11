"""
Accounts Microservice - FastAPI Application

Provides user authentication and account management endpoints.
"""
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI(title="Accounts Service", version="0.1.0")


@app.get("/healthz")
async def health_check():
    """Health check endpoint for liveness probe."""
    return {"status": "ok"}


@app.get("/readyz")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready"}


@app.get("/.well-known/jwks.json")
async def jwks_endpoint():
    """JWKS endpoint for JWT public key distribution (stub)."""
    return {"keys": []}


@app.get("/users/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Stub endpoint for current user information."""
    return {
        "user_id": "stub-user-id",
        "username": "stub-user",
        "message": "This is a stub endpoint. JWT verification not yet implemented."
    }
