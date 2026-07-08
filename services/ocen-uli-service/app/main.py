import logging
import sys
import time
import uuid
import datetime
from abc import ABC, abstractmethod
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import Base, Lender, Partner, LoanApplication, LoanOffer, AuditLog
from app.schemas import (
    LenderRegisterRequest, PartnerRegisterRequest,
    EligibilityCheckRequest, EligibilityCheckResponse,
    LoanApplicationCreate, LoanApplicationResponse,
    LoanOfferResponse, OfferComparisonResponse,
    LoanAcceptRequest, AIRecommendationResponse
)
from app.database import get_db, init_db, SessionLocal

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "ocen-uli-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ocen-uli-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN OCEN & ULI Digital Lending Integration Gateway Service",
    description="Production-ready mock integration gateway orchestrating Open Credit Enablement Network and Unified Lending Interface operations",
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
    request.state.correlation_id = correlation_id
    logger.info(f"AUDIT | Request: {request.method} {request.url.path} | Correlation ID: {correlation_id}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Correlation-ID"] = correlation_id
    
    logger.info(f"AUDIT | Completed: {request.method} {request.url.path} | Status: {response.status_code} | Process Time: {process_time:.4f}s")
    return response

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    correlation_id = getattr(request.state, "correlation_id", "unknown")
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

# ---------------------------------------------------------
# Audit Trail Helper
# ---------------------------------------------------------
def log_audit(db: Session, event_type: str, actor: str, message: str, details: str = None, correlation_id: str = "SYSTEM"):
    logger.info(f"AUDIT STORE | Event: {event_type} | Message: {message}")
    audit = AuditLog(
        correlation_id=correlation_id,
        event_type=event_type,
        actor=actor,
        message=message,
        details=details
    )
    db.add(audit)
    db.commit()

# ---------------------------------------------------------
# OCEN & ULI Abstractions and Mocks
# ---------------------------------------------------------
class OCENProvider(ABC):
    @abstractmethod
    def fetch_offers(self, uli_ref: str, requested_amount: float) -> List[dict]:
        pass

class ULIAdapter(ABC):
    @abstractmethod
    def verify_borrower_consent(self, customer_id: int) -> bool:
        pass
    
    @abstractmethod
    def pull_credit_score(self, customer_id: int) -> int:
        pass

class MockOCENProvider(OCENProvider):
    def __init__(self, db: Session):
        self.db = db

    def fetch_offers(self, uli_ref: str, requested_amount: float) -> List[dict]:
        active_lenders = self.db.query(Lender).filter(Lender.is_active == True).all()
        offers = []
        for l in active_lenders:
            if requested_amount <= l.max_loan_amount:
                rate = l.base_interest_rate
                tenure = 12
                # Simple EMI calculation: (P + (P * R * T / 100)) / T
                interest = requested_amount * (rate / 100.0) * (tenure / 12.0)
                total_payable = requested_amount + interest
                emi = total_payable / tenure
                
                offers.append({
                    "lender_id": l.lender_id,
                    "lender_name": l.name,
                    "offered_amount": requested_amount,
                    "interest_rate": rate,
                    "tenure_months": tenure,
                    "processing_fee": round(requested_amount * 0.01, 2),
                    "monthly_installment": round(emi, 2)
                })
        return offers

class MockULIProvider(ULIAdapter):
    def verify_borrower_consent(self, customer_id: int) -> bool:
        # Mocking Unified Lending Interface consent orchestration
        return True

    def pull_credit_score(self, customer_id: int) -> int:
        # Simulate standard credit Bureau registry check via ULI
        if customer_id == 125:
            return 780
        return 680

# ---------------------------------------------------------
# Seed Data helper
# ---------------------------------------------------------
def seed_lenders_and_partners(db: Session):
    if db.query(Lender).count() == 0:
        logger.info("Seeding default lenders...")
        lenders = [
            Lender(lender_id="LEND-IDBI", name="IDBI Bank Ltd", lender_type="BANK", base_interest_rate=9.5, max_loan_amount=10000000.0, min_credit_score=700),
            Lender(lender_id="LEND-HDFC", name="HDFC Bank", lender_type="BANK", base_interest_rate=10.25, max_loan_amount=5000000.0, min_credit_score=680),
            Lender(lender_id="LEND-TATA", name="Tata Capital", lender_type="NBFC", base_interest_rate=11.5, max_loan_amount=3000000.0, min_credit_score=650)
        ]
        db.add_all(lenders)
        db.commit()
    
    if db.query(Partner).count() == 0:
        logger.info("Seeding default ecosystem partners...")
        partners = [
            Partner(partner_id="PART-GSTN", name="GSTN Portal Service", partner_type="Tech Provider"),
            Partner(partner_id="PART-ONDC", name="ONDC Credit LSP App", partner_type="LSP")
        ]
        db.add_all(partners)
        db.commit()

