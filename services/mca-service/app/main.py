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

from app.models import MCACompanyProfile, MCADirector, MCACharge, MCACompanyFiling, MCAFinancialStatement, MCAGovernanceAnalytics
from app.schemas import (
    MCACompanyProfileResponse, MCASyncRequest, MCADirectorResponse,
    MCAChargeResponse, MCACompanyFilingResponse, MCAFinancialStatementResponse,
    MCAGovernanceAnalyticsResponse, MCAOverrideRequest
)
from app.database import get_db, init_db
from app.providers import get_mca_adapter

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

# Corporate Analytics Engine
def process_corporate_governance_score(profile_id: int, db: Session):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.id == profile_id).first()
    if not profile:
        return
        
    directors = db.query(MCADirector).filter(MCADirector.company_id == profile_id).all()
    charges = db.query(MCACharge).filter(MCACharge.company_id == profile_id).all()
    filings = db.query(MCACompanyFiling).filter(MCACompanyFiling.company_id == profile_id).all()
    financials = db.query(MCAFinancialStatement).filter(MCAFinancialStatement.company_id == profile_id).order_by(MCAFinancialStatement.financial_year.asc()).all()
    
    # 1. Company Age
    age = (datetime.datetime.utcnow() - profile.incorporation_date).days / 365.25
    
    # 2. Director Stability
    stable_directors = "Stable"
    disqualified_count = sum(1 for d in directors if d.is_disqualified)
    if disqualified_count > 0:
        stable_directors = "Unstable (Disqualifications detected)"
        
    # 3. Capital Structure
    cap_struct = "Adequate"
    if profile.paid_up_capital > profile.authorized_capital:
        cap_struct = "Warning: Exceeds Authorized Cap"
        
    # 4. Financial trends
    net_worth_trend = "Stable"
    rev_trend = "Stable"
    prof_trend = "Stable"
    debt_trend = "Stable"
    
    if len(financials) >= 2:
        # Net worth
        if financials[-1].net_worth > financials[-2].net_worth:
            net_worth_trend = "Increasing"
        elif financials[-1].net_worth < financials[-2].net_worth:
            net_worth_trend = "Decreasing"
            
        # Revenue
        if financials[-1].revenue > financials[-2].revenue:
            rev_trend = "Increasing"
        elif financials[-1].revenue < financials[-2].revenue:
            rev_trend = "Decreasing"
            
        # Profit
        if financials[-1].profit_after_tax > financials[-2].profit_after_tax:
            prof_trend = "Increasing"
        elif financials[-1].profit_after_tax < financials[-2].profit_after_tax:
            prof_trend = "Decreasing"
            
        # Debt
        if financials[-1].debt > financials[-2].debt:
            debt_trend = "Increasing"
        elif financials[-1].debt < financials[-2].debt:
            debt_trend = "Decreasing"
            
    # Compliance calculations
    late_filings = sum(1 for f in filings if f.filing_delay_days > 0)
    missing_filings = 2 - len(filings) if len(filings) < 2 else 0 # Expected at least AOC-4 and MGT-7
    
    compliance_score = max(0.0, 100.0 - (late_filings * 10) - (missing_filings * 25))
    if profile.company_status != "ACTIVE":
        compliance_score = 0.0
        
    # Open charges sum
    total_charges = sum(c.charge_amount for c in charges if c.status == "OPEN")
    excessive_charges = total_charges > profile.authorized_capital
    
    governance_score = 100.0
    if disqualified_count > 0:
        governance_score -= 40
    if late_filings > 0:
        governance_score -= 10
    if excessive_charges:
        governance_score -= 15
    governance_score = max(0.0, governance_score)
    
    # Risks
    gov_risk = "Low"
    if disqualified_count > 0:
        gov_risk = "Critical"
    elif governance_score < 75:
        gov_risk = "High"
        
    reg_risk = "Low"
    if compliance_score < 50:
        reg_risk = "Critical"
    elif compliance_score < 80:
        reg_risk = "High"
        
    fin_risk = "Low"
    if debt_trend == "Increasing" and prof_trend == "Decreasing":
        fin_risk = "High"
        
    dir_risk = "Low"
    if disqualified_count > 0:
        dir_risk = "Critical"
        
    legal_risk = "Low"
    if excessive_charges:
        legal_risk = "Medium"
        
    overall_risk = "Low"
    if "Critical" in (gov_risk, reg_risk, dir_risk):
        overall_risk = "Critical"
    elif "High" in (gov_risk, reg_risk, fin_risk):
        overall_risk = "High"
    elif "Medium" in (gov_risk, reg_risk, legal_risk):
        overall_risk = "Medium"
        
    # AI insights
    insights = []
    if governance_score > 90 and disqualified_count == 0:
        insights.append("Strong governance practices.")
    if compliance_score >= 90:
        insights.append("Timely statutory filings.")
    if disqualified_count == 0:
        insights.append("Stable board of directors.")
    if debt_trend == "Increasing":
        insights.append("Increasing leverage detected.")
    if disqualified_count > 0 or compliance_score < 70:
        insights.append("Potential governance concerns.")
    if age > 5:
        insights.append("Excellent long-term corporate stability.")
        
    # Save Analytics
    analytics = db.query(MCAGovernanceAnalytics).filter(MCAGovernanceAnalytics.company_id == profile_id).first()
    if not analytics:
        analytics = MCAGovernanceAnalytics(company_id=profile_id)
        db.add(analytics)
        
    analytics.company_age = age
    analytics.filing_consistency = "Consistent" if late_filings == 0 else "Delayed"
    analytics.director_stability = stable_directors
    analytics.capital_structure = cap_struct
    analytics.net_worth_trend = net_worth_trend
    analytics.revenue_trend = rev_trend
    analytics.profit_trend = prof_trend
    analytics.debt_trend = debt_trend
    analytics.compliance_history = f"Late filings: {late_filings}, Missing filings: {missing_filings}"
    analytics.compliance_score = compliance_score
    analytics.governance_score = governance_score
    
    analytics.governance_risk = gov_risk
    analytics.regulatory_risk = reg_risk
    analytics.financial_reporting_risk = fin_risk
    analytics.director_risk = dir_risk
    analytics.legal_risk = legal_risk
    analytics.overall_risk_level = overall_risk
    analytics.ai_insights = " | ".join(insights)
    
    db.commit()
    
    # Publish events
    publish_workflow_event("Compliance Calculated", profile.customer_id, {"compliance_score": compliance_score})
    publish_workflow_event("Governance Analysis Completed", profile.customer_id, {
        "governance_score": governance_score, "company_age": age, "overall_risk": overall_risk
    })
    publish_workflow_event("Corporate Risk Updated", profile.customer_id, {
        "governance_risk": gov_risk, "regulatory_risk": reg_risk, "financial_reporting_risk": fin_risk
    })
    
    logger.info(f"AUDIT | MCA Corporate governance calculations complete for Customer: {profile.customer_id}")

