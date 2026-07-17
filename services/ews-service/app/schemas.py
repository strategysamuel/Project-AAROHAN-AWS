from pydantic import BaseModel, ConfigDict
import datetime
from typing import List, Optional

class EWSWatchlistResponse(BaseModel):
    id: int
    customer_id: int
    risk_level: str
    added_at: datetime.datetime
    reason_code: str

    model_config = ConfigDict(from_attributes=True)

class EWSAlertResponse(BaseModel):
    id: int
    customer_id: int
    trigger_rule: str
    message: str
    created_at: datetime.datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class EWSRiskCaseResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    ai_risk_narrative: str
    mitigation_action: Optional[str]
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class EscalationRequest(BaseModel):
    comments: str
