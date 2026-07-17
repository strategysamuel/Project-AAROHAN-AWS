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

from app.models import LinkedAccount, AATransaction, AAAnalytics, AAConsent
from app.schemas import (
    LinkedAccountResponse, AAAnalyticsResponse, AATransactionResponse,
    AAConsentResponse, AAConsentCreateRequest, ConsentStatusUpdateRequest,
    DiscoveryRequest, LinkAccountRequest, SyncRequest
)
from app.database import get_db, init_db
from app.providers import get_aa_adapter

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "aa-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("aa-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN Account Aggregator & Cash Flow Intelligence Service",
    description="consented financial data retrieval, transactional normalization, cash flow evaluation, and behavioral risk scoring",
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

# Categorization and Normalization Engine
def normalize_and_categorize(narration: str) -> tuple[str, bool]:
    narr = narration.upper()
    category = "OTHERS"
    is_recurring = False
    
    if "CLIENT SETTLEMENT" in narr or "SALARY" in narr or "INFLOW" in narr:
        category = "INCOME"
        if "SALARY" in narr:
            is_recurring = True
    elif "RENT" in narr:
        category = "RENT"
        is_recurring = True
    elif "SUPPLIER" in narr or "VENDOR" in narr or "METAL" in narr:
        category = "VENDOR"
    elif "UTILITY" in narr or "ELECTRICITY" in narr or "WATER" in narr:
        category = "UTILITY"
        is_recurring = True
    elif "EMI" in narr or "LOAN" in narr:
        category = "EMI"
        is_recurring = True
    elif "TAX" in narr or "GST" in narr:
        category = "TAX"
        
    return category, is_recurring

