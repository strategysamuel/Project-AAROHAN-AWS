from pydantic import BaseModel, Field, ConfigDict
import datetime
from typing import List, Optional

class AATransactionResponse(BaseModel):
    id: int
    account_id: int
    txn_ref_num: str
    txn_date: datetime.datetime
    amount: float
    txn_type: str
    narration: Optional[str] = None
    category: str
    is_recurring: bool

    model_config = ConfigDict(from_attributes=True)

class LinkedAccountResponse(BaseModel):
    id: int
    customer_id: int
    account_ref_num: str
    masked_acc_num: str
    bank_name: str
    account_type: str
    balance: float
    currency: str
    is_active: bool
    last_synced_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AAAnalyticsResponse(BaseModel):
    id: int
    customer_id: int
    total_inflow: float
    total_outflow: float
    net_cash_flow: float
    avg_balance: float
    median_balance: float
    income_score: float
    debt_service_ratio: float
    
    monthly_credits: float
    monthly_debits: float
    cash_flow_stability: float
    seasonality: float
    income_stability: float
    expense_ratio: float
    working_capital_estimate: float
    savings_behaviour: str
    
    salary_regularity: str
    business_revenue_stability: str
    cheque_bounce_indicator: bool
    emi_discipline: str
    overdraft_usage: str
    high_cash_dependency: bool
    large_cash_withdrawals: bool
    frequent_low_balance: bool
    dormant_account: bool
    
    liquidity_risk: str
    cash_flow_risk: str
    behaviour_risk: str
    income_risk: str
    expense_risk: str
    banking_stability_score: float
    overall_score: float
    
    ai_insights: str
    last_calculated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class AAConsentResponse(BaseModel):
    id: int
    customer_id: int
    consent_artefact_id: str
    purpose: str
    data_requested: str
    validity: str
    frequency: str
    accounts_included: Optional[str] = None
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class AAConsentCreateRequest(BaseModel):
    customer_id: int
    purpose: str
    data_requested: str = "Transactions and Balance"
    validity_days: int = 30
    frequency: str = "ONCE"

class ConsentStatusUpdateRequest(BaseModel):
    status: str # APPROVED, REJECTED, EXPIRED, REVOKED
    accounts_included: Optional[str] = None

class DiscoveryRequest(BaseModel):
    customer_mobile: str = Field(..., pattern=r"^\d{10}$")

class LinkAccountRequest(BaseModel):
    account_ref_num: str
    masked_acc_num: str
    bank_name: str
    account_type: str

class SyncRequest(BaseModel):
    consent_id: str
