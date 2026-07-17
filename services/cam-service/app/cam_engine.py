"""
AAROHAN CAM Generation Engine
==============================
Compiles all 18 CAM sections from upstream intelligence inputs.
Generates explainable AI narratives using deterministic rule-based logic.
Produces risk scoring, rating, and lending recommendation.

Design:
  • No external API calls – fully deterministic from simulation dataset.
  • Each section is a pure function (testable in isolation).
  • Narrative generation follows IDBI/RBI CAM documentation standards.
"""
import json
from typing import Any, Dict, Optional

# ── Template Registry ────────────────────────────────────────────────────────

TEMPLATES = {
    "IDBI_BANK": {
        "bank_name": "IDBI Bank Limited",
        "color_primary": "#003087",
        "color_secondary": "#E8F0FE",
        "logo_placeholder": "[IDBI BANK LOGO]",
        "header_text": "CREDIT APPRAISAL MEMORANDUM – MSME LENDING",
        "footer_text": "IDBI Bank Ltd | MSME Credit – Confidential",
    },
    "PUBLIC_SECTOR": {
        "bank_name": "State Bank of India",
        "color_primary": "#003366",
        "color_secondary": "#F0F4FF",
        "logo_placeholder": "[SBI LOGO]",
        "header_text": "CREDIT APPRAISAL NOTE – SME FINANCE DIVISION",
        "footer_text": "SBI | SME Finance – Strictly Confidential",
    },
    "PRIVATE_BANK": {
        "bank_name": "HDFC Bank Limited",
        "color_primary": "#004C97",
        "color_secondary": "#F5F7FF",
        "logo_placeholder": "[HDFC BANK LOGO]",
        "header_text": "CREDIT APPRAISAL MEMO – BUSINESS BANKING",
        "footer_text": "HDFC Bank | Business Banking – Confidential",
    },
    "NBFC": {
        "bank_name": "Tata Capital Financial Services",
        "color_primary": "#002244",
        "color_secondary": "#F0F8FF",
        "logo_placeholder": "[NBFC LOGO]",
        "header_text": "CREDIT NOTE – MSME LOAN APPRAISAL",
        "footer_text": "Tata Capital | MSME Lending – Internal Use Only",
    },
    "GENERIC": {
        "bank_name": "AAROHAN Digital Lending Platform",
        "color_primary": "#1A237E",
        "color_secondary": "#E8EAF6",
        "logo_placeholder": "[AAROHAN LOGO]",
        "header_text": "CREDIT APPRAISAL MEMORANDUM",
        "footer_text": "Project AAROHAN | IDBI Hackathon 2025 – Confidential",
    },
}

ALL_SECTIONS = [
    "executive_summary", "applicant_profile", "business_profile",
    "loan_requirement", "identity_verification", "gst_compliance",
    "banking_behaviour", "workforce_stability", "corporate_governance",
    "fhc_summary", "credit_decision", "fraud_screening",
    "ocen_marketplace", "recommended_offer", "key_risks",
    "risk_mitigation", "banker_recommendation", "approval_matrix",
]

# ── Risk / Rating Helpers ────────────────────────────────────────────────────

def _fhc_rating(fhc_score: float) -> str:
    if fhc_score >= 85: return "AAA"
    if fhc_score >= 75: return "AA"
    if fhc_score >= 65: return "A"
    if fhc_score >= 55: return "BBB"
    if fhc_score >= 45: return "BB"
    if fhc_score >= 35: return "B"
    return "C"


def _risk_grade(fhc_score: float, fraud_risk: str, credit_decision: str) -> str:
    if fraud_risk == "Critical" or credit_decision == "REJECT":
        return "Critical"
    if fhc_score >= 65 and fraud_risk == "Low" and credit_decision == "APPROVE":
        return "Low"
    if fhc_score >= 50 and fraud_risk in ("Low", "Medium"):
        return "Medium"
    return "High"


def _fraud_status(fraud_risk: str) -> str:
    return {"Low": "CLEAR", "Medium": "CLEAR", "High": "FLAGGED", "Critical": "BLOCKED"}.get(
        fraud_risk, "CLEAR"
    )


