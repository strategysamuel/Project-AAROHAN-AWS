from pydantic import BaseModel
import datetime
from typing import List, Optional

class CAMVersionResponse(BaseModel):
    id: int
    version_num: int
    edited_by: str
    edited_at: datetime.datetime
    change_summary: Optional[str]
    executive_summary: str
    business_profile: str
    financial_analysis: str
    swot_analysis: str
    risk_assessment: str

    class Config:
        from_attributes = True

class CAMRecordResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    current_version: int
    executive_summary: str
    business_profile: str
    financial_analysis: str
    swot_analysis: str
    risk_assessment: str
    collateral_assessment: Optional[str]
    ai_recommendation: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    versions: List[CAMVersionResponse] = []

    class Config:
        from_attributes = True

class CAMUpdateRequest(BaseModel):
    edited_by: str
    change_summary: str
    executive_summary: str
    business_profile: str
    financial_analysis: str
    swot_analysis: str
    risk_assessment: str
    collateral_assessment: Optional[str] = None

class CAMApprovalRequest(BaseModel):
    approver_id: str
    action: str # APPROVED, REJECTED
    comments: Optional[str] = None
