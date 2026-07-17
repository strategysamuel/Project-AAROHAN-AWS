import logging
import sys
import time
import uuid
import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import Consent, ConsentArtifact, ConsentPurpose
from app.schemas import ConsentCreate, ConsentResponse, ConsentApprovalRequest, ConsentPurposeResponse
from app.database import get_db, init_db
from app.providers import get_provider

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "consent-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("consent-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN Consent Management Service",
    description="DPI-compatible consent request, validation, and audit tracking platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom auditing and Correlation ID middleware
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

# REST APIs

@app.post("/consents", response_model=ConsentResponse, status_code=status.HTTP_201_CREATED)
async def create_consent(payload: ConsentCreate, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Initiating Consent request for Customer: {payload.customer_id} | Provider: {payload.provider_type}")
    
    # Verify purpose exists
    purpose = db.query(ConsentPurpose).filter(ConsentPurpose.code == payload.purpose_code).first()
    if not purpose:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Consent purpose code '{payload.purpose_code}' is invalid."
        )
        
    consent = Consent(
        customer_id=payload.customer_id,
        provider_type=payload.provider_type,
        purpose_code=payload.purpose_code,
        valid_until=payload.valid_until,
        status="PENDING"
    )
    db.add(consent)
    db.commit()
    db.refresh(consent)
    
    # Event simulation trigger in logs (Future Pub/Sub topic push)
    logger.info(f"AUDIT | Event dispatched: bank.aarohan.consent.initiated | Consent ID: {consent.id}")
    return consent

@app.post("/consents/{id}/approve", response_model=ConsentResponse)
async def approve_consent(id: int, payload: ConsentApprovalRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Approving Consent ID: {id}")
    
    consent = db.query(Consent).filter(Consent.id == id).first()
    if not consent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consent record not found."
        )
        
    if consent.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve consent in status '{consent.status}'."
        )
        
    # Generate digital signature verification audit artifact
    artifact = ConsentArtifact(
        consent_id=consent.id,
        signature_hash=payload.signature_hash
    )
    db.add(artifact)
    
    consent.status = "APPROVED"
    db.commit()
    db.refresh(consent)
    
    logger.info(f"AUDIT | Consent ID: {id} approved successfully | Event: bank.aarohan.consent.completed")
    return consent

@app.post("/consents/{id}/revoke", response_model=ConsentResponse)
async def revoke_consent(id: int, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Revoking Consent ID: {id}")
    
    consent = db.query(Consent).filter(Consent.id == id).first()
    if not consent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consent record not found."
        )
        
    if consent.status != "APPROVED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot revoke consent in status '{consent.status}'. Only active consents can be revoked."
        )
        
    consent.status = "REVOKED"
    db.commit()
    db.refresh(consent)
    
    logger.info(f"AUDIT | Consent ID: {id} revoked | Event: bank.aarohan.consent.revoked")
    return consent

@app.get("/consents", response_model=List[ConsentResponse])
async def list_consents(
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Consent)
    if customer_id is not None:
        query = query.filter(Consent.customer_id == customer_id)
    if status is not None:
        query = query.filter(Consent.status == status)
        
    return query.offset(offset).limit(limit).all()

@app.get("/consents/purposes", response_model=List[ConsentPurposeResponse])
async def list_purposes(db: Session = Depends(get_db)):
    return db.query(ConsentPurpose).all()

@app.post("/consents/check-expiries")
async def check_expiries(db: Session = Depends(get_db)):
    """Automated cron checking and changing status for expired records"""
    logger.info("AUDIT | Running consent expiry scan scheduler")
    now = datetime.datetime.now(datetime.UTC)
    
    expired_records = db.query(Consent).filter(
        Consent.status == "APPROVED",
        Consent.valid_until <= now
    ).all()
    
    count = len(expired_records)
    for record in expired_records:
        record.status = "EXPIRED"
        
    if count > 0:
        db.commit()
        logger.info(f"AUDIT | Expiry Scheduler updated {count} records to EXPIRED")
        
    return {"message": f"Scan completed. Expired records updated: {count}"}

@app.get("/livez")
async def livez():
    return {"status": "UP"}
