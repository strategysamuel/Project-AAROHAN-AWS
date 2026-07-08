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

from app.models import LinkedAccount, AATransaction, AAAnalytics
from app.schemas import LinkedAccountResponse, AAAnalyticsResponse, DiscoveryRequest, LinkAccountRequest, SyncRequest
from app.database import get_db, init_db
from app.providers import AccountAggregatorMockProvider

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
    title="AAROHAN Account Aggregator & Financial Analytics Service",
    description="consented financial data retrieval, transactional normalization, and cash flow evaluation pipelines",
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

# Transaction Normalization & Analytics Engine
def normalize_and_categorize(narration: str) -> tuple[str, bool]:
    narr = narration.upper()
    category = "OTHERS"
    is_recurring = False
    
    if "CLIENT SETTLEMENT" in narr or "SALARY" in narr:
        category = "INCOME"
    elif "RENT" in narr:
        category = "RENT"
        is_recurring = True
    elif "SUPPLIER" in narr or "METAL" in narr:
        category = "VENDOR"
    elif "UTILITY" in narr or "ELECTRICITY" in narr:
        category = "UTILITY"
        is_recurring = True
        
    return category, is_recurring

def process_cash_flow_analytics(customer_id: int, db: Session):
    accounts = db.query(LinkedAccount).filter(
        LinkedAccount.customer_id == customer_id,
        LinkedAccount.is_active == True
    ).all()
    
    if not accounts:
        return
        
    account_ids = [a.id for a in accounts]
    txns = db.query(AATransaction).filter(AATransaction.account_id.in_(account_ids)).all()
    
    total_inflow = 0.0
    total_outflow = 0.0
    
    for t in txns:
        if t.txn_type == "CREDIT":
            total_inflow += t.amount
        else:
            total_outflow += t.amount
            
    net_flow = total_inflow - total_outflow
    avg_bal = sum(a.balance for a in accounts) / len(accounts)
    
    # Simple debt service coverage index simulation
    dsr = total_outflow / total_inflow if total_inflow > 0 else 0.0
    
    analytics = db.query(AAAnalytics).filter(AAAnalytics.customer_id == customer_id).first()
    if not analytics:
        analytics = AAAnalytics(customer_id=customer_id)
        db.add(analytics)
        
    analytics.total_inflow = total_inflow
    analytics.total_outflow = total_outflow
    analytics.net_cash_flow = net_flow
    analytics.avg_balance = avg_bal
    analytics.debt_service_ratio = dsr
    analytics.last_calculated_at = datetime.datetime.utcnow()
    
    db.commit()
    logger.info(f"AUDIT | Cash Flow Analytics recalculated for Customer: {customer_id}")

# REST APIs

@app.post("/aa/discover/{customer_id}", response_model=List[LinkedAccountResponse])
async def discover_accounts(customer_id: int, payload: DiscoveryRequest):
    logger.info(f"AUDIT | Querying AA registry for mobile: {payload.customer_mobile}")
    provider = AccountAggregatorMockProvider()
    accounts = provider.discover_financial_accounts(payload.customer_mobile)
    
    # Return discovered accounts mapping
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
            last_synced_at=datetime.datetime.utcnow()
        ) for idx, a in enumerate(accounts)
    ]

@app.post("/aa/link/{customer_id}", response_model=List[LinkedAccountResponse])
async def link_accounts(customer_id: int, payload: List[LinkAccountRequest], db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Linking accounts for Customer: {customer_id}")
    linked = []
    
    for val in payload:
        # Check duplicate
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
            balance=100000.0 if val.account_type == "SAVINGS" else 450000.0, # Seed default balances
            currency="INR"
        )
        db.add(acc)
        linked.append(acc)
        
    db.commit()
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
        
    provider = AccountAggregatorMockProvider()
    
    for a in accounts:
        # Delete existing transactions for idempotency
        db.query(AATransaction).filter(AATransaction.account_id == a.id).delete()
        
        # Pull transactional ledger from Mock AA
        ledger = provider.fetch_transaction_ledger(a.account_ref_num)
        
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
    
    # Process cash flow aggregations
    process_cash_flow_analytics(customer_id, db)
    
    analytics = db.query(AAAnalytics).filter(AAAnalytics.customer_id == customer_id).first()
    logger.info(f"AUDIT | Transaction sync completed | Event: bank.aarohan.spreading.completed")
    return analytics

@app.get("/aa/accounts/{customer_id}", response_model=List[LinkedAccountResponse])
async def list_linked_accounts(customer_id: int, db: Session = Depends(get_db)):
    return db.query(LinkedAccount).filter(LinkedAccount.customer_id == customer_id).all()

@app.get("/aa/analytics/{customer_id}", response_model=AAAnalyticsResponse)
async def get_aa_analytics(customer_id: int, db: Session = Depends(get_db)):
    analytics = db.query(AAAnalytics).filter(AAAnalytics.customer_id == customer_id).first()
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cash flow analytics not synced yet."
        )
    return analytics

@app.get("/livez")
async def livez():
    return {"status": "UP"}
