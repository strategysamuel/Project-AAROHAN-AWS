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

from app.models import CKYCRecord, CKYCVerificationLog
from app.schemas import CKYCRecordResponse, CKYCVerificationLogResponse, CKYCSearchRequest, CKYCVerificationRequest
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "ckyc-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ckyc-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN CKYC Registry Integration Gateway Service",
    description="consented India Central KYC search queries, identity match verifications, and Gemini KYC audits",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Correlation ID and auditing middleware
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

# CKYC Mock data generator
def pull_mock_registry_record(pan: str) -> dict:
    return {
        "ckyc_number": "30049281726354",
        "full_name": "Aditya Patel",
        "dob": "12-08-1988",
        "pan": pan,
        "kyc_status": "VERIFIED"
    }

# REST APIs

@app.post("/ckyc/search", response_model=CKYCRecordResponse)
async def search_ckyc_registry(payload: CKYCSearchRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Dispatching CKYC Registry Search | PAN: {payload.pan}")
    
    # Simulates pulling data from the Central Registry
    reg = pull_mock_registry_record(payload.pan)
    
    # Check if local record exists, otherwise create
    record = db.query(CKYCRecord).filter(CKYCRecord.pan == payload.pan).first()
    if not record:
        record = CKYCRecord(
            customer_id=125, # Mock customer mapping
            ckyc_number=reg["ckyc_number"],
            full_name=reg["full_name"],
            dob=reg["dob"],
            pan=reg["pan"],
            kyc_status=reg["kyc_status"]
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
    logger.info(f"AUDIT | CKYC Search found record for PAN: {payload.pan} | CKYC Num: {record.ckyc_number}")
    return record

@app.post("/ckyc/verify/{customer_id}", response_model=CKYCVerificationLogResponse)
async def verify_customer_kyc(customer_id: int, payload: CKYCVerificationRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Executing identity match checks for Customer: {customer_id} | Checked by: {payload.checked_by}")
    
    # Pull CKYC local record
    record = db.query(CKYCRecord).filter(CKYCRecord.customer_id == customer_id).first()
    if not record:
        # Auto-create mock details
        record = CKYCRecord(
            customer_id=customer_id,
            ckyc_number="30049281726354",
            full_name="Aditya Patel",
            dob="12-08-1988",
            pan="ABCDE1234F",
            kyc_status="VERIFIED"
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
    # Calculate identity matching confidence index
    # We compare CKYC full_name with local profile. For mock, let's return 96.5% match
    match_score = 96.5
    anomaly = False
    
    log = CKYCVerificationLog(
        customer_id=customer_id,
        checked_by=payload.checked_by,
        match_confidence=match_score,
        anomaly_detected=anomaly,
        verification_status="MATCHED"
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    
    # Event simulation trigger in logs (Future Pub/Sub topic push)
    logger.info(f"AUDIT | Gemini KYC summary generated | Match Score: {match_score}% | Event: bank.aarohan.kyc.verified")
    return log

@app.get("/ckyc/records/{customer_id}", response_model=CKYCRecordResponse)
async def get_ckyc_record(customer_id: int, db: Session = Depends(get_db)):
    record = db.query(CKYCRecord).filter(CKYCRecord.customer_id == customer_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CKYC sync record not found."
        )
    return record

@app.get("/livez")
async def livez():
    return {"status": "UP"}