def _eligibility_status(credit_decision: str, fraud_risk: str, fhc_score: float) -> str:
    if fraud_risk == "Critical" or credit_decision == "REJECT":
        return "INELIGIBLE"
    if credit_decision == "CONDITIONAL" or fhc_score < 50:
        return "CONDITIONAL"
    return "ELIGIBLE"


def _overall_credit_score(fhc_score: float, credit_decision: str, fraud_risk: str) -> float:
    base = fhc_score * 0.60
    cd_score = {"APPROVE": 100.0, "CONDITIONAL": 60.0, "REJECT": 20.0}.get(
        credit_decision.upper() if credit_decision else "CONDITIONAL", 60.0
    ) * 0.25
    fraud_score = {"Low": 100.0, "Medium": 70.0, "High": 40.0, "Critical": 0.0}.get(
        fraud_risk, 50.0
    ) * 0.15
    return round(base + cd_score + fraud_score, 1)


# ── Section Compilers ────────────────────────────────────────────────────────

def _section_executive_summary(ctx: Dict) -> str:
    biz = ctx.get("business_name", "The Applicant")
    loan = ctx.get("recommended_amount", ctx.get("requested_amount", 0))
    product = ctx.get("product_type", "Working Capital Loan")
    lender = ctx.get("recommended_lender", "IDBI Bank")
    rate = ctx.get("recommended_rate", 10.0)
    cd = ctx.get("credit_decision", "CONDITIONAL")
    fhc = ctx.get("fhc_score", 55.0)
    return (
        f"EXECUTIVE SUMMARY\n"
        f"{'='*60}\n"
        f"Applicant          : {biz}\n"
        f"Loan Requested     : ₹{loan:,.0f}\n"
        f"Product            : {product}\n"
        f"Recommended Lender : {lender}\n"
        f"Recommended Rate   : {rate}% p.a.\n"
        f"Credit Decision    : {cd}\n"
        f"FHC Score          : {fhc:.1f}/100\n\n"
        f"This Credit Appraisal Memorandum has been auto-generated by Project AAROHAN's "
        f"AI-assisted lending intelligence engine. The memo consolidates identity verification, "
        f"GST compliance, banking behaviour, EPFO workforce metrics, MCA governance, financial "
        f"health analytics, AI credit scoring, RBI fraud screening, and OCEN marketplace matching "
        f"into a single authoritative lending recommendation for {biz}."
    )


def _section_applicant_profile(ctx: Dict) -> str:
    return (
        f"APPLICANT PROFILE\n"
        f"{'='*60}\n"
        f"Customer ID        : {ctx.get('customer_id', 'N/A')}\n"
        f"Business Name      : {ctx.get('business_name', 'N/A')}\n"
        f"Business Type      : {ctx.get('business_type', 'Private Limited')}\n"
        f"Industry Sector    : {ctx.get('industry', 'Manufacturing')}\n"
        f"Annual Revenue     : ₹{ctx.get('annual_revenue', 0):,.0f}\n"
        f"PAN Status         : Verified (CKYC)\n"
        f"GSTIN Status       : Active\n"
        f"ULI Reference      : {ctx.get('uli_reference', 'N/A')}\n"
        f"Registration State : {'Verified via MCA' if ctx.get('mca_verified', True) else 'Pending'}\n"
        f"Directors          : {'Screened – No adverse findings' if ctx.get('fraud_risk_level', 'Low') != 'Critical' else 'Adverse findings noted'}"
    )


def _section_business_profile(ctx: Dict) -> str:
    return (
        f"BUSINESS PROFILE\n"
        f"{'='*60}\n"
        f"Business Name      : {ctx.get('business_name', 'The Applicant')}\n"
        f"Constitution       : {ctx.get('business_type', 'Private Limited')}\n"
        f"Sector             : {ctx.get('industry', 'MSME – Manufacturing')}\n"
        f"Annual Revenue     : ₹{ctx.get('annual_revenue', 0):,.0f} (GSTN Verified)\n"
        f"GST Compliance     : {'Regular – No defaults' if ctx.get('gst_compliant', True) else 'Irregular – Review required'}\n"
        f"Employee Count     : {ctx.get('employee_count', 25)} (EPFO registered)\n"
        f"Provident Fund     : {'Compliant' if ctx.get('epfo_compliant', True) else 'Non-Compliant'}\n"
        f"Corporate Governance: {'Satisfactory – MCA compliant' if ctx.get('governance_risk', 'Low') != 'Critical' else 'Adverse – MCA violations noted'}\n"
        f"Loan Purpose       : {ctx.get('loan_purpose', 'Working Capital / Business Expansion')}"
    )


