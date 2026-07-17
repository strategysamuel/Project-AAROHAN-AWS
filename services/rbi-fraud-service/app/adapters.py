"""
RBI Fraud Registry – Adapter Strategy Pattern
----------------------------------------------
Provides three interchangeable adapters:
  SimulationAdapter  – deterministic dataset-driven simulation
  SandboxAdapter     – delegates to simulation, stamps sandbox identifier
  ProductionAdapter  – future integration surface with real RBI CFR API

AML risk scoring, all five fraud categories, and configurable rule
thresholds are implemented entirely inside SimulationAdapter so that
every adapter benefits consistently.
"""
import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models import (
    FraudWatchlist, OnboardingCustomer, OnboardingBusiness,
    CKYCVerificationLog, AAAnalytics, MCAGovernanceAnalytics
)

logger = logging.getLogger("rbi-fraud-service.adapters")

# ---------------------------------------------------------------------------
# Fraud Rule Definitions (configurable via rule_params)
# ---------------------------------------------------------------------------
# Key                   Default   Meaning
# ─────────────────────────────────────────────────────────────────────────
# identity_threshold      80.0    CKYC match confidence below which
#                                  IDENTITY_MISMATCH flag is raised
# gst_delay_threshold     10      (reserved for future GST rule)
# aml_threshold           40.0    Minimum fraud_score to elevate AML risk
# critical_blacklist_cat  True    Blacklisted entity always → Critical
# ---------------------------------------------------------------------------

DEFAULT_RULE_PARAMS: Dict[str, Any] = {
    "identity_threshold": 80.0,
    "gst_delay_threshold": 10,
    "aml_threshold": 40.0,
    "critical_blacklist_cat": True,
}


# ---------------------------------------------------------------------------
# Helper: derive risk level from score
# ---------------------------------------------------------------------------

def _score_to_risk(score: float) -> str:
    if score >= 75.0:
        return "Critical"
    if score >= 55.0:
        return "High"
    if score >= 30.0:
        return "Medium"
    return "Low"


# ---------------------------------------------------------------------------
# Helper: AML risk narrative
# ---------------------------------------------------------------------------

