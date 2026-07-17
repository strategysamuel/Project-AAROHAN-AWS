from pydantic import BaseModel, model_validator, ConfigDict
import datetime
from typing import List, Optional, Dict, Any

class ScoreHistoryResponse(BaseModel):
    id: int
    recorded_at: datetime.datetime
    score_value: float
    rating: str

    model_config = ConfigDict(from_attributes=True)

class FinancialHealthCardResponse(BaseModel):
    id: int
    customer_id: int
    overall_score: float
    fhc_score: Optional[float] = None  # Alias for backward compatibility
    rating: str
    
    # 10 Sub-Scores Details
    identity_score: float
    identity_weight: float
    identity_reason: Optional[str]
    identity_recommendation: Optional[str]
    
    compliance_score: float
    compliance_weight: float
    compliance_reason: Optional[str]
    compliance_recommendation: Optional[str]
    
    liquidity_score: float
    liquidity_weight: float
    liquidity_reason: Optional[str]
    liquidity_recommendation: Optional[str]
    
    revenue_score: float
    revenue_weight: float
    revenue_reason: Optional[str]
    revenue_recommendation: Optional[str]
    
    # Added for backward compatibility with existing tests
    revenue_health_score: float
    
    cash_flow_score: float
    cash_flow_weight: float
    cash_flow_reason: Optional[str]
    cash_flow_recommendation: Optional[str]
    
    business_stability_score: float
    business_stability_weight: float
    business_stability_reason: Optional[str]
    business_stability_recommendation: Optional[str]
    
    governance_score: float
    governance_weight: float
    governance_reason: Optional[str]
    governance_recommendation: Optional[str]
    
    workforce_score: float
    workforce_weight: float
    workforce_reason: Optional[str]
    workforce_recommendation: Optional[str]
    
    banking_behaviour_score: float
    banking_behaviour_weight: float
    banking_behaviour_reason: Optional[str]
    banking_behaviour_recommendation: Optional[str]
    
    growth_score: float
    growth_weight: float
    growth_reason: Optional[str]
    growth_recommendation: Optional[str]
    
    # 14 Financial Dimensions
    identity_trust_score: float
    business_compliance_score: float
    gst_health_score: float
    banking_behaviour_dim_score: float
    cash_flow_stability_score: float
    liquidity_dim_score: float
    revenue_growth_score: float
    working_capital_score: float
    profitability_score: float
    payroll_stability_score: float
    corporate_governance_score: float
    operational_stability_score: float
    business_continuity_score: float
    digital_adoption_score: float
    overall_financial_strength_score: float
    
    # AI Explainability
    key_strengths: Optional[str]
    risk_concerns: Optional[str]
    opportunities: Optional[str]
    risk_factors: Optional[str]
    ai_explanation: Optional[str]
    
    # Override
    is_overridden: bool
    overridden_score: Optional[float]
    override_reason: Optional[str]
    overridden_by: Optional[str]
    override_date: Optional[datetime.datetime]
    
    created_at: datetime.datetime
    updated_at: datetime.datetime
    history: List[ScoreHistoryResponse] = []

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def set_fhc_score(self) -> 'FinancialHealthCardResponse':
        if self.fhc_score is None:
            self.fhc_score = self.overall_score
        return self

class CalculationRequest(BaseModel):
    customer_id: int

class ScoreOverrideRequest(BaseModel):
    overridden_score: float
    override_reason: str
    overridden_by: str

class ConfigUpdateRequest(BaseModel):
    weights: Dict[str, float]
    thresholds: Dict[str, Any]

class CompareRequest(BaseModel):
    customer_ids: List[int]
