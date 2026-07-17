from pydantic import BaseModel, field_validator, ConfigDict
import datetime
from typing import List, Optional, Dict, Any

class HumanApprovalLogResponse(BaseModel):
    id: int
    approver_id: str
    action: str
    comments: Optional[str]
    signed_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class AICreditDecisionResponse(BaseModel):
    id: int
    customer_id: int
    recommendation: str
    confidence_score: float
    decision_score: float
    risk_grade: str
    approval_probability: float
    
    # Lending Recommendation
    eligible_loan_amount: float
    recommended_product: Optional[str] = None
    recommended_tenure: int
    recommended_interest_rate: float
    collateral_recommendation: Optional[str] = None
    repayment_capacity: str
    emi_estimate: float
    debt_service_capacity: str
    
    # Explainable AI Lists
    top_positive_factors: List[str] = []
    top_negative_factors: List[str] = []
    risk_drivers: List[str] = []
    decision_explanation: Optional[str] = None
    recommended_actions: List[str] = []
    
    ai_narrative: Optional[str] = None
    policy_status: str
    approval_status: str
    rbi_fraud_status: str = "CLEAN"
    rbi_verification_log: Optional[str] = None
    explainability_tags: List[str] = []
    created_at: datetime.datetime
    approvals: List[HumanApprovalLogResponse] = []

    @field_validator("explainability_tags", mode="before")
    @classmethod
    def parse_explainability_tags(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v or []

    @field_validator("top_positive_factors", mode="before")
    @classmethod
    def parse_pos_factors(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v or []

    @field_validator("top_negative_factors", mode="before")
    @classmethod
    def parse_neg_factors(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v or []

    @field_validator("risk_drivers", mode="before")
    @classmethod
    def parse_risk_drivers(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v or []

    @field_validator("recommended_actions", mode="before")
    @classmethod
    def parse_actions(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v or []

    model_config = ConfigDict(from_attributes=True)

class EvaluationRequest(BaseModel):
    customer_id: int

class ApprovalSubmission(BaseModel):
    approver_id: str
    action: str # APPROVED, REJECTED, REQUEST_MORE_INFO
    comments: Optional[str] = None

class ConfigUpdateRequest(BaseModel):
    active_adapter: str
    risk_thresholds: Dict[str, Any]
    rule_parameters: Dict[str, Any]

class CompareRequest(BaseModel):
    customer_ids: List[int]
