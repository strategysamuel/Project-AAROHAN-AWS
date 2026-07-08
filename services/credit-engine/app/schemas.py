from pydantic import BaseModel
import datetime
from typing import List, Optional

class HumanApprovalLogResponse(BaseModel):
    id: int
    approver_id: str
    action: str
    comments: Optional[str]
    signed_at: datetime.datetime

    class Config:
        from_attributes = True

class AICreditDecisionResponse(BaseModel):
    id: int
    customer_id: int
    recommendation: str
    confidence_score: float
    ai_narrative: str
    policy_status: str
    approval_status: str
    created_at: datetime.datetime
    approvals: List[HumanApprovalLogResponse] = []

    class Config:
        from_attributes = True

class EvaluationRequest(BaseModel):
    customer_id: int

class ApprovalSubmission(BaseModel):
    approver_id: str
    action: str # APPROVED, REJECTED, REQUEST_MORE_INFO
    comments: Optional[str] = None