# Cash Flow Analytics Engine
def process_cash_flow_analytics(customer_id: int, db: Session):
    accounts = db.query(LinkedAccount).filter(
        LinkedAccount.customer_id == customer_id,
        LinkedAccount.is_active == True
    ).all()
    
    if not accounts:
        return
        
    account_ids = [a.id for a in accounts]
    txns = db.query(AATransaction).filter(AATransaction.account_id.in_(account_ids)).order_by(AATransaction.txn_date.asc()).all()
    
    balances = [a.balance for a in accounts]
    avg_bal = sum(balances) / len(balances) if balances else 0.0
    median_bal = statistics.median(balances) if balances else 0.0
    
    total_inflow = 0.0
    total_outflow = 0.0
    credits_list = []
    debits_list = []
    
    # Categorization flags
    bounce_detected = False
    high_cash_dependency = False
    large_cash_withdrawal = False
    low_balance_flag = False
    dormant_flag = False
    overdraft_util = "None"
    
    cash_inflow = 0.0
    cash_outflow = 0.0
    
    for t in txns:
        narr = t.narration.upper()
        if "BOUNCE" in narr or "RETURN" in narr:
            bounce_detected = True
            
        if "CASH" in narr or "ATM" in narr:
            if t.txn_type == "CREDIT":
                cash_inflow += t.amount
            else:
                cash_outflow += t.amount
                
        if t.txn_type == "DEBIT" and t.amount > 50000.0 and ("CASH" in narr or "ATM" in narr):
            large_cash_withdrawal = True
            
        if t.txn_type == "CREDIT":
            total_inflow += t.amount
            credits_list.append(t.amount)
        else:
            total_outflow += t.amount
            debits_list.append(t.amount)
            
    # Monthly averages
    monthly_credits = total_inflow / 6.0
    monthly_debits = total_outflow / 6.0
    net_flow = total_inflow - total_outflow
    
    # Expense Ratio
    exp_ratio = total_outflow / total_inflow if total_inflow > 0 else 1.0
    
    # Savings behavior
    if net_flow > (total_inflow * 0.3):
        savings_behaviour = "High Savings"
    elif net_flow > (total_inflow * 0.1):
        savings_behaviour = "Moderate Savings"
    else:
        savings_behaviour = "Low Savings"
        
    # High cash dependency
    if total_inflow > 0 and (cash_inflow + cash_outflow) / (total_inflow + total_outflow) > 0.40:
        high_cash_dependency = True
        
    # Frequent low balance check
    if avg_bal < 10000:
        low_balance_flag = True
        
    # Overdraft usage check
    for a in accounts:
        if a.account_type == "OD" or a.account_type == "CC":
            overdraft_util = "Frequent"
            break
            
    # Stability Score
    cf_stability = 100.0
    if total_inflow > 0:
        cv = statistics.stdev(credits_list) / monthly_credits if len(credits_list) > 1 and monthly_credits > 0 else 0.0
        cf_stability = max(0.0, 100.0 * (1.0 - cv))
        
    # Seasonality
    seasonality = max(credits_list) / min(credits_list) if credits_list and min(credits_list) > 0 else 1.0
    
    # Working Capital Estimate
    working_capital = max(0.0, (monthly_credits - monthly_debits) * 3)
    
    # Banking Stability score (starts at 100, drops for bounces/low balances/overdraft)
    stability_score = 100.0
    if bounce_detected:
        stability_score -= 40
    if low_balance_flag:
        stability_score -= 20
    if high_cash_dependency:
        stability_score -= 10
    stability_score = max(0.0, stability_score)
    
    # Risk Indicators
    risks = []
    
    # 1. Liquidity Risk
    if low_balance_flag or stability_score < 50:
        liq_risk = "Critical"
        risks.append("Liquidity Risk")
    elif avg_bal < 25000:
        liq_risk = "High"
        risks.append("Liquidity Risk")
    elif avg_bal < 50000:
        liq_risk = "Medium"
    else:
        liq_risk = "Low"
        
    # 2. Cash Flow Risk
    if net_flow < 0 or exp_ratio > 0.95:
        cf_risk = "Critical"
        risks.append("Cash Flow Risk")
    elif exp_ratio > 0.85:
        cf_risk = "High"
        risks.append("Cash Flow Risk")
    else:
        cf_risk = "Low"
        
    # 3. Behaviour Risk
    if bounce_detected:
        beh_risk = "Critical"
        risks.append("Behaviour Risk")
    elif large_cash_withdrawal or high_cash_dependency:
        beh_risk = "High"
        risks.append("Behaviour Risk")
    else:
        beh_risk = "Low"
        
    # 4. Income Risk
    if cf_stability < 40 or seasonality > 2.0:
        inc_risk = "High"
        risks.append("Income Risk")
    else:
        inc_risk = "Low"
        
    # 5. Expense Risk
    if exp_ratio > 0.90:
        exp_risk = "High"
        risks.append("Expense Risk")
    else:
        exp_risk = "Low"
        
    # Overall risk level
    overall_risk = "Low"
    if "Critical" in (liq_risk, cf_risk, beh_risk):
        overall_risk = "Critical"
    elif "High" in (liq_risk, cf_risk, beh_risk, inc_risk, exp_risk):
        overall_risk = "High"
    elif "Medium" in (liq_risk, cf_risk, beh_risk):
        overall_risk = "Medium"
        
    # AI Financial Insights
    insights = []
    if net_flow > 0 and cf_stability > 80:
        insights.append("Strong and consistent cash flow.")
    if seasonality > 1.5:
        insights.append("Highly seasonal business income.")
    if stability_score >= 90:
        insights.append("Excellent banking discipline.")
    if overdraft_util == "Frequent":
        insights.append("Frequent overdraft utilization.")
    if high_cash_dependency:
        insights.append("Revenue concentration detected.")
    if large_cash_withdrawal:
        insights.append("Large cash withdrawals observed.")
    if not high_cash_dependency:
        insights.append("High digital transaction adoption.")
    if low_balance_flag or overall_risk == "Critical":
        insights.append("Potential liquidity stress.")
        
    analytics = db.query(AAAnalytics).filter(AAAnalytics.customer_id == customer_id).first()
    if not analytics:
        analytics = AAAnalytics(customer_id=customer_id)
        db.add(analytics)
        
    analytics.total_inflow = total_inflow
    analytics.total_outflow = total_outflow
    analytics.net_cash_flow = net_flow
    analytics.avg_balance = avg_bal
    analytics.median_balance = median_bal
    analytics.income_score = cf_stability
    analytics.debt_service_ratio = exp_ratio
    
    analytics.monthly_credits = monthly_credits
    analytics.monthly_debits = monthly_debits
    analytics.cash_flow_stability = cf_stability
    analytics.seasonality = seasonality
    analytics.income_stability = cf_stability
    analytics.expense_ratio = exp_ratio
    analytics.working_capital_estimate = working_capital
    analytics.savings_behaviour = savings_behaviour
    
    analytics.salary_regularity = "Regular" if not dormant_flag else "Irregular"
    analytics.business_revenue_stability = "Stable" if cf_stability > 60 else "Volatile"
    analytics.cheque_bounce_indicator = bounce_detected
    analytics.emi_discipline = "Excellent" if not bounce_detected else "Poor"
    analytics.overdraft_usage = overdraft_util
    analytics.high_cash_dependency = high_cash_dependency
    analytics.large_cash_withdrawals = large_cash_withdrawal
    analytics.frequent_low_balance = low_balance_flag
    analytics.dormant_account = dormant_flag
    
    analytics.liquidity_risk = liq_risk
    analytics.cash_flow_risk = cf_risk
    analytics.behaviour_risk = beh_risk
    analytics.income_risk = inc_risk
    analytics.expense_risk = exp_risk
    analytics.banking_stability_score = stability_score
    analytics.overall_score = max(0.0, 100.0 - len(risks) * 15)
    analytics.ai_insights = " | ".join(insights)
    analytics.last_calculated_at = datetime.datetime.utcnow()
    
    db.commit()
    
    # Publish events
    publish_workflow_event("Cash Flow Analysis Completed", customer_id, {
        "monthly_credits": monthly_credits, "monthly_debits": monthly_debits, "net_cash_flow": net_flow
    })
    publish_workflow_event("Financial Behaviour Updated", customer_id, {
        "overall_score": analytics.overall_score, "stability_score": stability_score
    })
    publish_workflow_event("Risk Indicators Generated", customer_id, {
        "overall_risk": overall_risk, "indicators": risks
    })
    
    logger.info(f"AUDIT | Account Aggregator analytics calculated successfully for customer: {customer_id}")

