from pydantic import BaseModel, Field, ConfigDict
import datetime
from typing import List, Optional

class EPFOContributionResponse(BaseModel):
    id: int
    wage_month: str
    amount_paid: float
    employer_share: float
    employees_count: int
    payment_date: Optional[datetime.datetime]
    status: str

    model_config = ConfigDict(from_attributes=True)

class EPFOEmployeeResponse(BaseModel):
    id: int
    uan: str
    name: str
    joining_date: datetime.datetime
    exit_date: Optional[datetime.datetime] = None
    salary: float
    designation: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class EPFOAnalyticsResponse(BaseModel):
    id: int
    active_employees: int
    attrition_rate: float
    avg_employee_tenure: float
    monthly_payroll: float
    payroll_growth: float
    hiring_trend: str
    workforce_growth: float
    payroll_stability_index: float
    compliance_score: float
    
    payroll_risk: str
    compliance_risk: str
    attrition_risk: str
    workforce_stability_risk: str
    business_continuity_risk: str
    
    ai_insights: str

    model_config = ConfigDict(from_attributes=True)

class EPFOProfileResponse(BaseModel):
    id: int
    customer_id: int
    establishment_id: str
    establishment_name: str
    esic_registration_num: Optional[str]
    status: str
    number_of_employees: int
    average_monthly_payroll: float
    last_synced_at: datetime.datetime
    contributions: List[EPFOContributionResponse] = []
    employees: List[EPFOEmployeeResponse] = []
    analytics: List[EPFOAnalyticsResponse] = []

    model_config = ConfigDict(from_attributes=True)

class EPFOSyncRequest(BaseModel):
    establishment_id: str = Field(..., pattern=r"^[A-Z]{5}[0-9]{10}([0-9]{7})?$") # Standard 15-char or 22-char code validation check
    esic_registration_num: Optional[str] = None

class EPFOOverrideRequest(BaseModel):
    compliance_score: float
    checked_by: str
    comments: str
