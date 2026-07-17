"""
OCEN Marketplace – Matching Engine Adapters
============================================
Strategy pattern: SimulationAdapter / SandboxAdapter / ProductionAdapter

The SimulationAdapter implements the full deterministic matching engine:
  • Score-based lender eligibility (0–100 match score)
  • Interest rate calculation (risk-adjusted)
  • EMI computation (reducing balance)
  • Approval probability (function of FHC score + credit decision)
  • Explainable recommendations per offer
  • Offer ranking (best match score first)
"""
import json
import logging
import math
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ocen-uli-service.adapters")

# ---------------------------------------------------------------------------
# Default matching parameters (configurable via /ocen/config)
# ---------------------------------------------------------------------------
DEFAULT_MATCH_PARAMS: Dict[str, Any] = {
    "fhc_weight": 0.35,               # FHC score contribution to match score
    "credit_decision_weight": 0.30,   # Credit engine decision contribution
    "fraud_weight": 0.20,             # Fraud cleanliness contribution
    "loan_size_weight": 0.15,         # Loan-size feasibility contribution
    "min_fhc_for_approval": 55.0,     # Minimum FHC composite score
    "fraud_critical_block": True,     # Block if fraud_risk_level == Critical
}

# ---------------------------------------------------------------------------
# Simulated 10-lender registry (seeds database on startup)
# ---------------------------------------------------------------------------
LENDER_SEED_DATA = [
    {
        "lender_id": "LEND-IDBI-001",
        "name": "IDBI Bank – MSME Division",
        "lender_type": "BANK",
        "base_interest_rate": 8.75,
        "max_interest_rate": 12.50,
        "max_loan_amount": 10_000_000.0,
        "min_loan_amount": 100_000.0,
        "min_credit_score": 700,
        "processing_fee_pct": 0.5,
        "max_tenure_months": 84,
        "min_tenure_months": 12,
        "risk_appetite": "MEDIUM",
        "collateral_required": False,
        "preferred_industries": "Manufacturing,Trading,Services",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 5,
        "loan_products": "Working Capital Loan,Term Loan,Machinery Loan",
        "women_entrepreneur_scheme": True,
        "startup_friendly": False,
    },
    {
        "lender_id": "LEND-HDFC-001",
        "name": "HDFC Bank – Business Banking",
        "lender_type": "BANK",
        "base_interest_rate": 9.25,
        "max_interest_rate": 14.00,
        "max_loan_amount": 7_500_000.0,
        "min_loan_amount": 200_000.0,
        "min_credit_score": 680,
        "processing_fee_pct": 1.0,
        "max_tenure_months": 60,
        "min_tenure_months": 12,
        "risk_appetite": "MEDIUM",
        "collateral_required": False,
        "preferred_industries": "ALL",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 3,
        "loan_products": "Working Capital Loan,Term Loan,Invoice Financing",
        "women_entrepreneur_scheme": True,
        "startup_friendly": True,
    },
    {
        "lender_id": "LEND-SBI-001",
        "name": "State Bank of India – SME Finance",
        "lender_type": "BANK",
        "base_interest_rate": 8.50,
        "max_interest_rate": 11.00,
        "max_loan_amount": 25_000_000.0,
        "min_loan_amount": 500_000.0,
        "min_credit_score": 720,
        "processing_fee_pct": 0.35,
        "max_tenure_months": 120,
        "min_tenure_months": 12,
        "risk_appetite": "LOW",
        "collateral_required": True,
        "preferred_industries": "Manufacturing,Agriculture,Export",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 10,
        "loan_products": "Term Loan,Machinery Loan,Agriculture Loan,Export Finance",
        "women_entrepreneur_scheme": True,
        "startup_friendly": False,
    },
    {
        "lender_id": "LEND-TATA-001",
        "name": "Tata Capital – SME Lending",
        "lender_type": "NBFC",
        "base_interest_rate": 11.00,
        "max_interest_rate": 16.00,
        "max_loan_amount": 5_000_000.0,
        "min_loan_amount": 100_000.0,
        "min_credit_score": 650,
        "processing_fee_pct": 1.5,
        "max_tenure_months": 60,
        "min_tenure_months": 6,
        "risk_appetite": "HIGH",
        "collateral_required": False,
        "preferred_industries": "ALL",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 2,
        "loan_products": "Working Capital Loan,Term Loan,Supply Chain Finance",
        "women_entrepreneur_scheme": False,
        "startup_friendly": True,
    },
    {
        "lender_id": "LEND-BAJAJ-001",
        "name": "Bajaj Finserv – Business Loan",
        "lender_type": "NBFC",
        "base_interest_rate": 12.00,
        "max_interest_rate": 18.00,
        "max_loan_amount": 3_500_000.0,
        "min_loan_amount": 50_000.0,
        "min_credit_score": 620,
        "processing_fee_pct": 2.0,
        "max_tenure_months": 48,
        "min_tenure_months": 6,
        "risk_appetite": "HIGH",
        "collateral_required": False,
        "preferred_industries": "ALL",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 1,
        "loan_products": "Working Capital Loan,Emergency Credit Line,Women Entrepreneur Loan",
        "women_entrepreneur_scheme": True,
        "startup_friendly": True,
    },
    {
        "lender_id": "LEND-KOTAK-001",
        "name": "Kotak Mahindra Bank – Business Credit",
        "lender_type": "BANK",
        "base_interest_rate": 9.75,
        "max_interest_rate": 13.50,
        "max_loan_amount": 6_000_000.0,
        "min_loan_amount": 150_000.0,
        "min_credit_score": 690,
        "processing_fee_pct": 1.0,
        "max_tenure_months": 72,
        "min_tenure_months": 12,
        "risk_appetite": "MEDIUM",
        "collateral_required": False,
        "preferred_industries": "Trading,Services,Technology",
        "geographic_coverage": "Metro,Tier1",
        "tat_days": 4,
        "loan_products": "Working Capital Loan,Invoice Financing,Supply Chain Finance",
        "women_entrepreneur_scheme": False,
        "startup_friendly": True,
    },
    {
        "lender_id": "LEND-SIDBI-001",
        "name": "SIDBI – MSME Credit Line",
        "lender_type": "BANK",
        "base_interest_rate": 7.75,
        "max_interest_rate": 10.00,
        "max_loan_amount": 20_000_000.0,
        "min_loan_amount": 250_000.0,
        "min_credit_score": 700,
        "processing_fee_pct": 0.25,
        "max_tenure_months": 84,
        "min_tenure_months": 12,
        "risk_appetite": "LOW",
        "collateral_required": False,
        "preferred_industries": "Manufacturing,Handicrafts,Agriculture",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 7,
        "loan_products": "Term Loan,Machinery Loan,Women Entrepreneur Loan,Startup Loan",
        "women_entrepreneur_scheme": True,
        "startup_friendly": True,
    },
    {
        "lender_id": "LEND-FLEX-001",
        "name": "FlexiLoans – Digital NBFC",
        "lender_type": "FINTECH",
        "base_interest_rate": 13.50,
        "max_interest_rate": 20.00,
        "max_loan_amount": 2_000_000.0,
        "min_loan_amount": 25_000.0,
        "min_credit_score": 580,
        "processing_fee_pct": 2.5,
        "max_tenure_months": 24,
        "min_tenure_months": 3,
        "risk_appetite": "HIGH",
        "collateral_required": False,
        "preferred_industries": "ALL",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 1,
        "loan_products": "Working Capital Loan,Emergency Credit Line,Invoice Financing",
        "women_entrepreneur_scheme": False,
        "startup_friendly": True,
    },
    {
        "lender_id": "LEND-MUDRA-001",
        "name": "MUDRA – Tarun Scheme",
        "lender_type": "MFI",
        "base_interest_rate": 9.00,
        "max_interest_rate": 12.00,
        "max_loan_amount": 1_000_000.0,
        "min_loan_amount": 50_000.0,
        "min_credit_score": 600,
        "processing_fee_pct": 0.50,
        "max_tenure_months": 60,
        "min_tenure_months": 12,
        "risk_appetite": "MEDIUM",
        "collateral_required": False,
        "preferred_industries": "ALL",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 5,
        "loan_products": "Working Capital Loan,Women Entrepreneur Loan,Agriculture Loan",
        "women_entrepreneur_scheme": True,
        "startup_friendly": True,
    },
    {
        "lender_id": "LEND-IIFL-001",
        "name": "IIFL Finance – SME Division",
        "lender_type": "NBFC",
        "base_interest_rate": 12.50,
        "max_interest_rate": 17.50,
        "max_loan_amount": 4_000_000.0,
        "min_loan_amount": 100_000.0,
        "min_credit_score": 640,
        "processing_fee_pct": 1.75,
        "max_tenure_months": 48,
        "min_tenure_months": 6,
        "risk_appetite": "HIGH",
        "collateral_required": False,
        "preferred_industries": "ALL",
        "geographic_coverage": "PAN_INDIA",
        "tat_days": 2,
        "loan_products": "Working Capital Loan,Term Loan,Supply Chain Finance,Startup Loan",
        "women_entrepreneur_scheme": False,
        "startup_friendly": True,
    },
]