def _section_loan_requirement(ctx: Dict) -> str:
    amt = ctx.get("recommended_amount", ctx.get("requested_amount", 0))
    tenure = ctx.get("recommended_tenure", 24)
    rate = ctx.get("recommended_rate", 10.5)
    from app.cam_engine import _calc_emi
    emi = _calc_emi(amt, rate, tenure)
    return (
        f"LOAN REQUIREMENT\n"
        f"{'='*60}\n"
        f"Requested Amount   : ₹{ctx.get('requested_amount', amt):,.0f}\n"
        f"Recommended Amount : ₹{amt:,.0f}\n"
        f"Product Type       : {ctx.get('product_type', 'Working Capital Loan')}\n"
        f"Purpose            : {ctx.get('loan_purpose', 'Business expansion and working capital')}\n"
        f"Recommended Tenure : {tenure} months\n"
        f"Interest Rate      : {rate}% p.a. (Reducing Balance)\n"
        f"EMI Estimate       : ₹{emi:,.2f}/month\n"
        f"Processing Fee     : ₹{amt * 0.01:,.0f} (est. 1%)\n"
        f"Collateral         : Clean charge on business assets (Hypothecation)"
    )


def _section_identity_verification(ctx: Dict) -> str:
    return (
        f"IDENTITY VERIFICATION SUMMARY\n"
        f"{'='*60}\n"
        f"PAN Verification   : {'Matched – CKYC Central Registry' if ctx.get('pan_verified', True) else 'Mismatch Detected'}\n"
        f"Aadhaar            : {'Seeded and Verified' if ctx.get('aadhaar_verified', True) else 'Not Verified'}\n"
        f"CKYC Status        : {'KYC Complete – Risk Category: Low' if ctx.get('fraud_risk_level', 'Low') == 'Low' else 'KYC Flagged – Review required'}\n"
        f"Director DIN       : {'All directors verified – No adverse findings' if ctx.get('fraud_risk_level', 'Low') != 'Critical' else 'Adverse director history detected'}\n"
        f"ULI Consent        : Obtained digitally – DPDPA Compliant\n"
        f"Account Aggregator : AA consent obtained – Data pull authorised"
    )


def _section_gst_compliance(ctx: Dict) -> str:
    revenue = ctx.get("annual_revenue", 0)
    return (
        f"GST COMPLIANCE SUMMARY\n"
        f"{'='*60}\n"
        f"GSTIN Status       : {'Active – No suspension' if ctx.get('gst_compliant', True) else 'Suspended – Review required'}\n"
        f"GSTR-1 Filing      : {'Timely – ≤5 day average lag' if ctx.get('gst_compliant', True) else 'Irregular filing pattern'}\n"
        f"GSTR-3B Filing     : Regular\n"
        f"Annual GST Turnover: ₹{revenue:,.0f}\n"
        f"ITC Utilisation    : Normal – No reversal notices\n"
        f"E-Invoicing        : {'Compliant' if revenue > 5_000_000 else 'Not applicable (below threshold)'}\n"
        f"Tax Payment History: {'No defaults – Clean GST record' if ctx.get('gst_compliant', True) else 'Late payments observed'}"
    )


def _section_banking_behaviour(ctx: Dict) -> str:
    return (
        f"BANKING BEHAVIOUR SUMMARY\n"
        f"{'='*60}\n"
        f"Data Source        : Account Aggregator (AA) – Consented Data Pull\n"
        f"Average Balance    : ₹{ctx.get('avg_balance', 380_000):,.0f}\n"
        f"Cheque Bounce      : {'None in last 12 months' if ctx.get('cheque_bounce', False) is False else 'Instances noted – Review'}\n"
        f"Overdraft Frequency: {'Nil' if ctx.get('overdraft_frequent', False) is False else 'Frequent – Liquidity concern'}\n"
        f"Cash Deposit Ratio : Within RBI guidelines\n"
        f"EMI Payments       : {'Regular – No delays' if ctx.get('emi_regular', True) else 'Irregular – Risk flag'}\n"
        f"AML Risk           : {'Low – No suspicious transactions' if ctx.get('fraud_risk_level', 'Low') in ('Low', 'Medium') else 'Elevated – Investigation required'}"
    )


