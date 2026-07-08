import logging
import sys
import time
import uuid
import math
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import GSTProfile, GSTReturn, GSTAnalytics
from app.schemas import GSTProfileResponse, GSTAnalyticsResponse, GSTSyncRequest
from app.database import get_db, init_db
from app.providers import GSTNMockProvider

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "gst-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("gst-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN GSTN Integration & Financial Analytics Service",
    description="Corporate tax history ingestion, compliance evaluation, and business turnover forecasting pipelines",
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

# Financial Analytics Helper Functions
def run_financial_analytics(profile_id: int, db: Session):
    returns = db.query(GSTReturn).filter(
        GSTReturn.profile_id == profile_id,
        GSTReturn.return_type == "GSTR1"
    ).all()
    
    if not returns:
        return
        
    turnovers = [r.gross_turnover for r in returns]
    delay_days = [r.filing_delay_days for r in returns]
    
    # 1. Average Monthly Turnover
    avg_turnover = sum(turnovers) / len(turnovers)
    
    # 2. Peak Month
    max_idx = turnovers.index(max(turnovers))
    peak_month = returns[max_idx].tax_period
    
    # 3. Revenue Growth Rate (MoM average)
    mom_rates = []
    for idx in range(1, len(turnovers)):
        prev = turnovers[idx-1]
        if prev > 0:
            mom_rates.append(((turnovers[idx] - prev) / prev) * 100)
    avg_growth = sum(mom_rates) / len(mom_rates) if mom_rates else 0.0
    
    # 4. Revenue Stability (1 - Coeff of Variation)
    if avg_turnover > 0:
        variance = sum((x - avg_turnover) ** 2 for x in turnovers) / len(turnovers)
        std_dev = math.sqrt(variance)
        stability = max(0.0, 1.0 - (std_dev / avg_turnover))
    else:
        stability = 0.0
        
    # 5. Compliance & Filing Delay Scores
    compliance = 100.0 # Standard active filing state
    total_delays = sum(delay_days)
    delay_score = max(0.0, 100.0 - (total_delays * 3))
    
    # 6. Seasonality Index
    seasonality = max(turnovers) / min(turnovers) if min(turnovers) > 0 else 0.0
    
    # Write calculations to database
    analytics = db.query(GSTAnalytics).filter(GSTAnalytics.profile_id == profile_id).first()
    if not analytics:
        analytics = GSTAnalytics(profile_id=profile_id)
        db.add(analytics)
        
    analytics.avg_monthly_turnover = avg_turnover
    analytics.peak_turnover_month = peak_month
    analytics.revenue_growth_rate = avg_growth
    analytics.revenue_stability = stability
    analytics.compliance_score = compliance
    analytics.filing_delay_score = delay_score
    analytics.seasonality_index = seasonality
    
    db.commit()
    logger.info(f"AUDIT | Financial Analytics processed successfully for Profile: {profile_id}")

# REST APIs

@app.post("/gst/sync/{customer_id}", response_model=GSTProfileResponse, status_code=status.HTTP_200_OK)
async def sync_gst_data(customer_id: int, payload: GSTSyncRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Synchronizing GST data for Customer ID: {customer_id} | GSTIN: {payload.gstin}")
    
    # Delete existing profiles for idempotency
    existing = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        
    # Call mock DPI Provider Interface
    provider = GSTNMockProvider()
    profile_data = provider.fetch_gst_profile(payload.gstin)
    return_history = provider.fetch_return_filing_history(payload.gstin)
    
    # Write to local SQLite database
    profile = GSTProfile(
        customer_id=customer_id,
        gstin=profile_data["gstin"],
        legal_name=profile_data["legal_name"],
        trade_name=profile_data["trade_name"],
        registration_date=profile_data["registration_date"],
        status=profile_data["status"]
    )
    db.add(profile)
    db.flush() # Populate profile ID
    
    for r in return_history:
        ret = GSTReturn(
            profile_id=profile.id,
            return_type=r["return_type"],
            financial_year=r["financial_year"],
            tax_period=r["tax_period"],
            filing_date=r["filing_date"],
            status=r["status"],
            gross_turnover=r["gross_turnover"],
            tax_paid=r["tax_paid"],
            filing_delay_days=r["filing_delay_days"]
        )
        db.add(ret)
        
    db.commit()
    
    # Run analytical engine calculations
    run_financial_analytics(profile.id, db)
    
    db.refresh(profile)
    logger.info(f"AUDIT | GST synchronization complete | Event: bank.aarohan.spreading.completed")
    return profile

@app.get("/gst/profile/{customer_id}", response_model=GSTProfileResponse)
async def get_gst_profile(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GST Profile details not found."
        )
    return profile

@app.get("/gst/analytics/{customer_id}", response_model=GSTAnalyticsResponse)
async def get_gst_analytics(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GST Profile not found."
        )
    analytics = db.query(GSTAnalytics).filter(GSTAnalytics.profile_id == profile.id).first()
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analytics metrics not calculated."
        )
    return analytics

@app.get("/livez")
async def livez():
    return {"status": "UP"}
