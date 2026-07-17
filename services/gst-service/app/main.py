import logging
import sys
import time
import uuid
import datetime
import math
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import GSTProfile, GSTReturn, GSTAnalytics
from app.schemas import (
    GSTProfileResponse, GSTAnalyticsResponse, GSTReturnResponse,
    GSTSyncRequest, GSTOverrideRequest
)
from app.database import get_db, init_db
from app.providers import get_gst_adapter

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
    title="AAROHAN GSTN Simulation & Business Financial Analysis Service",
    description="India's GSTN simulation API integration, corporate tax returns analysis, and lending risk profiling",
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

# Financial Analytics Engine
def run_financial_analytics(profile_id: int, db: Session):
    profile = db.query(GSTProfile).filter(GSTProfile.id == profile_id).first()
    if not profile:
        return
        
    g1_returns = db.query(GSTReturn).filter(
        GSTReturn.profile_id == profile_id,
        GSTReturn.return_type == "GSTR1"
    ).order_by(GSTReturn.tax_period.asc()).all()
    
    g3b_returns = db.query(GSTReturn).filter(
        GSTReturn.profile_id == profile_id,
        GSTReturn.return_type == "GSTR3B"
    ).order_by(GSTReturn.tax_period.asc()).all()
    
    if not g1_returns:
        publish_workflow_event("GST Analysis Failed", profile.customer_id, {"reason": "No returns history found."})
        return
        
    turnovers = [r.gross_turnover for r in g1_returns]
    purchases = [r.purchases for r in g1_returns]
    itc_list = [r.input_tax_credit for r in g1_returns]
    delay_days = [r.filing_delay_days for r in g1_returns]
    
    # 1. Average Monthly Turnover & Purchases
    avg_turnover = sum(turnovers) / len(turnovers) if turnovers else 0.0
    avg_purchases = sum(purchases) / len(purchases) if purchases else 0.0
    
    # 2. Peak Turnover Month
    max_idx = turnovers.index(max(turnovers)) if turnovers else 0
    peak_month = g1_returns[max_idx].tax_period if g1_returns else None
    
    # 3. Revenue Growth Rate (MoM Average)
    mom_rates = []
    for idx in range(1, len(turnovers)):
        prev = turnovers[idx-1]
        if prev > 0:
            mom_rates.append(((turnovers[idx] - prev) / prev) * 100)
    avg_growth = sum(mom_rates) / len(mom_rates) if mom_rates else 0.0
    
    # 4. Volatility & Stability Score
    volatility = 0.0
    stability = 100.0
    if avg_turnover > 0:
        variance = sum((x - avg_turnover) ** 2 for x in turnovers) / len(turnovers)
        std_dev = math.sqrt(variance)
        volatility = std_dev / avg_turnover
        stability = max(0.0, 100.0 * (1.0 - volatility))
        
    # 5. Seasonality Index
    min_val = min(turnovers)
    seasonality = max(turnovers) / min_val if min_val > 0 else 1.0
    
    # 6. Working Capital Estimate (approx 3 months operating margin or 25% of turnover)
    working_capital = max(0.0, (avg_turnover - avg_purchases) * 3)
    if working_capital == 0.0:
        working_capital = avg_turnover * 0.25
        
    # 7. Compliance Engine & Risk Flags
    risks = []
    
    # Check Cancelled/Suspended
    if profile.status == "CANCELLED":
        risks.append("Cancelled Registration")
    elif profile.status in ("SUSPENDED", "INACTIVE"):
        risks.append("Inactive GST")
        
    # Nil Returns
    nil_count = sum(1 for x in turnovers if x == 0)
    if nil_count > 0:
        risks.append("Nil Returns")
        
    # Late Filings
    late_count = sum(1 for d in delay_days if d > 0)
    if late_count > 0:
        risks.append("Late Filings")
        
    # Non Filers
    unfiled_count = sum(1 for r in g1_returns if r.status != "FILED")
    if unfiled_count > 0:
        risks.append("Non-Filers")
        
    # Return Mismatches (Compare GSTR-1 and GSTR-3B turnovers)
    mismatch_detected = False
    for r1 in g1_returns:
        matching_3b = next((r3 for r3 in g3b_returns if r3.tax_period == r1.tax_period), None)
        if matching_3b and abs(r1.gross_turnover - matching_3b.gross_turnover) > (r1.gross_turnover * 0.05):
            mismatch_detected = True
            break
    if mismatch_detected:
        risks.append("Return Mismatches")
        
    # Abnormal Sales
    if volatility > 0.6:
        risks.append("Abnormal Sales")
        
    # Sudden Revenue Drop (compare last 3 months vs previous 3 months)
    sudden_drop = False
    if len(turnovers) >= 6:
        last_3_avg = sum(turnovers[-3:]) / 3
        prev_3_avg = sum(turnovers[-6:-3]) / 3
        if prev_3_avg > 0 and (prev_3_avg - last_3_avg) / prev_3_avg > 0.50:
            sudden_drop = True
            risks.append("Sudden Revenue Drop")
            
    # Suspicious Filing Behaviour
    if late_count > 3 or (nil_count >= 2 and consecutive_nil_runs(turnovers)):
        risks.append("Suspicious Filing Behaviour")
        
    # Compliance Score calculation
    filed_on_time = sum(1 for r in g1_returns if r.status == "FILED" and r.filing_delay_days == 0)
    compliance_score = (filed_on_time / len(g1_returns)) * 100 if g1_returns else 100.0
    
    # Filing delay penalty score
    total_delays = sum(delay_days)
    delay_score = max(0.0, 100.0 - (total_delays * 3))
    
    # Risk Level mapping
    if "Cancelled Registration" in risks or "Inactive GST" in risks or compliance_score < 50:
        risk_lvl = "Critical"
    elif "Sudden Revenue Drop" in risks or "Non-Filers" in risks or compliance_score < 75:
        risk_lvl = "High"
    elif "Late Filings" in risks or "Return Mismatches" in risks or volatility > 0.4:
        risk_lvl = "Medium"
    else:
        risk_lvl = "Low"
        
    # AI Narrative Insights
    insights = []
    if avg_growth > 2.0:
        insights.append("Business is growing steadily.")
    if sudden_drop:
        insights.append("Revenue has declined over the last three months.")
    if compliance_score >= 95.0:
        insights.append("Excellent GST compliance.")
    if seasonality > 1.4:
        insights.append("Seasonal revenue fluctuations detected.")
    if working_capital > 500000:
        insights.append("High working capital requirement.")
    if avg_growth < -2.0 or volatility > 0.5:
        insights.append("Potential cash-flow stress.")
        
    # Persistence
    analytics = db.query(GSTAnalytics).filter(GSTAnalytics.profile_id == profile_id).first()
    if not analytics:
        analytics = GSTAnalytics(profile_id=profile_id)
        db.add(analytics)
        
    analytics.avg_monthly_turnover = avg_turnover
    analytics.peak_turnover_month = peak_month
    analytics.revenue_growth_rate = avg_growth
    analytics.revenue_stability = stability
    analytics.compliance_score = compliance_score
    analytics.filing_delay_score = delay_score
    analytics.seasonality_index = seasonality
    analytics.working_capital_estimate = working_capital
    analytics.revenue_volatility = volatility
    analytics.business_stability_score = stability
    analytics.risk_indicators = ",".join(risks)
    analytics.risk_level = risk_lvl
    analytics.ai_insights = " | ".join(insights)
    
    db.commit()
    
    # Event publications
    publish_workflow_event("Compliance Calculated", profile.customer_id, {"compliance_score": compliance_score, "delay_score": delay_score})
    publish_workflow_event("Financial Analysis Completed", profile.customer_id, {
        "average_monthly_turnover": avg_turnover, "stability_score": stability, "working_capital_estimate": working_capital
    })
    if risk_lvl in ("High", "Critical"):
        publish_workflow_event("High Risk Identified", profile.customer_id, {"risk_level": risk_lvl, "indicators": risks})
        
    logger.info(f"AUDIT | GST Financial analytics processed successfully for customer: {profile.customer_id}")

