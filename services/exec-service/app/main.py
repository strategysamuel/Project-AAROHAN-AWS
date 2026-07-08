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

from app.models import ExecKPI, ExecBranchPerformance
from app.schemas import ExecKPIResponse, ExecBranchPerformanceResponse, ExecutiveBriefingResponse
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "exec-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("exec-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN Executive Command Center & Portfolio Intelligence Service",
    description="Enterprise KPI aggregates, branch leaderboards, and Gemini executive board briefings",
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

@app.get("/exec/kpis", response_model=List[ExecKPIResponse])
async def list_kpis(db: Session = Depends(get_db)):
    return db.query(ExecKPI).all()

@app.get("/exec/branches", response_model=List[ExecBranchPerformanceResponse])
async def list_branches(db: Session = Depends(get_db)):
    return db.query(ExecBranchPerformance).order_by(ExecBranchPerformance.loan_disbursed_amt.desc()).all()

@app.get("/exec/briefing", response_model=ExecutiveBriefingResponse)
async def get_executive_briefing(db: Session = Depends(get_db)):
    logger.info("AUDIT | Generating daily AI board briefing report via Gemini Analytics")
    
    # Simulates pulling portfolio volume metrics and regional concentrations from BigQuery
    summary_text = (
        "Project AAROHAN Portfolio Performance Brief:\n"
        "Total disbursed volume has reached ₹245 Crores across 1,240 active MSME accounts. "
        "Average financial health rating stands at 82.4/100, indicating low systematic risk. "
        "Mumbai Corporate and Coimbatore MSME Hubs account for 79% of active portfolio allocations, "
        "representing high regional concentration in South and West zones."
    )
    
    risk_warnings = [
        "High regional concentration in Coimbatore and Mumbai zones (79% of total portfolio).",
        "Average Current Account balance variance noted in retail segments MoM."
    ]
    
    strategic_recommendations = [
        "Accelerate Ludhiana and North zone marketing campaigns to diversify regional exposure.",
        "Launch targeted interest subvention schemes for light engineering manufacturing sectors."
    ]
    
    return ExecutiveBriefingResponse(
        briefing_date=datetime.date.today(),
        summary_text=summary_text,
        risk_warnings=risk_warnings,
        strategic_recommendations=strategic_recommendations
    )

@app.get("/livez")
async def livez():
    return {"status": "UP"}
