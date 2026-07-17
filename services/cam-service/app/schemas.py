"""
AAROHAN CAM Service – Pydantic V2 Schemas
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ── Version Snapshot ─────────────────────────────────────────────────────────

class CAMVersionResponse(BaseModel):
    id: int
    cam_id: int
    version_num: int
    edited_by: str
    edited_at: datetime
    change_summary: Optional[str]
    section_executive_summary: str
    section_banker_recommendation: str
    section_recommended_offer: str
    section_key_risks: str
    overall_credit_score: Optional[float]
    status: str

    model_config = ConfigDict(from_attributes=True)


# ── Approval Log ─────────────────────────────────────────────────────────────

class ApprovalLogResponse(BaseModel):
    id: int
    cam_id: int
    approver_id: str
    approver_role: str
    action: str
    level: int
    comments: Optional[str]
    signed_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Master CAM Response ───────────────────────────────────────────────────────

class CAMRecordResponse(BaseModel):
    id: int
    customer_id: int
    cam_reference: str
    status: str
    current_version: int
    template: str

    section_executive_summary: str
    section_applicant_profile: str
    section_business_profile: str
    section_loan_requirement: str
    section_identity_verification: str
    section_gst_compliance: str
    section_banking_behaviour: str
    section_workforce_stability: str
    section_corporate_governance: str
    section_fhc_summary: str
    section_credit_decision: str
    section_fraud_screening: str
    section_ocen_marketplace: str
    section_recommended_offer: str
    section_key_risks: str
    section_risk_mitigation: str
    section_banker_recommendation: str
    section_approval_matrix: str

    overall_credit_score: Optional[float]
    financial_health_rating: Optional[str]
    risk_grade: Optional[str]
    fraud_status: Optional[str]
    eligibility_status: Optional[str]
    recommended_loan_amount: Optional[float]
    recommended_interest_rate: Optional[float]
    recommended_tenure_months: Optional[int]

    narrative_customer_strengths: Optional[str]
    narrative_business_strengths: Optional[str]
    narrative_financial_observations: Optional[str]
    narrative_key_risks: Optional[str]
    narrative_mitigating_factors: Optional[str]
    narrative_lending_recommendation: Optional[str]
    narrative_monitoring_actions: Optional[str]

    created_at: datetime
    updated_at: datetime
    versions: List[CAMVersionResponse] = []
    approvals: List[ApprovalLogResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ── Generate Request ──────────────────────────────────────────────────────────

class CAMGenerateRequest(BaseModel):
    customer_id: int
    template: str = "IDBI_BANK"
    # Upstream intelligence (optional – service queries from shared DB if absent)
    fhc_score: Optional[float] = None
    credit_decision: Optional[str] = None
    fraud_risk_level: Optional[str] = None
    fraud_score: Optional[float] = None
    recommended_lender: Optional[str] = None
    recommended_amount: Optional[float] = None
    recommended_rate: Optional[float] = None
    recommended_tenure: Optional[int] = None
    # Customer meta
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    loan_purpose: Optional[str] = None


# ── Update Request ────────────────────────────────────────────────────────────

class CAMUpdateRequest(BaseModel):
    edited_by: str
    change_summary: str
    section_executive_summary: Optional[str] = None
    section_applicant_profile: Optional[str] = None
    section_business_profile: Optional[str] = None
    section_loan_requirement: Optional[str] = None
    section_identity_verification: Optional[str] = None
    section_gst_compliance: Optional[str] = None
    section_banking_behaviour: Optional[str] = None
    section_workforce_stability: Optional[str] = None
    section_corporate_governance: Optional[str] = None
    section_fhc_summary: Optional[str] = None
    section_credit_decision: Optional[str] = None
    section_fraud_screening: Optional[str] = None
    section_ocen_marketplace: Optional[str] = None
    section_recommended_offer: Optional[str] = None
    section_key_risks: Optional[str] = None
    section_risk_mitigation: Optional[str] = None
    section_banker_recommendation: Optional[str] = None
    section_approval_matrix: Optional[str] = None


# ── Approval ──────────────────────────────────────────────────────────────────

class CAMApprovalRequest(BaseModel):
    approver_id: str
    approver_role: str = "Branch Manager"
    action: str           # APPROVED | REJECTED | RETURNED
    level: int = 1
    comments: Optional[str] = None


# ── Template ──────────────────────────────────────────────────────────────────

class TemplateResponse(BaseModel):
    id: int
    template_key: str
    template_name: str
    bank_name: str
    color_primary: str
    color_secondary: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ── Dashboard ─────────────────────────────────────────────────────────────────

class CAMDashboardResponse(BaseModel):
    total_cams: int
    draft: int
    pending_approval: int
    approved: int
    rejected: int
    archived: int
    avg_credit_score: float
    recent_cams: List[CAMRecordResponse]


# ── Version Comparison ────────────────────────────────────────────────────────

class VersionDiff(BaseModel):
    field: str
    version_a: str
    version_b: str
    changed: bool


class VersionCompareResponse(BaseModel):
    cam_id: int
    version_a: int
    version_b: int
    diffs: List[VersionDiff]
    total_changes: int


# ── Config ────────────────────────────────────────────────────────────────────

class CAMConfigResponse(BaseModel):
    default_template: str
    auto_generate_on_ocen: bool
    require_fraud_clear: bool
    sections_enabled: List[str]
