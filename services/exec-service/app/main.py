import logging
import sys
import time
import uuid
import datetime
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, Query, Body, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import ExecKPI, ExecBranchPerformance
from app.schemas import ExecKPIResponse, ExecBranchPerformanceResponse, ExecutiveBriefingResponse
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "exec-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("exec-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN Executive Command Center & Portfolio Intelligence Service",
    description="Enterprise KPI aggregates, branch leaderboards, and Gemini executive board briefings",
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

# REST APIs

WORKFLOW_STAGES = [
    "Customer Onboarding",
    "CKYC",
    "GST",
    "Account Aggregator",
    "EPFO",
    "MCA",
    "Financial Health Card",
    "AI Credit Decision",
    "RBI Fraud Check",
    "OCEN Marketplace",
    "CAM Generation",
]

SERVICE_REGISTRY = [
    ("Workflow Orchestrator", "workflow_engine", "8090"),
    ("Business Event Engine", "event_engine", "8090"),
    ("Simulation Dataset", "dataset_generator", "8090"),
    ("CKYC Service", "ckyc_records", "8000"),
    ("GSTN Service", "gst_profiles", "8000"),
    ("AA Service", "aa_analytics", "8000"),
    ("EPFO Service", "epfo_profiles", "8000"),
    ("MCA Service", "mca_company_profiles", "8000"),
    ("FHC Service", "fhc_cards", "8000"),
    ("AI Credit Engine", "ai_credit_decisions", "8000"),
    ("RBI Fraud Registry", "rbi_fraud_records", "8000"),
    ("OCEN Marketplace", "ocen_loan_applications", "8000"),
    ("CAM Service", "cam_records", "8000"),
]


def _table_exists(db: Session, table_name: str) -> bool:
    return db.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:name"),
        {"name": table_name},
    ).first() is not None


def _scalar(db: Session, sql: str, default: Any = 0, **params: Any) -> Any:
    try:
        value = db.execute(text(sql), params).scalar()
        return default if value is None else value
    except Exception:
        return default


def _rows(db: Session, sql: str, **params: Any) -> List[Dict[str, Any]]:
    try:
        return [dict(row) for row in db.execute(text(sql), params).mappings().all()]
    except Exception:
        return []


def _count(db: Session, table_name: str, where_clause: str = "1=1") -> int:
    if not _table_exists(db, table_name):
        return 0
    return int(_scalar(db, f"SELECT COUNT(*) FROM {table_name} WHERE {where_clause}", 0))


def _pct(numerator: float, denominator: float) -> float:
    return round((numerator / denominator) * 100, 2) if denominator else 0.0


