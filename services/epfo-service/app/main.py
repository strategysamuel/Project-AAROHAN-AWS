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

from app.models import EPFOEstablishmentProfile, EPFOContribution
from app.schemas import EPFOProfileResponse, EPFOSyncRequest
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "epfo-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("epfo-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN EPFO & ESIC Integration Gateway Service",
    description="consented India EPFO/ESIC employer verification, payroll stability audits, and Gemini workforce intelligence summaries",
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

# EPFO mock data generator
def pull_epfo_mock_registry_data(est_id: str) -> dict:
    return {
        "establishment_id": est_id,
        "establishment_name": "Project AAROHAN Textiles Private Limited",
        "esic_registration_num": "27000283726354890",
        "status": "ACTIVE",
        "number_of_employees": 28,
        "average_monthly_payroll": 420000.0,
        "contributions": [
            {"wage_month": "042025", "amount_paid": 50400.0, "employees_count": 28, "payment_date": datetime.datetime(2025, 5, 12), "status": "PAID"},
            {"wage_month": "052025", "amount_paid": 50400.0, "employees_count": 28, "payment_date": datetime.datetime(2025, 6, 14), "status": "PAID"},
            {"wage_month": "062025", "amount_paid": 54000.0, "employees_count": 30, "payment_date": datetime.datetime(2025, 7, 10), "status": "PAID"}
        ]
    }

# REST APIs

@app.post("/epfo/sync/{customer_id}", response_model=EPFOProfileResponse, status_code=status.HTTP_200_OK)
async def sync_epfo_data(customer_id: int, payload: EPFOSyncRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Synchronizing EPFO registry details | Est ID: {payload.establishment_id} | Customer: {customer_id}")
    
    # Delete existing profiles for idempotency
    existing = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.customer_id == customer_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        
    reg = pull_epfo_mock_registry_data(payload.establishment_id)
    
    profile = EPFOEstablishmentProfile(
        customer_id=customer_id,
        establishment_id=reg["establishment_id"],
        establishment_name=reg["establishment_name"],
        esic_registration_num=payload.esic_registration_num or reg["esic_registration_num"],
        status=reg["status"],
        number_of_employees=reg["number_of_employees"],
        average_monthly_payroll=reg["average_monthly_payroll"]
    )
    db.add(profile)
    db.flush() # Populate profile ID
    
    # Map Contributions
    for c in reg["contributions"]:
        contrib = EPFOContribution(
            profile_id=profile.id,
            wage_month=c["wage_month"],
            amount_paid=c["amount_paid"],
            employees_count=c["employees_count"],
            payment_date=c["payment_date"],
            status=c["status"]
        )
        db.add(contrib)
        
    db.commit()
    db.refresh(profile)
    
    # Event simulation trigger in logs (Future Pub/Sub topic push)
    logger.info(f"AUDIT | EPFO Workforce Registry synchronization completed | Event: bank.aarohan.spreading.completed")
    return profile

@app.get("/epfo/profile/{customer_id}", response_model=EPFOProfileResponse)
async def get_epfo_profile(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EPFO employer profile details not found. Synchronize first."
        )
    return profile

@app.get("/livez")
async def livez():
    return {"status": "UP"}