LOAN_PRODUCTS_SEED = [
    ("WCL", "Working Capital Loan", "Short-term finance for day-to-day operations"),
    ("TERM", "Term Loan", "Medium/long-term capital expenditure funding"),
    ("MACH", "Machinery Loan", "Equipment and machinery procurement finance"),
    ("INV", "Invoice Financing", "Receivables-backed working capital"),
    ("SCF", "Supply Chain Finance", "Vendor/buyer credit in supply chain"),
    ("EXP", "Export Finance", "Pre/post-shipment export credit"),
    ("WEL", "Women Entrepreneur Loan", "Preferential scheme for women-led MSMEs"),
    ("STL", "Startup Loan", "Early-stage business credit for registered startups"),
    ("AGRI", "Agriculture Loan", "Agri-allied and allied processing units"),
    ("ECL", "Emergency Credit Line", "Emergency liquidity for distressed businesses"),
]

# ---------------------------------------------------------------------------
# EMI Calculator (reducing-balance method)
# ---------------------------------------------------------------------------

def calculate_emi(principal: float, annual_rate: float, months: int) -> float:
    """Standard reducing-balance EMI formula."""
    if annual_rate == 0 or months == 0:
        return round(principal / max(months, 1), 2)
    r = annual_rate / (12 * 100)
    emi = principal * r * math.pow(1 + r, months) / (math.pow(1 + r, months) - 1)
    return round(emi, 2)


