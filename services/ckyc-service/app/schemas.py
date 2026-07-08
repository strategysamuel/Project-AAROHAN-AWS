from pydantic import BaseModel, Field, ConfigDict
import datetime
from typing import List, Optional

class CKYCRecordResponse(BaseModel):
    id: int
    customer_id: int
    ckyc_number: str
    full_name: str
    dob: str
    pan: str
    kyc_status: str
    last_synced_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class CKYCVerificationLogResponse(BaseModel):
    id: int
    customer_id: int
    checked_by: str
    match_confidence: float
    anomaly_detected: bool
    verification_status: str
    verified_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class CKYCSearchRequest(BaseModel):
    pan: str = Field(..., pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")

class CKYCVerificationRequest(BaseModel):
    customer_id: int
    checked_by: str
