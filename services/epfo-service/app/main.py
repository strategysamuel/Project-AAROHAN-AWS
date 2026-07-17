import logging
import sys
import time
import uuid
import datetime
import statistics
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import EPFOEstablishmentProfile, EPFOContribution, EPFOEmployee, EPFOAnalytics
from app.schemas import (
    EPFOProfileResponse, EPFOSyncRequest, EPFOEmployeeResponse,
    EPFOContributionResponse, EPFOAnalyticsResponse, EPFOOverrideRequest
)
from app.database import get_db, init_db
from app.providers import get_epfo_adapter

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
    title="AAROHAN EPFO & Workforce Stability Gateway Service",
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

# Audit log helper
def publish_workflow_event(event_type: str, customer_id: int, payload: dict):
    logger.info(f"AUDIT | EVENT_BUS | Published: {event_type} | Customer: {customer_id} | Payload: {payload}")
    try:
        from event_engine import BusinessEventEngine
        engine = BusinessEventEngine()
        engine.dispatch(event_type, f"cust_{customer_id}", payload)
    except Exception as e:
        logger.warning(f"ESE core event engine dispatch skipped: {e}")

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

# Workforce Analytics Engine
def process_workforce_stability(profile_id: int, db: Session):
    profile = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.id == profile_id).first()
    if not profile:
        return
        
    employees = db.query(EPFOEmployee).filter(EPFOEmployee.profile_id == profile_id).all()
    contributions = db.query(EPFOContribution).filter(EPFOContribution.profile_id == profile_id).all()
    
    if not employees:
        return
        
    total_emp = len(employees)
    active_emp = sum(1 for e in employees if e.is_active)
    inactive_emp = total_emp - active_emp
    
    # 1. Attrition Rate
    attrition_rate = (inactive_emp / total_emp) * 100 if total_emp > 0 else 0.0
    
    # 2. Tenure (in months)
    tenures = []
    now = datetime.datetime.utcnow()
    for e in employees:
        end = e.exit_date if e.exit_date else now
        tenures.append((end - e.joining_date).days / 30.0)
    avg_tenure = sum(tenures) / len(tenures) if tenures else 0.0
    
    # 3. Monthly Payroll
    monthly_payroll = sum(e.salary for e in employees if e.is_active)
    
    # 4. Payroll growth & workforce growth
    con_amounts = [c.amount_paid for c in contributions]
    stability_index = 100.0
    if len(con_amounts) > 1:
        avg_con = sum(con_amounts) / len(con_amounts)
        std_con = statistics.stdev(con_amounts)
        cv = std_con / avg_con if avg_con > 0 else 0.0
        stability_index = max(0.0, 100.0 * (1.0 - cv))
        
    payroll_growth = 0.0
    if len(con_amounts) >= 2:
        payroll_growth = ((con_amounts[-1] - con_amounts[0]) / con_amounts[0]) * 100
        
    hiring_trend = "Stable"
    if payroll_growth > 5.0:
        hiring_trend = "Expansion"
    elif payroll_growth < -5.0:
        hiring_trend = "Decline"
        
    # Compliance Engine
    late_filings = sum(1 for c in contributions if c.status == "LATE")
    missing_contributions = sum(1 for c in contributions if c.status == "MISSING")
    
    # Contribution mismatch check
    mismatch_detected = False
    for c in contributions:
        expected_amount = c.employees_count * 1800.0 # EPFO approx wage cap share
        if abs(c.amount_paid - expected_amount) > expected_amount * 0.40:
            mismatch_detected = True
            
    # Calculate score out of 100
    compliance_score = max(0.0, 100.0 - (late_filings * 10) - (missing_contributions * 20))
    
    # Risk Indicators
    # 1. Attrition Risk
    if attrition_rate > 25.0:
        attr_risk = "Critical"
    elif attrition_rate > 15.0:
        attr_risk = "High"
    elif attrition_rate > 8.0:
        attr_risk = "Medium"
    else:
        attr_risk = "Low"
        
    # 2. Compliance Risk
    if compliance_score < 70.0:
        comp_risk = "Critical"
    elif compliance_score < 85.0:
        comp_risk = "High"
    elif compliance_score < 95.0:
        comp_risk = "Medium"
    else:
        comp_risk = "Low"
        
    # 3. Payroll Risk
    if payroll_growth < -15.0:
        pay_risk = "Critical"
    elif payroll_growth < -5.0:
        pay_risk = "High"
    else:
        pay_risk = "Low"
        
    # AI insights narrative
    insights = []
    if stability_index > 90 and attrition_rate < 10:
        insights.append("Stable workforce with consistent payroll.")
    if attrition_rate > 20:
        insights.append("High employee attrition detected.")
    if payroll_growth > 10.0:
        insights.append("Rapid hiring indicates business expansion.")
    if payroll_growth < -5.0:
        insights.append("Payroll declining over recent months.")
    if compliance_score >= 95.0:
        insights.append("EPFO compliance is excellent.")
    if attrition_rate > 15.0 or payroll_growth < -10.0:
        insights.append("Potential operational stress due to workforce reduction.")
        
    # Save Analytics
    analytics = db.query(EPFOAnalytics).filter(EPFOAnalytics.profile_id == profile_id).first()
    if not analytics:
        analytics = EPFOAnalytics(profile_id=profile_id)
        db.add(analytics)
        
    analytics.active_employees = active_emp
    analytics.attrition_rate = attrition_rate
    analytics.avg_employee_tenure = avg_tenure
    analytics.monthly_payroll = monthly_payroll
    analytics.payroll_growth = payroll_growth
    analytics.hiring_trend = hiring_trend
    analytics.workforce_growth = payroll_growth # Proportional
    analytics.payroll_stability_index = stability_index
    analytics.compliance_score = compliance_score
    
    analytics.payroll_risk = pay_risk
    analytics.compliance_risk = comp_risk
    analytics.attrition_risk = attr_risk
    analytics.workforce_stability_risk = attr_risk
    analytics.business_continuity_risk = attr_risk
    analytics.ai_insights = " | ".join(insights)
    
    db.commit()
    
    # Event publications
    publish_workflow_event("Compliance Calculated", profile.customer_id, {"compliance_score": compliance_score})
    publish_workflow_event("Workforce Analytics Completed", profile.customer_id, {
        "active_employees": active_emp, "attrition_rate": attrition_rate, "payroll_stability_index": stability_index
    })
    publish_workflow_event("Workforce Risk Updated", profile.customer_id, {
        "payroll_risk": pay_risk, "compliance_risk": comp_risk, "attrition_risk": attr_risk
    })
    
    logger.info(f"AUDIT | EPFO workforce stability processed successfully for Customer: {profile.customer_id}")

