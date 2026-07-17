from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


class RBIFraudRecord(Base):
    __tablename__ = "rbi_fraud_records"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    entity_type = Column(String(50), default="CUSTOMER") # CUSTOMER, BUSINESS, PAN, GSTIN, DIRECTOR, ACCOUNT
    entity_value = Column(String(100), nullable=False) # e.g. PAN string, GSTIN string, Account Number
    
    is_blacklisted = Column(Boolean, default=False)
    fraud_score = Column(Float, default=0.0) # 0 to 100
    fraud_category = Column(String(100), default="None") # Identity Fraud, Financial Fraud, Document Fraud, Transaction Fraud, Corporate Fraud
    risk_level = Column(String(50), default="Low") # Low, Medium, High, Critical
    risk_flags = Column(String(500), default="") # Comma-separated risk indicators
    ai_insights = Column(Text, nullable=True)
    
    # Audit & Override Controls
    is_overridden = Column(Boolean, default=False)
    override_reason = Column(String(500), nullable=True)
    overridden_by = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class FraudWatchlist(Base):
    __tablename__ = "rbi_fraud_watchlist"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    watchlist_type = Column(String(50), nullable=False) # PAN, GSTIN, ACCOUNT, DIRECTOR, CUSTOMER, BUSINESS
    value = Column(String(100), unique=True, nullable=False, index=True)
    reason = Column(String(250), nullable=True)
    flagged_at = Column(DateTime, default=datetime.datetime.utcnow)

class FraudServiceConfig(Base):
    __tablename__ = "rbi_fraud_config"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    active_adapter = Column(String(100), default="SIMULATION") # SIMULATION, SANDBOX, PRODUCTION
    rule_parameters = Column(Text, nullable=True) # JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# ============================================================
# Mapping models for Aggregated Services (Read-Only)
# ============================================================

class OnboardingCustomer(Base):
    __tablename__ = "onboarding_customers"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    legal_name = Column(String)
    mobile_number = Column(String)
    email = Column(String)
    pan = Column(String)

class OnboardingBusiness(Base):
    __tablename__ = "onboarding_businesses"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    trade_name = Column(String)
    gstin = Column(String)
    cin = Column(String)

class CKYCVerificationLog(Base):
    __tablename__ = "ckyc_verification_logs"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    match_confidence = Column(Float)
    anomaly_detected = Column(Boolean)

class AAAnalytics(Base):
    __tablename__ = "aa_analytics"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    cheque_bounce_indicator = Column(Boolean)
    overdraft_usage = Column(String)

class MCAGovernanceAnalytics(Base):
    __tablename__ = "mca_governance_analytics"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    overall_risk_level = Column(String)
