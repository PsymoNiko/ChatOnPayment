"""
Payments Microservice - FastAPI Application

Provides payment processing endpoints with idempotency support.
"""
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title="Payments Service", version="0.1.0")


class PaymentRequest(BaseModel):
    """Payment request model."""
    amount: float
    currency: str = "USD"
    description: Optional[str] = None


class PaymentResponse(BaseModel):
    """Payment response model."""
    payment_id: str
    status: str
    amount: float
    currency: str
    created_at: str


@app.get("/healthz")
async def health_check():
    """Health check endpoint for liveness probe."""
    return {"status": "ok"}


@app.get("/readyz")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready"}


@app.post("/payments", status_code=202)
async def create_payment(
    payment: PaymentRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    """
    Create a payment with idempotency support (stub implementation).
    
    Returns 202 Accepted as processing is asynchronous.
    """
    if not idempotency_key:
        raise HTTPException(
            status_code=400,
            detail="Idempotency-Key header is required"
        )
    
    # Stub implementation - return accepted status
    return PaymentResponse(
        payment_id=f"pay_{idempotency_key[:8]}",
        status="accepted",
        amount=payment.amount,
        currency=payment.currency,
        created_at=datetime.utcnow().isoformat()
    )