# ---------------------------------------------------------------------------
# Base adapter
# ---------------------------------------------------------------------------

class BaseMatchingAdapter:
    def search_eligible_lenders(self, lenders, params: Dict) -> List[Dict]:
        raise NotImplementedError

    def generate_offers(self, application, lenders, params: Dict) -> List[Dict]:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Simulation Adapter – full deterministic matching engine
# ---------------------------------------------------------------------------

class SimulationAdapter(BaseMatchingAdapter):
    """
    Deterministic marketplace matching engine.

    Match Score Components
    ───────────────────────
    FHC Score (0–100)         × fhc_weight (0.35)
    Credit Decision           × credit_decision_weight (0.30)
      APPROVE  → 100
      CONDITIONAL → 65
      REJECT  → 20
    Fraud Cleanliness         × fraud_weight (0.20)
      Low  → 100 · Medium → 70 · High → 30 · Critical → 0
    Loan-size feasibility     × loan_size_weight (0.15)
      requested / max_loan × 100 capped at 100

    Eligibility Gates (hard blocks)
    ─────────────────────────────────
    • fraud_risk_level == Critical → BLOCKED
    • credit_decision == REJECT  → BLOCKED
    • requested_amount > max_loan_amount → BLOCKED
    • requested_amount < min_loan_amount → BLOCKED
    • requested_tenure > max_tenure      → BLOCKED
    """

    def _fraud_score_component(self, fraud_risk: str) -> float:
        return {"Low": 100.0, "Medium": 70.0, "High": 30.0, "Critical": 0.0}.get(
            fraud_risk, 50.0
        )

    def _credit_decision_component(self, credit_decision: Optional[str]) -> float:
        if not credit_decision:
            return 65.0
        return {"APPROVE": 100.0, "CONDITIONAL": 65.0, "REJECT": 20.0}.get(
            credit_decision.upper(), 65.0
        )

    def _compute_match_score(
        self,
        lender,
        fhc_score: float,
        credit_decision: Optional[str],
        fraud_risk: str,
        requested_amount: float,
        params: Dict,
    ) -> float:
        fhc_w = params.get("fhc_weight", 0.35)
        cd_w = params.get("credit_decision_weight", 0.30)
        fraud_w = params.get("fraud_weight", 0.20)
        size_w = params.get("loan_size_weight", 0.15)

        fhc_component = min(fhc_score or 50.0, 100.0)
        cd_component = self._credit_decision_component(credit_decision)
        fraud_component = self._fraud_score_component(fraud_risk)
        size_pct = min((requested_amount / max(lender.max_loan_amount, 1)) * 100, 100)
        # Prefer mid-range loans (not too close to ceiling)
        size_component = max(100 - size_pct, 20.0)

        # Lender-specific bonus
        bonus = 0.0
        if lender.risk_appetite == "HIGH":
            bonus += 5.0
        if not lender.collateral_required:
            bonus += 3.0
        if lender.tat_days <= 2:
            bonus += 2.0

        raw = (
            fhc_component * fhc_w
            + cd_component * cd_w
            + fraud_component * fraud_w
            + size_component * size_w
            + bonus
        )
        return round(min(raw, 100.0), 2)

    def _is_eligible(
        self,
        lender,
        requested_amount: float,
        requested_tenure: int,
        credit_decision: Optional[str],
        fraud_risk: str,
        product_type: str,
        params: Dict,
    ) -> tuple[bool, List[str]]:
        reasons = []
        block = params.get("fraud_critical_block", True)

        if block and fraud_risk == "Critical":
            reasons.append("Blocked: Fraud risk level is Critical.")
        if credit_decision and credit_decision.upper() == "REJECT":
            reasons.append("Blocked: Credit decision is REJECT.")
        if requested_amount > lender.max_loan_amount:
            reasons.append(
                f"Requested ₹{requested_amount:,.0f} exceeds lender cap ₹{lender.max_loan_amount:,.0f}."
            )
        if requested_amount < lender.min_loan_amount:
            reasons.append(
                f"Requested ₹{requested_amount:,.0f} below lender floor ₹{lender.min_loan_amount:,.0f}."
            )
        if requested_tenure > lender.max_tenure_months:
            reasons.append(
                f"Tenure {requested_tenure}m exceeds lender maximum {lender.max_tenure_months}m."
            )
        if product_type and lender.loan_products and product_type not in lender.loan_products:
            reasons.append(f"Lender does not offer '{product_type}'.")

        return len(reasons) == 0, reasons

    def _risk_adjusted_rate(
        self, lender, fhc_score: float, fraud_risk: str
    ) -> float:
        """
        Risk-adjust the lender's base rate upward for higher-risk profiles.
        Cap at lender's max_interest_rate.
        """
        spread = 0.0
        if fhc_score < 40:
            spread += 2.0
        elif fhc_score < 55:
            spread += 1.0
        if fraud_risk == "Medium":
            spread += 0.5
        elif fraud_risk == "High":
            spread += 1.5
        adjusted = lender.base_interest_rate + spread
        return round(min(adjusted, lender.max_interest_rate), 2)

    def _approval_probability(
        self, fhc_score: float, credit_decision: Optional[str], fraud_risk: str
    ) -> float:
        base = 0.70
        if fhc_score >= 75:
            base += 0.15
        elif fhc_score >= 60:
            base += 0.08
        if credit_decision and credit_decision.upper() == "APPROVE":
            base += 0.10
        elif credit_decision and credit_decision.upper() == "CONDITIONAL":
            base += 0.02
        if fraud_risk == "Low":
            base += 0.05
        elif fraud_risk == "Medium":
            base -= 0.05
        elif fraud_risk == "High":
            base -= 0.15
        return round(min(max(base, 0.10), 0.98), 2)

    def _build_explanation(
        self,
        lender,
        match_score: float,
        fhc_score: float,
        credit_decision: Optional[str],
        fraud_risk: str,
        product_type: str,
    ) -> str:
        strengths = []
        constraints = []

        if fhc_score >= 65:
            strengths.append(f"Strong Financial Health Card score ({fhc_score:.1f}/100)")
        else:
            constraints.append(f"Below-average FHC score ({fhc_score:.1f}/100) – may require enhanced monitoring")

        if credit_decision and credit_decision.upper() == "APPROVE":
            strengths.append("AI Credit Decision: APPROVED")
        elif credit_decision and credit_decision.upper() == "CONDITIONAL":
            constraints.append("Credit decision is CONDITIONAL – additional documentation may be required")

        if fraud_risk == "Low":
            strengths.append("Clean RBI Fraud Registry status")
        else:
            constraints.append(f"Fraud risk rated {fraud_risk} – lender may impose conditions")

        if lender.tat_days <= 2:
            strengths.append(f"Fastest disbursement: {lender.tat_days} day(s)")

        if not lender.collateral_required:
            strengths.append("No collateral required")
        else:
            constraints.append("Collateral required – prepare asset documentation")

        steps = ["Complete digital KYC on lender portal", "Upload last 2 years GST returns"]
        if lender.collateral_required:
            steps.append("Submit collateral valuation report")
        steps.append("Await lender credit approval (typically " + str(lender.tat_days) + " working days)")

        explanation = {
            "why_selected": (
                f"{lender.name} offers '{product_type}' with a competitive base rate of "
                f"{lender.base_interest_rate}% p.a. and a match score of {match_score}/100."
            ),
            "why_customer_qualifies": (
                f"Customer's FHC score of {fhc_score:.1f}, credit decision of "
                f"'{credit_decision or 'N/A'}', and {fraud_risk} fraud risk satisfy "
                f"{lender.name}'s lending policy."
            ),
            "key_strengths": strengths,
            "key_constraints": constraints,
            "suggested_next_steps": steps,
        }
        return json.dumps(explanation)

    def search_eligible_lenders(self, lenders, params: Dict) -> List[Dict]:
        """Screen all lenders and return eligibility results (no offer generation)."""
        results = []
        rq_amount = params.get("requested_amount", 0)
        rq_tenure = params.get("requested_tenure", 12)
        fhc_score = params.get("fhc_score", 50.0) or 50.0
        credit_decision = params.get("credit_decision")
        fraud_risk = params.get("fraud_risk_level", "Low") or "Low"
        product_type = params.get("product_type", "Working Capital Loan")

        for lender in lenders:
            eligible, reasons = self._is_eligible(
                lender, rq_amount, rq_tenure, credit_decision, fraud_risk, product_type, params
            )
            score = 0.0
            if eligible:
                score = self._compute_match_score(
                    lender, fhc_score, credit_decision, fraud_risk, rq_amount, params
                )
            results.append({
                "lender_id": lender.lender_id,
                "lender_name": lender.name,
                "lender_type": lender.lender_type,
                "match_score": score,
                "base_interest_rate": lender.base_interest_rate,
                "max_loan_amount": lender.max_loan_amount,
                "tat_days": lender.tat_days,
                "risk_appetite": lender.risk_appetite,
                "eligible": eligible,
                "rejection_reasons": reasons,
                "product_match": product_type in (lender.loan_products or ""),
            })

        return sorted(results, key=lambda x: x["match_score"], reverse=True)

    def generate_offers(self, application, lenders, params: Dict) -> List[Dict]:
        """Generate ranked loan offers for all eligible lenders."""
        fhc_score = application.fhc_score or 50.0
        credit_decision = application.credit_decision
        fraud_risk = application.fraud_risk_level or "Low"
        requested_amount = application.requested_amount
        requested_tenure = application.requested_tenure_months
        product_type = application.product_type or "Working Capital Loan"

        offers = []
        for lender in lenders:
            eligible, reasons = self._is_eligible(
                lender, requested_amount, requested_tenure,
                credit_decision, fraud_risk, product_type, params
            )
            if not eligible:
                continue

            match_score = self._compute_match_score(
                lender, fhc_score, credit_decision, fraud_risk, requested_amount, params
            )
            rate = self._risk_adjusted_rate(lender, fhc_score, fraud_risk)
            tenure = min(requested_tenure, lender.max_tenure_months)
            emi = calculate_emi(requested_amount, rate, tenure)
            total_interest = round(emi * tenure - requested_amount, 2)
            proc_fee = round(requested_amount * lender.processing_fee_pct / 100, 2)
            approval_prob = self._approval_probability(fhc_score, credit_decision, fraud_risk)
            explanation = self._build_explanation(
                lender, match_score, fhc_score, credit_decision, fraud_risk, product_type
            )

            # Conditions text
            conds = []
            if lender.collateral_required:
                conds.append("Collateral documentation required.")
            if credit_decision and credit_decision.upper() == "CONDITIONAL":
                conds.append("Subject to additional lender verification.")
            if fraud_risk != "Low":
                conds.append("Enhanced due diligence may apply.")

            offers.append({
                "lender_id": lender.lender_id,
                "lender_name": lender.name,
                "lender_type": lender.lender_type,
                "product_type": product_type,
                "offered_amount": requested_amount,
                "interest_rate": rate,
                "tenure_months": tenure,
                "processing_fee": proc_fee,
                "monthly_installment": emi,
                "total_interest": total_interest,
                "approval_probability": approval_prob,
                "expected_disbursal_days": lender.tat_days,
                "match_score": match_score,
                "conditions": "; ".join(conds) if conds else "No special conditions.",
                "match_explanation": explanation,
            })

        # Rank by match score descending
        offers.sort(key=lambda x: x["match_score"], reverse=True)
        for i, offer in enumerate(offers):
            offer["rank"] = i + 1

        return offers