# REST APIs

@app.post("/epfo/sync/{customer_id}", response_model=EPFOProfileResponse, status_code=status.HTTP_200_OK)
async def sync_epfo_data(customer_id: int, payload: EPFOSyncRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Synchronizing EPFO registry details | Est ID: {payload.establishment_id} | Customer: {customer_id}")
    
    publish_workflow_event("EPFO Verification Started", customer_id, {"establishment_id": payload.establishment_id})
    
    # Delete existing profiles for idempotency
    existing = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.customer_id == customer_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        
    adapter = get_epfo_adapter()
    reg = adapter.fetch_establishment_profile(payload.establishment_id)
    employees = adapter.fetch_employee_summary(payload.establishment_id)
    contributions = adapter.fetch_monthly_contributions(payload.establishment_id)
    
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
    db.flush() # Populate ID
    
    # Map Employees
    for emp in employees:
        e_record = EPFOEmployee(
            profile_id=profile.id,
            uan=emp["uan"],
            name=emp["name"],
            joining_date=emp["joining_date"],
            exit_date=emp["exit_date"],
            salary=emp["salary"],
            designation=emp.get("designation", "Operator"),
            is_active=emp["is_active"]
        )
        db.add(e_record)
        
    # Map Contributions
    for c in contributions:
        contrib = EPFOContribution(
            profile_id=profile.id,
            wage_month=c["wage_month"],
            amount_paid=c["amount_paid"],
            employer_share=c.get("employer_share", c["amount_paid"] * 0.45),
            employees_count=c["employees_count"],
            payment_date=c["payment_date"],
            status=c["status"]
        )
        db.add(contrib)
        
    db.commit()
    
    publish_workflow_event("Payroll Imported", customer_id, {"count": len(employees)})
    
    # Process calculations
    process_workforce_stability(profile.id, db)
    
    db.commit()
    db.refresh(profile)
    
    publish_workflow_event("EPFO Verification Completed", customer_id, {"establishment_id": payload.establishment_id})
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

@app.get("/epfo/employees/{customer_id}", response_model=List[EPFOEmployeeResponse])
async def get_employee_summary(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="EPFO profile not found.")
    return db.query(EPFOEmployee).filter(EPFOEmployee.profile_id == profile.id).all()

@app.get("/epfo/contributions/{customer_id}", response_model=List[EPFOContributionResponse])
async def get_monthly_contributions(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="EPFO profile not found.")
    return db.query(EPFOContribution).filter(EPFOContribution.profile_id == profile.id).all()

@app.get("/epfo/analytics/{customer_id}", response_model=EPFOAnalyticsResponse)
async def get_epfo_analytics(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="EPFO profile not found.")
    
    analytics = db.query(EPFOAnalytics).filter(EPFOAnalytics.profile_id == profile.id).first()
    if not analytics:
        raise HTTPException(status_code=404, detail="EPFO Analytics not computed yet.")
    return analytics

@app.post("/epfo/analytics/{customer_id}/re-run", response_model=EPFOAnalyticsResponse)
async def rerun_epfo_analysis(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="EPFO profile not found.")
        
    process_workforce_stability(profile.id, db)
    db.commit()
    
    return db.query(EPFOAnalytics).filter(EPFOAnalytics.profile_id == profile.id).first()

@app.post("/epfo/override/{customer_id}", response_model=EPFOAnalyticsResponse)
async def override_compliance_classification(customer_id: int, payload: EPFOOverrideRequest, db: Session = Depends(get_db)):
    profile = db.query(EPFOEstablishmentProfile).filter(EPFOEstablishmentProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="EPFO profile not found.")
        
    analytics = db.query(EPFOAnalytics).filter(EPFOAnalytics.profile_id == profile.id).first()
    if not analytics:
        raise HTTPException(status_code=404, detail="EPFO Analytics details not found.")
        
    logger.info(f"AUDIT | Compliance score override requested by {payload.checked_by} | Comment: {payload.comments}")
    
    analytics.compliance_score = payload.compliance_score
    override_notice = f"[OVERRIDE: Compliance score manual set to {payload.compliance_score} by {payload.checked_by}: {payload.comments}]"
    if analytics.ai_insights:
        analytics.ai_insights += " | " + override_notice
    else:
        analytics.ai_insights = override_notice
        
    db.commit()
    db.refresh(analytics)
    
    publish_workflow_event("Compliance Calculated", customer_id, {"override": True, "compliance_score": payload.compliance_score})
    return analytics

@app.post("/epfo/reset")
async def reset_epfo_dataset(db: Session = Depends(get_db)):
    logger.info("AUDIT | Resetting EPFO Simulation Data")
    db.query(EPFOEmployee).delete()
    db.query(EPFOContribution).delete()
    db.query(EPFOAnalytics).delete()
    db.query(EPFOEstablishmentProfile).delete()
    db.commit()
    return {"message": "EPFO Simulation dataset reset successfully."}

@app.get("/livez")
async def livez():
    return {"status": "UP"}