# REST APIs

@app.post("/mca/sync/{customer_id}", response_model=MCACompanyProfileResponse, status_code=status.HTTP_200_OK)
async def sync_mca_data(customer_id: int, payload: MCASyncRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Synchronizing MCA registry details | CIN: {payload.cin} | Customer: {customer_id}")
    
    publish_workflow_event("MCA Verification Started", customer_id, {"cin": payload.cin})
    
    # Delete existing profiles for idempotency
    existing = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        
    adapter = get_mca_adapter()
    reg = adapter.fetch_company_profile(payload.cin)
    directors = adapter.fetch_directors(payload.cin)
    charges = adapter.fetch_charges(payload.cin)
    filings = adapter.fetch_filings(payload.cin)
    financials = adapter.fetch_financials(payload.cin)
    
    # Create profile
    profile = MCACompanyProfile(
        customer_id=customer_id,
        cin=reg["cin"],
        company_name=reg["company_name"],
        incorporation_date=reg["incorporation_date"],
        company_status=reg["company_status"],
        class_of_company=reg["class_of_company"],
        authorized_capital=reg["authorized_capital"],
        paid_up_capital=reg["paid_up_capital"],
        registered_office=reg.get("registered_office", "101, Textile Tower, Bandra East, Mumbai - 400051"),
        roc=reg.get("roc", "ROC Mumbai")
    )
    db.add(profile)
    db.flush() # Populate profile ID
    
    # Map Directors
    for d in directors:
        director = MCADirector(
            company_id=profile.id,
            din=d["din"],
            full_name=d["full_name"],
            appointment_date=d["appointment_date"],
            is_disqualified=d.get("is_disqualified", False)
        )
        db.add(director)
        
    # Map Charges
    for c in charges:
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
    for f in filings:
        filing = MCACompanyFiling(
            company_id=profile.id,
            form_name=f["form_name"],
            filing_date=f["filing_date"],
            status=f["status"],
            financial_year=f.get("financial_year", "2024-25"),
            filing_delay_days=f.get("filing_delay_days", 0)
        )
        db.add(filing)
        
    # Map Financials
    for fn in financials:
        financial_stmt = MCAFinancialStatement(
            company_id=profile.id,
            financial_year=fn["financial_year"],
            revenue=fn["revenue"],
            net_worth=fn["net_worth"],
            profit_after_tax=fn["profit_after_tax"],
            debt=fn["debt"]
        )
        db.add(financial_stmt)
        
    db.commit()
    
    publish_workflow_event("Company Profile Retrieved", customer_id, {"company_name": profile.company_name})
    
    # Process calculations
    process_corporate_governance_score(profile.id, db)
    
    db.commit()
    db.refresh(profile)
    
    publish_workflow_event("MCA Verification Completed", customer_id, {"cin": payload.cin})
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

@app.get("/mca/directors/{customer_id}", response_model=List[MCADirectorResponse])
async def get_directors(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="MCA Profile not found.")
    return db.query(MCADirector).filter(MCADirector.company_id == profile.id).all()

@app.get("/mca/charges/{customer_id}", response_model=List[MCAChargeResponse])
async def get_charges(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="MCA Profile not found.")
    return db.query(MCACharge).filter(MCACharge.company_id == profile.id).all()

@app.get("/mca/filings/{customer_id}", response_model=List[MCACompanyFilingResponse])
async def get_filings(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="MCA Profile not found.")
    return db.query(MCACompanyFiling).filter(MCACompanyFiling.company_id == profile.id).all()

@app.get("/mca/financials/{customer_id}", response_model=List[MCAFinancialStatementResponse])
async def get_financials(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="MCA Profile not found.")
    return db.query(MCAFinancialStatement).filter(MCAFinancialStatement.company_id == profile.id).all()

@app.get("/mca/analytics/{customer_id}", response_model=MCAGovernanceAnalyticsResponse)
async def get_governance_analytics(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="MCA Profile not found.")
    analytics = db.query(MCAGovernanceAnalytics).filter(MCAGovernanceAnalytics.company_id == profile.id).first()
    if not analytics:
        raise HTTPException(status_code=404, detail="Governance analytics not calculated.")
    return analytics

@app.post("/mca/analytics/{customer_id}/re-run", response_model=MCAGovernanceAnalyticsResponse)
async def rerun_mca_analysis(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="MCA Profile not found.")
        
    process_corporate_governance_score(profile.id, db)
    db.commit()
    return db.query(MCAGovernanceAnalytics).filter(MCAGovernanceAnalytics.company_id == profile.id).first()

@app.post("/mca/override/{customer_id}", response_model=MCAGovernanceAnalyticsResponse)
async def override_governance_classification(customer_id: int, payload: MCAOverrideRequest, db: Session = Depends(get_db)):
    profile = db.query(MCACompanyProfile).filter(MCACompanyProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="MCA Profile not found.")
        
    analytics = db.query(MCAGovernanceAnalytics).filter(MCAGovernanceAnalytics.company_id == profile.id).first()
    if not analytics:
        raise HTTPException(status_code=404, detail="Governance analytics not found.")
        
    logger.info(f"AUDIT | Governance score override applied by {payload.checked_by} | Score: {payload.governance_score}")
    
    analytics.governance_score = payload.governance_score
    override_notice = f"[OVERRIDE: Governance score manual set to {payload.governance_score} by {payload.checked_by}: {payload.comments}]"
    if analytics.ai_insights:
        analytics.ai_insights += " | " + override_notice
    else:
        analytics.ai_insights = override_notice
        
    db.commit()
    db.refresh(analytics)
    
    publish_workflow_event("Compliance Calculated", customer_id, {"override": True, "governance_score": payload.governance_score})
    return analytics

@app.post("/mca/reset")
async def reset_mca_dataset(db: Session = Depends(get_db)):
    logger.info("AUDIT | Resetting MCA Simulation Data")
    db.query(MCAFinancialStatement).delete()
    db.query(MCAGovernanceAnalytics).delete()
    db.query(MCADirector).delete()
    db.query(MCACharge).delete()
    db.query(MCACompanyFiling).delete()
    db.query(MCACompanyProfile).delete()
    db.commit()
    return {"message": "MCA Simulation dataset reset successfully."}

@app.get("/livez")
async def livez():
    return {"status": "UP"}
