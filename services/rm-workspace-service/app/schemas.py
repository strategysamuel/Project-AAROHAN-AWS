from pydantic import BaseModel
import datetime
from typing import List, Optional

class RMTaskBase(BaseModel):
    customer_id: int
    title: str
    description: Optional[str] = None
    due_date: datetime.datetime
    status: str = "PENDING"
    priority: str = "MEDIUM"

class RMTaskCreate(RMTaskBase):
    pass

class RMTaskResponse(RMTaskBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class RMLeadBase(BaseModel):
    company_name: str
    contact_person: str
    mobile: str
    pipeline_stage: str = "QUALIFICATION"
    estimated_loan_amt: float

class RMLeadCreate(RMLeadBase):
    pass

class RMLeadResponse(RMLeadBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class RMAlertResponse(BaseModel):
    id: int
    customer_id: int
    alert_type: str
    message: str
    severity: str
    is_read: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class RMInteractionCreate(BaseModel):
    customer_id: int
    staff_id: str
    interaction_type: str
    notes: str

class RMInteractionResponse(RMInteractionCreate):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class AssistantChatRequest(BaseModel):
    prompt: str

class NextBestActionResponse(BaseModel):
    action_code: str
    title: str
    description: str
    priority: str
