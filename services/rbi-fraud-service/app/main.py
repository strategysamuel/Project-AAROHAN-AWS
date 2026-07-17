"""
AAROHAN – RBI Central Fraud Registry Simulation Service
========================================================
Implements:
  • Fraud screening APIs (Customer / Business / PAN / GSTIN / Directors / Accounts)
  • Full fraud assessment with AML risk scoring
  • Fraud Dashboard (summary + investigation queue)
  • Fraud Timeline per customer
  • Watchlist management (list / add / delete)
  • Admin: re-run, override, config, import watchlist, export report
  • Business Event publishing (Fraud Screening Started → Cleared / Alert)
  • Adapter switching at runtime (SIMULATION / SANDBOX / PRODUCTION)
  • Workflow integration hooks (outputs for OCEN Marketplace, CAM Generator)
"""
import logging
import sys
import os
import time
import uuid
import datetime
import json
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Request, Depends, status, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

# ── Bootstrap path so ese-core / event_engine can be imported ──────────────
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
ese_core_path = os.path.join(WORKSPACE_ROOT, "services", "ese-core")
if ese_core_path not in sys.path:
    sys.path.insert(0, ese_core_path)

from app.models import (
    RBIFraudRecord, FraudWatchlist, FraudServiceConfig, Base,
    OnboardingCustomer, OnboardingBusiness, CKYCVerificationLog,
    AAAnalytics, MCAGovernanceAnalytics,
)
from app.schemas import (
    RBIFraudRecordResponse, FraudWatchlistResponse, WatchlistItemRequest,
    VerifyRequest, OverrideRequest, ConfigUpdateRequest,
    FraudDashboardResponse, FraudDashboardEntry, FraudAssessmentResponse,
)
from app.database import get_db, init_db
from app.adapters import (
    SimulationAdapter, SandboxAdapter, ProductionAdapter,
    DEFAULT_RULE_PARAMS,
)

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format=(
        '{"timestamp": "%(asctime)s", "severity": "%(levelname)s", '
        '"message": "%(message)s", "service": "rbi-fraud-service"}'
    ),
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("rbi-fraud-service")

# ── DB bootstrap ─────────────────────────────────────────────────────────────
init_db()

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="AAROHAN RBI Central Fraud Registry Screening Service",
    description=(
        "Consented fraud watchlist lookups, AML indicators, risk scoring, "
        "explainable AI insights, and human override controls."
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

# ── Middleware: correlation ID + audit log ────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    logger.info(
        f"AUDIT | Request: {request.method} {request.url.path} | Correlation-ID: {correlation_id}"
    )
    response = await call_next(request)
    elapsed = time.time() - start_time
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    response.headers["X-Correlation-ID"] = correlation_id
    logger.info(
        f"AUDIT | Completed: {request.method} {request.url.path} "
        f"| Status: {response.status_code} | Time: {elapsed:.4f}s"
    )
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
            "details": [],
        },
    )


# ── Configuration helpers ────────────────────────────────────────────────────

def get_active_config(db: Session):
    cfg = db.query(FraudServiceConfig).first()
    if not cfg:
        cfg = FraudServiceConfig(
            active_adapter="SIMULATION",
            rule_parameters=json.dumps(DEFAULT_RULE_PARAMS),
        )
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg.active_adapter, json.loads(cfg.rule_parameters)


def get_adapter_instance(adapter_name: str):
    if adapter_name == "SANDBOX":
        return SandboxAdapter()
    if adapter_name == "PRODUCTION":
        return ProductionAdapter()
    return SimulationAdapter()


# ── Business Event publisher ─────────────────────────────────────────────────

def publish_fraud_event(event_type: str, customer_id: int, payload: dict):
    logger.info(
        f"AUDIT | EVENT_BUS | Published: {event_type} | Customer: {customer_id}"
    )
    try:
        from event_engine import BusinessEventEngine
        engine = BusinessEventEngine()
        engine.dispatch(event_type, f"cust_{customer_id}", payload)
    except Exception as exc:
        logger.warning(f"Event bus unavailable ({event_type}): {exc}")


