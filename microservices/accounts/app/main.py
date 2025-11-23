"""
Accounts Microservice - FastAPI Application

Provides user authentication and account management endpoints.
"""
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid

app = FastAPI(title="Accounts Service", version="0.1.0")


class UserCreate(BaseModel):
    """User creation request model."""
    phone_number: str
    password: str
    date_of_birth: Optional[str] = None


class UserResponse(BaseModel):
    """User response model."""
    user_id: str
    phone_number: str
    date_of_birth: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: str


class AccountResponse(BaseModel):
    """Account response model."""
    account_id: str
    user_id: str
    balance: str
    created_at: str


class TransactionRequest(BaseModel):
    """Transaction request model."""
    sender_id: str
    receiver_id: str
    amount: str
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    """Transaction response model."""
    transaction_id: str
    sender_id: str
    receiver_id: str
    amount: str
    status: str
    created_at: str


# In-memory storage for demonstration (replace with database in production)
users = {}
accounts = {}
transactions = {}


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


@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user."""
    user_id = str(uuid.uuid4())
    
    # Check if phone number already exists
    for existing_user in users.values():
        if existing_user["phone_number"] == user.phone_number:
            raise HTTPException(status_code=400, detail="Phone number already exists")
    
    users[user_id] = {
        "phone_number": user.phone_number,
        "password": user.password,  # In production, hash this!
        "date_of_birth": user.date_of_birth,
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Create account for user
    account_id = str(uuid.uuid4())
    accounts[account_id] = {
        "user_id": user_id,
        "balance": "0.00",
        "created_at": datetime.utcnow().isoformat()
    }
    
    return UserResponse(
        user_id=user_id,
        phone_number=users[user_id]["phone_number"],
        date_of_birth=users[user_id]["date_of_birth"],
        is_active=users[user_id]["is_active"],
        is_admin=users[user_id]["is_admin"],
        created_at=users[user_id]["created_at"]
    )


@app.get("/users/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Stub endpoint for current user information."""
    return {
        "user_id": "stub-user-id",
        "username": "stub-user",
        "message": "This is a stub endpoint. JWT verification not yet implemented."
    }


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get user by ID."""
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users[user_id]
    return UserResponse(
        user_id=user_id,
        phone_number=user["phone_number"],
        date_of_birth=user["date_of_birth"],
        is_active=user["is_active"],
        is_admin=user["is_admin"],
        created_at=user["created_at"]
    )


@app.get("/accounts/user/{user_id}", response_model=AccountResponse)
async def get_account_by_user(user_id: str):
    """Get account for a user."""
    for account_id, account in accounts.items():
        if account["user_id"] == user_id:
            return AccountResponse(
                account_id=account_id,
                user_id=account["user_id"],
                balance=account["balance"],
                created_at=account["created_at"]
            )
    
    raise HTTPException(status_code=404, detail="Account not found")


@app.post("/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionRequest):
    """Create a transaction between accounts."""
    # Validate accounts exist
    sender_account = None
    receiver_account = None
    
    for acc_id, acc in accounts.items():
        if acc_id == transaction.sender_id:
            sender_account = acc
        if acc_id == transaction.receiver_id:
            receiver_account = acc
    
    if not sender_account:
        raise HTTPException(status_code=404, detail="Sender account not found")
    if not receiver_account:
        raise HTTPException(status_code=404, detail="Receiver account not found")
    
    # Check sufficient balance
    amount = Decimal(transaction.amount)
    sender_balance = Decimal(sender_account["balance"])
    
    if sender_balance < amount:
        status = "FAILED"
    else:
        # Update balances
        sender_account["balance"] = str(sender_balance - amount)
        receiver_account["balance"] = str(Decimal(receiver_account["balance"]) + amount)
        status = "SUCCESS"
    
    transaction_id = str(uuid.uuid4())
    transactions[transaction_id] = {
        "sender_id": transaction.sender_id,
        "receiver_id": transaction.receiver_id,
        "amount": transaction.amount,
        "status": status,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return TransactionResponse(
        transaction_id=transaction_id,
        sender_id=transaction.sender_id,
        receiver_id=transaction.receiver_id,
        amount=transaction.amount,
        status=status,
        created_at=transactions[transaction_id]["created_at"]
    )


@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str):
    """Get transaction by ID."""
    if transaction_id not in transactions:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    txn = transactions[transaction_id]
    return TransactionResponse(
        transaction_id=transaction_id,
        sender_id=txn["sender_id"],
        receiver_id=txn["receiver_id"],
        amount=txn["amount"],
        status=txn["status"],
        created_at=txn["created_at"]
    )