# ---------------------------------------------------------------------------
# Sandbox Adapter
# ---------------------------------------------------------------------------

class SandboxAdapter(BaseMatchingAdapter):
    """Delegates to simulation; stamps a sandbox marker in explanations."""

    def search_eligible_lenders(self, lenders, params: Dict) -> List[Dict]:
        results = SimulationAdapter().search_eligible_lenders(lenders, params)
        for r in results:
            r["_sandbox"] = True
        return results

    def generate_offers(self, application, lenders, params: Dict) -> List[Dict]:
        offers = SimulationAdapter().generate_offers(application, lenders, params)
        for o in offers:
            o["conditions"] = "SANDBOX MODE. " + (o.get("conditions") or "")
        return offers


# ---------------------------------------------------------------------------
# Production Adapter (stub)
# ---------------------------------------------------------------------------

class ProductionAdapter(BaseMatchingAdapter):
    """
    Production integration stub.  Replace generate_offers() with real
    OCEN API calls when the production gateway is available.
    """

    def search_eligible_lenders(self, lenders, params: Dict) -> List[Dict]:
        return SimulationAdapter().search_eligible_lenders(lenders, params)

    def generate_offers(self, application, lenders, params: Dict) -> List[Dict]:
        return SimulationAdapter().generate_offers(application, lenders, params)