# REST APIs

@app.post("/aa/consents", response_model=AAConsentResponse, status_code=status.HTTP_201_CREATED)
async def generate_consent_request(payload: AAConsentCreateRequest, db: Session = Depends(get_db)):
    consent_id = f"consent_art_{uuid.uuid4().hex[:12]}"
    validity_date = datetime.datetime.utcnow() + datetime.timedelta(days=payload.validity_days)
    
    consent = AAConsent(
        customer_id=payload.customer_id,
        consent_artefact_id=consent_id,
        purpose=payload.purpose,
        data_requested=payload.data_requested,
        validity=validity_date.strftime("%Y-%m-%d"),
        frequency=payload.frequency,
        status="PENDING"
    )
    db.add(consent)
    db.commit()
    db.refresh(consent)
    
    publish_workflow_event("AA Consent Requested", payload.customer_id, {"consent_id": consent_id})
    return consent

@app.post("/aa/consents/{consent_id}/approve", response_model=AAConsentResponse)
async def approve_consent(consent_id: str, payload: ConsentStatusUpdateRequest, db: Session = Depends(get_db)):
    consent = db.query(AAConsent).filter(AAConsent.consent_artefact_id == consent_id).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent request not found.")
        
    consent.status = "APPROVED"
    consent.accounts_included = payload.accounts_included or "SBI-ACC-CURRENT,IDBI-ACC-SAVINGS"
    db.commit()
    db.refresh(consent)
    
    publish_workflow_event("Consent Approved", consent.customer_id, {"consent_id": consent_id})
    return consent

@app.post("/aa/consents/{consent_id}/reject", response_model=AAConsentResponse)
async def reject_consent(consent_id: str, db: Session = Depends(get_db)):
    consent = db.query(AAConsent).filter(AAConsent.consent_artefact_id == consent_id).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent request not found.")
        
    consent.status = "REJECTED"
    db.commit()
    db.refresh(consent)
    return consent

@app.post("/aa/consents/{consent_id}/revoke", response_model=AAConsentResponse)
async def revoke_consent(consent_id: str, db: Session = Depends(get_db)):
    consent = db.query(AAConsent).filter(AAConsent.consent_artefact_id == consent_id).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent request not found.")
        
    consent.status = "REVOKED"
    db.commit()
    db.refresh(consent)
    return consent

@app.get("/aa/consents/{consent_id}", response_model=AAConsentResponse)
async def get_consent_details(consent_id: str, db: Session = Depends(get_db)):
    consent = db.query(AAConsent).filter(AAConsent.consent_artefact_id == consent_id).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent request not found.")
    return consent

