from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

class MCADirectorResponse(BaseModel):
    id: int
    din: str
    full_name: str
    appointment_date: datetime.datetime

    class Config:
        from_attributes = True

class MCAChargeResponse(BaseModel):
    id: int
    charge_id: str
    holder_name: str
    charge_amount: float
    creation_date: datetime.datetime
    status: str

    class Config:
        from_attributes = True

class MCACompanyFilingResponse(BaseModel):
    id: int
    form_name: str
    filing_date: datetime.datetime
    status: str

    class Config:
        from_attributes = True

class MCACompanyProfileResponse(BaseModel):
    id: int
    customer_id: int
    cin: str
    company_name: str
    incorporation_date: datetime.datetime
    company_status: str
    class_of_company: str
    authorized_capital: float
    paid_up_capital: float
    last_synced_at: datetime.datetime
    directors: List[MCADirectorResponse] = []
    charges: List[MCAChargeResponse] = []
    filings: List[MCACompanyFilingResponse] = []

    class Config:
        from_attributes = True

class MCASyncRequest(BaseModel):
    cin: str = Field(..., pattern=r"^[U|L][0-9]{5}[A-Z]{2}[0-9]{4}[PTC][0-9]{6}$")
