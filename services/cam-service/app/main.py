"""
AAROHAN – CAM Generation Service (v2)
======================================
Implements the Enterprise Credit Appraisal Memo generation service:
  • 18-section structured CAM
  • Multi-format output: JSON | HTML | PDF
  • Version history with section-level diff comparison
  • Multi-level approval workflow
  • Template-driven bank branding (5 templates)
  • Explainable AI narratives
  • CAM Dashboard and download centre
  • Admin: regenerate, archive, configure
  • Business event publishing
  • Workflow integration: OCEN → CAM → Executive Dashboard
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
from fastapi.responses import JSONResponse, HTMLResponse, Response
from sqlalchemy import text
from sqlalchemy.orm import Session

import os
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
ese_path = os.path.join(WORKSPACE_ROOT, "services", "ese-core")
if ese_path not in sys.path:
    sys.path.insert(0, ese_path)

from app.models import CAMRecord, CAMVersion, CAMApprovalLog, CAMTemplate, CAMConfig
from app.schemas import (
    CAMRecordResponse, CAMVersionResponse, ApprovalLogResponse,
    CAMGenerateRequest, CAMUpdateRequest, CAMApprovalRequest,
    TemplateResponse, CAMDashboardResponse,
    VersionCompareResponse, VersionDiff, CAMConfigResponse,
)
from app.database import get_db, init_db, SessionLocal
from app.cam_engine import compile_cam, TEMPLATES, ALL_SECTIONS, _calc_emi

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format=(
        '{"timestamp": "%(asctime)s", "severity": "%(levelname)s", '
        '"message": "%(message)s", "service": "cam-service"}'
    ),
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("cam-service")

init_db()

app = FastAPI(
    title="AAROHAN Enterprise CAM Generation Service",
    description=(
        "Automated Credit Appraisal Memo generator consuming all upstream lending modules. "
        "Produces professional 18-section CAMs in JSON, HTML, and PDF formats."
    ),
    version="2.0.0",
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
async def process_middleware(request: Request, call_next):
    start = time.time()
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = cid
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.time()-start:.4f}"
    response.headers["X-Correlation-ID"] = cid
    return response


@app.exception_handler(HTTPException)
async def http_exc(request: Request, exc: HTTPException):
    cid = getattr(request.state, "correlation_id", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={"errorCode": f"AAR-ERR-{exc.status_code}", "message": exc.detail, "correlationId": cid},
    )


# ── Helpers ──────────────────────────────────────────────────────────────────

def _publish(event: str, customer_id: int, payload: dict):
    logger.info(f"AUDIT | EVENT_BUS | {event} | cust={customer_id}")
    try:
        from event_engine import BusinessEventEngine
        BusinessEventEngine().dispatch(event, f"cust_{customer_id}", payload)
    except Exception as exc:
        logger.warning(f"Event bus unavailable ({event}): {exc}")


def _cam_ref() -> str:
    return f"CAM-{uuid.uuid4().hex[:8].upper()}"


def _table_exists(db: Session, table_name: str) -> bool:
    result = db.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:name"),
        {"name": table_name},
    ).first()
    return result is not None


def _one(db: Session, sql: str, **params: Any) -> Optional[Dict[str, Any]]:
    try:
        row = db.execute(text(sql), params).mappings().first()
        return dict(row) if row else None
    except Exception as exc:
        logger.debug(f"CAM aggregation skipped query: {exc}")
        return None


def _normalise_credit_decision(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    decision = value.upper()
    if decision in ("APPROVED", "APPROVE"):
        return "APPROVE"
    if decision in ("REJECTED", "REJECT", "DECLINED"):
        return "REJECT"
    if decision in ("APPROVE_WITH_CONDITIONS", "CONDITIONAL", "PENDING_HUMAN_REVIEW", "MANUAL_REVIEW"):
        return "CONDITIONAL"
    return decision


def _aggregate_upstream_context(db: Session, customer_id: int) -> Dict[str, Any]:
    """Read consolidated module outputs from the shared simulation database."""
    ctx: Dict[str, Any] = {"customer_id": customer_id}

    if _table_exists(db, "onboarding_businesses"):
        business = _one(
            db,
            """
            SELECT trade_name, constitution_type, annual_turnover, industry_segment,
                   employee_count, gstin, cin
            FROM onboarding_businesses
            WHERE customer_id=:customer_id
            ORDER BY id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if business:
            ctx.update({
                "business_name": business.get("trade_name"),
                "business_type": business.get("constitution_type"),
                "annual_revenue": business.get("annual_turnover"),
                "industry": business.get("industry_segment"),
                "employee_count": business.get("employee_count"),
            })

    if _table_exists(db, "ckyc_verification_logs"):
        ckyc = _one(
            db,
            """
            SELECT verification_status, anomaly_detected
            FROM ckyc_verification_logs
            WHERE customer_id=:customer_id
            ORDER BY id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if ckyc:
            status_text = str(ckyc.get("verification_status") or "").upper()
            ctx["pan_verified"] = status_text in ("VERIFIED", "MATCHED", "SUCCESS")
            ctx["aadhaar_verified"] = not bool(ckyc.get("anomaly_detected"))

    if _table_exists(db, "gst_profiles"):
        gst = _one(
            db,
            """
            SELECT gp.status, ga.compliance_score, ga.risk_level, ga.avg_monthly_turnover
            FROM gst_profiles gp
            LEFT JOIN gst_analytics ga ON ga.profile_id = gp.id
            WHERE gp.customer_id=:customer_id
            ORDER BY ga.id DESC, gp.id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if gst:
            status_text = str(gst.get("status") or "").upper()
            risk_text = str(gst.get("risk_level") or "Low")
            ctx["gst_compliant"] = status_text == "ACTIVE" and risk_text not in ("High", "Critical")
            if not ctx.get("annual_revenue") and gst.get("avg_monthly_turnover"):
                ctx["annual_revenue"] = float(gst["avg_monthly_turnover"]) * 12

    if _table_exists(db, "aa_analytics"):
        aa = _one(
            db,
            """
            SELECT avg_balance, cheque_bounce_indicator, overdraft_usage, emi_discipline
            FROM aa_analytics
            WHERE customer_id=:customer_id
            ORDER BY id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if aa:
            ctx["avg_balance"] = aa.get("avg_balance")
            ctx["cheque_bounce"] = bool(aa.get("cheque_bounce_indicator"))
            ctx["overdraft_frequent"] = str(aa.get("overdraft_usage") or "").lower() in ("frequent", "high")
            ctx["emi_regular"] = str(aa.get("emi_discipline") or "Regular").lower() not in ("poor", "irregular")

    if _table_exists(db, "epfo_profiles"):
        epfo = _one(
            db,
            """
            SELECT ep.number_of_employees, ea.compliance_score, ea.workforce_stability_risk
            FROM epfo_profiles ep
            LEFT JOIN epfo_analytics ea ON ea.profile_id = ep.id
            WHERE ep.customer_id=:customer_id
            ORDER BY ea.id DESC, ep.id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if epfo:
            ctx["employee_count"] = epfo.get("number_of_employees") or ctx.get("employee_count")
            ctx["epfo_compliant"] = (epfo.get("compliance_score") or 100) >= 70

    if _table_exists(db, "mca_company_profiles"):
        mca = _one(
            db,
            """
            SELECT mg.overall_risk_level
            FROM mca_company_profiles mp
            LEFT JOIN mca_governance_analytics mg ON mg.company_id = mp.id
            WHERE mp.customer_id=:customer_id
            ORDER BY mg.id DESC, mp.id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if mca:
            ctx["mca_verified"] = True
            ctx["governance_risk"] = mca.get("overall_risk_level") or "Low"

    if _table_exists(db, "fhc_cards"):
        fhc = _one(
            db,
            """
            SELECT overall_score, rating
            FROM fhc_cards
            WHERE customer_id=:customer_id
            ORDER BY id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if fhc:
            ctx["fhc_score"] = fhc.get("overall_score")

    if _table_exists(db, "ai_credit_decisions"):
        credit = _one(
            db,
            """
            SELECT recommendation, eligible_loan_amount, recommended_product,
                   recommended_tenure, recommended_interest_rate, approval_probability
            FROM ai_credit_decisions
            WHERE customer_id=:customer_id
            ORDER BY id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if credit:
            ctx["credit_decision"] = _normalise_credit_decision(credit.get("recommendation"))
            ctx["recommended_amount"] = credit.get("eligible_loan_amount")
            ctx["product_type"] = credit.get("recommended_product")
            ctx["recommended_tenure"] = credit.get("recommended_tenure")
            ctx["recommended_rate"] = credit.get("recommended_interest_rate")
            ctx["approval_probability"] = credit.get("approval_probability")

    if _table_exists(db, "rbi_fraud_records"):
        fraud = _one(
            db,
            """
            SELECT fraud_score, risk_level
            FROM rbi_fraud_records
            WHERE customer_id=:customer_id
            ORDER BY fraud_score DESC, id DESC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if fraud:
            ctx["fraud_score"] = fraud.get("fraud_score")
            ctx["fraud_risk_level"] = fraud.get("risk_level")

    if _table_exists(db, "ocen_loan_applications"):
        ocen = _one(
            db,
            """
            SELECT la.uli_reference, la.requested_amount, la.requested_tenure_months,
                   la.product_type, la.purpose, la.fhc_score, la.credit_decision,
                   la.fraud_score, la.fraud_risk_level,
                   lo.lender_name, lo.offered_amount, lo.interest_rate,
                   lo.tenure_months, lo.match_score, lo.approval_probability,
                   lo.expected_disbursal_days, lo.conditions
            FROM ocen_loan_applications la
            LEFT JOIN ocen_loan_offers lo
              ON lo.application_id = la.id
             AND (lo.id = la.selected_offer_id OR lo.rank = 1)
            WHERE la.customer_id=:customer_id
            ORDER BY la.id DESC, lo.rank ASC
            LIMIT 1
            """,
            customer_id=customer_id,
        )
        if ocen:
            ctx.update({
                "uli_reference": ocen.get("uli_reference"),
                "requested_amount": ocen.get("requested_amount"),
                "loan_purpose": ocen.get("purpose"),
                "product_type": ocen.get("product_type"),
                "recommended_lender": ocen.get("lender_name"),
                "recommended_amount": ocen.get("offered_amount") or ctx.get("recommended_amount"),
                "recommended_rate": ocen.get("interest_rate") or ctx.get("recommended_rate"),
                "recommended_tenure": ocen.get("tenure_months") or ctx.get("recommended_tenure"),
                "match_score": ocen.get("match_score"),
                "approval_probability": ocen.get("approval_probability") or ctx.get("approval_probability"),
                "expected_disbursal_days": ocen.get("expected_disbursal_days"),
                "offer_conditions": ocen.get("conditions"),
                "fhc_score": ocen.get("fhc_score") or ctx.get("fhc_score"),
                "credit_decision": _normalise_credit_decision(ocen.get("credit_decision")) or ctx.get("credit_decision"),
                "fraud_score": ocen.get("fraud_score") or ctx.get("fraud_score"),
                "fraud_risk_level": ocen.get("fraud_risk_level") or ctx.get("fraud_risk_level"),
            })

    return {k: v for k, v in ctx.items() if v is not None}


def _merge_context(payload: CAMGenerateRequest, db: Session) -> Dict[str, Any]:
    aggregated = _aggregate_upstream_context(db, payload.customer_id)
    explicit = payload.model_dump(exclude_none=True)
    return {**aggregated, **explicit}


def _get_config(db: Session) -> CAMConfig:
    cfg = db.query(CAMConfig).first()
    if not cfg:
        cfg = CAMConfig(default_template="IDBI_BANK",
                        sections_enabled=json.dumps(ALL_SECTIONS))
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg


def _snapshot_version(cam: CAMRecord, db: Session, edited_by: str = "SYSTEM",
                       change_summary: str = "Auto-generated"):
    db.add(CAMVersion(
        cam_id=cam.id,
        version_num=cam.current_version,
        edited_by=edited_by,
        change_summary=change_summary,
        section_executive_summary=cam.section_executive_summary,
        section_banker_recommendation=cam.section_banker_recommendation,
        section_recommended_offer=cam.section_recommended_offer,
        section_key_risks=cam.section_key_risks,
        overall_credit_score=cam.overall_credit_score,
        status=cam.status,
    ))


# ── HTML Template ─────────────────────────────────────────────────────────────

def _build_html(cam: CAMRecord, tmpl: dict) -> str:
    emi = ""
    if cam.recommended_loan_amount and cam.recommended_interest_rate and cam.recommended_tenure_months:
        emi = f"₹{_calc_emi(cam.recommended_loan_amount, cam.recommended_interest_rate, cam.recommended_tenure_months):,.2f}/month"

    sections = [
        ("Executive Summary", cam.section_executive_summary),
        ("Applicant Profile", cam.section_applicant_profile),
        ("Business Profile", cam.section_business_profile),
        ("Loan Requirement", cam.section_loan_requirement),
        ("Identity Verification", cam.section_identity_verification),
        ("GST Compliance", cam.section_gst_compliance),
        ("Banking Behaviour", cam.section_banking_behaviour),
        ("Workforce Stability", cam.section_workforce_stability),
        ("Corporate Governance", cam.section_corporate_governance),
        ("Financial Health Card", cam.section_fhc_summary),
        ("AI Credit Decision", cam.section_credit_decision),
        ("Fraud Screening", cam.section_fraud_screening),
        ("OCEN Marketplace", cam.section_ocen_marketplace),
        ("Recommended Offer", cam.section_recommended_offer),
        ("Key Risks", cam.section_key_risks),
        ("Risk Mitigation", cam.section_risk_mitigation),
        ("Banker Recommendation", cam.section_banker_recommendation),
        ("Approval Matrix", cam.section_approval_matrix),
    ]

    sections_html = ""
    for title, content in sections:
        sections_html += f"""
        <div class="section">
            <h2>{title}</h2>
            <pre class="content">{content}</pre>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CAM – {cam.cam_reference}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; color: #222; }}
  .page {{ max-width: 1100px; margin: 0 auto; background: #fff; padding: 0; }}
  .header {{ background: {tmpl.get('color_primary','#003366')}; color: white; padding: 32px 40px; }}
  .header h1 {{ font-size: 22px; font-weight: 700; letter-spacing: 1px; }}
  .header .sub {{ font-size: 13px; margin-top: 6px; opacity: 0.8; }}
  .score-bar {{ background: {tmpl.get('color_secondary','#E8F0FE')}; display: flex; gap: 32px; padding: 20px 40px; border-bottom: 2px solid {tmpl.get('color_primary','#003366')}; flex-wrap: wrap; }}
  .metric {{ text-align: center; }}
  .metric .val {{ font-size: 28px; font-weight: 700; color: {tmpl.get('color_primary','#003366')}; }}
  .metric .lbl {{ font-size: 11px; color: #555; text-transform: uppercase; letter-spacing: 0.5px; }}
  .badge {{ display: inline-block; padding: 4px 14px; border-radius: 20px; font-weight: 700; font-size: 13px; }}
  .badge-green {{ background: #d4edda; color: #155724; }}
  .badge-amber {{ background: #fff3cd; color: #856404; }}
  .badge-red {{ background: #f8d7da; color: #721c24; }}
  .body {{ padding: 32px 40px; }}
  .section {{ margin-bottom: 28px; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; }}
  .section h2 {{ background: {tmpl.get('color_primary','#003366')}; color: white; font-size: 14px; padding: 10px 18px; letter-spacing: 0.5px; }}
  .content {{ padding: 16px 18px; font-size: 13px; line-height: 1.7; white-space: pre-wrap; word-wrap: break-word; background: #fafafa; }}
  .narrative {{ background: {tmpl.get('color_secondary','#E8F0FE')}; border-left: 4px solid {tmpl.get('color_primary','#003366')}; padding: 18px 24px; margin-bottom: 28px; border-radius: 0 8px 8px 0; }}
  .narrative h3 {{ font-size: 14px; color: {tmpl.get('color_primary','#003366')}; margin-bottom: 10px; }}
  .narrative p {{ font-size: 13px; line-height: 1.6; margin-bottom: 6px; }}
  .footer {{ background: #f0f0f0; padding: 16px 40px; font-size: 11px; color: #888; text-align: center; border-top: 1px solid #ddd; }}
</style>
</head>
<body>
<div class="page">
  <div class="header">
    <div>{tmpl.get('logo_placeholder','')}</div>
    <h1>{tmpl.get('header_text','CREDIT APPRAISAL MEMORANDUM')}</h1>
    <div class="sub">Reference: {cam.cam_reference} &nbsp;|&nbsp; Customer ID: {cam.customer_id} &nbsp;|&nbsp; Version: {cam.current_version} &nbsp;|&nbsp; Status: {cam.status}</div>
  </div>
  <div class="score-bar">
    <div class="metric"><div class="val">{cam.overall_credit_score or '–'}</div><div class="lbl">Credit Score</div></div>
    <div class="metric"><div class="val">{cam.financial_health_rating or '–'}</div><div class="lbl">FHC Rating</div></div>
    <div class="metric"><div class="val">{cam.risk_grade or '–'}</div><div class="lbl">Risk Grade</div></div>
    <div class="metric"><div class="val">{cam.fraud_status or '–'}</div><div class="lbl">Fraud Status</div></div>
    <div class="metric"><div class="val">₹{cam.recommended_loan_amount:,.0f}</div><div class="lbl">Recommended Amount</div></div>
    <div class="metric"><div class="val">{cam.recommended_interest_rate}%</div><div class="lbl">Interest Rate</div></div>
    <div class="metric"><div class="val">{emi}</div><div class="lbl">EMI Estimate</div></div>
  </div>
  <div class="body">
    <div class="narrative">
      <h3>🏢 AI Lending Narrative</h3>
      <p><strong>Customer Strengths:</strong> {cam.narrative_customer_strengths or '–'}</p>
      <p><strong>Financial Observations:</strong> {cam.narrative_financial_observations or '–'}</p>
      <p><strong>Key Risks:</strong> {cam.narrative_key_risks or '–'}</p>
      <p><strong>Recommendation:</strong> {cam.narrative_lending_recommendation or '–'}</p>
      <p><strong>Monitoring:</strong> {cam.narrative_monitoring_actions or '–'}</p>
    </div>
    {sections_html}
  </div>
  <div class="footer">{tmpl.get('footer_text','')} &nbsp;|&nbsp; Generated by AAROHAN AI Engine &nbsp;|&nbsp; {datetime.datetime.now().strftime('%d %b %Y %H:%M')}</div>
</div>
</body>
</html>"""


def _build_pdf_stub(cam: CAMRecord, tmpl: dict) -> bytes:
    """Minimal PDF-1.4 compatible structure with all 18 sections."""
    ref = cam.cam_reference
    bank = tmpl.get("bank_name", "AAROHAN")
    hdr = tmpl.get("header_text", "CREDIT APPRAISAL MEMORANDUM")

    lines = [
        "%PDF-1.4",
        f"1 0 obj\n<< /Title ({hdr}) /Author ({bank}) /Subject (CAM {ref}) >>\nendobj",
        "2 0 obj\n<< /Type /Catalog /Pages 3 0 R >>\nendobj",
        "3 0 obj\n<< /Type /Pages /Kids [4 0 R] /Count 1 >>\nendobj",
        "4 0 obj\n<< /Type /Page /Parent 3 0 R /MediaBox [0 0 595 1200] /Contents 5 0 R >>\nendobj",
        "5 0 obj\n<< /Length 9000 >>\nstream",
        f"BT /F1 18 Tf 50 1150 Td ({hdr}) Tj ET",
        f"BT /F1 10 Tf 50 1120 Td (Reference: {ref}) Tj ET",
        f"BT /F1 10 Tf 50 1100 Td (Customer ID: {cam.customer_id}   Status: {cam.status}   Version: {cam.current_version}) Tj ET",
        f"BT /F1 12 Tf 50 1070 Td (CREDIT SCORING SUMMARY) Tj ET",
        f"BT /F1 10 Tf 50 1050 Td (Overall Credit Score: {cam.overall_credit_score or 'N/A'}) Tj ET",
        f"BT /F1 10 Tf 50 1030 Td (Financial Health Rating: {cam.financial_health_rating or 'N/A'}) Tj ET",
        f"BT /F1 10 Tf 50 1010 Td (Risk Grade: {cam.risk_grade or 'N/A'}   Fraud Status: {cam.fraud_status or 'N/A'}) Tj ET",
        f"BT /F1 10 Tf 50 990 Td (Eligibility: {cam.eligibility_status or 'N/A'}) Tj ET",
        f"BT /F1 10 Tf 50 970 Td (Recommended Amount: Rs {cam.recommended_loan_amount or 0:,.0f}   Rate: {cam.recommended_interest_rate or 0}% p.a.   Tenure: {cam.recommended_tenure_months or 0} months) Tj ET",
        f"BT /F1 12 Tf 50 940 Td (AI NARRATIVE) Tj ET",
        f"BT /F1 9 Tf 50 920 Td (Customer Strengths: {(cam.narrative_customer_strengths or '')[:100]}) Tj ET",
        f"BT /F1 9 Tf 50 900 Td (Key Risks: {(cam.narrative_key_risks or '')[:100]}) Tj ET",
        f"BT /F1 9 Tf 50 880 Td (Recommendation: {(cam.narrative_lending_recommendation or '')[:100]}) Tj ET",
        f"BT /F1 12 Tf 50 850 Td (18-SECTION CAM DOCUMENT) Tj ET",
    ]

    section_texts = [
        cam.section_executive_summary, cam.section_applicant_profile,
        cam.section_business_profile, cam.section_loan_requirement,
        cam.section_identity_verification, cam.section_gst_compliance,
        cam.section_banking_behaviour, cam.section_workforce_stability,
        cam.section_corporate_governance, cam.section_fhc_summary,
        cam.section_credit_decision, cam.section_fraud_screening,
        cam.section_ocen_marketplace, cam.section_recommended_offer,
        cam.section_key_risks, cam.section_risk_mitigation,
        cam.section_banker_recommendation, cam.section_approval_matrix,
    ]
    section_names = [
        "Executive Summary", "Applicant Profile", "Business Profile", "Loan Requirement",
        "Identity Verification", "GST Compliance", "Banking Behaviour", "Workforce Stability",
        "Corporate Governance", "FHC Summary", "Credit Decision", "Fraud Screening",
        "OCEN Marketplace", "Recommended Offer", "Key Risks", "Risk Mitigation",
        "Banker Recommendation", "Approval Matrix",
    ]

    y = 820
    for name, text in zip(section_names, section_texts):
        snippet = (text or "")[:80].replace("(", "[").replace(")", "]").replace("\n", " ")
        lines.append(f"BT /F1 8 Tf 50 {y} Td ({name}: {snippet}...) Tj ET")
        y -= 18
        if y < 50:
            break

    lines += [
        f"BT /F1 8 Tf 50 50 Td (Generated by AAROHAN AI Engine | {bank} | {datetime.datetime.now().strftime('%d %b %Y')}) Tj ET",
        "endstream\nendobj",
        "xref\n0 6\n0000000000 65535 f",
        "trailer\n<< /Size 6 /Root 2 0 R >>\nstartxref\n%%EOF",
    ]
    return "\n".join(lines).encode("utf-8")


# ============================================================================
#  1. CAM GENERATE
# ============================================================================

@app.post(
    "/cam/generate",
    response_model=CAMRecordResponse,
    summary="Generate CAM",
    tags=["CAM"],
    status_code=201,
)
async def generate_cam(payload: CAMGenerateRequest, db: Session = Depends(get_db)):
    """Auto-generates a full 18-section CAM from upstream intelligence."""
    _publish("CAM Generation Started", payload.customer_id, {"customer_id": payload.customer_id})

    # Delete existing draft for this customer (idempotent regeneration)
    existing = db.query(CAMRecord).filter(CAMRecord.customer_id == payload.customer_id).first()
    if existing:
        db.delete(existing)
        db.commit()

    ctx = _merge_context(payload, db)
    sections = compile_cam(ctx)

    cam = CAMRecord(
        customer_id=payload.customer_id,
        cam_reference=_cam_ref(),
        status="DRAFT",
        current_version=1,
        template=payload.template,
        **sections,
    )
    db.add(cam)
    db.flush()

    _snapshot_version(cam, db, edited_by="AAROHAN-AI-ENGINE",
                      change_summary="Initial auto-generated CAM")
    db.commit()
    db.refresh(cam)

    _publish("CAM Generated", payload.customer_id, {
        "cam_id": cam.id, "cam_reference": cam.cam_reference,
        "credit_score": cam.overall_credit_score,
        "eligibility": cam.eligibility_status,
    })
    logger.info(f"AUDIT | CAM generated | ID: {cam.id} | ref: {cam.cam_reference}")
    return cam


@app.post(
    "/cam/generate/{customer_id:int}",
    response_model=CAMRecordResponse,
    summary="Generate CAM by Customer ID (quick trigger)",
    tags=["CAM"],
    status_code=201,
)
async def generate_cam_by_id(
    customer_id: int,
    template: str = Query("IDBI_BANK"),
    db: Session = Depends(get_db),
):
    payload = CAMGenerateRequest(customer_id=customer_id, template=template)
    return await generate_cam(payload, db)


# ============================================================================
#  2. CAM RETRIEVE
# ============================================================================

@app.get(
    "/cam/{customer_id:int}",
    response_model=CAMRecordResponse,
    summary="Retrieve CAM",
    tags=["CAM"],
)
async def get_cam(customer_id: int, db: Session = Depends(get_db)):
    cam = db.query(CAMRecord).filter(CAMRecord.customer_id == customer_id).first()
    if not cam:
        raise HTTPException(status_code=404, detail=f"No CAM found for customer {customer_id}.")
    return cam


@app.get(
    "/cam/record/{cam_id:int}",
    response_model=CAMRecordResponse,
    summary="Retrieve CAM by CAM ID",
    tags=["CAM"],
)
async def get_cam_by_id(cam_id: int, db: Session = Depends(get_db)):
    cam = db.query(CAMRecord).filter(CAMRecord.id == cam_id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="CAM not found.")
    return cam


# ============================================================================
#  3. CAM REFRESH
# ============================================================================

@app.post(
    "/cam/refresh/{customer_id:int}",
    response_model=CAMRecordResponse,
    summary="Refresh CAM (Regenerate)",
    tags=["CAM"],
)
async def refresh_cam(
    customer_id: int,
    template: str = Query("IDBI_BANK"),
    db: Session = Depends(get_db),
):
    """Re-generate the CAM with current upstream intelligence."""
    payload = CAMGenerateRequest(customer_id=customer_id, template=template)
    return await generate_cam(payload, db)


# ============================================================================
#  4. CAM UPDATE (Section edit with version bump)
# ============================================================================

@app.put(
    "/cam/{cam_id:int}",
    response_model=CAMRecordResponse,
    summary="Update CAM Sections",
    tags=["CAM"],
)
async def update_cam(
    cam_id: int, payload: CAMUpdateRequest, db: Session = Depends(get_db)
):
    cam = db.query(CAMRecord).filter(CAMRecord.id == cam_id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="CAM not found.")

    cam.current_version += 1

    # Apply provided section updates
    update_fields = payload.model_dump(exclude={"edited_by", "change_summary"})
    for field, value in update_fields.items():
        if value is not None:
            setattr(cam, f"section_{field}" if not field.startswith("section_") else field, value)

    _snapshot_version(cam, db, edited_by=payload.edited_by,
                      change_summary=payload.change_summary)
    db.commit()
    db.refresh(cam)
    logger.info(f"AUDIT | CAM {cam_id} updated to v{cam.current_version}")
    return cam


# ============================================================================
#  5. DOWNLOAD – PDF, HTML, JSON
# ============================================================================

@app.get(
    "/cam/{cam_id:int}/download",
    summary="Download CAM",
    tags=["CAM"],
)
async def download_cam(
    cam_id: int,
    format: str = Query("json", description="json | html | pdf"),
    db: Session = Depends(get_db),
):
    cam = db.query(CAMRecord).filter(CAMRecord.id == cam_id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="CAM not found.")

    tmpl_key = cam.template or "IDBI_BANK"
    tmpl = TEMPLATES.get(tmpl_key, TEMPLATES["GENERIC"])

    if format.lower() == "json":
        _publish("CAM Exported", cam.customer_id, {"cam_id": cam_id, "format": "json"})
        return {
            "cam_reference": cam.cam_reference,
            "customer_id": cam.customer_id,
            "status": cam.status,
            "version": cam.current_version,
            "template": cam.template,
            "scoring": {
                "overall_credit_score": cam.overall_credit_score,
                "financial_health_rating": cam.financial_health_rating,
                "risk_grade": cam.risk_grade,
                "fraud_status": cam.fraud_status,
                "eligibility_status": cam.eligibility_status,
                "recommended_loan_amount": cam.recommended_loan_amount,
                "recommended_interest_rate": cam.recommended_interest_rate,
                "recommended_tenure_months": cam.recommended_tenure_months,
            },
            "narratives": {
                "customer_strengths": cam.narrative_customer_strengths,
                "business_strengths": cam.narrative_business_strengths,
                "financial_observations": cam.narrative_financial_observations,
                "key_risks": cam.narrative_key_risks,
                "mitigating_factors": cam.narrative_mitigating_factors,
                "lending_recommendation": cam.narrative_lending_recommendation,
                "monitoring_actions": cam.narrative_monitoring_actions,
            },
            "sections": {
                "executive_summary": cam.section_executive_summary,
                "applicant_profile": cam.section_applicant_profile,
                "business_profile": cam.section_business_profile,
                "loan_requirement": cam.section_loan_requirement,
                "identity_verification": cam.section_identity_verification,
                "gst_compliance": cam.section_gst_compliance,
                "banking_behaviour": cam.section_banking_behaviour,
                "workforce_stability": cam.section_workforce_stability,
                "corporate_governance": cam.section_corporate_governance,
                "fhc_summary": cam.section_fhc_summary,
                "credit_decision": cam.section_credit_decision,
                "fraud_screening": cam.section_fraud_screening,
                "ocen_marketplace": cam.section_ocen_marketplace,
                "recommended_offer": cam.section_recommended_offer,
                "key_risks": cam.section_key_risks,
                "risk_mitigation": cam.section_risk_mitigation,
                "banker_recommendation": cam.section_banker_recommendation,
                "approval_matrix": cam.section_approval_matrix,
            },
        }

    if format.lower() == "html":
        html = _build_html(cam, tmpl)
        _publish("CAM Exported", cam.customer_id, {"cam_id": cam_id, "format": "html"})
        return HTMLResponse(
            content=html,
            headers={"Content-Disposition": f"attachment; filename=CAM_{cam.cam_reference}.html"},
        )

    if format.lower() == "pdf":
        pdf = _build_pdf_stub(cam, tmpl)
        _publish("CAM Exported", cam.customer_id, {"cam_id": cam_id, "format": "pdf"})
        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=CAM_{cam.cam_reference}.pdf"},
        )

    raise HTTPException(status_code=400, detail="Unsupported format. Use 'json', 'html', or 'pdf'.")


@app.get(
    "/cam/{cam_id:int}/export/json",
    summary="Export CAM JSON",
    tags=["CAM"],
)
async def export_cam_json(cam_id: int, db: Session = Depends(get_db)):
    return await download_cam(cam_id=cam_id, format="json", db=db)


# ============================================================================
#  6. APPROVAL WORKFLOW
# ============================================================================

@app.post(
    "/cam/{cam_id:int}/approve",
    response_model=CAMRecordResponse,
    summary="Approve / Reject CAM",
    tags=["Approval"],
)
async def approve_cam(
    cam_id: int, payload: CAMApprovalRequest, db: Session = Depends(get_db)
):
    cam = db.query(CAMRecord).filter(CAMRecord.id == cam_id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="CAM not found.")

    db.add(CAMApprovalLog(
        cam_id=cam.id,
        approver_id=payload.approver_id,
        approver_role=payload.approver_role,
        action=payload.action.upper(),
        level=payload.level,
        comments=payload.comments,
    ))

    if payload.action.upper() == "APPROVED":
        cam.status = "APPROVED"
        _publish("CAM Approved", cam.customer_id, {"cam_id": cam_id, "approver": payload.approver_id})
    elif payload.action.upper() in ("REJECTED", "DECLINED"):
        cam.status = "REJECTED"
    elif payload.action.upper() == "RETURNED":
        cam.status = "PENDING_APPROVAL"
    else:
        cam.status = payload.action.upper()

    db.commit()
    db.refresh(cam)
    logger.info(f"AUDIT | CAM {cam_id} approved/actioned | Status: {cam.status}")
    return cam


@app.get(
    "/cam/{cam_id:int}/approvals",
    response_model=List[ApprovalLogResponse],
    summary="Get Approval Trail",
    tags=["Approval"],
)
async def get_approvals(cam_id: int, db: Session = Depends(get_db)):
    return db.query(CAMApprovalLog).filter(CAMApprovalLog.cam_id == cam_id).all()


# ============================================================================
#  7. VERSION HISTORY & COMPARISON
# ============================================================================

@app.get(
    "/cam/{cam_id:int}/versions",
    response_model=List[CAMVersionResponse],
    summary="Version History",
    tags=["Versions"],
)
async def get_versions(cam_id: int, db: Session = Depends(get_db)):
    return db.query(CAMVersion).filter(CAMVersion.cam_id == cam_id).order_by(CAMVersion.version_num).all()


@app.get(
    "/cam/{cam_id:int}/compare",
    response_model=VersionCompareResponse,
    summary="Compare Two CAM Versions",
    tags=["Versions"],
)
async def compare_versions(
    cam_id: int,
    v_a: int = Query(..., description="Version A number"),
    v_b: int = Query(..., description="Version B number"),
    db: Session = Depends(get_db),
):
    va = db.query(CAMVersion).filter(CAMVersion.cam_id == cam_id, CAMVersion.version_num == v_a).first()
    vb = db.query(CAMVersion).filter(CAMVersion.cam_id == cam_id, CAMVersion.version_num == v_b).first()
    if not va or not vb:
        raise HTTPException(status_code=404, detail="One or both versions not found.")

    compare_fields = [
        "section_executive_summary", "section_banker_recommendation",
        "section_recommended_offer", "section_key_risks", "overall_credit_score", "status",
    ]
    diffs = []
    for f in compare_fields:
        a_val = str(getattr(va, f, "") or "")
        b_val = str(getattr(vb, f, "") or "")
        diffs.append(VersionDiff(
            field=f,
            version_a=a_val[:200],
            version_b=b_val[:200],
            changed=a_val != b_val,
        ))

    return VersionCompareResponse(
        cam_id=cam_id,
        version_a=v_a,
        version_b=v_b,
        diffs=diffs,
        total_changes=sum(1 for d in diffs if d.changed),
    )


# ============================================================================
#  8. DASHBOARD
# ============================================================================

@app.get(
    "/cam/dashboard/summary",
    response_model=CAMDashboardResponse,
    summary="CAM Dashboard",
    tags=["Dashboard"],
)
async def cam_dashboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    all_cams = db.query(CAMRecord).all()
    scores = [c.overall_credit_score for c in all_cams if c.overall_credit_score]
    recent = sorted(all_cams, key=lambda c: c.created_at, reverse=True)[:limit]

    return CAMDashboardResponse(
        total_cams=len(all_cams),
        draft=sum(1 for c in all_cams if c.status == "DRAFT"),
        pending_approval=sum(1 for c in all_cams if c.status == "PENDING_APPROVAL"),
        approved=sum(1 for c in all_cams if c.status == "APPROVED"),
        rejected=sum(1 for c in all_cams if c.status == "REJECTED"),
        archived=sum(1 for c in all_cams if c.status == "ARCHIVED"),
        avg_credit_score=round(sum(scores) / len(scores), 2) if scores else 0.0,
        recent_cams=recent,
    )


# ============================================================================
#  9. TEMPLATES
# ============================================================================

@app.get(
    "/cam/templates",
    response_model=List[TemplateResponse],
    summary="List CAM Templates",
    tags=["Templates"],
)
async def list_templates(db: Session = Depends(get_db)):
    return db.query(CAMTemplate).filter(CAMTemplate.is_active == True).all()


@app.get(
    "/cam/templates/{template_key}",
    response_model=TemplateResponse,
    summary="Get Template Details",
    tags=["Templates"],
)
async def get_template(template_key: str, db: Session = Depends(get_db)):
    t = db.query(CAMTemplate).filter(CAMTemplate.template_key == template_key).first()
    if not t:
        raise HTTPException(status_code=404, detail=f"Template '{template_key}' not found.")
    return t


# ============================================================================
#  10. ADMIN
# ============================================================================

@app.post(
    "/cam/{cam_id:int}/archive",
    response_model=CAMRecordResponse,
    summary="Archive CAM",
    tags=["Admin"],
)
async def archive_cam(cam_id: int, db: Session = Depends(get_db)):
    cam = db.query(CAMRecord).filter(CAMRecord.id == cam_id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="CAM not found.")
    cam.status = "ARCHIVED"
    db.commit()
    db.refresh(cam)
    return cam


@app.get(
    "/cam/admin/config",
    response_model=CAMConfigResponse,
    summary="Get CAM Config",
    tags=["Admin"],
)
async def get_cam_config(db: Session = Depends(get_db)):
    cfg = _get_config(db)
    return CAMConfigResponse(
        default_template=cfg.default_template,
        auto_generate_on_ocen=cfg.auto_generate_on_ocen,
        require_fraud_clear=cfg.require_fraud_clear,
        sections_enabled=json.loads(cfg.sections_enabled or "[]"),
    )


@app.post(
    "/cam/admin/config",
    summary="Update CAM Config",
    tags=["Admin"],
)
async def update_cam_config(
    default_template: str = Body(...),
    auto_generate: bool = Body(True),
    require_fraud_clear: bool = Body(True),
    db: Session = Depends(get_db),
):
    cfg = _get_config(db)
    cfg.default_template = default_template
    cfg.auto_generate_on_ocen = auto_generate
    cfg.require_fraud_clear = require_fraud_clear
    db.commit()
    return {"message": "Config updated."}


@app.post(
    "/cam/admin/sections",
    response_model=CAMConfigResponse,
    summary="Configure CAM Sections",
    tags=["Admin"],
)
async def configure_cam_sections(
    sections_enabled: List[str] = Body(...),
    db: Session = Depends(get_db),
):
    unknown = [section for section in sections_enabled if section not in ALL_SECTIONS]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown CAM sections: {unknown}")
    cfg = _get_config(db)
    cfg.sections_enabled = json.dumps(sections_enabled)
    db.commit()
    return CAMConfigResponse(
        default_template=cfg.default_template,
        auto_generate_on_ocen=cfg.auto_generate_on_ocen,
        require_fraud_clear=cfg.require_fraud_clear,
        sections_enabled=sections_enabled,
    )


@app.put(
    "/cam/admin/templates/{template_key}",
    response_model=TemplateResponse,
    summary="Configure Bank Branding",
    tags=["Admin"],
)
async def update_template_branding(
    template_key: str,
    template_name: Optional[str] = Body(None),
    bank_name: Optional[str] = Body(None),
    color_primary: Optional[str] = Body(None),
    color_secondary: Optional[str] = Body(None),
    is_active: Optional[bool] = Body(None),
    db: Session = Depends(get_db),
):
    template = db.query(CAMTemplate).filter(CAMTemplate.template_key == template_key).first()
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_key}' not found.")
    for field, value in {
        "template_name": template_name,
        "bank_name": bank_name,
        "color_primary": color_primary,
        "color_secondary": color_secondary,
        "is_active": is_active,
    }.items():
        if value is not None:
            setattr(template, field, value)
    db.commit()
    db.refresh(template)
    return template


@app.post(
    "/cam/admin/narrative-templates",
    summary="Edit Narrative Templates",
    tags=["Admin"],
)
async def update_narrative_templates(templates: Dict[str, str] = Body(...)):
    # Narrative persistence can later move to a dedicated table; the API contract is stable now.
    return {"message": "Narrative templates accepted.", "templates": templates}


@app.get(
    "/cam/workflow/ocen-trigger/{customer_id:int}",
    response_model=CAMRecordResponse,
    summary="OCEN → CAM Auto-Trigger",
    tags=["Workflow Integration"],
)
async def ocen_trigger_cam(
    customer_id: int,
    template: str = Query("IDBI_BANK"),
    db: Session = Depends(get_db),
):
    """Called automatically after OCEN marketplace completes for a customer."""
    payload = CAMGenerateRequest(customer_id=customer_id, template=template)
    return await generate_cam(payload, db)


@app.get(
    "/cam/workflow/executive-feed",
    summary="Executive Dashboard Feed",
    tags=["Workflow Integration"],
)
async def executive_feed(db: Session = Depends(get_db)):
    all_cams = db.query(CAMRecord).all()
    return {
        "total_cams": len(all_cams),
        "approved": sum(1 for c in all_cams if c.status == "APPROVED"),
        "pending": sum(1 for c in all_cams if c.status == "PENDING_APPROVAL"),
        "avg_credit_score": round(
            sum(c.overall_credit_score for c in all_cams if c.overall_credit_score)
            / max(1, sum(1 for c in all_cams if c.overall_credit_score)), 2
        ),
        "total_recommended_value": sum(
            c.recommended_loan_amount for c in all_cams
            if c.recommended_loan_amount and c.status == "APPROVED"
        ),
    }


# ============================================================================
#  HEALTH
# ============================================================================

@app.get("/livez", summary="Liveness", tags=["Health"])
async def livez():
    return {"status": "UP", "service": "cam-service", "version": "2.0.0"}


@app.get("/readyz", summary="Readiness", tags=["Health"])
async def readyz(db: Session = Depends(get_db)):
    try:
        db.query(CAMRecord).first()
        return {"status": "READY"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"DB not ready: {exc}")
