import logging
import sys
import datetime
import time
import uuid
from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.models import User, RefreshToken
from app.auth import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_access_token,
    TokenData,
    oauth2_scheme,
    PermissionChecker
)
from app.database import get_db, seed_database

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "auth-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("auth-service")

# Seed database on startup
seed_database()

app = FastAPI(
    title="AAROHAN Identity Service",
    description="Identity management, login, logout, and token orchestration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom HTTP Middleware for Auditing & Correlation IDs
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    logger.info(f"AUDIT | Request: {request.method} {request.url.path} | Correlation ID: {correlation_id}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Correlation-ID"] = correlation_id
    
    logger.info(f"AUDIT | Completed: {request.method} {request.url.path} | Status: {response.status_code} | Process Time: {process_time:.4f}s")
    return response

# Custom HTTP Exception Handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorCode": f"AAR-ERR-{exc.status_code}",
            "message": exc.detail,
            "correlationId": correlation_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "details": []
        }
    )

# Pydantic Schemas
class LoginRequest(BaseModel):
    mobile_number: str = Field(..., pattern=r"^\d{10}$")
    password: str = Field(..., min_length=6)

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900
    role: str

class UserProfileResponse(BaseModel):
    id: int
    mobile_number: str
    email: str | None
    full_name: str
    role: str
    permissions: List[str]

# Endpoints
@app.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Login attempt | Mobile: {payload.mobile_number}")
    
    user = db.query(User).filter(User.mobile_number == payload.mobile_number).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        logger.warning(f"AUDIT | Login failed | Mobile: {payload.mobile_number}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect mobile number or password."
        )
        
    permissions = [p.name for p in user.role.permissions]
    access = create_access_token(user.id, user.mobile_number, user.role.name, permissions)
    refresh = create_refresh_token(user.id)
    
    # Store refresh token record in SQLite
    refresh_record = RefreshToken(
        user_id=user.id,
        token=refresh,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
    )
    db.add(refresh_record)
    db.commit()
    
    logger.info(f"AUDIT | Login successful | User: {user.id} | Role: {user.role.name}")
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        role=user.role.name
    )

@app.post("/auth/token/refresh", response_model=TokenResponse)
async def refresh_token(payload: TokenRefreshRequest, db: Session = Depends(get_db)):
    logger.info("AUDIT | Token refresh requested")
    
    record = db.query(RefreshToken).filter(
        RefreshToken.token == payload.refresh_token,
        RefreshToken.is_revoked == False
    ).first()
    
    if not record:
        logger.warning("AUDIT | Refresh token rejected: token not found or revoked")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired or refresh token is invalid."
        )
        
    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with token not found."
        )
        
    permissions = [p.name for p in user.role.permissions]
    new_access = create_access_token(user.id, user.mobile_number, user.role.name, permissions)
    
    logger.info(f"AUDIT | Token refreshed successfully | User: {user.id}")
    return TokenResponse(
        access_token=new_access,
        refresh_token=payload.refresh_token,
        role=user.role.name
    )

@app.post("/auth/logout")
async def logout(payload: TokenRefreshRequest, db: Session = Depends(get_db)):
    logger.info("AUDIT | Logout requested")
    record = db.query(RefreshToken).filter(RefreshToken.token == payload.refresh_token).first()
    if record:
        record.is_revoked = True
        db.commit()
    logger.info("AUDIT | Session revoked successfully")
    return {"message": "Logged out successfully."}

@app.get("/auth/me", response_model=UserProfileResponse)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = verify_access_token(token)
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found."
        )
        
    permissions = [p.name for p in user.role.permissions]
    return UserProfileResponse(
        id=user.id,
        mobile_number=user.mobile_number,
        email=user.email,
        full_name=user.full_name,
        role=user.role.name,
        permissions=permissions
    )

# Protected Test Endpoint validating permission scope logic
@app.get("/auth/test-permission")
async def test_permission(token_data: TokenData = Depends(PermissionChecker("loan:approve"))):
    return {"message": f"Welcome user {token_data.user_id}. Access granted for 'loan:approve' permission."}

@app.get("/livez")
async def livez():
    return {"status": "UP"}

@app.get("/health")
async def health():
    return {"status": "UP"}

@app.get("/readiness")
async def readiness():
    return {"status": "READY"}
