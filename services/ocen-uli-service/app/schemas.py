from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# Registries
class LenderRegisterRequest(BaseModel):
    lender_id: str
    name: str
    lender_type: str = "BANK"
    base_interest_rate: float
    max_loan_amount: float
    min_credit_score: int

class PartnerRegisterRequest(BaseModel):
    partner_id: str
    name: str
    partner_type: str = "LSP"

# Eligibility
class EligibilityCheckRequest(BaseModel):
    customer_id: int
    annual_revenue: float
    credit_score: int
    requested_amount: float

class EligibilityCheckResponse(BaseModel):
    eligible: bool
    reason: str
    max_eligible_amount: float
    uli_reference: str

# Loan Applications
class LoanApplicationCreate(BaseModel):
    customer_id: int
    requested_amount: float
    requested_tenure_months: int = 12
    purpose: Optional[str] = None

class LoanApplicationResponse(BaseModel):
    id: int
    customer_id: int
    uli_reference: str
    requested_amount: float
    requested_tenure_months: int
    purpose: Optional[str]
    status: str
    selected_offer_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Loan Offers
class LoanOfferResponse(BaseModel):
    id: int
    application_id: int
    lender_id: str
    lender_name: str
    offered_amount: float
    interest_rate: float
    tenure_months: int
    processing_fee: float
    monthly_installment: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Comparison
class OfferComparisonResponse(BaseModel):
    offers: List[LoanOfferResponse]
    best_rate_offer_id: Optional[int]
    best_amount_offer_id: Optional[int]
    comparison_notes: str

# Application Accept
class LoanAcceptRequest(BaseModel):
    offer_id: int

# AI Recommendation
class AIRecommendationResponse(BaseModel):
    suitability_score: float
    dynamic_summary: str
    recommended_offer_id: Optional[int]
    breakdown: str
