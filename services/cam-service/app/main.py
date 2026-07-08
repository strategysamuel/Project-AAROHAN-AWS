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

from app.models import CAMRecord, CAMVersion, CAMApprovalLog
from app.schemas import CAMRecordResponse, CAMUpdateRequest, CAMApprovalRequest, CAMVersionResponse
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "cam-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("cam-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN AI Credit Appraisal Memorandum (CAM) Generator Service",
    description="Automated draft formatting, manual edits versioning tracking, and underwriting approvals",
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

# Gemini CAM Generation Template Helper
def compile_cam_template(customer_id: int) -> dict:
    exec_summary = (
        "Executive Summary Proposal:\n"
        "Underwriting request is for Aditya Garments Pvt Ltd. Customer is seeking ₹50 Lakhs "
        "working capital enhancement to expand textile trading inventory. Cash flow reports "
        "and GST returns substantiate steady credit eligibility metrics with minor risk variances."
    )
    bus_profile = (
        "Business Profile Overview:\n"
        "Constitution: Private Limited. Segment: Textiles and Garments Manufacturing. "
        "Incorporated in 2018. Operational facilities located in Coimbatore, Tamil Nadu. "
        "Active staff size: 28."
    )
    fin_analysis = (
        "Financial Analysis Spread:\n"
        "Average Monthly Turnover: ₹12.4 Lakhs (GSTN verified).\n"
        "Debt Service Ratio: 0.24. Average Bank balance: ₹3.8 Lakhs (consented AA statement)."
    )
    swot = (
        "SWOT Assessment:\n"
        "Strengths: Consistent GSTR compliance history.\n"
        "Weaknesses: High dependence on Q3 textile seasonal cycles.\n"
        "Opportunities: Export channel integrations.\n"
        "Threats: Inflation in raw yarn prices."
    )
    risk_ass = (
        "Risk Assessment Indicators:\n"
        "1. Liquidity variance: Minor current account cash outflows during Q1.\n"
        "2. Compliance delays: Historic 5 days filing lag in GST returns. Level: Low Risk."
    )
    ai_reco = (
        "AI Recommendation:\n"
        "Limit Recommended: ₹50,000,000. Interest Rate: 9.8% p.a. Margin: 15%."
    )
    
    return {
        "executive_summary": exec_summary,
        "business_profile": bus_profile,
        "financial_analysis": fin_analysis,
        "swot_analysis": swot,
        "risk_assessment": risk_ass,
        "ai_recommendation": ai_reco
    }

# REST APIs

@app.post("/cam/generate/{customer_id}", response_model=CAMRecordResponse, status_code=status.HTTP_201_CREATED)
async def generate_cam_draft(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Dispatching CAM draft generation via Gemini Templates for Customer: {customer_id}")
    
    # Idempotency check: Delete existing draft
    existing = db.query(CAMRecord).filter(CAMRecord.customer_id == customer_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        
    template = compile_cam_template(customer_id)
    
    cam = CAMRecord(
        customer_id=customer_id,
        executive_summary=template["executive_summary"],
        business_profile=template["business_profile"],
        financial_analysis=template["financial_analysis"],
        swot_analysis=template["swot_analysis"],
        risk_assessment=template["risk_assessment"],
        collateral_assessment="N/A - Primary business assets charge hypothecation",
        ai_recommendation=template["ai_recommendation"],
        status="DRAFT",
        current_version=1
    )
    db.add(cam)
    db.flush() # Populate CAM ID
    
    # Save Initial Version Snapshot
    version = CAMVersion(
        cam_id=cam.id,
        version_num=1,
        edited_by="GEMINI-AI-TEMPLATE-ENGINE",
        change_summary="Initial auto-draft compiled",
        executive_summary=cam.executive_summary,
        business_profile=cam.business_profile,
        financial_analysis=cam.financial_analysis,
        swot_analysis=cam.swot_analysis,
        risk_assessment=cam.risk_assessment
    )
    db.add(version)
    db.commit()
    
    db.refresh(cam)
    logger.info(f"AUDIT | CAM draft generation complete | ID: {cam.id} | Event: bank.aarohan.cam.drafted")
    return cam

@app.put("/cam/{id}", response_model=CAMRecordResponse)
async def edit_cam_sections(id: int, payload: CAMUpdateRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Modifying CAM ID: {id} | Editor: {payload.edited_by}")
    
    cam = db.query(CAMRecord).filter(CAMRecord.id == id).first()
    if not cam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CAM record not found."
        )
        
    # Increment version
    new_version_num = cam.current_version + 1
    
    # Save old values to Version History Snapshot
    version = CAMVersion(
        cam_id=cam.id,
        version_num=new_version_num,
        edited_by=payload.edited_by,
        change_summary=payload.change_summary,
        executive_summary=payload.executive_summary,
        business_profile=payload.business_profile,
        financial_analysis=payload.financial_analysis,
        swot_analysis=payload.swot_analysis,
        risk_assessment=payload.risk_assessment
    )
    db.add(version)
    
    # Update current fields
    cam.executive_summary = payload.executive_summary
    cam.business_profile = payload.business_profile
    cam.financial_analysis = payload.financial_analysis
    cam.swot_analysis = payload.swot_analysis
    cam.risk_assessment = payload.risk_assessment
    if payload.collateral_assessment is not None:
        cam.collateral_assessment = payload.collateral_assessment
        
    cam.current_version = new_version_num
    db.commit()
    db.refresh(cam)
    
    logger.info(f"AUDIT | CAM ID: {id} versioned up to: {cam.current_version}")
    return cam

@app.get("/cam/{customer_id}", response_model=CAMRecordResponse)
async def get_cam(customer_id: int, db: Session = Depends(get_db)):
    cam = db.query(CAMRecord).filter(CAMRecord.customer_id == customer_id).first()
    if not cam:
        # Auto-create if not generated
        return await generate_cam_draft(customer_id, db)
    return cam

@app.post("/cam/{id}/approve", response_model=CAMRecordResponse)
async def approve_cam(id: int, payload: CAMApprovalRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Submitting CAM approval sign-off | ID: {id} | Approver: {payload.approver_id}")
    
    cam = db.query(CAMRecord).filter(CAMRecord.id == id).first()
    if not cam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CAM record not found."
        )
        
    # Log approval action
    log = CAMApprovalLog(
        cam_id=cam.id,
        approver_id=payload.approver_id,
        action=payload.action,
        comments=payload.comments
    )
    db.add(log)
    
    cam.status = payload.action
    db.commit()
    db.refresh(cam)
    
    logger.info(f"AUDIT | CAM sign-off complete | ID: {id} | Status: {cam.status} | Event: bank.aarohan.cam.completed")
    return cam

@app.get("/cam/{id}/export")
async def export_cam_pdf(id: int, db: Session = Depends(get_db)):
    cam = db.query(CAMRecord).filter(CAMRecord.id == id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="CAM record not found.")
    
    # Return mock GCS PDF download path URL
    download_url = f"https://storage.googleapis.com/aarohan-cam-reports/CAM_{cam.customer_id}_V{cam.current_version}.pdf"
    return {"download_url": download_url, "file_name": f"CAM_{cam.customer_id}_V{cam.current_version}.pdf"}

@app.get("/livez")
async def livez():
    return {"status": "UP"}
