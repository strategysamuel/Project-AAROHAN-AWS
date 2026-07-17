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
    aadhaar_masked: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    kyc_status: str
    image_url: Optional[str] = None
    last_synced_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class CKYCVerificationLogResponse(BaseModel):
    id: int
    customer_id: int
    checked_by: str
    match_confidence: float
    risk_indicators: str
    anomaly_detected: bool
    verification_status: str
    comments: Optional[str] = None
    verified_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class CKYCSearchRequest(BaseModel):
    pan: str = Field(..., pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")

class CKYCVerificationRequest(BaseModel):
    checked_by: str = "SYSTEM"

class CKYCRecordCreate(BaseModel):
    customer_id: int
    ckyc_number: str
    full_name: str
    dob: str
    pan: str
    aadhaar_masked: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    kyc_status: str = "VERIFIED"
    image_url: Optional[str] = None

class CKYCRecordUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[str] = None
    pan: Optional[str] = None
    aadhaar_masked: Optional[str] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    kyc_status: Optional[str] = None
    image_url: Optional[str] = None

class CKYCOverrideRequest(BaseModel):
    checked_by: str
    status: str # VERIFIED, REJECTED, etc.
    comments: str
