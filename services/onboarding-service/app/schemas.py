from pydantic import BaseModel, Field, EmailStr, field_validator
import re
import datetime
from typing import List, Optional

# Regular expression patterns for Indian financial registry validation
PAN_REGEX = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")
GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")
CIN_REGEX = re.compile(r"^[U|L][0-9]{5}[A-Z]{2}[0-9]{4}[PTC][0-9]{6}$")
AADHAAR_REGEX = re.compile(r"^(X{8}\d{4})|(\d{12})$") # Supports full 12-digit or masked (8 Xs + 4 digits)
MOBILE_REGEX = re.compile(r"^\d{10}$")
PINCODE_REGEX = re.compile(r"^\d{6}$")

class AddressBase(BaseModel):
    address_line1: str = Field(..., min_length=5)
    address_line2: Optional[str] = None
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    pincode: str
    address_type: str = Field("OFFICE")

    @field_validator("pincode")
    def validate_pincode(cls, v):
        if not PINCODE_REGEX.match(v):
            raise ValueError("Pincode must be exactly 6 digits.")
        return v

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True

class ProprietorDirectorBase(BaseModel):
    full_name: str = Field(..., min_length=3)
    pan: str
    aadhaar_masked: str
    mobile: str

    @field_validator("pan")
    def validate_pan(cls, v):
        if not PAN_REGEX.match(v):
            raise ValueError("Invalid PAN format. Must be 5 uppercase letters, 4 digits, and 1 uppercase letter.")
        return v

    @field_validator("aadhaar_masked")
    def validate_aadhaar(cls, v):
        if not AADHAAR_REGEX.match(v):
            raise ValueError("Invalid Aadhaar structure. Must be 12 digits or masked (e.g. XXXXXXXX1234).")
        return v

    @field_validator("mobile")
    def validate_mobile(cls, v):
        if not MOBILE_REGEX.match(v):
            raise ValueError("Mobile must be exactly 10 digits.")
        return v

class ProprietorDirectorCreate(ProprietorDirectorBase):
    pass

class ProprietorDirectorResponse(ProprietorDirectorBase):
    id: int

    class Config:
        from_attributes = True

class BusinessEntityBase(BaseModel):
    trade_name: str = Field(..., min_length=3)
    gstin: str
    cin: Optional[str] = None
    constitution_type: str
    annual_turnover: float = Field(0.0, ge=0.0)
    industry_segment: str
    lifecycle_state: str = "REGISTERED"

    @field_validator("gstin")
    def validate_gstin(cls, v):
        if not GSTIN_REGEX.match(v):
            raise ValueError("Invalid GSTIN structure format.")
        return v

    @field_validator("cin")
    def validate_cin(cls, v):
        if v and not CIN_REGEX.match(v):
            raise ValueError("Invalid CIN format.")
        return v

class BusinessEntityCreate(BusinessEntityBase):
    directors: List[ProprietorDirectorCreate] = []

class BusinessEntityResponse(BusinessEntityBase):
    id: int
    directors: List[ProprietorDirectorResponse] = []

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    legal_name: str = Field(..., min_length=3)
    mobile_number: str
    email: EmailStr
    pan: str

    @field_validator("pan")
    def validate_pan(cls, v):
        if not PAN_REGEX.match(v):
            raise ValueError("Invalid PAN format.")
        return v

    @field_validator("mobile_number")
    def validate_mobile(cls, v):
        if not MOBILE_REGEX.match(v):
            raise ValueError("Mobile must be 10 digits.")
        return v

class CustomerCreate(CustomerBase):
    businesses: List[BusinessEntityCreate] = []
    addresses: List[AddressCreate] = []

class CustomerResponse(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime.datetime
    businesses: List[BusinessEntityResponse] = []
    addresses: List[AddressResponse] = []

    class Config:
        from_attributes = True
