from pydantic import BaseModel, Field, ConfigDict
import datetime
from typing import List, Optional

class MCADirectorResponse(BaseModel):
    id: int
    din: str
    full_name: str
    appointment_date: datetime.datetime
    is_disqualified: bool

    model_config = ConfigDict(from_attributes=True)

class MCAChargeResponse(BaseModel):
    id: int
    charge_id: str
    holder_name: str
    charge_amount: float
    creation_date: datetime.datetime
    status: str

    model_config = ConfigDict(from_attributes=True)

class MCACompanyFilingResponse(BaseModel):
    id: int
    form_name: str
    filing_date: datetime.datetime
    status: str
    financial_year: str
    filing_delay_days: int

    model_config = ConfigDict(from_attributes=True)

class MCAFinancialStatementResponse(BaseModel):
    id: int
    financial_year: str
    revenue: float
    net_worth: float
    profit_after_tax: float
    debt: float

    model_config = ConfigDict(from_attributes=True)

class MCAGovernanceAnalyticsResponse(BaseModel):
    id: int
    company_age: float
    filing_consistency: str
    director_stability: str
    capital_structure: str
    net_worth_trend: str
    revenue_trend: str
    profit_trend: str
    debt_trend: str
    compliance_history: str
    compliance_score: float
    governance_score: float
    
    governance_risk: str
    regulatory_risk: str
    financial_reporting_risk: str
    director_risk: str
    legal_risk: str
    overall_risk_level: str
    
    ai_insights: str

    model_config = ConfigDict(from_attributes=True)

class MCACompanyProfileResponse(BaseModel):
    id: int
    customer_id: int
    cin: str
    company_name: str
    incorporation_date: datetime.datetime
    company_status: str
    class_of_company: str
    authorized_capital: float
    paid_up_capital: float
    registered_office: str
    roc: str
    last_synced_at: datetime.datetime
    directors: List[MCADirectorResponse] = []
    charges: List[MCAChargeResponse] = []
    filings: List[MCACompanyFilingResponse] = []
    financials: List[MCAFinancialStatementResponse] = []
    analytics: List[MCAGovernanceAnalyticsResponse] = []

    model_config = ConfigDict(from_attributes=True)

class MCASyncRequest(BaseModel):
    cin: str = Field(..., pattern=r"^[U|L][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$")

class MCAOverrideRequest(BaseModel):
    governance_score: float
    checked_by: str
    comments: str
