import logging
import sys
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import RMLead, RMTask, RMAlert, RMInteraction
from app.schemas import RMLeadResponse, RMTaskResponse, RMAlertResponse, RMInteractionResponse, AssistantChatRequest, NextBestActionResponse, RMTaskCreate, RMLeadCreate
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "rm-workspace-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("rm-workspace-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN RM Workspace Service",
    description="Relationship manager workspace, pipeline trackers, and Gemini bank assistant gateway",
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

@app.get("/rm/tasks", response_model=List[RMTaskResponse])
async def list_tasks(db: Session = Depends(get_db)):
    return db.query(RMTask).all()

@app.post("/rm/tasks", response_model=RMTaskResponse)
async def create_task(payload: RMTaskCreate, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Registering RM Task: {payload.title}")
    task = RMTask(
        customer_id=payload.customer_id,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        priority=payload.priority,
        status="PENDING"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/rm/leads", response_model=List[RMLeadResponse])
async def list_leads(db: Session = Depends(get_db)):
    return db.query(RMLead).all()

@app.post("/rm/leads", response_model=RMLeadResponse)
async def create_lead(payload: RMLeadCreate, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Creating lead company: {payload.company_name}")
    lead = RMLead(
        company_name=payload.company_name,
        contact_person=payload.contact_person,
        mobile=payload.mobile,
        pipeline_stage=payload.pipeline_stage,
        estimated_loan_amt=payload.estimated_loan_amt
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@app.get("/rm/alerts", response_model=List[RMAlertResponse])
async def list_alerts(db: Session = Depends(get_db)):
    return db.query(RMAlert).all()

@app.get("/rm/actions/{customer_id}", response_model=List[NextBestActionResponse])
async def next_best_actions(customer_id: int, db: Session = Depends(get_db)):
    """Next Best Action Engine analyzing active warnings and expiry triggers"""
    logger.info(f"AUDIT | Analyzing next best actions for Customer: {customer_id}")
    actions = []
    
    alerts = db.query(RMAlert).filter(RMAlert.customer_id == customer_id, RMAlert.is_read == False).all()
    for a in alerts:
        if a.alert_type == "CONSENT_EXPIRY":
            actions.append(NextBestActionResponse(
                action_code="TRIGGER_CONSENT_RENEWAL",
                title="Trigger Consent Renewal Link",
                description="Send SMS consent renewal invite to registered director mobile to keep AA flows active.",
                priority="HIGH"
            ))
        elif a.alert_type == "LIQUIDITY_DROP":
            actions.append(NextBestActionResponse(
                action_code="SCHEDULE_CREDIT_CALL",
                title="Schedule Liquidity Review Call",
                description="Arrange brief review call with client regarding current account cash flow declines.",
                priority="MEDIUM"
            ))
            
    # Default fallbacks
    if not actions:
        actions.append(NextBestActionResponse(
            action_code="GST_HEALTH_CHECK",
            title="GST Compliance Health check",
            description="Assess latest monthly filing timeline logs to update ratings.",
            priority="LOW"
        ))
        
    return actions

@app.post("/rm/assistant/chat")
async def assistant_chat(payload: AssistantChatRequest):
    """Gemini Assistant Mock answers"""
    prompt = payload.prompt.upper()
    logger.info(f"AUDIT | RM Chat assistant processing prompt: {payload.prompt}")
    
    if "MEETING" in prompt or "PREP" in prompt:
        response = (
            "Gemini meeting prep brief:\n"
            "Client: Aditya Garments Pvt Ltd. Underwriting limit of ₹50 Lakhs is pending review.\n"
            "Key discussion points:\n"
            "1. Verify recent Q3 textile seasonal turnover spikes (₹19.5 L).\n"
            "2. Confirm machine hypothecation collateral valuation.\n"
            "3. Request updates regarding the 5 days filing lag warning."
        )
    elif "RISK" in prompt or "ALERTS" in prompt:
        response = (
            "Gemini Risk analysis summary:\n"
            "1. Liquidity warning: Average balance down 15% MoM.\n"
            "2. Consent alert: AA consent expires in 5 days. Action: Send renewal sms."
        )
    else:
        response = (
            "Gemini Agent Help Desk:\n"
            "I can assist with meeting preparation sheets, customer 360 summaries, and credit policy updates. "
            "How can I help you support MSME appraising pipelines today?"
        )
        
    return {"response": response}

@app.get("/livez")
async def livez():
    return {"status": "UP"}