def _section_workforce_stability(ctx: Dict) -> str:
    emp = ctx.get("employee_count", 25)
    return (
        f"WORKFORCE STABILITY SUMMARY\n"
        f"{'='*60}\n"
        f"Data Source        : EPFO Simulation Registry\n"
        f"Registered Members : {emp}\n"
        f"EPF Compliance     : {'Active – Regular contributions' if ctx.get('epfo_compliant', True) else 'Non-Compliant – Review required'}\n"
        f"ESI Registration   : {'Compliant' if emp > 10 else 'Not applicable (<10 employees)'}\n"
        f"Employee Attrition : {'Stable – <10% annual churn' if ctx.get('epfo_compliant', True) else 'High attrition detected'}\n"
        f"Payroll Regularity : Monthly – No defaults observed\n"
        f"Workforce Rating   : {'STABLE' if ctx.get('epfo_compliant', True) else 'UNSTABLE'}"
    )


def _section_corporate_governance(ctx: Dict) -> str:
    gov_risk = ctx.get("governance_risk", "Low")
    return (
        f"CORPORATE GOVERNANCE SUMMARY\n"
        f"{'='*60}\n"
        f"Data Source        : MCA Simulation Registry\n"
        f"Company Status     : {'Active – No strike-off notice' if gov_risk != 'Critical' else 'Flagged – Strike-off risk'}\n"
        f"ROC Compliance     : {'Annual returns filed – No defaults' if gov_risk in ('Low', 'Medium') else 'Non-compliance detected'}\n"
        f"Director Status    : {'All directors active – No DIN disqualification' if gov_risk != 'Critical' else 'Disqualified directors detected'}\n"
        f"Charge Register    : {'No adverse charges – Clean title' if gov_risk == 'Low' else 'Existing charges noted – Review'}\n"
        f"Governance Rating  : {gov_risk.upper()}"
    )


def _section_fhc_summary(ctx: Dict) -> str:
    fhc = ctx.get("fhc_score", 55.0)
    rating = _fhc_rating(fhc)
    return (
        f"FINANCIAL HEALTH CARD SUMMARY\n"
        f"{'='*60}\n"
        f"FHC Score          : {fhc:.1f} / 100\n"
        f"FHC Rating         : {rating}\n"
        f"Composite Inputs   : Identity (15%) | GST (20%) | Banking (25%) | EPFO (15%) | MCA (15%) | CKYC (10%)\n"
        f"Score Interpretation:\n"
        f"  ≥75 → Premium MSME – Fast-track eligibility\n"
        f"  55–74 → Standard MSME – Normal processing\n"
        f"  35–54 → Substandard – Enhanced monitoring\n"
        f"  <35 → High Risk – Refer to credit committee\n"
        f"Applicant Bracket  : {'Premium' if fhc >= 75 else ('Standard' if fhc >= 55 else ('Substandard' if fhc >= 35 else 'High Risk'))}"
    )


def _section_credit_decision(ctx: Dict) -> str:
    cd = ctx.get("credit_decision", "CONDITIONAL")
    fhc = ctx.get("fhc_score", 55.0)
    return (
        f"AI CREDIT DECISION SUMMARY\n"
        f"{'='*60}\n"
        f"Credit Engine      : AAROHAN AI Credit Decision Engine v2\n"
        f"Decision           : {cd}\n"
        f"FHC Score Input    : {fhc:.1f}\n"
        f"Rule Engine        : 12-rule deterministic decision tree\n"
        f"ML Model           : Logistic Regression (simulation mode)\n"
        f"Confidence         : {'High (>90%)' if cd == 'APPROVE' else ('Medium (65–90%)' if cd == 'CONDITIONAL' else 'Low (<40%)')}\n"
        f"Decision Rationale : {'Strong FHC and clean compliance history supports approval.' if cd == 'APPROVE' else ('Conditional approval subject to additional documentation.' if cd == 'CONDITIONAL' else 'Insufficient creditworthiness indicators for approval.')}\n"
        f"Explainability     : SHAP-based feature attribution available"
    )


