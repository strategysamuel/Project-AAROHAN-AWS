from pydantic import BaseModel
import datetime
from typing import List, Optional

class ScoreHistoryResponse(BaseModel):
    id: int
    recorded_at: datetime.datetime
    score_value: float

    class Config:
        from_attributes = True

class FinancialHealthCardResponse(BaseModel):
    id: int
    customer_id: int
    overall_score: float
    revenue_health_score: float
    cash_flow_score: float
    liquidity_score: float
    banking_behaviour_score: float
    compliance_score: float
    growth_score: float
    key_strengths: Optional[str]
    risk_concerns: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    history: List[ScoreHistoryResponse] = []

    class Config:
        from_attributes = True

class CalculationRequest(BaseModel):
    customer_id: int