def consecutive_nil_runs(turnovers: List[float]) -> bool:
    for i in range(1, len(turnovers)):
        if turnovers[i] == 0.0 and turnovers[i-1] == 0.0:
            return True
    return False

# REST APIs

@app.post("/gst/sync/{customer_id}", response_model=GSTProfileResponse, status_code=status.HTTP_200_OK)
async def sync_gst_data(customer_id: int, payload: GSTSyncRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Synchronizing GST data for Customer ID: {customer_id} | GSTIN: {payload.gstin}")
    
    publish_workflow_event("GST Verification Started", customer_id, {"gstin": payload.gstin})
    
    # Delete existing profiles for idempotency
    existing = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if existing:
        db.delete(existing)
        db.commit()
        
    # Call Active Adapter Factory
    adapter = get_gst_adapter()
    profile_data = adapter.fetch_gst_profile(payload.gstin)
    return_history = adapter.fetch_return_filing_history(payload.gstin)
    
    # Write to database
    profile = GSTProfile(
        customer_id=customer_id,
        gstin=profile_data["gstin"],
        legal_name=profile_data["legal_name"],
        trade_name=profile_data["trade_name"],
        registration_date=profile_data["registration_date"],
        status=profile_data["status"],
        business_constitution=profile_data.get("business_constitution", "Private Limited"),
        filing_frequency=profile_data.get("filing_frequency", "MONTHLY")
    )
    db.add(profile)
    db.flush() # Populate ID
    
    for r in return_history:
        ret = GSTReturn(
            profile_id=profile.id,
            return_type=r["return_type"],
            financial_year=r["financial_year"],
            tax_period=r["tax_period"],
            filing_date=r["filing_date"],
            status=r["status"],
            gross_turnover=r["gross_turnover"],
            purchases=r.get("purchases", r["gross_turnover"] * 0.7),
            tax_paid=r["tax_paid"],
            input_tax_credit=r.get("input_tax_credit", r["tax_paid"] * 0.8),
            filing_delay_days=r["filing_delay_days"]
        )
        db.add(ret)
        
    db.commit()
    
    # Process compliance scoring and financial health spreading analytics
    run_financial_analytics(profile.id, db)
    
    db.commit()
    db.refresh(profile)
    
    publish_workflow_event("GST Verification Completed", customer_id, {"gstin": payload.gstin, "status": profile.status})
    
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

@app.get("/gst/returns/{customer_id}", response_model=List[GSTReturnResponse])
async def get_return_history(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="GST Profile not found.")
    return db.query(GSTReturn).filter(GSTReturn.profile_id == profile.id).all()

@app.get("/gst/returns/{customer_id}/gstr1", response_model=List[GSTReturnResponse])
async def get_gstr1_returns(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="GST Profile not found.")
    return db.query(GSTReturn).filter(GSTReturn.profile_id == profile.id, GSTReturn.return_type == "GSTR1").all()

@app.get("/gst/returns/{customer_id}/gstr3b", response_model=List[GSTReturnResponse])
async def get_gstr3b_returns(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="GST Profile not found.")
    return db.query(GSTReturn).filter(GSTReturn.profile_id == profile.id, GSTReturn.return_type == "GSTR3B").all()

@app.get("/gst/returns/{customer_id}/annual", response_model=dict)
async def get_annual_summary(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="GST Profile not found.")
    
    g1_returns = db.query(GSTReturn).filter(GSTReturn.profile_id == profile.id, GSTReturn.return_type == "GSTR1").all()
    total_sales = sum(r.gross_turnover for r in g1_returns)
    total_tax = sum(r.tax_paid for r in g1_returns)
    total_purchases = sum(r.purchases for r in g1_returns)
    total_itc = sum(r.input_tax_credit for r in g1_returns)
    
    return {
        "financial_year": "2025-26",
        "total_gross_sales": total_sales,
        "total_tax_paid": total_tax,
        "total_purchases": total_purchases,
        "total_input_tax_credit": total_itc,
        "net_tax_liability": max(0.0, total_tax - total_itc)
    }

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

@app.post("/gst/analytics/{customer_id}/re-run", response_model=GSTAnalyticsResponse)
async def rerun_financial_analysis(customer_id: int, db: Session = Depends(get_db)):
    profile = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="GST Profile not found.")
        
    run_financial_analytics(profile.id, db)
    db.commit()
    
    return db.query(GSTAnalytics).filter(GSTAnalytics.profile_id == profile.id).first()