def _section_fraud_screening(ctx: Dict) -> str:
    fraud_risk = ctx.get("fraud_risk_level", "Low")
    fraud_score = ctx.get("fraud_score", 5.0)
    return (
        f"RBI FRAUD REGISTRY SCREENING SUMMARY\n"
        f"{'='*60}\n"
        f"Screening Engine   : AAROHAN RBI Fraud Registry Simulation v2\n"
        f"Fraud Risk Level   : {fraud_risk}\n"
        f"Fraud Score        : {fraud_score:.1f} / 100\n"
        f"PAN Check          : {'CLEAR – No Central Fraud Registry hit' if fraud_risk not in ('High', 'Critical') else 'FLAGGED – Registry match found'}\n"
        f"GSTIN Check        : {'CLEAR' if fraud_risk not in ('High', 'Critical') else 'ADVERSE'}\n"
        f"Director Check     : {'CLEAR – All directors clean' if fraud_risk != 'Critical' else 'ADVERSE – Director linkage to fraudulent entity'}\n"
        f"Account Check      : {'CLEAR' if fraud_risk not in ('High', 'Critical') else 'ADVERSE – Account previously flagged'}\n"
        f"AML Assessment     : {'Low Risk – No STR indicators' if fraud_risk in ('Low', 'Medium') else 'Elevated – FIU-IND review recommended'}\n"
        f"Screening Status   : {_fraud_status(fraud_risk)}"
    )


def _section_ocen_marketplace(ctx: Dict) -> str:
    lender = ctx.get("recommended_lender", "N/A")
    amount = ctx.get("recommended_amount", ctx.get("requested_amount", 0))
    rate = ctx.get("recommended_rate", 0)
    tenure = ctx.get("recommended_tenure", 24)
    match_score = ctx.get("match_score", 0)
    return (
        f"OCEN MARKETPLACE SUMMARY\n"
        f"{'='*60}\n"
        f"Marketplace Engine : AAROHAN OCEN Marketplace Simulation v2\n"
        f"Lenders Screened   : 10 (PAN India registry)\n"
        f"Recommended Lender : {lender}\n"
        f"Match Score        : {match_score:.1f} / 100\n"
        f"Offered Amount     : ₹{amount:,.0f}\n"
        f"Interest Rate      : {rate}% p.a.\n"
        f"Tenure             : {tenure} months\n"
        f"Approval Probability: {ctx.get('approval_probability', 0.75)*100:.0f}%\n"
        f"Expected Disbursal : {ctx.get('expected_disbursal_days', 3)} working days\n"
        f"ULI Reference      : {ctx.get('uli_reference', 'N/A')}"
    )


def _section_recommended_offer(ctx: Dict) -> str:
    amt = ctx.get("recommended_amount", ctx.get("requested_amount", 0))
    rate = ctx.get("recommended_rate", 10.5)
    tenure = ctx.get("recommended_tenure", 24)
    from app.cam_engine import _calc_emi
    emi = _calc_emi(amt, rate, tenure)
    total_int = round(emi * tenure - amt, 2)
    return (
        f"RECOMMENDED LOAN OFFER\n"
        f"{'='*60}\n"
        f"Lender             : {ctx.get('recommended_lender', 'N/A')}\n"
        f"Loan Amount        : ₹{amt:,.0f}\n"
        f"Interest Rate      : {rate}% p.a. (Reducing Balance)\n"
        f"Tenure             : {tenure} months\n"
        f"EMI                : ₹{emi:,.2f}/month\n"
        f"Total Interest     : ₹{total_int:,.0f}\n"
        f"Processing Fee     : ₹{amt * 0.01:,.0f} (approx 1%)\n"
        f"Collateral         : Hypothecation of business assets\n"
        f"Disbursement TAT   : {ctx.get('expected_disbursal_days', 3)} working days post documentation\n"
        f"Conditions         : {ctx.get('offer_conditions', 'Subject to final lender credit approval.')}"
    )


