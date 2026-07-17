"""
OCEN Marketplace – Pydantic V2 Schemas
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ── Lender ──────────────────────────────────────────────────────────────────

class LenderRegisterRequest(BaseModel):
    lender_id: str
    name: str
    lender_type: str = "BANK"
    base_interest_rate: float
    max_interest_rate: float = 18.0
    max_loan_amount: float
    min_loan_amount: float = 50_000.0
    min_credit_score: int = 650
    processing_fee_pct: float = 1.0
    max_tenure_months: int = 60
    min_tenure_months: int = 6
    risk_appetite: str = "MEDIUM"
    collateral_required: bool = False
    preferred_industries: str = "ALL"
    geographic_coverage: str = "PAN_INDIA"
    tat_days: int = 3
    loan_products: str = "Working Capital Loan,Term Loan"
    women_entrepreneur_scheme: bool = False
    startup_friendly: bool = False
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class LenderResponse(LenderRegisterRequest):
    id: int
    created_at: datetime


# ── Partner ──────────────────────────────────────────────────────────────────

class PartnerRegisterRequest(BaseModel):
    partner_id: str
    name: str
    partner_type: str = "LSP"

    model_config = ConfigDict(from_attributes=True)


# ── Eligibility ──────────────────────────────────────────────────────────────

class EligibilityCheckRequest(BaseModel):
    customer_id: int
    annual_revenue: float
    credit_score: int
    requested_amount: float
    fhc_score: Optional[float] = None
    credit_decision: Optional[str] = None
    fraud_risk_level: Optional[str] = None


class EligibilityCheckResponse(BaseModel):
    eligible: bool
    reason: str
    max_eligible_amount: float
    uli_reference: str


# ── Loan Application ─────────────────────────────────────────────────────────

class LoanApplicationCreate(BaseModel):
    customer_id: int
    requested_amount: float
    requested_tenure_months: int = 12
    product_type: str = "Working Capital Loan"
    purpose: Optional[str] = None
    fhc_score: Optional[float] = None
    credit_decision: Optional[str] = None
    fraud_score: Optional[float] = None
    fraud_risk_level: Optional[str] = "Low"


class LoanApplicationResponse(BaseModel):
    id: int
    customer_id: int
    uli_reference: str
    requested_amount: float
    requested_tenure_months: int
    product_type: str
    purpose: Optional[str]
    status: str
    selected_offer_id: Optional[int]
    fhc_score: Optional[float]
    credit_decision: Optional[str]
    fraud_score: Optional[float]
    fraud_risk_level: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Loan Offer ───────────────────────────────────────────────────────────────

class MatchExplanation(BaseModel):
    why_selected: str
    why_customer_qualifies: str
    key_strengths: List[str]
    key_constraints: List[str]
    suggested_next_steps: List[str]


class LoanOfferResponse(BaseModel):
    id: int
    application_id: int
    lender_id: str
    lender_name: str
    lender_type: str
    product_type: str
    offered_amount: float
    interest_rate: float
    tenure_months: int
    processing_fee: float
    monthly_installment: float
    total_interest: float
    approval_probability: float
    expected_disbursal_days: int
    match_score: float
    rank: int
    conditions: Optional[str]
    match_explanation: Optional[str]
    status: str
    rejection_reason: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Offer Comparison ─────────────────────────────────────────────────────────

class OfferComparisonResponse(BaseModel):
    total_offers: int
    offers: List[LoanOfferResponse]
    best_rate_offer_id: Optional[int]
    best_match_offer_id: Optional[int]
    best_amount_offer_id: Optional[int]
    comparison_notes: str


# ── Accept / Reject ──────────────────────────────────────────────────────────

class LoanAcceptRequest(BaseModel):
    offer_id: int


class LoanRejectRequest(BaseModel):
    offer_id: int
    rejection_reason: str


# ── Marketplace Status / Dashboard ───────────────────────────────────────────

class MarketplaceDashboardResponse(BaseModel):
    total_applications: int
    offers_generated: int
    offers_accepted: int
    offers_rejected: int
    active_lenders: int
    avg_match_score: float
    avg_interest_rate: float
    top_lender: Optional[str]
    recent_applications: List[LoanApplicationResponse]


class LenderSearchRequest(BaseModel):
    customer_id: int
    requested_amount: float
    product_type: str = "Working Capital Loan"
    fhc_score: Optional[float] = None
    credit_decision: Optional[str] = None
    fraud_risk_level: Optional[str] = "Low"
    preferred_industry: Optional[str] = None
    max_interest_rate: Optional[float] = None
    women_entrepreneur: Optional[bool] = False


class LenderSearchResult(BaseModel):
    lender_id: str
    lender_name: str
    lender_type: str
    match_score: float
    base_interest_rate: float
    max_loan_amount: float
    tat_days: int
    risk_appetite: str
    eligible: bool
    rejection_reasons: List[str]
    product_match: bool


class LenderSearchResponse(BaseModel):
    total_lenders_screened: int
    eligible_lenders: int
    results: List[LenderSearchResult]


# ── AI Recommendation ────────────────────────────────────────────────────────

class AIRecommendationResponse(BaseModel):
    suitability_score: float
    dynamic_summary: str
    recommended_offer_id: Optional[int]
    breakdown: str


# ── Admin ────────────────────────────────────────────────────────────────────

class ConfigUpdateRequest(BaseModel):
    active_adapter: str
    match_params: Dict[str, Any] = {}


class MarketplaceReplayRequest(BaseModel):
    application_id: int