@app.get("/aa/consents", response_model=List[AAConsentResponse])
async def list_consent_history(customer_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(AAConsent)
    if customer_id:
        query = query.filter(AAConsent.customer_id == customer_id)
    return query.order_by(AAConsent.created_at.desc()).all()

@app.post("/aa/discover/{customer_id}", response_model=List[LinkedAccountResponse])
async def discover_accounts(customer_id: int, payload: DiscoveryRequest):
    logger.info(f"AUDIT | Querying AA registry for mobile: {payload.customer_mobile}")
    adapter = get_aa_adapter()
    accounts = adapter.discover_financial_accounts(payload.customer_mobile)
    
    return [
        LinkedAccountResponse(
            id=idx,
            customer_id=customer_id,
            account_ref_num=a["account_ref_num"],
            masked_acc_num=a["masked_acc_num"],
            bank_name=a["bank_name"],
            account_type=a["account_type"],
            balance=a["balance"],
            currency=a["currency"],
            is_active=True,
            last_synced_at=datetime.datetime.utcnow()
        ) for idx, a in enumerate(accounts)
    ]

@app.post("/aa/link/{customer_id}", response_model=List[LinkedAccountResponse])
async def link_accounts(customer_id: int, payload: List[LinkAccountRequest], db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Linking accounts for Customer: {customer_id}")
    linked = []
    
    for val in payload:
        existing = db.query(LinkedAccount).filter(LinkedAccount.account_ref_num == val.account_ref_num).first()
        if existing:
            linked.append(existing)
            continue
            
        acc = LinkedAccount(
            customer_id=customer_id,
            account_ref_num=val.account_ref_num,
            masked_acc_num=val.masked_acc_num,
            bank_name=val.bank_name,
            account_type=val.account_type,
            balance=val.balance if hasattr(val, "balance") else (100000.0 if val.account_type == "SAVINGS" else 450000.0),
            currency="INR"
        )
        db.add(acc)
        linked.append(acc)
        
    db.commit()
    
    publish_workflow_event("Accounts Retrieved", customer_id, {"count": len(linked)})
    return linked

@app.post("/aa/sync/{customer_id}", response_model=AAAnalyticsResponse)
async def sync_financial_records(customer_id: int, payload: SyncRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Syncing bank statements via AA Consent: {payload.consent_id}")
    
    accounts = db.query(LinkedAccount).filter(
        LinkedAccount.customer_id == customer_id,
        LinkedAccount.is_active == True
    ).all()
    
    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No linked accounts found. Discover and link accounts first."
        )
        
    adapter = get_aa_adapter()
    
    for a in accounts:
        db.query(AATransaction).filter(AATransaction.account_id == a.id).delete()
        ledger = adapter.fetch_transaction_ledger(a.account_ref_num)
        
        for txn in ledger:
            category, is_recurring = normalize_and_categorize(txn["narration"])
            
            t_record = AATransaction(
                account_id=a.id,
                txn_ref_num=txn["txn_ref_num"],
                txn_date=txn["txn_date"],
                amount=txn["amount"],
                txn_type=txn["txn_type"],
                narration=txn["narration"],
                category=category,
                is_recurring=is_recurring
            )
            db.add(t_record)
            
        a.last_synced_at = datetime.datetime.utcnow()
        
    db.commit()
    
    publish_workflow_event("Transactions Imported", customer_id, {"consent_id": payload.consent_id})
    
    # Process cash flow aggregations
    process_cash_flow_analytics(customer_id, db)
    
    analytics = db.query(AAAnalytics).filter(AAAnalytics.customer_id == customer_id).first()
    return analytics

@app.get("/aa/accounts/{customer_id}", response_model=List[LinkedAccountResponse])
async def list_linked_accounts(customer_id: int, db: Session = Depends(get_db)):
    return db.query(LinkedAccount).filter(LinkedAccount.customer_id == customer_id).all()

@app.get("/aa/financial-info/{customer_id}", response_model=List[AATransactionResponse])
async def get_financial_information(customer_id: int, db: Session = Depends(get_db)):
    accounts = db.query(LinkedAccount).filter(LinkedAccount.customer_id == customer_id).all()
    account_ids = [a.id for a in accounts]
    return db.query(AATransaction).filter(AATransaction.account_id.in_(account_ids)).all()

@app.get("/aa/analytics/{customer_id}", response_model=AAAnalyticsResponse)
async def get_aa_analytics(customer_id: int, db: Session = Depends(get_db)):
    analytics = db.query(AAAnalytics).filter(AAAnalytics.customer_id == customer_id).first()
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cash flow analytics not synced yet."
        )
    return analytics

@app.post("/aa/replay/{customer_id}", response_model=AAAnalyticsResponse)
async def replay_financial_import(customer_id: int, db: Session = Depends(get_db)):
    # Auto-generates standard consent and synchronizes transactional data
    consent_id = f"consent_art_replay"
    consent = db.query(AAConsent).filter(AAConsent.consent_artefact_id == consent_id).first()
    if not consent:
        consent = AAConsent(
            customer_id=customer_id,
            consent_artefact_id=consent_id,
            purpose="Automatic Replay Spreading",
            data_requested="Balance & Transactions",
            validity="2026-12-31",
            status="APPROVED"
        )
        db.add(consent)
        db.commit()
        
    sync_req = SyncRequest(consent_id=consent_id)
    return await sync_financial_records(customer_id, sync_req, db)

@app.post("/aa/reset")
async def reset_aa_dataset(db: Session = Depends(get_db)):
    logger.info("AUDIT | Resetting AA Dataset")
    db.query(AATransaction).delete()
    db.query(AAAnalytics).delete()
    db.query(LinkedAccount).delete()
    db.query(AAConsent).delete()
    db.commit()
    return {"message": "Account Aggregator dataset reset successfully."}

@app.get("/livez")
async def livez():
    return {"status": "UP"}
