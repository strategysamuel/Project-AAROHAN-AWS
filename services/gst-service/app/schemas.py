from pydantic import BaseModel, Field, ConfigDict
import datetime
from typing import List, Optional

class GSTReturnResponse(BaseModel):
    id: int
    return_type: str
    financial_year: str
    tax_period: str
    filing_date: Optional[datetime.datetime]
    status: str
    gross_turnover: float
    purchases: float
    tax_paid: float
    input_tax_credit: float
    filing_delay_days: int

    model_config = ConfigDict(from_attributes=True)

class GSTAnalyticsResponse(BaseModel):
    id: int
    avg_monthly_turnover: float
    peak_turnover_month: Optional[str]
    revenue_growth_rate: float
    revenue_stability: float
    compliance_score: float
    filing_delay_score: float
    seasonality_index: float
    working_capital_estimate: float
    revenue_volatility: float
    business_stability_score: float
    risk_indicators: str
    risk_level: str
    ai_insights: str

    model_config = ConfigDict(from_attributes=True)

class GSTProfileResponse(BaseModel):
    id: int
    customer_id: int
    gstin: str
    legal_name: str
    trade_name: Optional[str]
    registration_date: datetime.datetime
    status: str
    business_constitution: str
    filing_frequency: str
    returns: List[GSTReturnResponse] = []
    analytics: List[GSTAnalyticsResponse] = []

    model_config = ConfigDict(from_attributes=True)

class GSTSyncRequest(BaseModel):
    gstin: str = Field(..., pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")

class GSTOverrideRequest(BaseModel):
    risk_level: str # Low, Medium, High, Critical
    checked_by: str
    comments: str
