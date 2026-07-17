"""
AAROHAN – OCEN Marketplace Simulation Service (v2)
===================================================
Implements the full Open Credit Enablement Network marketplace:
  • Lender search and eligibility screening
  • Ranked loan offer generation with explainability
  • Offer comparison, acceptance and rejection
  • Marketplace dashboard and status
  • Admin: lender CRUD, policy config, replay, export
  • Workflow integration: FHC → Credit Decision → RBI Fraud → OCEN
  • Business Event publishing
  • Adapter switching (SIMULATION / SANDBOX / PRODUCTION)
"""
import json
import logging
import sys
import time
import uuid
import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, Depends, Query, Body, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

# ── Bootstrap ese-core path ──────────────────────────────────────────────────
import os
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
ese_core_path = os.path.join(WORKSPACE_ROOT, "services", "ese-core")
if ese_core_path not in sys.path:
    sys.path.insert(0, ese_core_path)

from app.models import (
    Base, Lender, LoanProduct, Partner,
    LoanApplication, LoanOffer, MarketplaceMatch,
    MarketplaceConfig, AuditLog,
)
from app.schemas import (
    LenderRegisterRequest, LenderResponse, PartnerRegisterRequest,
    EligibilityCheckRequest, EligibilityCheckResponse,
    LoanApplicationCreate, LoanApplicationResponse,
    LoanOfferResponse, OfferComparisonResponse,
    LoanAcceptRequest, LoanRejectRequest,
    AIRecommendationResponse,
    MarketplaceDashboardResponse,
    LenderSearchRequest, LenderSearchResponse, LenderSearchResult,
    ConfigUpdateRequest, MarketplaceReplayRequest,
)
from app.database import get_db, init_db, SessionLocal
from app.adapters import (
    SimulationAdapter, SandboxAdapter, ProductionAdapter,
    DEFAULT_MATCH_PARAMS, LENDER_SEED_DATA, LOAN_PRODUCTS_SEED,
)

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format=(
        '{"timestamp": "%(asctime)s", "severity": "%(levelname)s", '
        '"message": "%(message)s", "service": "ocen-uli-service"}'
    ),
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ocen-uli-service")

