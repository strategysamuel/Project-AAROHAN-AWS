from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

class AATransactionResponse(BaseModel):
    id: int
    txn_ref_num: str
    txn_date: datetime.datetime
    amount: float
    txn_type: str
    narration: Optional[str]
    category: str
    is_recurring: bool

    class Config:
        from_attributes = True

class LinkedAccountResponse(BaseModel):
    id: int
    customer_id: int
    account_ref_num: str
    masked_acc_num: str
    bank_name: str
    account_type: str
    balance: float
    currency: str
    last_synced_at: datetime.datetime

    class Config:
        from_attributes = True

class AAAnalyticsResponse(BaseModel):
    id: int
    customer_id: int
    total_inflow: float
    total_outflow: float
    net_cash_flow: float
    avg_balance: float
    income_score: float
    debt_service_ratio: float
    last_calculated_at: datetime.datetime

    class Config:
        from_attributes = True

class DiscoveryRequest(BaseModel):
    customer_mobile: str = Field(..., pattern=r"^\d{10}$")

class LinkAccountRequest(BaseModel):
    account_ref_num: str
    bank_name: str
    account_type: str
    masked_acc_num: str

class SyncRequest(BaseModel):
    consent_id: int
