import logging
import sys
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import AICreditDecision, HumanApprovalLog
from app.schemas import AICreditDecisionResponse, EvaluationRequest, ApprovalSubmission
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "credit-engine"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("credit-engine")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN AI Credit Decision Intelligence Engine",
    description="consented credit policy compliance audits, Gemini reasoning generators, and human approval trackers",
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

# Gemini AI reasoning simulation
def run_gemini_credit_reasoning(customer_id: int) -> dict:
    # Simulates consolidations of GST, AA, and FHC metrics inside Gemini 2.x reasoning engine
    # Let's mock a standard approved case
    recommendation = "APPROVED"
    confidence = 86.4
    narrative = (
        "Gemini Credit Intelligence Report:\n"
        "MSME exhibits low default probability based on structured cash flow variables. "
        "Average monthly turnover calculated from GSTR-1 filings stands at ₹24.5 Lakhs with "
        "steady MoM revenue growth rate (+6.8%). Pincode and GST status are verified and active. "
        "Debt service coverage ratio (0.24) indicates sufficient cash buffer to handle working capital limits. "
        "Final underwriting recommendation: APPROVE loan request with a limit of ₹50 Lakhs."
    )
    policy_status = "COMPLIANT"
    
    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "narrative": narrative,
        "policy_status": policy_status
    }

# REST APIs

@app.post("/credit/evaluate/{customer_id}", response_model=AICreditDecisionResponse)
async def evaluate_credit_risk(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Dispatching credit request to Gemini Reasoning Engine for Customer: {customer_id}")
    
    # Run mock Gemini ADK orchestration
    results = run_gemini_credit_reasoning(customer_id)
    
    # Save decision
    decision = AICreditDecision(
        customer_id=customer_id,
        recommendation=results["recommendation"],
        confidence_score=results["confidence"],
        ai_narrative=results["narrative"],
        policy_status=results["policy_status"],
        approval_status="PENDING_HUMAN_REVIEW"
    )
    db.add(decision)
    db.commit()
    db.refresh(decision)
    
    logger.info(f"AUDIT | Gemini credit appraisal completed | Decision ID: {decision.id} | Event: bank.aarohan.credit.evaluated")
    return decision

@app.post("/credit/approve/{decision_id}", response_model=AICreditDecisionResponse)
async def submit_human_approval(decision_id: int, payload: ApprovalSubmission, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Submitting human-in-the-loop sign-off | Decision ID: {decision_id} | Approver: {payload.approver_id}")
    
    decision = db.query(AICreditDecision).filter(AICreditDecision.id == decision_id).first()
    if not decision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credit decision record not found."
        )
        
    if decision.approval_status != "PENDING_HUMAN_REVIEW":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot sign off decision. Current status is '{decision.approval_status}'."
        )
        
    # Log human review action
    log = HumanApprovalLog(
        decision_id=decision.id,
        approver_id=payload.approver_id,
        action=payload.action,
        comments=payload.comments
    )
    db.add(log)
    
    # Update decision status
    decision.approval_status = payload.action
    db.commit()
    db.refresh(decision)
    
    logger.info(f"AUDIT | Underwriter review finalized | Decision ID: {decision_id} | Action: {decision.approval_status} | Event: bank.aarohan.credit.approved")
    return decision

@app.get("/credit/decisions/{customer_id}", response_model=List[AICreditDecisionResponse])
async def list_decisions(customer_id: int, db: Session = Depends(get_db)):
    return db.query(AICreditDecision).filter(AICreditDecision.customer_id == customer_id).all()

@app.get("/livez")
async def livez():
    return {"status": "UP"}
