import logging
import sys
import time
import uuid
import datetime
import re
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import CKYCRecord, CKYCVerificationLog, OnboardingCustomer, OnboardingAddress
from app.schemas import (
    CKYCRecordResponse, CKYCVerificationLogResponse, CKYCSearchRequest, CKYCVerificationRequest,
    CKYCRecordCreate, CKYCRecordUpdate, CKYCOverrideRequest
)
from app.database import get_db, init_db
from app.adapters import get_ckyc_adapter

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
    title="AAROHAN CKYC Registry Integration & Verification Service",
    description="Identity verification, confidence scoring, risk indicator analysis, and central registry simulation for MSME lending onboarding",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Audit log helper
def publish_workflow_event(event_type: str, customer_id: int, payload: dict):
    # Log for event engine tracking
    logger.info(f"AUDIT | EVENT_BUS | Published: {event_type} | Customer: {customer_id} | Payload: {payload}")
    # Dispatch to ESE Core Event Engine if available
    try:
        from event_engine import BusinessEventEngine
        engine = BusinessEventEngine()
        engine.dispatch(event_type, f"cust_{customer_id}", payload)
    except Exception as e:
        logger.warning(f"ESE core event engine dispatch skipped: {e}")

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

@app.get("/ckyc/stats", response_model=dict)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    records = db.query(CKYCRecord).all()
    stats = {
        "VERIFIED": 0,
        "VERIFIED_WITH_WARNING": 0,
        "PENDING": 0,
        "MANUAL_REVIEW": 0,
        "FAILED": 0,
        "DUPLICATE_RECORD": 0,
        "DATA_MISMATCH": 0,
        "TOTAL": len(records)
    }
    for r in records:
        status_key = r.kyc_status.upper().replace(" ", "_")
        if status_key in stats:
            stats[status_key] += 1
    return stats

