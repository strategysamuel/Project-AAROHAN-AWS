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

from app.models import MCACompanyProfile, MCADirector, MCACharge, MCACompanyFiling
from app.schemas import MCACompanyProfileResponse, MCASyncRequest
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "mca-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("mca-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN MCA Corporate Registry Integration Gateway Service",
    description="consented Ministry of Corporate Affairs (MCA) sync records, directors checklists, active charges, and filings history",
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

# MCA mock data generator
def pull_mca_mock_registry_data(cin: str) -> dict:
    return {
        "cin": cin,
        "company_name": "Project AAROHAN Textiles Private Limited",
        "incorporation_date": datetime.datetime(2018, 5, 20),
        "company_status": "ACTIVE",
        "class_of_company": "Private Limited",
        "authorized_capital": 50000000.0,
        "paid_up_capital": 35000000.0,
        "directors": [
            {"din": "08192837", "full_name": "Aditya Patel", "appointment_date": datetime.datetime(2018, 5, 20)},
            {"din": "09283746", "full_name": "Sanjay Patel", "appointment_date": datetime.datetime(2020, 8, 15)}
        ],
        "charges": [
            {"charge_id": "CHG-9988-293", "holder_name": "State Bank of India", "charge_amount": 15000000.0, "creation_date": datetime.datetime(2021, 10, 5), "status": "OPEN"},
            {"charge_id": "CHG-9988-555", "holder_name": "IDBI Bank", "charge_amount": 8000000.0, "creation_date": datetime.datetime(2024, 2, 11), "status": "OPEN"}
        ],
        "filings": [
            {"form_name": "AOC-4", "filing_date": datetime.datetime(2025, 10, 22), "status": "APPROVED"},
            {"form_name": "MGT-7", "filing_date": datetime.datetime(2025, 11, 5), "status": "APPROVED"}
        ]
    }

# REST APIs

@app.post("/mca/sync/{customer_id}", response_model=MCACompanyProfileResponse, status_code=status.HTTP_200_OK)
async def sync_mca_data(customer_id: int, payload: MCASyncRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Synchronizing MCA registry details | CIN: {payload.cin} | Customer: {customer_id}")
    
    # Delete existing profiles for idempotency
    existing = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        
    reg = pull_mca_mock_registry_data(payload.cin)
    
    # Create profile
    profile = MCACompanyProfile(
        customer_id=customer_id,
        cin=reg["cin"],
        company_name=reg["company_name"],
        incorporation_date=reg["incorporation_date"],
        company_status=reg["company_status"],
        class_of_company=reg["class_of_company"],
        authorized_capital=reg["authorized_capital"],
        paid_up_capital=reg["paid_up_capital"]
    )
    db.add(profile)
    db.flush() # Populate profile ID
    
    # Map Directors
    for d in reg["directors"]:
        director = MCADirector(
            company_id=profile.id,
            din=d["din"],
            full_name=d["full_name"],
            appointment_date=d["appointment_date"]
        )
        db.add(director)
        
    # Map Charges
    for c in reg["charges"]:
        charge = MCACharge(
            company_id=profile.id,
            charge_id=c["charge_id"],
            holder_name=c["holder_name"],
            charge_amount=c["charge_amount"],
            creation_date=c["creation_date"],
            status=c["status"]
        )
        db.add(charge)
        
    # Map Filings
    for f in reg["filings"]:
        filing = MCACompanyFiling(
            company_id=profile.id,
            form_name=f["form_name"],
            filing_date=f["filing_date"],
            status=f["status"]
        )
        db.add(filing)
        
    db.commit()
    db.refresh(profile)
    
    # Event simulation trigger in logs (Future Pub/Sub topic push)
    logger.info(f"AUDIT | MCA Corporate Registry synchronization completed | Event: bank.aarohan.spreading.completed")
    return profile

@app.get("/mca/profile/{customer_id}", response_model=MCACompanyProfileResponse)
async def get_mca_profile(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MCA corporate profile details not found. Synchronize first."
        )
    return profile

@app.get("/livez")
async def livez():
    return {"status": "UP"}
