import logging
import sys
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import EWSWatchlist, EWSAlert, EWSRiskCase
from app.schemas import EWSWatchlistResponse, EWSAlertResponse, EWSRiskCaseResponse, EscalationRequest
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "ews-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ews-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN Enterprise Early Warning System (EWS) Service",
    description="consented risk rule evaluations, watchlist triggers, and AI risk narrative compilations",
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

# REST APIs

@app.post("/ews/evaluate/{customer_id}", response_model=EWSRiskCaseResponse)
async def evaluate_early_warning_signals(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Evaluating risk metrics for Customer ID: {customer_id}")
    
    # 1. Simulates running risk rule engine checks:
    # Rule A: Check if customer has active GST delay warnings.
    # Rule B: Check if account aggregator deposits dropped > 10% MoM.
    # Let's register a watchlist hit for simulation
    
    watchlist_entry = db.query(EWSWatchlist).filter(EWSWatchlist.customer_id == customer_id).first()
    if not watchlist_entry:
        watchlist_entry = EWSWatchlist(
            customer_id=customer_id,
            risk_level="HIGH",
            reason_code="RULE_GST_CASHFLOW_COLLISION"
        )
        db.add(watchlist_entry)
        
    # Trigger new alerts
    alert = EWSAlert(
        customer_id=customer_id,
        trigger_rule="RULE_GST_CASHFLOW_COLLISION",
        message="GST filing delay of 5 days overlaps with current account balance dip of 15%."
    )
    db.add(alert)
    
    # Generate Gemini Risk Narrative
    narrative = (
        "Gemini Early Warning Risk Report:\n"
        "Customer displays an elevated risk profile due to a combined GST filing delay (+5 days) "
        "and MoM cash flow decline (-15%) on their primary current account. "
        "Current balance buffers are constrained, increasing the default probability index. "
        "Escalation recommendation: Move case to high-priority underwriter review queue."
    )
    
    case = db.query(EWSRiskCase).filter(EWSRiskCase.customer_id == customer_id).first()
    if not case:
        case = EWSRiskCase(customer_id=customer_id)
        db.add(case)
        
    case.status = "OPEN"
    case.ai_risk_narrative = narrative
    case.mitigation_action = "Schedule relationship review meeting; verify upcoming vendor receivables invoice."
    
    db.commit()
    db.refresh(case)
    
    logger.info(f"AUDIT | Early warning evaluation complete | Case ID: {case.id} | Event: bank.aarohan.ews.completed")
    return case

@app.get("/ews/cases", response_model=List[EWSRiskCaseResponse])
async def list_active_cases(db: Session = Depends(get_db)):
    return db.query(EWSRiskCase).all()

@app.post("/ews/cases/{id}/escalate", response_model=EWSRiskCaseResponse)
async def escalate_risk_case(id: int, payload: EscalationRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Escalating Risk Case ID: {id} | Underwriter comments: {payload.comments}")
    
    case = db.query(EWSRiskCase).filter(EWSRiskCase.id == id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk case not found."
        )
        
    case.status = "ESCALATED"
    case.mitigation_action = f"Escalated action: {payload.comments}"
    db.commit()
    db.refresh(case)
    
    logger.info(f"AUDIT | Risk Case ID: {id} escalated successfully")
    return case

@app.get("/ews/watchlist", response_model=List[EWSWatchlistResponse])
async def list_watchlist(db: Session = Depends(get_db)):
    return db.query(EWSWatchlist).all()

@app.get("/livez")
async def livez():
    return {"status": "UP"}
