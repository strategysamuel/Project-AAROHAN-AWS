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

from app.models import TReDSBuyer, TReDSInvoice
from app.schemas import TReDSInvoiceResponse, TReDSSyncRequest
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "treds-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("treds-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN TReDS Supply Chain Finance Integration Gateway Service",
    description="consented India TReDS invoice discounting, buyer credit performance, and Gemini receivables intelligence",
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

# TReDS mock registry records
def pull_treds_mock_invoice_data(customer_id: int) -> List[dict]:
    return [
        {
            "invoice_number": "INV-2025-001",
            "buyer_pan": "BUYER9988C",
            "buyer_name": "Tata Motors Limited",
            "amount": 2500000.0,
            "tenure_days": 60,
            "issue_date": datetime.datetime(2025, 6, 1),
            "due_date": datetime.datetime(2025, 8, 1)
        },
        {
            "invoice_number": "INV-2025-002",
            "buyer_pan": "BUYER7766K",
            "buyer_name": "Reliance Retail Private Limited",
            "amount": 1800000.0,
            "tenure_days": 45,
            "issue_date": datetime.datetime(2025, 6, 10),
            "due_date": datetime.datetime(2025, 7, 25)
        }
    ]

# REST APIs

@app.post("/treds/sync/{customer_id}", response_model=List[TReDSInvoiceResponse], status_code=status.HTTP_200_OK)
async def sync_treds_invoices(customer_id: int, payload: TReDSSyncRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Syncing TReDS invoices registry | Seller PAN: {payload.seller_pan} | Customer: {customer_id}")
    
    # Delete existing eligible invoices for idempotency
    db.query(TReDSInvoice).filter(TReDSInvoice.customer_id == customer_id, TReDSInvoice.status == "ELIGIBLE").delete()
    db.commit()
    
    invoices = pull_treds_mock_invoice_data(customer_id)
    created_records = []
    
    for inv in invoices:
        record = TReDSInvoice(
            customer_id=customer_id,
            invoice_number=inv["invoice_number"],
            buyer_pan=inv["buyer_pan"],
            buyer_name=inv["buyer_name"],
            amount=inv["amount"],
            tenure_days=inv["tenure_days"],
            issue_date=inv["issue_date"],
            due_date=inv["due_date"],
            status="ELIGIBLE"
        )
        db.add(record)
        created_records.append(record)
        
    db.commit()
    
    # Refresh records
    for r in created_records:
        db.refresh(r)
        
    logger.info(f"AUDIT | TReDS Invoice sync complete | Count: {len(created_records)} | Event: bank.aarohan.treds.synced")
    return created_records

@app.get("/treds/invoices/{customer_id}", response_model=List[TReDSInvoiceResponse])
async def list_invoices(customer_id: int, db: Session = Depends(get_db)):
    return db.query(TReDSInvoice).filter(TReDSInvoice.customer_id == customer_id).all()

@app.post("/treds/discount/{invoice_id}", response_model=TReDSInvoiceResponse)
async def discount_invoice(invoice_id: int, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Executing TReDS discounting flow for Invoice ID: {invoice_id}")
    
    invoice = db.query(TReDSInvoice).filter(TReDSInvoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TReDS invoice details not found."
        )
        
    if invoice.status != "ELIGIBLE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invoice is already discounted or settled."
        )
        
    invoice.status = "DISCOUNTED"
    db.commit()
    db.refresh(invoice)
    
    # Event simulation trigger in logs (Future Pub/Sub topic push)
    logger.info(f"AUDIT | Invoice discounted successfully | Disbursed Amount: {invoice.amount} | Event: bank.aarohan.treds.discounted")
    return invoice

@app.get("/livez")
async def livez():
    return {"status": "UP"}
