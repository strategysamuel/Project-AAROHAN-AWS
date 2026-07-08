from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

class EPFOContributionResponse(BaseModel):
    id: int
    wage_month: str
    amount_paid: float
    employees_count: int
    payment_date: Optional[datetime.datetime]
    status: str

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

class EPFOSyncRequest(BaseModel):
    establishment_id: str = Field(..., pattern=r"^[A-Z]{5}[0-9]{7}[0-9]{3}[0-9]{7}$") # Standard 15-char code validation check
    esic_registration_num: Optional[str] = None