# ── DB init ──────────────────────────────────────────────────────────────────
init_db()

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="AAROHAN OCEN Marketplace Simulation Service",
    description=(
        "Intelligent loan matching marketplace for MSME borrowers. "
        "Simulates OCEN-compatible lender ecosystem with explainable AI."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Middleware ────────────────────────────────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = cid
    logger.info(f"AUDIT | {request.method} {request.url.path} | cid={cid}")
    response = await call_next(request)
    elapsed = time.time() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    response.headers["X-Correlation-ID"] = cid
    return response


@app.exception_handler(HTTPException)
async def http_exc_handler(request: Request, exc: HTTPException):
    cid = getattr(request.state, "correlation_id", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorCode": f"AAR-ERR-{exc.status_code}",
            "message": exc.detail,
            "correlationId": cid,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
    )


# ── Helpers ──────────────────────────────────────────────────────────────────

def _log_audit(
    db: Session, event_type: str, actor: str, message: str,
    details: str = None, correlation_id: str = "SYSTEM",
):
    logger.info(f"AUDIT | {event_type} | {message}")
    db.add(AuditLog(
        correlation_id=correlation_id,
        event_type=event_type,
        actor=actor,
        message=message,
        details=details,
    ))
    db.commit()


def _publish_event(event_type: str, customer_id: int, payload: dict):
    logger.info(f"AUDIT | EVENT_BUS | {event_type} | cid={customer_id}")
    try:
        from event_engine import BusinessEventEngine
        BusinessEventEngine().dispatch(event_type, f"cust_{customer_id}", payload)
    except Exception as exc:
        logger.warning(f"Event bus unavailable ({event_type}): {exc}")


def _get_active_config(db: Session):
    cfg = db.query(MarketplaceConfig).first()
    if not cfg:
        cfg = MarketplaceConfig(
            active_adapter="SIMULATION",
            match_params=json.dumps(DEFAULT_MATCH_PARAMS),
        )
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg.active_adapter, json.loads(cfg.match_params or "{}")


def _get_adapter(adapter_name: str):
    if adapter_name == "SANDBOX":
        return SandboxAdapter()
    if adapter_name == "PRODUCTION":
        return ProductionAdapter()
    return SimulationAdapter()


def _active_lenders(db: Session):
    return db.query(Lender).filter(Lender.is_active == True).all()


# ===========================================================================
#  1. LENDER REGISTRY
# ===========================================================================

@app.get(
    "/ocen/lenders",
    response_model=List[LenderResponse],
    summary="List All Lenders",
    tags=["Lender Registry"],
)
async def list_lenders(
    lender_type: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
):
    q = db.query(Lender)
    if active_only:
        q = q.filter(Lender.is_active == True)
    if lender_type:
        q = q.filter(Lender.lender_type == lender_type.upper())
    return q.all()


@app.get(
    "/ocen/lenders/{lender_id}",
    response_model=LenderResponse,
    summary="Get Lender Details",
    tags=["Lender Registry"],
)
async def get_lender(lender_id: str, db: Session = Depends(get_db)):
    lender = db.query(Lender).filter(Lender.lender_id == lender_id).first()
    if not lender:
        raise HTTPException(status_code=404, detail=f"Lender '{lender_id}' not found.")
    return lender


@app.post(
    "/ocen/lenders",
    response_model=LenderResponse,
    summary="Register New Lender",
    tags=["Lender Registry"],
)
async def register_lender(payload: LenderRegisterRequest, db: Session = Depends(get_db)):
    if db.query(Lender).filter(Lender.lender_id == payload.lender_id).first():
        raise HTTPException(status_code=409, detail="Lender ID already exists.")
    lender = Lender(**payload.model_dump())
    db.add(lender)
    db.commit()
    db.refresh(lender)
    _log_audit(db, "LENDER_REGISTERED", "ADMIN", f"Lender registered: {payload.name}")
    return lender


@app.put(
    "/ocen/lenders/{lender_id}",
    response_model=LenderResponse,
    summary="Update Lender",
    tags=["Lender Registry"],
)
async def update_lender(
    lender_id: str, payload: LenderRegisterRequest, db: Session = Depends(get_db)
):
    lender = db.query(Lender).filter(Lender.lender_id == lender_id).first()
    if not lender:
        raise HTTPException(status_code=404, detail="Lender not found.")
    for field, value in payload.model_dump(exclude={"lender_id"}).items():
        setattr(lender, field, value)
    db.commit()
    db.refresh(lender)
    _log_audit(db, "LENDER_UPDATED", "ADMIN", f"Lender updated: {lender_id}")
    return lender


@app.delete(
    "/ocen/lenders/{lender_id}",
    summary="Disable Lender",
    tags=["Lender Registry"],
)
async def disable_lender(lender_id: str, db: Session = Depends(get_db)):
    lender = db.query(Lender).filter(Lender.lender_id == lender_id).first()
    if not lender:
        raise HTTPException(status_code=404, detail="Lender not found.")
    lender.is_active = False
    db.commit()
    _log_audit(db, "LENDER_DISABLED", "ADMIN", f"Lender disabled: {lender_id}")
    return {"message": f"Lender {lender_id} disabled."}


# ===========================================================================
#  2. LOAN PRODUCTS
# ===========================================================================

@app.get(
    "/ocen/products",
    summary="List Loan Products",
    tags=["Loan Products"],
)
async def list_products(db: Session = Depends(get_db)):
    return db.query(LoanProduct).filter(LoanProduct.is_active == True).all()


# ===========================================================================
#  3. MARKETPLACE SEARCH – Find Eligible Lenders
# ===========================================================================

@app.post(
    "/ocen/marketplace/search",
    response_model=LenderSearchResponse,
    summary="Search Eligible Lenders",
    tags=["Marketplace"],
)
async def search_eligible_lenders(
    payload: LenderSearchRequest, db: Session = Depends(get_db)
):
    """
    Screen all active lenders against the customer's profile and return
    a ranked list with match scores and eligibility reasons.
    """
    _publish_event("Marketplace Search Started", payload.customer_id, {
        "requested_amount": payload.requested_amount,
        "product_type": payload.product_type,
    })

    adapter_name, match_params = _get_active_config(db)
    adapter = _get_adapter(adapter_name)
    lenders = _active_lenders(db)

    search_params = {
        "requested_amount": payload.requested_amount,
        "requested_tenure": 12,
        "fhc_score": payload.fhc_score,
        "credit_decision": payload.credit_decision,
        "fraud_risk_level": payload.fraud_risk_level,
        "product_type": payload.product_type,
        **match_params,
    }

    results = adapter.search_eligible_lenders(lenders, search_params)
    eligible_count = sum(1 for r in results if r["eligible"])

    return LenderSearchResponse(
        total_lenders_screened=len(results),
        eligible_lenders=eligible_count,
        results=[LenderSearchResult(**r) for r in results],
    )


# ===========================================================================
#  4. LOAN APPLICATION + OFFER GENERATION
# ===========================================================================

@app.post(
    "/ocen/apply",
    response_model=LoanApplicationResponse,
    summary="Submit Loan Application & Generate Offers",
    tags=["Marketplace"],
)
async def apply_for_loan(
    payload: LoanApplicationCreate, db: Session = Depends(get_db)
):
    """
    End-to-end marketplace flow:
    1. Create application with upstream intelligence (FHC, credit decision, fraud).
    2. Run matching engine across all active lenders.
    3. Generate ranked offers with explainability.
    4. Persist and publish events.
    """
    uli_ref = f"ULI-{uuid.uuid4().hex[:8].upper()}"

    application = LoanApplication(
        customer_id=payload.customer_id,
        uli_reference=uli_ref,
        requested_amount=payload.requested_amount,
        requested_tenure_months=payload.requested_tenure_months,
        product_type=payload.product_type,
        purpose=payload.purpose,
        fhc_score=payload.fhc_score,
        credit_decision=payload.credit_decision,
        fraud_score=payload.fraud_score,
        fraud_risk_level=payload.fraud_risk_level,
        status="APPLIED",
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    _publish_event("Marketplace Search Started", payload.customer_id, {
        "application_id": application.id, "uli_reference": uli_ref,
    })
    _log_audit(db, "LOAN_APPLIED", str(payload.customer_id),
               f"Application {application.id} created | ULI: {uli_ref}")

    # Block if Critical fraud risk
    if (payload.fraud_risk_level or "").strip() == "Critical":
        application.status = "BLOCKED_FRAUD"
        db.commit()
        _publish_event("Marketplace Completed", payload.customer_id, {
            "application_id": application.id, "result": "BLOCKED_FRAUD",
        })
        _log_audit(db, "MARKETPLACE_BLOCKED", "SYSTEM",
                   f"Application {application.id} blocked due to Critical fraud risk.")
        db.refresh(application)
        return application

    adapter_name, match_params = _get_active_config(db)
    adapter = _get_adapter(adapter_name)
    lenders = _active_lenders(db)

    offers_data = adapter.generate_offers(application, lenders, match_params)

    if not offers_data:
        application.status = "NO_OFFERS"
        db.commit()
        _publish_event("Marketplace Completed", payload.customer_id, {
            "application_id": application.id, "result": "NO_OFFERS",
        })
        _log_audit(db, "NO_OFFERS", "SYSTEM",
                   f"No eligible lenders found for application {application.id}")
    else:
        for offer_data in offers_data:
            offer = LoanOffer(
                application_id=application.id,
                lender_id=offer_data["lender_id"],
                lender_name=offer_data["lender_name"],
                lender_type=offer_data.get("lender_type", "BANK"),
                product_type=offer_data.get("product_type", payload.product_type),
                offered_amount=offer_data["offered_amount"],
                interest_rate=offer_data["interest_rate"],
                tenure_months=offer_data["tenure_months"],
                processing_fee=offer_data["processing_fee"],
                monthly_installment=offer_data["monthly_installment"],
                total_interest=offer_data.get("total_interest", 0.0),
                approval_probability=offer_data.get("approval_probability", 0.75),
                expected_disbursal_days=offer_data.get("expected_disbursal_days", 3),
                match_score=offer_data["match_score"],
                rank=offer_data["rank"],
                conditions=offer_data.get("conditions", ""),
                match_explanation=offer_data.get("match_explanation", "{}"),
                status="PENDING",
            )
            db.add(offer)
            _publish_event("Lender Matched", payload.customer_id, {
                "lender_id": offer_data["lender_id"],
                "match_score": offer_data["match_score"],
            })

        application.status = "OFFERS_GENERATED"
        db.commit()

        # Record marketplace match summary
        best = offers_data[0]
        db.add(MarketplaceMatch(
            application_id=application.id,
            lenders_screened=len(lenders),
            lenders_matched=len(offers_data),
            lenders_rejected=len(lenders) - len(offers_data),
            best_rate=best["interest_rate"],
            best_match_score=best["match_score"],
        ))
        db.commit()

        _publish_event("Loan Offer Generated", payload.customer_id, {
            "application_id": application.id,
            "offers_count": len(offers_data),
            "best_rate": best["interest_rate"],
        })
        _log_audit(db, "OFFERS_GENERATED", "SYSTEM",
                   f"{len(offers_data)} offers generated for application {application.id}")

    db.refresh(application)
    return application


# ===========================================================================
#  5. OFFERS – View / Compare / Accept / Reject
# ===========================================================================

@app.get(
    "/ocen/applications/{app_id}",
    response_model=LoanApplicationResponse,
    summary="Get Application",
    tags=["Marketplace"],
)
async def get_application(app_id: int, db: Session = Depends(get_db)):
    rec = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Application not found.")
    return rec


@app.get(
    "/ocen/applications/{app_id}/offers",
    response_model=List[LoanOfferResponse],
    summary="Get Offers for Application",
    tags=["Marketplace"],
)
async def get_offers(app_id: int, db: Session = Depends(get_db)):
    return (
        db.query(LoanOffer)
        .filter(LoanOffer.application_id == app_id)
        .order_by(LoanOffer.rank)
        .all()
    )


@app.get(
    "/ocen/offers/compare/{app_id}",
    response_model=OfferComparisonResponse,
    summary="Compare Loan Offers",
    tags=["Marketplace"],
)
async def compare_offers(app_id: int, db: Session = Depends(get_db)):
    rec = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Application not found.")

    offers = (
        db.query(LoanOffer)
        .filter(LoanOffer.application_id == app_id, LoanOffer.status == "PENDING")
        .order_by(LoanOffer.rank)
        .all()
    )

    if not offers:
        return OfferComparisonResponse(
            total_offers=0, offers=[], best_rate_offer_id=None,
            best_match_offer_id=None, best_amount_offer_id=None,
            comparison_notes="No active offers available for comparison.",
        )

    best_rate = min(offers, key=lambda x: x.interest_rate)
    best_match = max(offers, key=lambda x: x.match_score)
    best_amount = max(offers, key=lambda x: x.offered_amount)

    notes = (
        f"Comparison Engine: {best_match.lender_name} scores highest match ({best_match.match_score}/100). "
        f"{best_rate.lender_name} offers the lowest APR ({best_rate.interest_rate}%). "
        f"All {len(offers)} offers ranked by match score."
    )

    return OfferComparisonResponse(
        total_offers=len(offers),
        offers=offers,
        best_rate_offer_id=best_rate.id,
        best_match_offer_id=best_match.id,
        best_amount_offer_id=best_amount.id,
        comparison_notes=notes,
    )


@app.post(
    "/ocen/offers/accept",
    response_model=LoanApplicationResponse,
    summary="Accept Loan Offer",
    tags=["Marketplace"],
)
async def accept_offer(payload: LoanAcceptRequest, db: Session = Depends(get_db)):
    offer = db.query(LoanOffer).filter(LoanOffer.id == payload.offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found.")
    if offer.status != "PENDING":
        raise HTTPException(status_code=400, detail=f"Offer status is '{offer.status}', cannot accept.")

    application = db.query(LoanApplication).filter(
        LoanApplication.id == offer.application_id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Associated application not found.")

    offer.status = "ACCEPTED"
    application.status = "ACCEPTED"
    application.selected_offer_id = offer.id

    # Expire other pending offers
    for other in db.query(LoanOffer).filter(
        LoanOffer.application_id == application.id,
        LoanOffer.id != offer.id,
        LoanOffer.status == "PENDING",
    ).all():
        other.status = "EXPIRED"

    db.commit()
    db.refresh(application)

    _publish_event("Offer Accepted", application.customer_id, {
        "application_id": application.id,
        "offer_id": offer.id,
        "lender": offer.lender_name,
        "amount": offer.offered_amount,
        "rate": offer.interest_rate,
    })
    _publish_event("Marketplace Completed", application.customer_id, {
        "application_id": application.id, "result": "ACCEPTED",
    })
    _log_audit(db, "OFFER_ACCEPTED", str(application.customer_id),
               f"Offer {offer.id} ({offer.lender_name}) accepted for app {application.id}",
               correlation_id=application.uli_reference)

    return application


@app.post(
    "/ocen/offers/reject",
    response_model=LoanOfferResponse,
    summary="Reject Loan Offer",
    tags=["Marketplace"],
)
async def reject_offer(payload: LoanRejectRequest, db: Session = Depends(get_db)):
    offer = db.query(LoanOffer).filter(LoanOffer.id == payload.offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found.")

    offer.status = "REJECTED"
    offer.rejection_reason = payload.rejection_reason
    db.commit()
    db.refresh(offer)

    application = db.query(LoanApplication).filter(
        LoanApplication.id == offer.application_id
    ).first()

    _publish_event("Offer Rejected", application.customer_id if application else 0, {
        "offer_id": offer.id, "reason": payload.rejection_reason,
    })
    _log_audit(db, "OFFER_REJECTED", "CUSTOMER",
               f"Offer {offer.id} rejected: {payload.rejection_reason}")
    return offer


@app.get(
    "/ocen/marketplace/status/{app_id}",
    summary="Retrieve Marketplace Status",
    tags=["Marketplace"],
)
async def marketplace_status(app_id: int, db: Session = Depends(get_db)):
    application = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    offers = db.query(LoanOffer).filter(LoanOffer.application_id == app_id).all()
    match_record = db.query(MarketplaceMatch).filter(
        MarketplaceMatch.application_id == app_id
    ).first()

    return {
        "application_id": app_id,
        "uli_reference": application.uli_reference,
        "status": application.status,
        "total_offers": len(offers),
        "pending_offers": sum(1 for o in offers if o.status == "PENDING"),
        "accepted_offer_id": application.selected_offer_id,
        "lenders_screened": match_record.lenders_screened if match_record else 0,
        "lenders_matched": match_record.lenders_matched if match_record else 0,
        "best_match_score": match_record.best_match_score if match_record else None,
        "best_rate": match_record.best_rate if match_record else None,
    }


# ===========================================================================
#  6. AI ADVISOR / RECOMMENDATION
# ===========================================================================

@app.get(
    "/ocen/ai-advisor/{app_id}",
    response_model=AIRecommendationResponse,
    summary="AI Loan Recommendation",
    tags=["Marketplace"],
)
async def ai_advisor(app_id: int, db: Session = Depends(get_db)):
    application = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    offers = (
        db.query(LoanOffer)
        .filter(LoanOffer.application_id == app_id, LoanOffer.status == "PENDING")
        .order_by(LoanOffer.rank)
        .all()
    )

    if not offers:
        return AIRecommendationResponse(
            suitability_score=0.0,
            dynamic_summary="No active offers available for AI analysis.",
            recommended_offer_id=None,
            breakdown="Submit a loan application first to receive AI-driven recommendations.",
        )

    best = offers[0]
    suitability = round(best.match_score * best.approval_probability, 1)

    exp = {}
    if best.match_explanation:
        try:
            exp = json.loads(best.match_explanation)
        except Exception:
            pass

    summary = (
        f"AAROHAN AI recommends {best.lender_name} as the optimal lender match "
        f"(Match Score: {best.match_score}/100, Approval Probability: {best.approval_probability*100:.0f}%). "
        f"Offer: ₹{best.offered_amount:,.0f} at {best.interest_rate}% p.a. | "
        f"EMI: ₹{best.monthly_installment:,.2f}/month | TAT: {best.expected_disbursal_days} day(s)."
    )
    breakdown = (
        f"Matching Analysis:\n"
        f"  • Lender selected: {exp.get('why_selected', best.lender_name)}\n"
        f"  • Customer qualifies: {exp.get('why_customer_qualifies', 'Profile meets policy criteria.')}\n"
        f"  • Key strengths: {'; '.join(exp.get('key_strengths', []))}\n"
        f"  • Constraints: {'; '.join(exp.get('key_constraints', ['None']))}\n"
        f"  • Next steps: {'; '.join(exp.get('suggested_next_steps', ['Accept offer on lender portal']))}"
    )

    return AIRecommendationResponse(
        suitability_score=suitability,
        dynamic_summary=summary,
        recommended_offer_id=best.id,
        breakdown=breakdown,
    )


# ===========================================================================
#  7. MARKETPLACE DASHBOARD
# ===========================================================================

@app.get(
    "/ocen/dashboard",
    response_model=MarketplaceDashboardResponse,
    summary="Marketplace Dashboard",
    tags=["Dashboard"],
)
async def marketplace_dashboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    all_apps = db.query(LoanApplication).all()
    all_offers = db.query(LoanOffer).all()
    active_lenders = db.query(Lender).filter(Lender.is_active == True).count()

    offers_accepted = sum(1 for o in all_offers if o.status == "ACCEPTED")
    offers_rejected = sum(1 for o in all_offers if o.status == "REJECTED")

    scores = [o.match_score for o in all_offers if o.match_score > 0]
    rates = [o.interest_rate for o in all_offers if o.interest_rate > 0]

    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0
    avg_rate = round(sum(rates) / len(rates), 2) if rates else 0.0

    # Top lender by accepted offers
    accepted_by_lender: Dict[str, int] = {}
    for o in all_offers:
        if o.status == "ACCEPTED":
            accepted_by_lender[o.lender_name] = accepted_by_lender.get(o.lender_name, 0) + 1
    top_lender = max(accepted_by_lender, key=accepted_by_lender.get) if accepted_by_lender else None

    recent = sorted(all_apps, key=lambda a: a.created_at, reverse=True)[:limit]

    return MarketplaceDashboardResponse(
        total_applications=len(all_apps),
        offers_generated=len(all_offers),
        offers_accepted=offers_accepted,
        offers_rejected=offers_rejected,
        active_lenders=active_lenders,
        avg_match_score=avg_score,
        avg_interest_rate=avg_rate,
        top_lender=top_lender,
        recent_applications=recent,
    )


# ===========================================================================
#  8. ELIGIBILITY CHECK (ULI standalone)
# ===========================================================================

@app.post(
    "/ocen/eligibility",
    response_model=EligibilityCheckResponse,
    summary="Pre-check Eligibility",
    tags=["Marketplace"],
)
async def check_eligibility(
    payload: EligibilityCheckRequest, db: Session = Depends(get_db)
):
    max_eligible = payload.annual_revenue * 0.30
    uli_ref = f"ULI-{uuid.uuid4().hex[:8].upper()}"

    eligible = True
    reasons = []

    min_fhc = DEFAULT_MATCH_PARAMS["min_fhc_for_approval"]
    if payload.fhc_score is not None and payload.fhc_score < min_fhc:
        eligible = False
        reasons.append(f"FHC score {payload.fhc_score:.1f} below minimum {min_fhc}.")
    if payload.credit_score < 600:
        eligible = False
        reasons.append(f"Credit score {payload.credit_score} below minimum 600.")
    if payload.requested_amount > max_eligible:
        eligible = False
        reasons.append(
            f"Requested ₹{payload.requested_amount:,.0f} exceeds revenue-based ceiling "
            f"₹{max_eligible:,.0f}."
        )
    if payload.fraud_risk_level and payload.fraud_risk_level == "Critical":
        eligible = False
        reasons.append("Fraud risk level is Critical – marketplace blocked.")

    reason_str = " | ".join(reasons) if reasons else (
        "All eligibility criteria satisfied. Consented ULI checks cleared."
    )

    _log_audit(db, "ELIGIBILITY_CHECKED", str(payload.customer_id),
               f"Eligible={eligible} | ULI={uli_ref}")

    return EligibilityCheckResponse(
        eligible=eligible,
        reason=reason_str,
        max_eligible_amount=max_eligible,
        uli_reference=uli_ref,
    )


# ===========================================================================
#  9. LOAN DISBURSEMENT
# ===========================================================================

@app.post(
    "/ocen/disburse/{app_id}",
    response_model=LoanApplicationResponse,
    summary="Disburse Accepted Loan",
    tags=["Marketplace"],
)
async def disburse_loan(app_id: int, db: Session = Depends(get_db)):
    rec = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Application not found.")
    if rec.status != "ACCEPTED":
        raise HTTPException(status_code=400, detail="Application must be ACCEPTED to disburse.")
    rec.status = "DISBURSED"
    db.commit()
    db.refresh(rec)
    _publish_event("Marketplace Completed", rec.customer_id, {
        "application_id": app_id, "result": "DISBURSED",
    })
    _log_audit(db, "LOAN_DISBURSED", "SYSTEM",
               f"Loan disbursed for application {app_id}", correlation_id=rec.uli_reference)
    return rec


# ===========================================================================
#  10. ADMINISTRATION
# ===========================================================================

@app.get("/ocen/config", summary="Get Marketplace Config", tags=["Administration"])
async def get_config(db: Session = Depends(get_db)):
    adapter, params = _get_active_config(db)
    return {"active_adapter": adapter, "match_params": params}


@app.post("/ocen/config", summary="Update Marketplace Config", tags=["Administration"])
async def update_config(payload: ConfigUpdateRequest, db: Session = Depends(get_db)):
    cfg = db.query(MarketplaceConfig).first()
    if not cfg:
        cfg = MarketplaceConfig()
        db.add(cfg)
    cfg.active_adapter = payload.active_adapter.upper()
    cfg.match_params = json.dumps(payload.match_params)
    db.commit()
    _log_audit(db, "CONFIG_UPDATED", "ADMIN",
               f"Marketplace config updated. Adapter: {cfg.active_adapter}")
    return {"message": "Marketplace configuration updated."}


@app.post(
    "/ocen/admin/replay",
    response_model=LoanApplicationResponse,
    summary="Replay Matching Process",
    tags=["Administration"],
)
async def replay_matching(
    payload: MarketplaceReplayRequest, db: Session = Depends(get_db)
):
    """Re-run offer generation for an existing application."""
    application = db.query(LoanApplication).filter(
        LoanApplication.id == payload.application_id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    # Expire existing pending offers
    for offer in db.query(LoanOffer).filter(
        LoanOffer.application_id == application.id,
        LoanOffer.status == "PENDING",
    ).all():
        offer.status = "EXPIRED"
    db.commit()

    adapter_name, match_params = _get_active_config(db)
    adapter = _get_adapter(adapter_name)
    lenders = _active_lenders(db)
    offers_data = adapter.generate_offers(application, lenders, match_params)

    for offer_data in offers_data:
        db.add(LoanOffer(
            application_id=application.id,
            lender_id=offer_data["lender_id"],
            lender_name=offer_data["lender_name"],
            lender_type=offer_data.get("lender_type", "BANK"),
            product_type=offer_data.get("product_type", application.product_type),
            offered_amount=offer_data["offered_amount"],
            interest_rate=offer_data["interest_rate"],
            tenure_months=offer_data["tenure_months"],
            processing_fee=offer_data["processing_fee"],
            monthly_installment=offer_data["monthly_installment"],
            total_interest=offer_data.get("total_interest", 0.0),
            approval_probability=offer_data.get("approval_probability", 0.75),
            expected_disbursal_days=offer_data.get("expected_disbursal_days", 3),
            match_score=offer_data["match_score"],
            rank=offer_data["rank"],
            conditions=offer_data.get("conditions", ""),
            match_explanation=offer_data.get("match_explanation", "{}"),
            status="PENDING",
        ))

    application.status = "OFFERS_GENERATED"
    db.commit()
    db.refresh(application)
    _log_audit(db, "MARKETPLACE_REPLAYED", "ADMIN",
               f"Replay completed for application {application.id}: {len(offers_data)} offers")
    return application


@app.get(
    "/ocen/admin/export/{app_id}",
    summary="Export Marketplace Result",
    tags=["Administration"],
)
async def export_marketplace_result(
    app_id: int,
    format: str = Query("json", description="json | pdf"),
    db: Session = Depends(get_db),
):
    application = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    offers = (
        db.query(LoanOffer)
        .filter(LoanOffer.application_id == app_id)
        .order_by(LoanOffer.rank)
        .all()
    )

    if format.lower() == "json":
        return {
            "application": {
                "id": application.id,
                "customer_id": application.customer_id,
                "uli_reference": application.uli_reference,
                "requested_amount": application.requested_amount,
                "product_type": application.product_type,
                "status": application.status,
                "fhc_score": application.fhc_score,
                "credit_decision": application.credit_decision,
                "fraud_risk_level": application.fraud_risk_level,
            },
            "offers": [
                {
                    "rank": o.rank, "lender": o.lender_name, "rate": o.interest_rate,
                    "emi": o.monthly_installment, "match_score": o.match_score,
                    "status": o.status,
                }
                for o in offers
            ],
        }

    if format.lower() == "pdf":
        title = "OCEN MARKETPLACE LOAN OFFER REPORT"
        lines = [
            "%PDF-1.4",
            f"1 0 obj\n<< /Title ({title}) /Author (Project AAROHAN) >>\nendobj",
            "2 0 obj\n<< /Type /Catalog /Pages 3 0 R >>\nendobj",
            "3 0 obj\n<< /Type /Pages /Kids [4 0 R] /Count 1 >>\nendobj",
            "4 0 obj\n<< /Type /Page /Parent 3 0 R /MediaBox [0 0 595 842] /Contents 5 0 R >>\nendobj",
            "5 0 obj\n<< /Length 800 >>\nstream",
            f"BT /F1 16 Tf 50 750 Td ({title}) Tj ET",
            f"BT /F1 10 Tf 50 710 Td (Application ID: {application.id}) Tj ET",
            f"BT /F1 10 Tf 50 690 Td (ULI Reference: {application.uli_reference}) Tj ET",
            f"BT /F1 10 Tf 50 670 Td (Product: {application.product_type}) Tj ET",
            f"BT /F1 10 Tf 50 650 Td (Requested Amount: Rs {application.requested_amount:,.0f}) Tj ET",
            f"BT /F1 10 Tf 50 630 Td (Status: {application.status}) Tj ET",
            f"BT /F1 10 Tf 50 610 Td (FHC Score: {application.fhc_score}) Tj ET",
            f"BT /F1 10 Tf 50 590 Td (Credit Decision: {application.credit_decision}) Tj ET",
            f"BT /F1 10 Tf 50 570 Td (Total Offers: {len(offers)}) Tj ET",
        ]
        for i, o in enumerate(offers[:5]):
            y = 540 - i * 20
            lines.append(
                f"BT /F1 9 Tf 50 {y} Td "
                f"(#{o.rank} {o.lender_name} | Rate: {o.interest_rate}% | EMI: Rs {o.monthly_installment:,.0f} | Score: {o.match_score}) Tj ET"
            )
        lines += [
            "BT /F1 8 Tf 50 100 Td (*Generated by AAROHAN OCEN Marketplace – Project AAROHAN*) Tj ET",
            "endstream\nendobj",
            "xref\n0 6\n0000000000 65535 f",
            "trailer\n<< /Size 6 /Root 2 0 R >>\nstartxref\n%%EOF",
        ]
        return Response(
            content="\n".join(lines).encode("utf-8"),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=ocen_offers_{app_id}.pdf"},
        )

    raise HTTPException(status_code=400, detail="Unsupported format. Use 'json' or 'pdf'.")


# ===========================================================================
#  11. WORKFLOW INTEGRATION – CAM / Executive Dashboard outputs
# ===========================================================================

@app.get(
    "/ocen/cam-summary/{app_id}",
    summary="CAM Generator Summary",
    tags=["Workflow Integration"],
)
async def cam_summary(app_id: int, db: Session = Depends(get_db)):
    application = db.query(LoanApplication).filter(LoanApplication.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    selected_offer = None
    if application.selected_offer_id:
        selected_offer = db.query(LoanOffer).filter(
            LoanOffer.id == application.selected_offer_id
        ).first()

    return {
        "application_id": app_id,
        "uli_reference": application.uli_reference,
        "status": application.status,
        "requested_amount": application.requested_amount,
        "product_type": application.product_type,
        "fhc_score": application.fhc_score,
        "credit_decision": application.credit_decision,
        "fraud_risk_level": application.fraud_risk_level,
        "selected_lender": selected_offer.lender_name if selected_offer else None,
        "approved_amount": selected_offer.offered_amount if selected_offer else None,
        "approved_rate": selected_offer.interest_rate if selected_offer else None,
        "monthly_installment": selected_offer.monthly_installment if selected_offer else None,
        "tenure_months": selected_offer.tenure_months if selected_offer else None,
        "match_score": selected_offer.match_score if selected_offer else None,
    }


@app.get(
    "/ocen/executive-summary",
    summary="Executive Dashboard Summary",
    tags=["Workflow Integration"],
)
async def executive_summary(db: Session = Depends(get_db)):
    all_apps = db.query(LoanApplication).all()
    all_offers = db.query(LoanOffer).all()
    return {
        "total_applications": len(all_apps),
        "disbursed": sum(1 for a in all_apps if a.status == "DISBURSED"),
        "accepted": sum(1 for a in all_apps if a.status == "ACCEPTED"),
        "offers_generated": len(all_offers),
        "avg_interest_rate": round(
            sum(o.interest_rate for o in all_offers) / len(all_offers), 2
        ) if all_offers else 0.0,
        "total_loan_value": sum(
            o.offered_amount for o in all_offers if o.status == "ACCEPTED"
        ),
    }


# ===========================================================================
#  12. AUDIT LOGS
# ===========================================================================

@app.get("/ocen/audit-logs", summary="Audit Logs", tags=["Administration"])
async def get_audit_logs(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": l.id,
            "correlation_id": l.correlation_id,
            "event_type": l.event_type,
            "actor": l.actor,
            "message": l.message,
            "details": l.details,
            "timestamp": l.timestamp.isoformat(),
        }
        for l in logs
    ]


# ===========================================================================
#  13. HEALTH
# ===========================================================================

@app.get("/healthz", summary="Liveness Probe", tags=["Health"])
async def healthz():
    return {"status": "healthy", "service": "ocen-uli-service", "version": "2.0.0"}


@app.get("/readyz", summary="Readiness Probe", tags=["Health"])
async def readyz(db: Session = Depends(get_db)):
    try:
        db.query(Lender).first()
        return {"status": "READY"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB not ready: {exc}")
