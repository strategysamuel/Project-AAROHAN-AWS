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

from app.models import FinancialHealthCard, ScoreHistory
from app.schemas import FinancialHealthCardResponse, ScoreHistoryResponse
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "fhc-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("fhc-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN Financial Health Card Engine Service",
    description="Business stability index calculations, compliance health, and AI readiness pipelines",
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

# Scoring calculation helper
def calculate_financial_health(customer_id: int) -> dict:
    # Simulates pulling and aggregating values from GST (turnover growth) and AA (cash flow ratios)
    rev_score = 88.0
    cf_score = 82.0
    liq_score = 75.0
    bb_score = 90.0
    comp_score = 95.0
    grow_score = 80.0
    
    # Configurable weighted score summation logic
    overall = (
        (rev_score * 0.20) +
        (cf_score * 0.20) +
        (liq_score * 0.15) +
        (bb_score * 0.15) +
        (comp_score * 0.15) +
        (grow_score * 0.15)
    )
    
    key_strengths = (
        "Strong compliance consistency (95%);"
        "Stable transaction behavior with zero bank defaults;"
        "Healthy GSTR-1 turnover growth of 88%"
    )
    risk_concerns = (
        "Moderate current account liquidity variance (75%);"
        "Minor filing delay of 5 days in Q2 tax periods"
    )
    
    return {
        "overall": overall,
        "revenue": rev_score,
        "cash_flow": cf_score,
        "liquidity": liq_score,
        "banking": bb_score,
        "compliance": comp_score,
        "growth": grow_score,
        "key_strengths": key_strengths,
        "risk_concerns": risk_concerns
    }

# REST APIs

@app.post("/fhc/calculate/{customer_id}", response_model=FinancialHealthCardResponse)
async def trigger_score_calculation(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Triggering scoring engine calculations for Customer: {customer_id}")
    
    results = calculate_financial_health(customer_id)
    
    # Query or Create card
    card = db.query(FinancialHealthCard).filter(FinancialHealthCard.customer_id == customer_id).first()
    if not card:
        card = FinancialHealthCard(customer_id=customer_id)
        db.add(card)
        db.flush()
        
    card.overall_score = results["overall"]
    card.revenue_health_score = results["revenue"]
    card.cash_flow_score = results["cash_flow"]
    card.liquidity_score = results["liquidity"]
    card.banking_behaviour_score = results["banking"]
    card.compliance_score = results["compliance"]
    card.growth_score = results["growth"]
    card.key_strengths = results["key_strengths"]
    card.risk_concerns = results["risk_concerns"]
    
    # Add to Score History
    history_record = ScoreHistory(
        card_id=card.id,
        score_value=results["overall"]
    )
    db.add(history_record)
    db.commit()
    
    db.refresh(card)
    logger.info(f"AUDIT | Scoring engine calculations completed | Score: {card.overall_score:.2f} | Event: bank.aarohan.score.calculated")
    return card

@app.get("/fhc/{customer_id}", response_model=FinancialHealthCardResponse)
async def get_health_card(customer_id: int, db: Session = Depends(get_db)):
    card = db.query(FinancialHealthCard).filter(FinancialHealthCard.customer_id == customer_id).first()
    if not card:
        # Auto-calculate if first query
        return await trigger_score_calculation(customer_id, db)
    return card

@app.get("/fhc/history/{customer_id}", response_model=List[ScoreHistoryResponse])
async def get_score_history(customer_id: int, db: Session = Depends(get_db)):
    card = db.query(FinancialHealthCard).filter(FinancialHealthCard.customer_id == customer_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health card not found. Calculate score first."
        )
    return db.query(ScoreHistory).filter(ScoreHistory.card_id == card.id).all()

@app.get("/livez")
async def livez():
    return {"status": "UP"}