@app.post("/ckyc/search", response_model=CKYCRecordResponse)
async def search_ckyc_registry(payload: CKYCSearchRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Dispatching CKYC Registry Search | PAN: {payload.pan}")
    
    # Check if local record exists, otherwise create
    record = db.query(CKYCRecord).filter(CKYCRecord.pan == payload.pan).first()
    if not record:
        adapter = get_ckyc_adapter()
        reg = adapter.fetch_record(payload.pan)
        
        # Search onboarding database for mapping, else mock ID
        onb_cust = db.query(OnboardingCustomer).filter(OnboardingCustomer.pan == payload.pan).first()
        customer_id = onb_cust.id if onb_cust else 125
        
        record = CKYCRecord(
            customer_id=customer_id,
            ckyc_number=reg["ckyc_number"],
            full_name=reg["full_name"],
            dob=reg["dob"],
            pan=reg["pan"],
            aadhaar_masked=reg.get("aadhaar_masked", "XXXXXXXX1234"),
            address=reg.get("address", "123 MSME Road, City, State - 400001"),
            mobile=reg.get("mobile", "9876543210"),
            email=reg.get("email", "info@ckyc.gov.in"),
            kyc_status=reg["kyc_status"]
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
    logger.info(f"AUDIT | CKYC Search found record for PAN: {payload.pan} | CKYC Num: {record.ckyc_number}")
    return record

@app.post("/ckyc/records", response_model=CKYCRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_simulated_record(payload: CKYCRecordCreate, db: Session = Depends(get_db)):
    # Check if record exists
    existing = db.query(CKYCRecord).filter(
        (CKYCRecord.customer_id == payload.customer_id) | 
        (CKYCRecord.pan == payload.pan) | 
        (CKYCRecord.ckyc_number == payload.ckyc_number)
    ).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A CKYC record with this Customer ID, PAN, or CKYC Number already exists."
        )
    
    record = CKYCRecord(
        customer_id=payload.customer_id,
        ckyc_number=payload.ckyc_number,
        full_name=payload.full_name,
        dob=payload.dob,
        pan=payload.pan,
        aadhaar_masked=payload.aadhaar_masked,
        address=payload.address,
        mobile=payload.mobile,
        email=payload.email,
        kyc_status=payload.kyc_status,
        image_url=payload.image_url
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    logger.info(f"AUDIT | Created simulated CKYC record for PAN: {payload.pan}")
    return record

@app.put("/ckyc/records/{customer_id}", response_model=CKYCRecordResponse)
async def update_simulated_record(customer_id: int, payload: CKYCRecordUpdate, db: Session = Depends(get_db)):
    record = db.query(CKYCRecord).filter(CKYCRecord.customer_id == customer_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="CKYC record not found.")
    
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    logger.info(f"AUDIT | Updated simulated CKYC record for Customer: {customer_id}")
    return record

@app.post("/ckyc/verify/{customer_id}", response_model=CKYCVerificationLogResponse)
async def verify_customer_kyc(customer_id: int, payload: CKYCVerificationRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Executing CKYC verification checks for Customer: {customer_id}")
    
    publish_workflow_event("CKYC Verification Started", customer_id, {"checked_by": payload.checked_by})
    
    # 1. Fetch onboarding customer data
    cust = db.query(OnboardingCustomer).filter(OnboardingCustomer.id == customer_id).first()
    if not cust:
        # Fallback Mock Customer for pure mock tests
        cust = OnboardingCustomer(
            id=customer_id,
            legal_name="Aditya Patel",
            mobile_number="9876543210",
            email="aditya@garments.com",
            pan="ABCDE1234F",
            aadhaar_masked="XXXXXXXX9876",
            district="Mumbai"
        )
    
    # 2. Fetch CKYC record
    record = db.query(CKYCRecord).filter(CKYCRecord.customer_id == customer_id).first()
    if not record:
        # Pull via adapter to auto-link
        adapter = get_ckyc_adapter()
        reg = adapter.fetch_record(cust.pan)
        record = CKYCRecord(
            customer_id=customer_id,
            ckyc_number=reg["ckyc_number"],
            full_name=reg["full_name"],
            dob=reg["dob"],
            pan=reg["pan"],
            aadhaar_masked=reg.get("aadhaar_masked", cust.aadhaar_masked),
            address=reg.get("address", "123 MSME Road, City, State - 400001"),
            mobile=reg.get("mobile", cust.mobile_number),
            email=reg.get("email", cust.email),
            kyc_status=reg["kyc_status"]
        )
        db.add(record)
        db.commit()
        db.refresh(record)

    # 3. Validation Rules and Risk Indicators calculation
    score = 100.0
    risks = []
    anomaly = False
    
    # PAN validation format check
    if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", cust.pan):
        score -= 50
        risks.append("Invalid PAN Format")
        anomaly = True
    
    # Aadhaar validation format check
    if cust.aadhaar_masked and not re.match(r"^(X{8}\d{4})|(\d{12})$", cust.aadhaar_masked):
        score -= 40
        risks.append("Invalid Aadhaar Format")
        anomaly = True
        
    # Duplicate PAN Check
    dup_pan = db.query(OnboardingCustomer).filter(
        OnboardingCustomer.pan == cust.pan, OnboardingCustomer.id != customer_id
    ).first()
    if dup_pan:
        score -= 50
        risks.append("Duplicate Identity")
        anomaly = True
        
    # Duplicate CKYC Number check
    dup_ckyc = db.query(CKYCRecord).filter(
        CKYCRecord.ckyc_number == record.ckyc_number, CKYCRecord.customer_id != customer_id
    ).first()
    if dup_ckyc:
        score -= 50
        risks.append("Duplicate Identity")
        anomaly = True

    # Name similarity check
    name1 = cust.legal_name.lower().replace(" ", "")
    name2 = record.full_name.lower().replace(" ", "")
    overlap = len(set(name1) & set(name2))
    total = max(len(set(name1)), len(set(name2)))
    similarity = overlap / total if total > 0 else 0
    
    if similarity < 0.8:
        score -= 30
        risks.append("Name Mismatch")
        anomaly = True

    # Address consistency check
    onb_addr = db.query(OnboardingAddress).filter(OnboardingAddress.customer_id == customer_id).first()
    if onb_addr and record.address:
        # Check if state or city is missing in CKYC record address
        if onb_addr.state.lower() not in record.address.lower():
            score -= 20
            risks.append("Address Mismatch")
            anomaly = True
            
    # Mobile consistency check
    if cust.mobile_number != record.mobile:
        score -= 15
        risks.append("Mobile Mismatch")
        anomaly = True
        
    # Expired Verification check
    age_delta = datetime.datetime.utcnow() - record.last_synced_at
    if age_delta.days > 365:
        score -= 10
        risks.append("Expired Verification")
        anomaly = True
        
    # High Risk Geography Simulation
    if cust.district and cust.district.lower() in ["jammu", "kashmir", "srinagar", "imphal", "naxalite-zone"]:
        score -= 10
        risks.append("High-Risk Geography (simulation)")
        anomaly = True
        
    score = max(0.0, score)
    
    # 4. Resolve Verification Outcome
    if "Duplicate Identity" in risks:
        status_outcome = "DUPLICATE RECORD"
    elif similarity < 0.4:
        status_outcome = "DATA MISMATCH"
    elif score >= 90:
        status_outcome = "VERIFIED"
    elif score >= 70:
        status_outcome = "VERIFIED WITH WARNING"
    elif score >= 50:
        status_outcome = "MANUAL REVIEW"
    else:
        status_outcome = "FAILED"
        
    # Sync CKYC Record status field
    record.kyc_status = status_outcome
    record.last_synced_at = datetime.datetime.utcnow()
    
    log = CKYCVerificationLog(
        customer_id=customer_id,
        checked_by=payload.checked_by,
        match_confidence=score,
        risk_indicators=",".join(risks),
        anomaly_detected=anomaly,
        verification_status=status_outcome
    )
    
    db.add(log)
    db.commit()
    db.refresh(log)
    
    # Publish Completion events
    event_payload = {
        "customer_id": customer_id,
        "status": status_outcome,
        "score": score,
        "risks": risks
    }
    if status_outcome == "FAILED":
        publish_workflow_event("CKYC Verification Failed", customer_id, event_payload)
    elif status_outcome == "MANUAL_REVIEW" or status_outcome == "MANUAL REVIEW":
        publish_workflow_event("Manual Review Required", customer_id, event_payload)
    else:
        publish_workflow_event("CKYC Verification Completed", customer_id, event_payload)
        
    logger.info(f"AUDIT | CKYC verification complete | Outcome: {status_outcome} | Score: {score}")
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

@app.get("/ckyc/verification-logs", response_model=List[CKYCVerificationLogResponse])
async def list_verification_logs(customer_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(CKYCVerificationLog)
    if customer_id:
        query = query.filter(CKYCVerificationLog.customer_id == customer_id)
    return query.order_by(CKYCVerificationLog.verified_at.desc()).all()

@app.get("/ckyc/manual-queue", response_model=List[CKYCVerificationLogResponse])
async def list_manual_queue(db: Session = Depends(get_db)):
    return db.query(CKYCVerificationLog).filter(
        CKYCVerificationLog.verification_status == "MANUAL REVIEW"
    ).order_by(CKYCVerificationLog.verified_at.desc()).all()

@app.post("/ckyc/override/{log_id}", response_model=CKYCVerificationLogResponse)
async def override_verification(log_id: int, payload: CKYCOverrideRequest, db: Session = Depends(get_db)):
    log = db.query(CKYCVerificationLog).filter(CKYCVerificationLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Verification log not found.")
        
    logger.info(f"AUDIT | Admin Overriding CKYC verification log: {log_id} to status: {payload.status} by: {payload.checked_by}")
    
    # Update verification log
    log.verification_status = payload.status
    log.checked_by = payload.checked_by
    log.comments = payload.comments
    log.verified_at = datetime.datetime.utcnow()
    
    # Update associated CKYC record
    record = db.query(CKYCRecord).filter(CKYCRecord.customer_id == log.customer_id).first()
    if record:
        record.kyc_status = payload.status
        record.last_synced_at = datetime.datetime.utcnow()
        
    db.commit()
    db.refresh(log)
    
    # Publish completion
    publish_workflow_event("CKYC Verification Completed", log.customer_id, {
        "status": payload.status, "score": log.match_confidence, "override": True, "by": payload.checked_by
    })
    
    return log

@app.get("/livez")
async def livez():
    return {"status": "UP"}
