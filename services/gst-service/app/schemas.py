from pydantic import BaseModel, Field
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
    tax_paid: float
    filing_delay_days: int

    class Config:
        from_attributes = True

class GSTAnalyticsResponse(BaseModel):
    id: int
    avg_monthly_turnover: float
    peak_turnover_month: Optional[str]
    revenue_growth_rate: float
    revenue_stability: float
    compliance_score: float
    filing_delay_score: float
    seasonality_index: float

    class Config:
        from_attributes = True

class GSTProfileResponse(BaseModel):
    id: int
    customer_id: int
    gstin: str
    legal_name: str
    trade_name: Optional[str]
    registration_date: datetime.datetime
    status: str
    returns: List[GSTReturnResponse] = []
    analytics: List[GSTAnalyticsResponse] = []

    class Config:
        from_attributes = True

class GSTSyncRequest(BaseModel):
    gstin: str = Field(..., pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")