def _aml_assessment(fraud_score: float, risk_flags: list, rule_params: Dict) -> str:
    aml_threshold = rule_params.get("aml_threshold", 40.0)
    if fraud_score >= 75.0:
        return "AML Risk: CRITICAL – transaction laundering pattern suspected; escalate to FIU-IND."
    if fraud_score >= aml_threshold:
        return "AML Risk: HIGH – structured cash-flow anomalies detected; manual AML review required."
    if "SUSPICIOUS_BANKING" in risk_flags:
        return "AML Risk: MEDIUM – irregular banking behaviour; monitor for STR filing."
    return "AML Risk: LOW – no money-laundering indicators detected."


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class BaseFraudAdapter:
    def verify(
        self,
        entity_type: str,
        entity_value: str,
        customer_id: int,
        db: Session,
        rule_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Simulation Adapter
# ---------------------------------------------------------------------------

class SimulationAdapter(BaseFraudAdapter):
    """
    Deterministic fraud-screening simulation that exercises all fraud rules
    against the Enterprise Simulation Dataset stored in the shared SQLite
    database.

    Rules implemented
    -----------------
    Rule A – Watchlist / Blacklist Match          → Critical fraud score 95
    Rule B – Repeated identity mismatch (CKYC)    → High risk 65
    Rule C – Suspicious banking pattern (AA)      → Medium risk 45
    Rule D – Director linked to fraud (MCA)       → High risk 75
    Rule E – Multiple flagged businesses          → Critical risk 80
    AML    – Derived from aggregate fraud score
    """

    def verify(
        self,
        entity_type: str,
        entity_value: str,
        customer_id: int,
        db: Session,
        rule_params: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            f"SimulationAdapter | entity_type={entity_type} | value={entity_value} | cid={customer_id}"
        )

        identity_threshold = rule_params.get("identity_threshold", 80.0)

        # ── Initialise accumulators ──────────────────────────────────────
        fraud_score = 0.0
        fraud_category = "None"
        risk_level = "Low"
        risk_flags: list = []
        ai_insights: list = []

        # ── Rule A: Watchlist / Blacklist Match ──────────────────────────
        wl_entry = (
            db.query(FraudWatchlist)
            .filter(FraudWatchlist.value == entity_value)
            .first()
        )
        is_blacklisted = wl_entry is not None

        if is_blacklisted:
            fraud_score = 95.0
            fraud_category = (
                "Identity Fraud" if entity_type in ("PAN", "DIRECTOR") else "Financial Fraud"
            )
            risk_level = "Critical"
            risk_flags.append("BLACK_LIST_MATCH")
            ai_insights.append(
                f"Entity matched RBI Central Fraud Registry blacklist record: {wl_entry.reason}."
            )

        # ── Rule B: Repeated identity mismatch (CKYC) ───────────────────
        ckyc_log = (
            db.query(CKYCVerificationLog)
            .filter(CKYCVerificationLog.customer_id == customer_id)
            .first()
        )
        if ckyc_log:
            if ckyc_log.match_confidence < identity_threshold or ckyc_log.anomaly_detected:
                prev = fraud_score
                fraud_score = max(fraud_score, 65.0)
                if fraud_score > prev:
                    fraud_category = "Identity Fraud"
                risk_flags.append("IDENTITY_MISMATCH")
                ai_insights.append(
                    "Repeated identity mismatch flagged by CKYC Verification service; "
                    f"match confidence {ckyc_log.match_confidence:.1f}% below threshold "
                    f"{identity_threshold:.1f}%."
                )
                if risk_level not in ("Critical",):
                    risk_level = "High"

        # ── Rule C: Suspicious banking pattern (Account Aggregator) ─────
        aa_anal = (
            db.query(AAAnalytics)
            .filter(AAAnalytics.customer_id == customer_id)
            .first()
        )
        if aa_anal:
            if aa_anal.cheque_bounce_indicator or aa_anal.overdraft_usage == "Frequent":
                prev = fraud_score
                fraud_score = max(fraud_score, 45.0)
                if fraud_score > prev and fraud_category == "None":
                    fraud_category = "Transaction Fraud"
                risk_flags.append("SUSPICIOUS_BANKING")
                ai_insights.append(
                    "Suspicious transaction activity detected: "
                    + ("cheque bounce history, " if aa_anal.cheque_bounce_indicator else "")
                    + ("frequent overdraft usage." if aa_anal.overdraft_usage == "Frequent" else ".")
                )
                if risk_level == "Low":
                    risk_level = "Medium"

        # ── Rule D: Director linked to fraud (MCA Governance) ───────────
        mca_anal = db.query(MCAGovernanceAnalytics).first()
        if mca_anal and mca_anal.overall_risk_level == "Critical":
            prev = fraud_score
            fraud_score = max(fraud_score, 75.0)
            if fraud_score > prev:
                fraud_category = "Corporate Fraud"
            risk_flags.append("DIRECTOR_LINKED_FRAUD")
            ai_insights.append(
                "Board member shares associations with flagged corporate shell entities; "
                "MCA governance risk rated Critical."
            )
            if risk_level not in ("Critical",):
                risk_level = "High"

        # ── Rule E: Multiple linked fraudulent businesses ────────────────
        biz = (
            db.query(OnboardingBusiness)
            .filter(OnboardingBusiness.customer_id == customer_id)
            .all()
        )
        blacklisted_biz = 0
        for b in biz:
            if b.gstin and db.query(FraudWatchlist).filter(FraudWatchlist.value == b.gstin).first():
                blacklisted_biz += 1
        if blacklisted_biz >= 2:
            fraud_score = max(fraud_score, 80.0)
            risk_level = "Critical"
            fraud_category = "Corporate Fraud"
            risk_flags.append("MULTI_ENTITY_FRAUD")
            ai_insights.append(
                f"Customer linked to {blacklisted_biz} businesses with blacklisted GSTINs; "
                "multiple fraudulent entity network detected."
            )

        # ── Document Fraud (Document entity type) ────────────────────────
        if entity_type == "DOCUMENT" and is_blacklisted:
            fraud_category = "Document Fraud"
            risk_flags.append("DOCUMENT_FRAUD")
            ai_insights.append("Submitted document identity flagged in fraud registry.")

        # ── AML risk assessment ──────────────────────────────────────────
        aml_note = _aml_assessment(fraud_score, risk_flags, rule_params)
        ai_insights.append(aml_note)

        # ── Clean-slate narrative ────────────────────────────────────────
        if not any(f for f in risk_flags if f != "CLEAN"):
            ai_insights.insert(
                0, "No fraud indicators detected. Strong identity consistency observed."
            )

        # ── Consolidate ──────────────────────────────────────────────────
        risk_level = _score_to_risk(fraud_score)
        insights_str = " | ".join(ai_insights)
        flags_str = ",".join(risk_flags) if risk_flags else "CLEAN"

        return {
            "is_blacklisted": is_blacklisted,
            "fraud_score": round(fraud_score, 2),
            "fraud_category": fraud_category,
            "risk_level": risk_level,
            "risk_flags": flags_str,
            "ai_insights": insights_str,
        }


# ---------------------------------------------------------------------------
# Sandbox Adapter
# ---------------------------------------------------------------------------

class SandboxAdapter(BaseFraudAdapter):
    """
    Runs simulation logic then overwrites ai_insights with an explicit
    'Sandbox API Mock' marker so callers can identify the adapter in use.
    """

    def verify(
        self,
        entity_type: str,
        entity_value: str,
        customer_id: int,
        db: Session,
        rule_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        logger.info(
            f"SandboxAdapter | entity_type={entity_type} | value={entity_value} | cid={customer_id}"
        )
        res = SimulationAdapter().verify(entity_type, entity_value, customer_id, db, rule_params)
        res["ai_insights"] = "Sandbox API Mock"
        return res


# ---------------------------------------------------------------------------
# Production Adapter (interface stub)
# ---------------------------------------------------------------------------

class ProductionAdapter(BaseFraudAdapter):
    """
    Production integration stub.  Replace the body of verify() with the
    official RBI Central Fraud Registry client call when available.
    The method signature and return contract remain unchanged so that no
    business-logic modifications are required.
    """

    def verify(
        self,
        entity_type: str,
        entity_value: str,
        customer_id: int,
        db: Session,
        rule_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        logger.info(
            f"ProductionAdapter | entity_type={entity_type} | value={entity_value} | cid={customer_id}"
        )
        # Delegate to simulation until production integration is active
        return SimulationAdapter().verify(entity_type, entity_value, customer_id, db, rule_params)