# Seed databases on startup
with SessionLocal() as db_session:
    seed_lenders_and_partners(db_session)

# ---------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------
@app.get("/healthz", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy", "service": "ocen-uli-service", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

# ---------------------------------------------------------
# REST APIs
# ---------------------------------------------------------

@app.get("/ocen/lenders", response_model=List[LenderRegisterRequest])
async def list_lenders(db: Session = Depends(get_db)):
    return db.query(Lender).all()

@app.post("/ocen/lenders", response_model=LenderRegisterRequest)
async def register_lender(payload: LenderRegisterRequest, db: Session = Depends(get_db)):
    # Check duplicate
    exists = db.query(Lender).filter(Lender.lender_id == payload.lender_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Lender ID already exists.")
    
    lender = Lender(**payload.dict())
    db.add(lender)
    db.commit()
    log_audit(db, "LENDER_REGISTERED", "SYSTEM", f"Lender registered: {payload.name}")
    return lender

@app.get("/ocen/partners")
async def list_partners(db: Session = Depends(get_db)):
    return db.query(Partner).all()

@app.post("/ocen/partners", response_model=PartnerRegisterRequest)
async def register_partner(payload: PartnerRegisterRequest, db: Session = Depends(get_db)):
    exists = db.query(Partner).filter(Partner.partner_id == payload.partner_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Partner ID already exists.")
    
    partner = Partner(**payload.dict())
    db.add(partner)
    db.commit()
    log_audit(db, "PARTNER_REGISTERED", "SYSTEM", f"Ecosystem partner registered: {payload.name}")
    return partner

@app.post("/ocen/eligibility", response_model=EligibilityCheckResponse)
async def check_eligibility(payload: EligibilityCheckRequest, db: Session = Depends(get_db)):
    # ULI adapter flow
    uli = MockULIProvider()
    consent = uli.verify_borrower_consent(payload.customer_id)
    if not consent:
        raise HTTPException(status_code=400, detail="ULI Consent Verification Failed.")
        
    credit_score = uli.pull_credit_score(payload.customer_id)
    
    # Simple logic
    eligible = True
    reason = "Consented checks cleared. Customer matches platform lending criteria."
    max_eligible_amount = payload.annual_revenue * 0.3
    
    if credit_score < 650:
        eligible = False
        reason = f"Credit Score {credit_score} is below minimum requirement of 650."
    elif payload.requested_amount > max_eligible_amount:
        eligible = False
        reason = f"Requested amount exceeds maximum threshold based on annual revenue of {payload.annual_revenue}."

    uli_ref = f"ULI-{uuid.uuid4().hex[:8].upper()}"
    
    log_audit(db, "ELIGIBILITY_CHECKED", str(payload.customer_id), 
              f"Eligibility check processed. Status: {eligible}, Reference: {uli_ref}", 
              details=f"Score: {credit_score}, Revenue: {payload.annual_revenue}")
              
    return EligibilityCheckResponse(
        eligible=eligible,
        reason=reason,
        max_eligible_amount=max_eligible_amount,
        uli_reference=uli_ref
    )

@app.post("/ocen/apply", response_model=LoanApplicationResponse)
async def apply_loan(payload: LoanApplicationCreate, db: Session = Depends(get_db)):
    # 1. Trigger ULI UliRef Generation
    uli_ref = f"ULI-{uuid.uuid4().hex[:8].upper()}"
    
    app_record = LoanApplication(
        customer_id=payload.customer_id,
        uli_reference=uli_ref,
        requested_amount=payload.requested_amount,
        requested_tenure_months=payload.requested_tenure_months,
        purpose=payload.purpose,
        status="APPLIED"
    )
    db.add(app_record)
    db.commit()
    db.refresh(app_record)
    
    log_audit(db, "LOAN_APPLIED", str(payload.customer_id), 
              f"Created Loan Application ID: {app_record.id} with ULI reference: {uli_ref}", 
              correlation_id=uli_ref)
              
    # 2. Fetch OCEN Lender Offers
    ocen = MockOCENProvider(db)
    offers_data = ocen.fetch_offers(uli_ref, payload.requested_amount)
    
    if not offers_data:
        app_record.status = "REJECTED"
        db.commit()
        log_audit(db, "LOAN_REJECTED", "SYSTEM", f"No available lenders matched requested amount {payload.requested_amount}", correlation_id=uli_ref)
    else:
        for offer in offers_data:
            off = LoanOffer(
                application_id=app_record.id,
                lender_id=offer["lender_id"],
                lender_name=offer["lender_name"],
                offered_amount=offer["offered_amount"],
                interest_rate=offer["interest_rate"],
                tenure_months=offer["tenure_months"],
                processing_fee=offer["processing_fee"],
                monthly_installment=offer["monthly_installment"],
                status="PENDING"
            )
            db.add(off)
        app_record.status = "OFFERS_GENERATED"
        db.commit()
        log_audit(db, "OFFERS_GENERATED", "SYSTEM", f"Generated {len(offers_data)} mock OCEN offers", correlation_id=uli_ref)
        
    db.refresh(app_record)
    return app_record

@app.get("/ocen/applications/{app_id}", response_model=LoanApplicationResponse)
async def get_application(app_id: int, db: Session = Depends(get_db)):
    app_record = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found.")
    return app_record

@app.get("/ocen/applications/{app_id}/offers", response_model=List[LoanOfferResponse])
async def get_application_offers(app_id: int, db: Session = Depends(get_db)):
    return db.query(LoanOffer).filter(LoanOffer.application_id == app_id).all()

@app.get("/ocen/offers/compare/{app_id}", response_model=OfferComparisonResponse)
async def compare_offers(app_id: int, db: Session = Depends(get_db)):
    app_record = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found.")
        
    offers = db.query(LoanOffer).filter(LoanOffer.application_id == app_id).all()
    if not offers:
        return OfferComparisonResponse(offers=[], best_rate_offer_id=None, best_amount_offer_id=None, comparison_notes="No offers generated.")
        
    # Sort
    best_rate = min(offers, key=lambda x: x.interest_rate)
    best_amount = max(offers, key=lambda x: x.offered_amount)
    
    notes = f"Comparison Engine: {best_rate.lender_name} offers the lowest APR ({best_rate.interest_rate}%)."
    
    return OfferComparisonResponse(
        offers=offers,
        best_rate_offer_id=best_rate.id,
        best_amount_offer_id=best_amount.id,
        comparison_notes=notes
    )

@app.post("/ocen/offers/accept", response_model=LoanApplicationResponse)
async def accept_offer(payload: LoanAcceptRequest, db: Session = Depends(get_db)):
    offer = db.query(LoanOffer).filter(LoanOffer.id == payload.offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found.")
        
    app_record = db.query(LoanApplication).filter(LoanApplication.id == offer.application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Associated application not found.")
        
    # Accept
    offer.status = "ACCEPTED"
    app_record.status = "ACCEPTED"
    app_record.selected_offer_id = offer.id
    
    # Reject others
    db.query(LoanOffer).filter(
        LoanOffer.application_id == app_record.id,
        LoanOffer.id != offer.id
    ).update({"status": "EXPIRED"})
    
    db.commit()
    db.refresh(app_record)
    
    log_audit(db, "LOAN_ACCEPTED", str(app_record.customer_id), 
              f"Accepted Loan Offer ID: {offer.id} from {offer.lender_name}", 
              correlation_id=app_record.uli_reference)
              
    return app_record

@app.post("/ocen/disburse/{app_id}", response_model=LoanApplicationResponse)
async def disburse_loan(app_id: int, db: Session = Depends(get_db)):
    app_record = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found.")
        
    if app_record.status != "ACCEPTED":
        raise HTTPException(status_code=400, detail="Application must be in ACCEPTED state to disburse.")
        
    app_record.status = "DISBURSED"
    db.commit()
    db.refresh(app_record)
    
    log_audit(db, "LOAN_DISBURSED", "SYSTEM", 
              f"Digital disbursement completed for application: {app_id}", 
              correlation_id=app_record.uli_reference)
              
    return app_record

@app.get("/ocen/ai-advisor/{app_id}", response_model=AIRecommendationResponse)
async def get_ai_advisor_rec(app_id: int, db: Session = Depends(get_db)):
    app_record = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found.")
        
    offers = db.query(LoanOffer).filter(LoanOffer.application_id == app_id).all()
    if not offers:
        return AIRecommendationResponse(
            suitability_score=0.0,
            dynamic_summary="No active credit offers found to analyze.",
            recommended_offer_id=None,
            breakdown="Create a credit application first."
        )
        
    best_offer = min(offers, key=lambda x: x.interest_rate)
    
    # Simulate Gemini/Vertex AI recommendation
    summary = f"Gemini Recommendation Engine identifies {best_offer.lender_name} as the prime suitability match."
    breakdown = (
        f"Lending Assistant Analysis:\n"
        f"- Lender: {best_offer.lender_name} matches primary banking tier.\n"
        f"- Net Monthly Installment (EMI): ₹{best_offer.monthly_installment:,.2f} is well within your working capital margins.\n"
        f"- Interest rate of {best_offer.interest_rate}% APR is optimal compared to alternative capital options."
    )
    
    return AIRecommendationResponse(
        suitability_score=94.5,
        dynamic_summary=summary,
        recommended_offer_id=best_offer.id,
        breakdown=breakdown
    )

@app.get("/ocen/audit-logs", response_model=List[dict])
async def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
    return [
        {
            "id": l.id,
            "correlation_id": l.correlation_id,
            "event_type": l.event_type,
            "actor": l.actor,
            "message": l.message,
            "details": l.details,
            "timestamp": l.timestamp.isoformat()
        } for l in logs
    ]
