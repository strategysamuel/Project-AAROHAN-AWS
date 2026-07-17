"""
RBI Fraud Registry – Pydantic Request/Response Schemas
"""
from pydantic import BaseModel, ConfigDict
import datetime
from typing import List, Optional, Dict, Any


class RBIFraudRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    entity_type: str
    entity_value: str
    is_blacklisted: bool
    fraud_score: float
    fraud_category: str
    risk_level: str
    risk_flags: str
    ai_insights: Optional[str] = None
    is_overridden: bool
    override_reason: Optional[str] = None
    overridden_by: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class FraudWatchlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    watchlist_type: str
    value: str
    reason: Optional[str] = None
    flagged_at: datetime.datetime


class WatchlistItemRequest(BaseModel):
    watchlist_type: str
    value: str
    reason: Optional[str] = None


class VerifyRequest(BaseModel):
    customer_id: int
    entity_type: str   # CUSTOMER | BUSINESS | PAN | GSTIN | DIRECTOR | ACCOUNT | DOCUMENT
    entity_value: str


class OverrideRequest(BaseModel):
    override_reason: str
    overridden_by: str


class ConfigUpdateRequest(BaseModel):
    active_adapter: str
    rule_parameters: Dict[str, Any]


# ── Dashboard Schemas ──────────────────────────────────────────────────────

class FraudDashboardEntry(BaseModel):
    """Single row in the Fraud Dashboard summary."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    entity_type: str
    entity_value: str
    fraud_score: float
    risk_level: str
    fraud_category: str
    is_blacklisted: bool
    is_overridden: bool
    risk_flags: str
    ai_insights: Optional[str] = None
    created_at: datetime.datetime


class FraudDashboardResponse(BaseModel):
    """Aggregate Fraud Dashboard payload."""
    total_screened: int
    cleared: int
    low_risk: int
    medium_risk: int
    high_risk: int
    critical_risk: int
    blacklisted: int
    overridden: int
    pending_investigation: int
    recent_alerts: List[FraudDashboardEntry]
    investigation_queue: List[FraudDashboardEntry]


class FraudAssessmentResponse(BaseModel):
    """Full consolidated fraud assessment for a single customer."""
    customer_id: int
    overall_risk_level: str
    overall_fraud_score: float
    aml_status: str
    fraud_categories_detected: List[str]
    all_risk_flags: List[str]
    ai_observations: List[str]
    screening_records: List[RBIFraudRecordResponse]
    recommendation: str