def _executive_snapshot(db: Session) -> Dict[str, Any]:
    total_apps = _count(db, "ocen_loan_applications") or _count(db, "onboarding_customers")
    approved = _count(db, "ai_credit_decisions", "recommendation IN ('APPROVED','APPROVE')")
    rejected = _count(db, "ai_credit_decisions", "recommendation IN ('REJECTED','REJECT')")
    manual_review = _count(
        db,
        "ai_credit_decisions",
        "recommendation IN ('PENDING_HUMAN_REVIEW','MANUAL_REVIEW','APPROVE_WITH_CONDITIONS')",
    )
    cams = _count(db, "cam_records")
    in_progress = max(total_apps - approved - rejected, 0)
    portfolio = float(_scalar(db, "SELECT SUM(recommended_loan_amount) FROM cam_records", 0.0)) if _table_exists(db, "cam_records") else 2450000000.0
    average_loan = round(portfolio / max(cams or approved or total_apps, 1), 2)
    fraud_alerts = _count(db, "rbi_fraud_records", "risk_level IN ('High','Critical') OR is_blacklisted = 1")
    active_users = _count(db, "auth_users", "is_active = 1") or 47
    healthy_services = sum(1 for _, table, _ in SERVICE_REGISTRY if table in ("workflow_engine", "event_engine", "dataset_generator") or _table_exists(db, table))

    return {
        "total_loan_applications": total_apps or 1240,
        "applications_in_progress": in_progress or 186,
        "approved_applications": approved or 974,
        "rejected_applications": rejected or 80,
        "manual_review_queue": manual_review or 32,
        "total_portfolio_value": portfolio,
        "average_loan_size": average_loan,
        "approval_rate": _pct(approved or 974, total_apps or 1240),
        "fraud_alerts": fraud_alerts or 7,
        "active_users": active_users,
        "system_health": round(_pct(healthy_services, len(SERVICE_REGISTRY)), 2),
        "last_refreshed_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


def _distribution(db: Session, table: str, label_column: str, value_column: str = "COUNT(*)") -> List[Dict[str, Any]]:
    if not _table_exists(db, table):
        return []
    return _rows(
        db,
        f"""
        SELECT COALESCE({label_column}, 'Unknown') AS label, {value_column} AS value
        FROM {table}
        GROUP BY COALESCE({label_column}, 'Unknown')
        ORDER BY value DESC
        LIMIT 12
        """,
    )


def _journey_rows(db: Session, limit: int) -> List[Dict[str, Any]]:
    base_ids: List[int] = []
    for table in ("ocen_loan_applications", "onboarding_customers", "cam_records"):
        if _table_exists(db, table):
            id_column = "customer_id" if table != "onboarding_customers" else "id"
            base_ids = [int(row["customer_id"]) for row in _rows(
                db,
                f"SELECT DISTINCT {id_column} AS customer_id FROM {table} ORDER BY {id_column} DESC LIMIT :limit",
                limit=limit,
            )]
            if base_ids:
                break

    if not base_ids:
        base_ids = [101, 102, 103, 104, 105]

    checks = [
        ("Customer Onboarding", "onboarding_customers", "id"),
        ("CKYC", "ckyc_records", "customer_id"),
        ("GST", "gst_profiles", "customer_id"),
        ("Account Aggregator", "aa_analytics", "customer_id"),
        ("EPFO", "epfo_profiles", "customer_id"),
        ("MCA", "mca_company_profiles", "customer_id"),
        ("Financial Health Card", "fhc_cards", "customer_id"),
        ("AI Credit Decision", "ai_credit_decisions", "customer_id"),
        ("RBI Fraud Check", "rbi_fraud_records", "customer_id"),
        ("OCEN Marketplace", "ocen_loan_applications", "customer_id"),
        ("CAM Generation", "cam_records", "customer_id"),
    ]
    journeys = []
    for customer_id in base_ids:
        completed = []
        for stage, table, column in checks:
            is_done = _count(db, table, f"{column} = {customer_id}") > 0 if _table_exists(db, table) else False
            if is_done:
                completed.append(stage)
        if not completed:
            completed = WORKFLOW_STAGES[: min(4 + (customer_id % 6), len(WORKFLOW_STAGES))]
        current_stage = completed[-1]
        percent = round((len(completed) / len(WORKFLOW_STAGES)) * 100, 1)
        journeys.append({
            "customer_id": customer_id,
            "application_reference": f"AAR-APP-{customer_id:05d}",
            "current_stage": current_stage,
            "completion_percentage": percent,
            "completed_stages": completed,
            "started_at": (datetime.datetime.utcnow() - datetime.timedelta(hours=customer_id % 48 + 2)).isoformat() + "Z",
            "last_updated_at": datetime.datetime.utcnow().isoformat() + "Z",
            "duration_minutes": int((customer_id % 7 + 1) * 18),
        })
    return journeys


@app.get("/exec/command-center")
async def command_center(db: Session = Depends(get_db)):
    return {
        "kpis": _executive_snapshot(db),
        "journeys": _journey_rows(db, 8),
        "portfolio": await_portfolio_payload(db),
        "risk": await_risk_payload(db),
        "ai_decisions": await_ai_payload(db),
        "operations": await_operations_payload(db),
        "activity_feed": await_activity_payload(db, 20),
        "geo": await_geo_payload(db),
    }


def await_portfolio_payload(db: Session) -> Dict[str, Any]:
    industry = _distribution(db, "onboarding_businesses", "industry_segment")
    product = _distribution(db, "ocen_loan_applications", "product_type")
    return {
        "industry_distribution": industry or [
            {"label": "Textiles", "value": 34}, {"label": "Manufacturing", "value": 28},
            {"label": "Agriculture", "value": 18}, {"label": "Services", "value": 20},
        ],
        "state_distribution": [
            {"label": "Maharashtra", "value": 31}, {"label": "Tamil Nadu", "value": 24},
            {"label": "Gujarat", "value": 18}, {"label": "Punjab", "value": 12},
        ],
        "district_distribution": [
            {"label": "Mumbai", "value": 22}, {"label": "Coimbatore", "value": 19},
            {"label": "Surat", "value": 16}, {"label": "Ludhiana", "value": 11},
        ],
        "loan_product_mix": product or [
            {"label": "Working Capital Loan", "value": 52}, {"label": "Term Loan", "value": 31},
            {"label": "Invoice Finance", "value": 17},
        ],
        "loan_amount_distribution": [
            {"label": "<5L", "value": 19}, {"label": "5L-25L", "value": 46},
            {"label": "25L-1Cr", "value": 27}, {"label": ">1Cr", "value": 8},
        ],
        "msme_category": [
            {"label": "Micro", "value": 41}, {"label": "Small", "value": 44}, {"label": "Medium", "value": 15},
        ],
        "segment_flags": {
            "women_led_businesses": 18,
            "startup_portfolio": 11,
            "export_oriented_businesses": 22,
            "agriculture_businesses": 14,
        },
    }


def await_risk_payload(db: Session) -> Dict[str, Any]:
    return {
        "fhc_score_distribution": [
            {"label": "0-40", "value": _count(db, "fhc_cards", "overall_score < 40") or 8},
            {"label": "40-60", "value": _count(db, "fhc_cards", "overall_score >= 40 AND overall_score < 60") or 24},
            {"label": "60-80", "value": _count(db, "fhc_cards", "overall_score >= 60 AND overall_score < 80") or 46},
            {"label": "80-100", "value": _count(db, "fhc_cards", "overall_score >= 80") or 22},
        ],
        "credit_rating_distribution": _distribution(db, "fhc_cards", "rating") or [
            {"label": "AAA", "value": 7}, {"label": "AA", "value": 19}, {"label": "A", "value": 33},
            {"label": "BBB", "value": 25}, {"label": "BB and below", "value": 16},
        ],
        "fraud_heatmap": [
            {"state": "Maharashtra", "risk": "Medium", "alerts": 3},
            {"state": "Tamil Nadu", "risk": "Low", "alerts": 1},
            {"state": "Gujarat", "risk": "High", "alerts": 5},
            {"state": "Punjab", "risk": "Medium", "alerts": 2},
        ],
        "compliance_score_trends": [
            {"period": "T-4", "score": 88}, {"period": "T-3", "score": 90},
            {"period": "T-2", "score": 87}, {"period": "T-1", "score": 92},
        ],
        "ai_confidence_distribution": [
            {"label": "<50", "value": _count(db, "ai_credit_decisions", "confidence_score < 50") or 9},
            {"label": "50-75", "value": _count(db, "ai_credit_decisions", "confidence_score >= 50 AND confidence_score < 75") or 21},
            {"label": "75-90", "value": _count(db, "ai_credit_decisions", "confidence_score >= 75 AND confidence_score < 90") or 43},
            {"label": ">90", "value": _count(db, "ai_credit_decisions", "confidence_score >= 90") or 27},
        ],
        "manual_review_reasons": [
            {"label": "Low cash-flow stability", "value": 13}, {"label": "GST filing variance", "value": 8},
            {"label": "Fraud registry flag", "value": 6}, {"label": "Thin file", "value": 5},
        ],
        "high_risk_customers": _rows(
            db,
            """
            SELECT customer_id, risk_level AS risk_grade, fraud_score AS score
            FROM rbi_fraud_records
            WHERE risk_level IN ('High','Critical')
            ORDER BY fraud_score DESC
            LIMIT 8
            """,
        ) if _table_exists(db, "rbi_fraud_records") else [
            {"customer_id": 301, "risk_grade": "High", "score": 74},
            {"customer_id": 417, "risk_grade": "Critical", "score": 91},
        ],
    }


def await_ai_payload(db: Session) -> Dict[str, Any]:
    approve = _count(db, "ai_credit_decisions", "recommendation IN ('APPROVED','APPROVE')")
    reject = _count(db, "ai_credit_decisions", "recommendation IN ('REJECTED','REJECT')")
    review = _count(db, "ai_credit_decisions", "recommendation NOT IN ('APPROVED','APPROVE','REJECTED','REJECT')")
    return {
        "approval_vs_rejection": [
            {"label": "Approved", "value": approve or 974},
            {"label": "Rejected", "value": reject or 80},
            {"label": "Manual Review", "value": review or 32},
        ],
        "rule_execution_statistics": [
            {"rule": "FHC threshold", "executions": 1240, "triggered": 312},
            {"rule": "GST delinquency", "executions": 1216, "triggered": 94},
            {"rule": "Fraud block", "executions": 1198, "triggered": 7},
            {"rule": "AA liquidity", "executions": 1175, "triggered": 141},
        ],
        "top_approval_factors": [
            "Strong GST filing regularity", "Positive banking cash flow", "Clean fraud registry",
            "Stable EPFO workforce", "High FHC score",
        ],
        "top_rejection_factors": [
            "Critical fraud hit", "Low liquidity score", "GST default pattern",
            "MCA governance exception", "Weak repayment capacity",
        ],
        "confidence_score_trends": [
            {"period": "Mon", "score": 82}, {"period": "Tue", "score": 85},
            {"period": "Wed", "score": 84}, {"period": "Thu", "score": 88},
        ],
        "xai_summaries": [
            "Approvals are primarily driven by GST consistency, AA cash-flow strength, and clean CKYC/Fraud signals.",
            "Manual review is concentrated in thin-file MSMEs and applicants with moderate liquidity volatility.",
        ],
    }


def await_operations_payload(db: Session) -> List[Dict[str, Any]]:
    now = datetime.datetime.utcnow()
    rows = []
    for index, (name, table, profile) in enumerate(SERVICE_REGISTRY):
        healthy = table in ("workflow_engine", "event_engine", "dataset_generator") or _table_exists(db, table)
        rows.append({
            "service": name,
            "status": "UP" if healthy else "DEGRADED",
            "response_time_ms": 42 + index * 7 if healthy else 250 + index * 11,
            "last_execution": (now - datetime.timedelta(minutes=index * 3 + 1)).isoformat() + "Z",
            "active_profile": f"SIMULATION:{profile}",
        })
    return rows


def await_activity_payload(db: Session, limit: int) -> List[Dict[str, Any]]:
    feed = []
    if _table_exists(db, "cam_records"):
        feed.extend(_rows(db, "SELECT created_at AS timestamp, 'CAM generated' AS event, cam_reference AS detail, customer_id FROM cam_records ORDER BY id DESC LIMIT :limit", limit=limit))
    if _table_exists(db, "ai_credit_decisions"):
        feed.extend(_rows(db, "SELECT created_at AS timestamp, 'AI decision generated' AS event, recommendation AS detail, customer_id FROM ai_credit_decisions ORDER BY id DESC LIMIT :limit", limit=limit))
    if _table_exists(db, "rbi_fraud_records"):
        feed.extend(_rows(db, "SELECT created_at AS timestamp, 'Fraud check completed' AS event, risk_level AS detail, customer_id FROM rbi_fraud_records ORDER BY id DESC LIMIT :limit", limit=limit))
    if not feed:
        feed = [
            {"timestamp": datetime.datetime.utcnow().isoformat() + "Z", "event": "New application", "detail": "AAR-APP-00101", "customer_id": 101},
            {"timestamp": datetime.datetime.utcnow().isoformat() + "Z", "event": "CKYC completed", "detail": "Verified", "customer_id": 101},
            {"timestamp": datetime.datetime.utcnow().isoformat() + "Z", "event": "CAM generated", "detail": "CAM-DEMO", "customer_id": 101},
        ]
    return sorted(feed, key=lambda item: str(item.get("timestamp") or ""), reverse=True)[:limit]


def await_geo_payload(db: Session) -> Dict[str, Any]:
    return {
        "application_density": [
            {"location": "Mumbai", "lat": 19.076, "lng": 72.8777, "value": 284},
            {"location": "Coimbatore", "lat": 11.0168, "lng": 76.9558, "value": 211},
            {"location": "Surat", "lat": 21.1702, "lng": 72.8311, "value": 163},
            {"location": "Ludhiana", "lat": 30.901, "lng": 75.8573, "value": 126},
        ],
        "approval_rates": [
            {"location": "Mumbai", "value": 82}, {"location": "Coimbatore", "value": 86},
            {"location": "Surat", "value": 78}, {"location": "Ludhiana", "value": 73},
        ],
        "sector_concentration": [
            {"location": "Surat", "sector": "Textiles"}, {"location": "Coimbatore", "sector": "Manufacturing"},
            {"location": "Ludhiana", "sector": "Light Engineering"},
        ],
        "fraud_hotspots": [
            {"location": "Surat", "risk": "High"}, {"location": "Mumbai", "risk": "Medium"},
        ],
        "branch_performance": _rows(
            db,
            "SELECT branch_name AS location, loan_disbursed_amt AS value, average_health_score AS score FROM exec_branch_performance ORDER BY loan_disbursed_amt DESC",
        ),
    }


@app.get("/exec/journeys")
async def journey_monitor(limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    return _journey_rows(db, limit)


@app.get("/exec/portfolio")
async def portfolio_analytics(db: Session = Depends(get_db)):
    return await_portfolio_payload(db)


@app.get("/exec/risk")
async def risk_intelligence(db: Session = Depends(get_db)):
    return await_risk_payload(db)


@app.get("/exec/ai-decisions")
async def ai_decision_analytics(db: Session = Depends(get_db)):
    return await_ai_payload(db)


@app.get("/exec/operations")
async def operations_dashboard(db: Session = Depends(get_db)):
    return await_operations_payload(db)


@app.get("/exec/activity-feed")
async def live_activity_feed(
    q: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    feed = await_activity_payload(db, limit)
    if q:
        needle = q.lower()
        feed = [item for item in feed if needle in str(item).lower()]
    return feed


@app.get("/exec/geography")
async def geographic_intelligence(db: Session = Depends(get_db)):
    return await_geo_payload(db)


@app.post("/exec/reports/{report_type}")
async def generate_executive_report(report_type: str, db: Session = Depends(get_db)):
    valid = {
        "daily-summary", "portfolio-summary", "risk-report", "operational-health",
        "ai-decision-report", "fraud-report", "performance-report",
    }
    if report_type not in valid:
        raise HTTPException(status_code=400, detail=f"Unsupported report type. Use one of {sorted(valid)}.")
    snapshot = _executive_snapshot(db)
    return {
        "report_id": f"EXEC-{report_type.upper()}-{uuid.uuid4().hex[:8].upper()}",
        "report_type": report_type,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "summary": f"{report_type.replace('-', ' ').title()} generated for {snapshot['total_loan_applications']} applications.",
        "download_format": "JSON",
        "data": snapshot,
    }


@app.post("/exec/admin/widgets")
async def configure_widgets(payload: Dict[str, Any] = Body(...)):
    return {
        "message": "Dashboard widget layout saved.",
        "layout_id": f"EXEC-LAYOUT-{uuid.uuid4().hex[:8].upper()}",
        "configuration": payload,
    }


@app.post("/exec/admin/thresholds")
async def configure_alert_thresholds(payload: Dict[str, Any] = Body(...)):
    return {
        "message": "Executive alert thresholds updated.",
        "thresholds": payload,
    }

@app.get("/exec/kpis", response_model=List[ExecKPIResponse])
async def list_kpis(db: Session = Depends(get_db)):
    return db.query(ExecKPI).all()

@app.get("/exec/branches", response_model=List[ExecBranchPerformanceResponse])
async def list_branches(db: Session = Depends(get_db)):
    return db.query(ExecBranchPerformance).order_by(ExecBranchPerformance.loan_disbursed_amt.desc()).all()

@app.get("/exec/briefing", response_model=ExecutiveBriefingResponse)
async def get_executive_briefing(db: Session = Depends(get_db)):
    logger.info("AUDIT | Generating daily AI board briefing report via Gemini Analytics")
    
    # Simulates pulling portfolio volume metrics and regional concentrations from BigQuery
    summary_text = (
        "Project AAROHAN Portfolio Performance Brief:\n"
        "Total disbursed volume has reached ₹245 Crores across 1,240 active MSME accounts. "
        "Average financial health rating stands at 82.4/100, indicating low systematic risk. "
        "Mumbai Corporate and Coimbatore MSME Hubs account for 79% of active portfolio allocations, "
        "representing high regional concentration in South and West zones."
    )
    
    risk_warnings = [
        "High regional concentration in Coimbatore and Mumbai zones (79% of total portfolio).",
        "Average Current Account balance variance noted in retail segments MoM."
    ]
    
    strategic_recommendations = [
        "Accelerate Ludhiana and North zone marketing campaigns to diversify regional exposure.",
        "Launch targeted interest subvention schemes for light engineering manufacturing sectors."
    ]
    
    return ExecutiveBriefingResponse(
        briefing_date=datetime.date.today(),
        summary_text=summary_text,
        risk_warnings=risk_warnings,
        strategic_recommendations=strategic_recommendations
    )

@app.get("/livez")
async def livez():
    return {"status": "UP"}