@app.post("/gst/override/{customer_id}", response_model=GSTAnalyticsResponse)
async def override_risk_level(customer_id: int, payload: GSTOverrideRequest, db: Session = Depends(get_db)):
    profile = db.query(GSTProfile).filter(GSTProfile.customer_id == customer_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="GST Profile not found.")
        
    analytics = db.query(GSTAnalytics).filter(GSTAnalytics.profile_id == profile.id).first()
    if not analytics:
        raise HTTPException(status_code=404, detail="GST Analytics not found.")
        
    logger.info(f"AUDIT | Risk override applied for customer: {customer_id} | Risk Level: {payload.risk_level} by {payload.checked_by}")
    
    analytics.risk_level = payload.risk_level
    # Append override notice to AI insights
    override_notice = f"[OVERRIDE: Set to {payload.risk_level} by {payload.checked_by} on {datetime.date.today().isoformat()}: {payload.comments}]"
    if analytics.ai_insights:
        analytics.ai_insights += " | " + override_notice
    else:
        analytics.ai_insights = override_notice
        
    db.commit()
    db.refresh(analytics)
    
    publish_workflow_event("Compliance Calculated", customer_id, {"override": True, "risk_level": payload.risk_level})
    
    return analytics

@app.post("/gst/reset")
async def reset_simulation_data(db: Session = Depends(get_db)):
    logger.info("AUDIT | Resetting GST Simulation Data")
    db.query(GSTReturn).delete()
    db.query(GSTAnalytics).delete()
    db.query(GSTProfile).delete()
    db.commit()
    return {"message": "GST Simulation dataset reset successfully."}

@app.get("/livez")
async def livez():
    return {"status": "UP"}
