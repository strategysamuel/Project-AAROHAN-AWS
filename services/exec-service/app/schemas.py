from pydantic import BaseModel
import datetime
from typing import List, Optional

class ExecKPIResponse(BaseModel):
    id: int
    metric_name: str
    metric_value: float
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class ExecBranchPerformanceResponse(BaseModel):
    id: int
    branch_name: str
    region: str
    loan_disbursed_amt: float
    active_accounts: int
    average_health_score: float

    class Config:
        from_attributes = True

class ExecutiveBriefingResponse(BaseModel):
    briefing_date: datetime.date
    summary_text: str
    risk_warnings: List[str]
    strategic_recommendations: List[str]