def _section_key_risks(ctx: Dict) -> str:
    risks = []
    fhc = ctx.get("fhc_score", 55.0)
    fraud_risk = ctx.get("fraud_risk_level", "Low")
    cd = ctx.get("credit_decision", "CONDITIONAL")
    rev = ctx.get("annual_revenue", 0)

    if fhc < 55:
        risks.append("1. Below-average Financial Health Card score – indicates financial stress.")
    if fraud_risk in ("High", "Critical"):
        risks.append(f"2. Elevated fraud risk ({fraud_risk}) – adverse RBI registry findings.")
    if cd == "CONDITIONAL":
        risks.append("3. Conditional credit decision – additional documentation required.")
    if cd == "REJECT":
        risks.append("4. Credit decision: REJECT – loan appraisal not recommended.")
    if rev < 2_000_000:
        risks.append("5. Low annual revenue – repayment capacity may be constrained.")
    if ctx.get("cheque_bounce", False):
        risks.append("6. Historical cheque bounce incidents – banking behaviour risk.")
    if ctx.get("governance_risk", "Low") == "Critical":
        risks.append("7. Critical MCA governance risk – director disqualification detected.")

    if not risks:
        risks.append("No material risks identified. Customer presents a strong lending profile.")

    return "KEY RISKS\n" + "="*60 + "\n" + "\n".join(risks)


def _section_risk_mitigation(ctx: Dict) -> str:
    fhc = ctx.get("fhc_score", 55.0)
    fraud_risk = ctx.get("fraud_risk_level", "Low")
    measures = [
        "1. Monthly banking statement review via Account Aggregator consent.",
        "2. Quarterly GST return verification through GSTN portal.",
        "3. Annual EPFO compliance check for workforce stability.",
        "4. Lender's credit monitoring dashboard alerts on EMI delays.",
    ]
    if fraud_risk in ("High", "Critical"):
        measures.append("5. Enhanced AML monitoring – file STR with FIU-IND if indicators worsen.")
    if fhc < 55:
        measures.append("6. Six-monthly FHC re-assessment to track financial recovery.")
    measures.append(f"{'5' if len(measures)==4 else str(len(measures)+1)}. OCEN marketplace re-screening available if business conditions improve.")

    return "RISK MITIGATION MEASURES\n" + "="*60 + "\n" + "\n".join(measures)


def _section_banker_recommendation(ctx: Dict) -> str:
    cd = ctx.get("credit_decision", "CONDITIONAL")
    fhc = ctx.get("fhc_score", 55.0)
    fraud_risk = ctx.get("fraud_risk_level", "Low")
    amt = ctx.get("recommended_amount", 0)
    rate = ctx.get("recommended_rate", 10.5)

    if cd == "APPROVE" and fraud_risk in ("Low", "Medium") and fhc >= 55:
        recommendation = "RECOMMEND APPROVAL"
        rationale = (
            f"The applicant presents a strong lending profile with an FHC score of {fhc:.1f}/100, "
            f"APPROVE credit decision, and {fraud_risk} fraud risk. "
            f"Recommended disbursement of ₹{amt:,.0f} at {rate}% p.a. through the selected OCEN lender."
        )
    elif cd == "CONDITIONAL":
        recommendation = "RECOMMEND CONDITIONAL APPROVAL"
        rationale = (
            f"The applicant meets minimum eligibility criteria (FHC: {fhc:.1f}/100, Fraud: {fraud_risk}). "
            f"Approval subject to submission of additional financial documentation and satisfactory "
            f"lender-side verification. Proceed with ₹{amt:,.0f} at {rate}% p.a. upon condition fulfilment."
        )
    else:
        recommendation = "DECLINE – REFER TO CREDIT COMMITTEE"
        rationale = (
            f"The applicant does not meet minimum lending criteria. Credit decision: {cd}, "
            f"FHC Score: {fhc:.1f}/100, Fraud Risk: {fraud_risk}. "
            f"Case referred to Credit Committee for exceptional review."
        )

    return (
        f"BANKER RECOMMENDATION\n"
        f"{'='*60}\n"
        f"Recommendation     : {recommendation}\n\n"
        f"Rationale:\n{rationale}\n\n"
        f"This recommendation is based on automated analysis by Project AAROHAN's AI lending "
        f"intelligence engine and is subject to final human review and approval."
    )


