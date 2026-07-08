from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

class TReDSBuyerResponse(BaseModel):
    id: int
    buyer_pan: str
    buyer_name: str
    credit_rating: str
    payment_behaviour_days: int

    class Config:
        from_attributes = True

class TReDSInvoiceResponse(BaseModel):
    id: int
    customer_id: int
    invoice_number: str
    buyer_pan: str
    buyer_name: str
    amount: float
    tenure_days: int
    issue_date: datetime.datetime
    due_date: datetime.datetime
    status: str
    last_synced_at: datetime.datetime

    class Config:
        from_attributes = True

class TReDSSyncRequest(BaseModel):
    seller_pan: str = Field(..., pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")
