from pydantic import BaseModel, Field, field_validator
import datetime
from typing import List, Optional

class ConsentPurposeBase(BaseModel):
    code: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    data_minimization_rules: Optional[str] = None

class ConsentPurposeCreate(ConsentPurposeBase):
    pass

class ConsentPurposeResponse(ConsentPurposeBase):
    id: int

    class Config:
        from_attributes = True

class ConsentBase(BaseModel):
    customer_id: int
    provider_type: str = Field(..., description="e.g. ACCOUNT_AGGREGATOR, GSTN, CKYC, DIGILOCKER")
    purpose_code: str
    valid_until: datetime.datetime

    @field_validator("valid_until")
    def validate_valid_until(cls, v):
        if v <= datetime.datetime.utcnow():
            raise ValueError("Expiration date must be in the future.")
        return v

    @field_validator("provider_type")
    def validate_provider(cls, v):
        valid = ["ACCOUNT_AGGREGATOR", "GSTN", "CKYC", "DIGILOCKER", "MCA", "EPFO", "TREDS"]
        if v not in valid:
            raise ValueError(f"Provider must be one of: {', '.join(valid)}")
        return v

class ConsentCreate(ConsentBase):
    pass

class ConsentArtifactResponse(BaseModel):
    id: int
    signature_hash: str
    signed_timestamp: datetime.datetime

    class Config:
        from_attributes = True

class ConsentResponse(ConsentBase):
    id: int
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    artifacts: List[ConsentArtifactResponse] = []

    class Config:
        from_attributes = True

class ConsentApprovalRequest(BaseModel):
    signature_hash: str

class ConsentSearchFilters(BaseModel):
    customer_id: Optional[int] = None
    status: Optional[str] = None
    provider_type: Optional[str] = None