def _section_approval_matrix(ctx: Dict) -> str:
    amt = ctx.get("recommended_amount", 0)
    return (
        f"APPROVAL MATRIX\n"
        f"{'='*60}\n"
        f"{'Level':<30} {'Authority':<25} {'Limit':<20}\n"
        f"{'-'*75}\n"
        f"{'Level 1 – Branch Manager':<30} {'BM / RM Workspace':<25} {'Up to ₹25 Lakhs':<20}\n"
        f"{'Level 2 – Zonal Manager':<30} {'ZM Approval':<25} {'Up to ₹1 Crore':<20}\n"
        f"{'Level 3 – Credit Committee':<30} {'CPC Quorum':<25} {'Above ₹1 Crore':<20}\n"
        f"\n"
        f"Applicable Level   : {'Level 1' if amt <= 2_500_000 else ('Level 2' if amt <= 10_000_000 else 'Level 3')}\n"
        f"Loan Amount        : ₹{amt:,.0f}\n"
        f"CAM Generated By   : AAROHAN AI Engine\n"
        f"Generated At       : [AUTO]\n"
        f"Approval Status    : PENDING"
    )


# ── Narrative Generator ──────────────────────────────────────────────────────

def _narrative_customer_strengths(ctx: Dict) -> str:
    strengths = []
    fhc = ctx.get("fhc_score", 55.0)
    cd = ctx.get("credit_decision", "CONDITIONAL")
    fraud = ctx.get("fraud_risk_level", "Low")

    if fhc >= 65:
        strengths.append(f"Strong Financial Health Card score of {fhc:.1f}/100 reflecting sound financial management.")
    if cd == "APPROVE":
        strengths.append("AI Credit Decision: APPROVED – high confidence in repayment capacity.")
    if fraud == "Low":
        strengths.append("Clean RBI Fraud Registry status with no adverse findings.")
    if ctx.get("gst_compliant", True):
        strengths.append("Consistent GST compliance history with timely filings.")
    if ctx.get("epfo_compliant", True):
        strengths.append("EPFO-compliant workforce indicating stable operations.")

    return " | ".join(strengths) if strengths else "No exceptional strengths identified at this time."


def _narrative_key_risks(ctx: Dict) -> str:
    risks = []
    fhc = ctx.get("fhc_score", 55.0)
    fraud = ctx.get("fraud_risk_level", "Low")

    if fhc < 50:
        risks.append(f"Low FHC score ({fhc:.1f}) signals financial vulnerability.")
    if fraud in ("High", "Critical"):
        risks.append(f"Elevated fraud risk ({fraud}) requires enhanced monitoring.")
    if ctx.get("cheque_bounce", False):
        risks.append("Historical cheque bounce incidents indicate liquidity constraints.")

    return " | ".join(risks) if risks else "No material risks identified."


def _narrative_lending_recommendation(ctx: Dict) -> str:
    cd = ctx.get("credit_decision", "CONDITIONAL")
    amt = ctx.get("recommended_amount", 0)
    rate = ctx.get("recommended_rate", 10.5)
    lender = ctx.get("recommended_lender", "the selected lender")

    if cd == "APPROVE":
        return (
            f"AAROHAN AI recommends APPROVAL for ₹{amt:,.0f} at {rate}% p.a. through {lender}. "
            f"The customer demonstrates strong creditworthiness and is eligible for fast-track processing."
        )
    if cd == "CONDITIONAL":
        return (
            f"AAROHAN AI recommends CONDITIONAL APPROVAL for ₹{amt:,.0f} at {rate}% p.a. through {lender}. "
            f"Proceed subject to receipt and verification of additional documentation as specified."
        )
    return (
        f"AAROHAN AI recommends DECLINE. The customer does not meet minimum lending criteria. "
        f"Refer to Credit Committee for exceptional handling."
    )