# ── Core verify helper ───────────────────────────────────────────────────────

def _run_verification(
    customer_id: int,
    entity_type: str,
    entity_value: str,
    db: Session,
) -> RBIFraudRecord:
    """Run adapter verification and persist the result."""
    publish_fraud_event(
        "Fraud Screening Started",
        customer_id,
        {"entity_type": entity_type, "entity_value": entity_value},
    )

    adapter_name, rule_params = get_active_config(db)
    adapter = get_adapter_instance(adapter_name)
    results = adapter.verify(entity_type, entity_value, customer_id, db, rule_params)

    record = RBIFraudRecord(
        customer_id=customer_id,
        entity_type=entity_type.upper(),
        entity_value=entity_value,
        is_blacklisted=results["is_blacklisted"],
        fraud_score=results["fraud_score"],
        fraud_category=results["fraud_category"],
        risk_level=results["risk_level"],
        risk_flags=results["risk_flags"],
        ai_insights=results["ai_insights"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    publish_fraud_event(
        "Fraud Screening Completed",
        customer_id,
        {"record_id": record.id},
    )
    publish_fraud_event(
        "Fraud Risk Updated",
        customer_id,
        {"fraud_score": record.fraud_score, "risk_level": record.risk_level},
    )

    if record.is_blacklisted or record.risk_level in ("High", "Critical"):
        publish_fraud_event(
            "Fraud Alert Raised",
            customer_id,
            {"record_id": record.id, "reason": record.ai_insights},
        )
        if record.risk_level == "High":
            publish_fraud_event(
                "Manual Investigation Required",
                customer_id,
                {"record_id": record.id},
            )
    else:
        publish_fraud_event(
            "Customer Cleared",
            customer_id,
            {"record_id": record.id},
        )

    return record


# ===========================================================================
#  FRAUD SCREENING APIs
# ===========================================================================

@app.post(
    "/rbi/verify/customer",
    response_model=RBIFraudRecordResponse,
    summary="Verify Customer – General Entity Lookup",
    tags=["Fraud Screening"],
)
async def verify_customer(payload: VerifyRequest, db: Session = Depends(get_db)):
    """
    Generic fraud screening entry point.  entity_type should be one of:
    CUSTOMER, BUSINESS, PAN, GSTIN, DIRECTOR, ACCOUNT, DOCUMENT.
    """
    logger.info(
        f"AUDIT | verify_customer | cid={payload.customer_id} | type={payload.entity_type}"
    )
    return _run_verification(
        payload.customer_id, payload.entity_type.upper(), payload.entity_value, db
    )


@app.post(
    "/rbi/verify/customer/{customer_id}",
    response_model=RBIFraudRecordResponse,
    summary="Verify Customer by ID",
    tags=["Fraud Screening"],
)
async def verify_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    cust = db.query(OnboardingCustomer).filter(OnboardingCustomer.id == customer_id).first()
    pan = cust.pan if cust else "UNKNOWN_PAN"
    return _run_verification(customer_id, "PAN", pan, db)


@app.post(
    "/rbi/verify/business",
    response_model=RBIFraudRecordResponse,
    summary="Verify Business",
    tags=["Fraud Screening"],
)
async def verify_business(payload: VerifyRequest, db: Session = Depends(get_db)):
    """Verify a business entity (GSTIN-level screening)."""
    return _run_verification(payload.customer_id, "BUSINESS", payload.entity_value, db)


@app.post(
    "/rbi/verify/pan",
    response_model=RBIFraudRecordResponse,
    summary="Verify PAN",
    tags=["Fraud Screening"],
)
async def verify_pan(payload: VerifyRequest, db: Session = Depends(get_db)):
    return _run_verification(payload.customer_id, "PAN", payload.entity_value, db)


@app.post(
    "/rbi/verify/gstin",
    response_model=RBIFraudRecordResponse,
    summary="Verify GSTIN",
    tags=["Fraud Screening"],
)
async def verify_gstin(payload: VerifyRequest, db: Session = Depends(get_db)):
    return _run_verification(payload.customer_id, "GSTIN", payload.entity_value, db)


@app.post(
    "/rbi/verify/directors",
    response_model=RBIFraudRecordResponse,
    summary="Verify Directors",
    tags=["Fraud Screening"],
)
async def verify_directors(payload: VerifyRequest, db: Session = Depends(get_db)):
    return _run_verification(payload.customer_id, "DIRECTOR", payload.entity_value, db)


@app.post(
    "/rbi/verify/accounts",
    response_model=RBIFraudRecordResponse,
    summary="Verify Accounts",
    tags=["Fraud Screening"],
)
async def verify_accounts(payload: VerifyRequest, db: Session = Depends(get_db)):
    return _run_verification(payload.customer_id, "ACCOUNT", payload.entity_value, db)


# ===========================================================================
#  FRAUD HISTORY & ASSESSMENT
# ===========================================================================

@app.get(
    "/rbi/history/{customer_id}",
    response_model=List[RBIFraudRecordResponse],
    summary="Retrieve Fraud History",
    tags=["Fraud Intelligence"],
)
async def retrieve_fraud_history(customer_id: int, db: Session = Depends(get_db)):
    """Return all fraud screening records for a customer, newest first."""
    return (
        db.query(RBIFraudRecord)
        .filter(RBIFraudRecord.customer_id == customer_id)
        .order_by(RBIFraudRecord.created_at.desc())
        .all()
    )


@app.post(
    "/rbi/assessment/{customer_id}",
    response_model=FraudAssessmentResponse,
    summary="Generate Full Fraud Assessment",
    tags=["Fraud Intelligence"],
)
async def generate_fraud_assessment(customer_id: int, db: Session = Depends(get_db)):
    """
    Run fresh PAN screening then aggregate all historical records into a
    consolidated fraud assessment with AML status and a single recommendation.
    """
    # Run fresh PAN verification
    cust = db.query(OnboardingCustomer).filter(OnboardingCustomer.id == customer_id).first()
    pan = cust.pan if cust else "UNKNOWN_PAN"
    _run_verification(customer_id, "PAN", pan, db)

    # Also verify linked business GSTIN if available
    biz = db.query(OnboardingBusiness).filter(OnboardingBusiness.customer_id == customer_id).first()
    if biz and biz.gstin:
        _run_verification(customer_id, "GSTIN", biz.gstin, db)

    # Aggregate all records
    records = (
        db.query(RBIFraudRecord)
        .filter(RBIFraudRecord.customer_id == customer_id)
        .order_by(RBIFraudRecord.created_at.desc())
        .all()
    )

    if not records:
        raise HTTPException(status_code=404, detail="No fraud records found for customer.")

    overall_score = max(r.fraud_score for r in records)
    categories = list({r.fraud_category for r in records if r.fraud_category != "None"})
    flags_raw = ",".join(r.risk_flags for r in records if r.risk_flags != "CLEAN")
    all_flags = list({f for f in flags_raw.split(",") if f})
    observations = [r.ai_insights for r in records if r.ai_insights]

    from app.adapters import _score_to_risk, _aml_assessment
    risk_level = _score_to_risk(overall_score)
    aml_status = _aml_assessment(overall_score, all_flags, {})

    if overall_score >= 75.0:
        recommendation = (
            "REJECT – High fraud risk detected. Stop workflow. Raise manual investigation."
        )
    elif overall_score >= 55.0:
        recommendation = (
            "MANUAL REVIEW – Elevated fraud risk. Flag for compliance officer review "
            "before proceeding to OCEN Marketplace."
        )
    elif overall_score >= 30.0:
        recommendation = (
            "CONDITIONAL PROCEED – Medium risk. Apply additional monitoring conditions "
            "before OCEN Marketplace routing."
        )
    else:
        recommendation = (
            "PROCEED – No material fraud risk. Customer cleared for OCEN Marketplace integration."
        )

    return FraudAssessmentResponse(
        customer_id=customer_id,
        overall_risk_level=risk_level,
        overall_fraud_score=round(overall_score, 2),
        aml_status=aml_status,
        fraud_categories_detected=categories,
        all_risk_flags=all_flags,
        ai_observations=observations,
        screening_records=[RBIFraudRecordResponse.model_validate(r) for r in records],
        recommendation=recommendation,
    )


# ===========================================================================
#  FRAUD DASHBOARD
# ===========================================================================

@app.get(
    "/rbi/dashboard",
    response_model=FraudDashboardResponse,
    summary="Fraud Dashboard",
    tags=["Dashboard"],
)
async def fraud_dashboard(
    limit: int = Query(20, ge=1, le=200, description="Max alerts to return"),
    db: Session = Depends(get_db),
):
    """
    Aggregated fraud dashboard showing screening counts by risk tier,
    recent alerts, and the investigation queue.
    """
    all_records = db.query(RBIFraudRecord).all()

    cleared = sum(1 for r in all_records if not r.is_blacklisted and r.risk_level == "Low")
    low = sum(1 for r in all_records if r.risk_level == "Low")
    medium = sum(1 for r in all_records if r.risk_level == "Medium")
    high = sum(1 for r in all_records if r.risk_level == "High")
    critical = sum(1 for r in all_records if r.risk_level == "Critical")
    blacklisted = sum(1 for r in all_records if r.is_blacklisted)
    overridden = sum(1 for r in all_records if r.is_overridden)

    # Investigation queue: High or Critical, not yet overridden
    investigation_q = [
        r for r in all_records
        if r.risk_level in ("High", "Critical") and not r.is_overridden
    ]
    pending = len(investigation_q)

    # Recent alerts: any non-Low record
    recent_alerts_raw = sorted(
        [r for r in all_records if r.risk_level != "Low"],
        key=lambda r: r.created_at,
        reverse=True,
    )[:limit]

    def _to_entry(r):
        return FraudDashboardEntry(
            id=r.id,
            customer_id=r.customer_id,
            entity_type=r.entity_type,
            entity_value=r.entity_value,
            fraud_score=r.fraud_score,
            risk_level=r.risk_level,
            fraud_category=r.fraud_category,
            is_blacklisted=r.is_blacklisted,
            is_overridden=r.is_overridden,
            risk_flags=r.risk_flags,
            ai_insights=r.ai_insights,
            created_at=r.created_at,
        )

    return FraudDashboardResponse(
        total_screened=len(all_records),
        cleared=cleared,
        low_risk=low,
        medium_risk=medium,
        high_risk=high,
        critical_risk=critical,
        blacklisted=blacklisted,
        overridden=overridden,
        pending_investigation=pending,
        recent_alerts=[_to_entry(r) for r in recent_alerts_raw],
        investigation_queue=[_to_entry(r) for r in investigation_q[:limit]],
    )


@app.get(
    "/rbi/dashboard/timeline/{customer_id}",
    response_model=List[FraudDashboardEntry],
    summary="Fraud Timeline for Customer",
    tags=["Dashboard"],
)
async def fraud_timeline(customer_id: int, db: Session = Depends(get_db)):
    """Chronological fraud-event timeline for a single customer."""
    records = (
        db.query(RBIFraudRecord)
        .filter(RBIFraudRecord.customer_id == customer_id)
        .order_by(RBIFraudRecord.created_at.asc())
        .all()
    )
    return [
        FraudDashboardEntry(
            id=r.id, customer_id=r.customer_id, entity_type=r.entity_type,
            entity_value=r.entity_value, fraud_score=r.fraud_score,
            risk_level=r.risk_level, fraud_category=r.fraud_category,
            is_blacklisted=r.is_blacklisted, is_overridden=r.is_overridden,
            risk_flags=r.risk_flags, ai_insights=r.ai_insights,
            created_at=r.created_at,
        )
        for r in records
    ]


# ===========================================================================
#  WATCHLIST MANAGEMENT
# ===========================================================================

@app.get(
    "/rbi/watchlist",
    response_model=List[FraudWatchlistResponse],
    summary="List Watchlist",
    tags=["Administration"],
)
async def list_watchlist(
    watchlist_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(FraudWatchlist)
    if watchlist_type:
        q = q.filter(FraudWatchlist.watchlist_type == watchlist_type.upper())
    return q.order_by(FraudWatchlist.flagged_at.desc()).all()


@app.post(
    "/rbi/watchlist",
    response_model=FraudWatchlistResponse,
    summary="Add to Watchlist",
    tags=["Administration"],
)
async def add_to_watchlist(payload: WatchlistItemRequest, db: Session = Depends(get_db)):
    existing = (
        db.query(FraudWatchlist).filter(FraudWatchlist.value == payload.value).first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Value already exists in watchlist.")
    entry = FraudWatchlist(
        watchlist_type=payload.watchlist_type.upper(),
        value=payload.value,
        reason=payload.reason,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    logger.info(f"AUDIT | WATCHLIST | Added {payload.watchlist_type}: {payload.value}")
    return entry


@app.delete(
    "/rbi/watchlist/{watchlist_id}",
    summary="Remove from Watchlist",
    tags=["Administration"],
)
async def remove_from_watchlist(watchlist_id: int, db: Session = Depends(get_db)):
    entry = db.query(FraudWatchlist).filter(FraudWatchlist.id == watchlist_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Watchlist entry not found.")
    db.delete(entry)
    db.commit()
    logger.info(f"AUDIT | WATCHLIST | Removed entry id={watchlist_id}")
    return {"message": f"Watchlist entry {watchlist_id} removed."}


@app.post(
    "/rbi/watchlist/import",
    summary="Bulk Import Watchlist",
    tags=["Administration"],
)
async def import_watchlist(
    items: List[WatchlistItemRequest] = Body(...),
    db: Session = Depends(get_db),
):
    """Bulk-import watchlist entries.  Skips duplicates silently."""
    from sqlalchemy.exc import IntegrityError

    imported = 0
    skipped = 0
    for item in items:
        # Check in-memory first (covers seeded + already-committed rows)
        existing = db.query(FraudWatchlist).filter(FraudWatchlist.value == item.value).first()
        if existing:
            skipped += 1
            continue
        try:
            entry = FraudWatchlist(
                watchlist_type=item.watchlist_type.upper(),
                value=item.value,
                reason=item.reason,
            )
            db.add(entry)
            db.flush()   # flush per-item so IntegrityError is per-row
            imported += 1
        except IntegrityError:
            db.rollback()
            skipped += 1
    db.commit()
    logger.info(f"AUDIT | WATCHLIST | Bulk import: {imported} added, {skipped} skipped.")
    return {"imported": imported, "skipped": skipped}


# ===========================================================================
#  ADMINISTRATION – Override / Re-run / Config / Export
# ===========================================================================

@app.post(
    "/rbi/override/{customer_id}",
    response_model=RBIFraudRecordResponse,
    summary="Override Fraud Decision (with Audit)",
    tags=["Administration"],
)
async def override_fraud_decision(
    customer_id: int, payload: OverrideRequest, db: Session = Depends(get_db)
):
    record = (
        db.query(RBIFraudRecord)
        .filter(RBIFraudRecord.customer_id == customer_id)
        .order_by(RBIFraudRecord.created_at.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="No fraud record found for customer.")

    logger.info(
        f"AUDIT | OVERRIDE | Customer {customer_id} | by {payload.overridden_by} "
        f"| reason: {payload.override_reason}"
    )
    record.is_overridden = True
    record.is_blacklisted = False
    record.fraud_score = 10.0
    record.risk_level = "Low"
    record.override_reason = payload.override_reason
    record.overridden_by = payload.overridden_by
    record.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(record)

    publish_fraud_event(
        "Fraud Risk Updated",
        customer_id,
        {"override": True, "fraud_score": 10.0, "risk_level": "Low"},
    )
    publish_fraud_event("Customer Cleared", customer_id, {"override": True})
    return record


@app.post(
    "/rbi/rerun/{customer_id}",
    response_model=RBIFraudRecordResponse,
    summary="Re-run Fraud Check",
    tags=["Administration"],
)
async def rerun_fraud_check(customer_id: int, db: Session = Depends(get_db)):
    """Force a fresh fraud screening for a customer."""
    logger.info(f"AUDIT | RERUN | Fraud check re-run for customer {customer_id}")
    return _run_verification(customer_id, "PAN",
                             _get_pan(customer_id, db), db)


def _get_pan(customer_id: int, db: Session) -> str:
    cust = db.query(OnboardingCustomer).filter(OnboardingCustomer.id == customer_id).first()
    return cust.pan if cust else "UNKNOWN_PAN"


@app.get("/rbi/config", summary="Get Active Config", tags=["Administration"])
async def get_config(db: Session = Depends(get_db)):
    adapter, rule_params = get_active_config(db)
    return {"active_adapter": adapter, "rule_parameters": rule_params}


@app.post("/rbi/config", summary="Update Config", tags=["Administration"])
async def update_config(payload: ConfigUpdateRequest, db: Session = Depends(get_db)):
    cfg = db.query(FraudServiceConfig).first()
    if not cfg:
        cfg = FraudServiceConfig()
        db.add(cfg)
    cfg.active_adapter = payload.active_adapter.upper()
    cfg.rule_parameters = json.dumps(payload.rule_parameters)
    db.commit()
    logger.info(f"AUDIT | CONFIG | Active adapter set to {cfg.active_adapter}")
    return {"message": "RBI fraud screening configuration updated successfully."}


@app.get(
    "/rbi/export/{customer_id}",
    summary="Export Fraud Report",
    tags=["Administration"],
)
async def export_fraud_report(
    customer_id: int,
    format: str = Query("json", description="json | pdf"),
    db: Session = Depends(get_db),
):
    record = (
        db.query(RBIFraudRecord)
        .filter(RBIFraudRecord.customer_id == customer_id)
        .order_by(RBIFraudRecord.created_at.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="No fraud record found for customer.")

    if format.lower() == "json":
        return RBIFraudRecordResponse.model_validate(record)

    if format.lower() == "pdf":
        title = "RBI CENTRAL FRAUD REGISTRY WATCHLIST REPORT"
        lines = [
            "%PDF-1.4",
            f"1 0 obj\n<< /Title ({title}) /Author (Project AAROHAN) >>\nendobj",
            "2 0 obj\n<< /Type /Catalog /Pages 3 0 R >>\nendobj",
            "3 0 obj\n<< /Type /Pages /Kids [4 0 R] /Count 1 >>\nendobj",
            "4 0 obj\n<< /Type /Page /Parent 3 0 R /MediaBox [0 0 595 842] "
            "/Contents 5 0 R >>\nendobj",
            "5 0 obj\n<< /Length 500 >>\nstream",
            f"BT /F1 16 Tf 50 750 Td ({title}) Tj ET",
            f"BT /F1 10 Tf 50 700 Td (Customer ID: {customer_id}) Tj ET",
            f"BT /F1 10 Tf 50 680 Td (Screened Entity: {record.entity_type} - "
            f"{record.entity_value}) Tj ET",
            f"BT /F1 10 Tf 50 660 Td (Blacklist Match: {record.is_blacklisted}) Tj ET",
            f"BT /F1 10 Tf 50 640 Td (Fraud Risk Score: {record.fraud_score:.1f} / 100) Tj ET",
            f"BT /F1 10 Tf 50 620 Td (Fraud Risk Grade: {record.risk_level}) Tj ET",
            f"BT /F1 10 Tf 50 600 Td (Fraud Category: {record.fraud_category}) Tj ET",
            f"BT /F1 10 Tf 50 580 Td (Risk Flags: {record.risk_flags}) Tj ET",
            f"BT /F1 10 Tf 50 560 Td (AI Insights: {str(record.ai_insights)[:120]}) Tj ET",
            f"BT /F1 8 Tf 50 100 Td "
            "(*Digitally Signed – RBI CFR Simulation Gateway – Project AAROHAN*) Tj ET",
            "endstream\nendobj",
            "xref\n0 6\n0000000000 65535 f",
            "trailer\n<< /Size 6 /Root 2 0 R >>\nstartxref\n%%EOF",
        ]
        pdf_data = "\n".join(lines).encode("utf-8")
        return Response(
            content=pdf_data,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=rbi_fraud_{customer_id}.pdf"
            },
        )

    raise HTTPException(status_code=400, detail="Unsupported format. Use 'json' or 'pdf'.")


# ===========================================================================
#  WORKFLOW INTEGRATION OUTPUTS
# ===========================================================================

@app.get(
    "/rbi/ocen-clearance/{customer_id}",
    summary="OCEN Marketplace Clearance Signal",
    tags=["Workflow Integration"],
)
async def ocen_clearance(customer_id: int, db: Session = Depends(get_db)):
    """
    Output consumed by OCEN Marketplace to decide whether to proceed
    with loan-offer matching for this customer.
    """
    record = (
        db.query(RBIFraudRecord)
        .filter(RBIFraudRecord.customer_id == customer_id)
        .order_by(RBIFraudRecord.created_at.desc())
        .first()
    )
    if not record:
        return {"customer_id": customer_id, "cleared": False, "reason": "No fraud record found."}

    cleared = record.risk_level in ("Low", "Medium") and not record.is_blacklisted
    return {
        "customer_id": customer_id,
        "cleared": cleared,
        "risk_level": record.risk_level,
        "fraud_score": record.fraud_score,
        "fraud_category": record.fraud_category,
        "is_overridden": record.is_overridden,
        "message": (
            "Customer cleared for OCEN Marketplace routing."
            if cleared
            else "Customer blocked – fraud risk too high for OCEN routing."
        ),
    }


@app.get(
    "/rbi/cam-summary/{customer_id}",
    summary="CAM Generator Fraud Summary",
    tags=["Workflow Integration"],
)
async def cam_summary(customer_id: int, db: Session = Depends(get_db)):
    """Summary payload consumed by the CAM Generator service."""
    records = (
        db.query(RBIFraudRecord)
        .filter(RBIFraudRecord.customer_id == customer_id)
        .order_by(RBIFraudRecord.created_at.desc())
        .all()
    )
    if not records:
        return {"customer_id": customer_id, "summary": "No fraud data available."}

    latest = records[0]
    return {
        "customer_id": customer_id,
        "rbi_fraud_score": latest.fraud_score,
        "rbi_risk_level": latest.risk_level,
        "rbi_fraud_category": latest.fraud_category,
        "rbi_blacklisted": latest.is_blacklisted,
        "rbi_risk_flags": latest.risk_flags,
        "rbi_ai_insights": latest.ai_insights,
        "rbi_override_applied": latest.is_overridden,
        "screening_count": len(records),
    }


# ===========================================================================
#  HEALTH
# ===========================================================================

@app.get("/livez", summary="Liveness Probe", tags=["Health"])
async def livez():
    return {"status": "UP", "service": "rbi-fraud-service", "version": "2.0.0"}


@app.get("/readyz", summary="Readiness Probe", tags=["Health"])
async def readyz(db: Session = Depends(get_db)):
    try:
        db.query(RBIFraudRecord).first()
        return {"status": "READY"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Database not ready: {exc}")