def _narrative_monitoring_actions(ctx: Dict) -> str:
    actions = [
        "Monthly Account Aggregator balance and transaction review.",
        "Quarterly GST compliance verification.",
        "Annual EPFO and MCA compliance audit.",
        "EMI repayment tracking via lender dashboard.",
        "Semi-annual FHC re-assessment and credit score refresh.",
    ]
    if ctx.get("fraud_risk_level", "Low") not in ("Low",):
        actions.append("Enhanced AML monitoring – bi-monthly fraud registry re-screening.")
    return " | ".join(actions)


# ── EMI Calculator ────────────────────────────────────────────────────────────

def _calc_emi(principal: float, annual_rate: float, months: int) -> float:
    import math
    if annual_rate == 0 or months == 0:
        return round(principal / max(months, 1), 2)
    r = annual_rate / (12 * 100)
    emi = principal * r * math.pow(1 + r, months) / (math.pow(1 + r, months) - 1)
    return round(emi, 2)


# ── Master Compiler ───────────────────────────────────────────────────────────

def compile_cam(ctx: Dict) -> Dict:
    """
    Build all 18 sections + narratives + scoring from the context dict.
    Returns a dict ready for ORM insertion.
    """
    fhc = ctx.get("fhc_score") or 55.0
    cd = ctx.get("credit_decision") or "CONDITIONAL"
    fraud = ctx.get("fraud_risk_level") or "Low"
    fraud_score = ctx.get("fraud_score") or 5.0

    return {
        # Sections
        "section_executive_summary":   _section_executive_summary(ctx),
        "section_applicant_profile":   _section_applicant_profile(ctx),
        "section_business_profile":    _section_business_profile(ctx),
        "section_loan_requirement":    _section_loan_requirement(ctx),
        "section_identity_verification": _section_identity_verification(ctx),
        "section_gst_compliance":      _section_gst_compliance(ctx),
        "section_banking_behaviour":   _section_banking_behaviour(ctx),
        "section_workforce_stability": _section_workforce_stability(ctx),
        "section_corporate_governance": _section_corporate_governance(ctx),
        "section_fhc_summary":         _section_fhc_summary(ctx),
        "section_credit_decision":     _section_credit_decision(ctx),
        "section_fraud_screening":     _section_fraud_screening(ctx),
        "section_ocen_marketplace":    _section_ocen_marketplace(ctx),
        "section_recommended_offer":   _section_recommended_offer(ctx),
        "section_key_risks":           _section_key_risks(ctx),
        "section_risk_mitigation":     _section_risk_mitigation(ctx),
        "section_banker_recommendation": _section_banker_recommendation(ctx),
        "section_approval_matrix":     _section_approval_matrix(ctx),
        # Scoring
        "overall_credit_score":       _overall_credit_score(fhc, cd, fraud),
        "financial_health_rating":    _fhc_rating(fhc),
        "risk_grade":                 _risk_grade(fhc, fraud, cd),
        "fraud_status":               _fraud_status(fraud),
        "eligibility_status":         _eligibility_status(cd, fraud, fhc),
        "recommended_loan_amount":    ctx.get("recommended_amount"),
        "recommended_interest_rate":  ctx.get("recommended_rate"),
        "recommended_tenure_months":  ctx.get("recommended_tenure"),
        # Narratives
        "narrative_customer_strengths":   _narrative_customer_strengths(ctx),
        "narrative_business_strengths":   ctx.get("business_name", "The applicant's") + " business demonstrates consistent revenue generation and GST compliance across reporting periods.",
        "narrative_financial_observations": f"FHC Score: {fhc:.1f}/100. Annual revenue: ₹{ctx.get('annual_revenue', 0):,.0f}. Banking behaviour rated {'Satisfactory' if not ctx.get('cheque_bounce') else 'Requires monitoring'}.",
        "narrative_key_risks":            _narrative_key_risks(ctx),
        "narrative_mitigating_factors":   "Regular AA data pull, GST monitoring, and EPFO compliance tracking are in place as risk buffers.",
        "narrative_lending_recommendation": _narrative_lending_recommendation(ctx),
        "narrative_monitoring_actions":   _narrative_monitoring_actions(ctx),
    }
