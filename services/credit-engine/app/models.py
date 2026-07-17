from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


class AICreditDecision(Base):
    __tablename__ = "ai_credit_decisions"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    recommendation = Column(String(50), nullable=False) # APPROVED, REJECTED, PENDING_HUMAN_REVIEW, MANUAL_REVIEW, APPROVE_WITH_CONDITIONS
    confidence_score = Column(Float, default=0.0) # 0.0 to 100.0
    decision_score = Column(Float, default=0.0) # 0.0 to 100.0
    risk_grade = Column(String(50), default="Medium") # Low, Medium, High, Critical
    approval_probability = Column(Float, default=0.0) # 0.0 to 1.0
    
    # Lending Recommendation
    eligible_loan_amount = Column(Float, default=0.0)
    recommended_product = Column(String(150), nullable=True)
    recommended_tenure = Column(Integer, default=12) # in months
    recommended_interest_rate = Column(Float, default=10.5) # % p.a.
    collateral_recommendation = Column(String(300), nullable=True)
    repayment_capacity = Column(String(100), default="Adequate")
    emi_estimate = Column(Float, default=0.0)
    debt_service_capacity = Column(String(100), default="Adequate")
    
    # Explainable AI
    top_positive_factors = Column(String(1000), nullable=True)
    top_negative_factors = Column(String(1000), nullable=True)
    risk_drivers = Column(String(1000), nullable=True)
    decision_explanation = Column(Text, nullable=True)
    recommended_actions = Column(String(1000), nullable=True)
    
    ai_narrative = Column(Text, nullable=True) # Gemini generated analytical commentary
    policy_status = Column(String(50), default="COMPLIANT") # COMPLIANT, VIOLATION
    approval_status = Column(String(50), default="PENDING_HUMAN_REVIEW") # PENDING_HUMAN_REVIEW, APPROVED, REJECTED
    rbi_fraud_status = Column(String(50), default="CLEAN") # CLEAN, BLACKLISTED, PENDING_MANUAL_CHECK
    rbi_verification_log = Column(String(500), nullable=True)
    explainability_tags = Column(String(500), default="") # Comma-separated list of tags
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    approvals = relationship("HumanApprovalLog", back_populates="decision", cascade="all, delete-orphan")

class HumanApprovalLog(Base):
    __tablename__ = "human_approval_logs"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("ai_credit_decisions.id"), nullable=False)
    approver_id = Column(String(100), nullable=False) # Staff/Underwriter ID
    action = Column(String(50), nullable=False) # APPROVED, REJECTED, REQUEST_MORE_INFO
    comments = Column(String(500), nullable=True) # Text feedback capturing underwriting notes
    signed_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    decision = relationship("AICreditDecision", back_populates="approvals")

class CreditEngineConfig(Base):
    __tablename__ = "credit_engine_config"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    active_adapter = Column(String(100), default="RULE_ENGINE") # RULE_ENGINE, VERTEX_AI, CUSTOM_ML, OPENAI_LLM
    risk_thresholds = Column(Text, nullable=True) # JSON string for thresholds
    rule_parameters = Column(Text, nullable=True) # JSON string for rule params
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# ============================================================
# Mapping models for Aggregated Services (Read-Only)
# ============================================================

class FinancialHealthCard(Base):
    __tablename__ = "fhc_cards"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, unique=True, index=True)
    overall_score = Column(Float)
    rating = Column(String)
    identity_score = Column(Float)
    compliance_score = Column(Float)
    liquidity_score = Column(Float)
    revenue_score = Column(Float)
    cash_flow_score = Column(Float)
    business_stability_score = Column(Float)
    governance_score = Column(Float)
    workforce_score = Column(Float)
    banking_behaviour_score = Column(Float)
    growth_score = Column(Float)

class OnboardingCustomer(Base):
    __tablename__ = "onboarding_customers"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    legal_name = Column(String)
    mobile_number = Column(String)
    email = Column(String)
    pan = Column(String)
    onboarding_status = Column(String)

class OnboardingBusiness(Base):
    __tablename__ = "onboarding_businesses"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    trade_name = Column(String)
    gstin = Column(String)
    udyam_number = Column(String)
    cin = Column(String)
    constitution_type = Column(String)
    annual_turnover = Column(Float)
    industry_segment = Column(String)
    business_vintage_years = Column(Integer)
    employee_count = Column(Integer)

class CKYCRecord(Base):
    __tablename__ = "ckyc_records"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    ckyc_number = Column(String)
    kyc_status = Column(String)
    pan = Column(String)

class CKYCVerificationLog(Base):
    __tablename__ = "ckyc_verification_logs"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    match_confidence = Column(Float)
    anomaly_detected = Column(Boolean)
    verification_status = Column(String)

class GSTAnalytics(Base):
    __tablename__ = "gst_analytics"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer)
    compliance_score = Column(Float)
    risk_level = Column(String)

class AAAnalytics(Base):
    __tablename__ = "aa_analytics"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    net_cash_flow = Column(Float)
    cash_flow_stability = Column(Float)
    cheque_bounce_indicator = Column(Boolean)
    overdraft_usage = Column(String)

class EPFOAnalytics(Base):
    __tablename__ = "epfo_analytics"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer)
    compliance_score = Column(Float)

class MCACompanyProfile(Base):
    __tablename__ = "mca_company_profiles"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    company_status = Column(String)

class MCAGovernanceAnalytics(Base):
    __tablename__ = "mca_governance_analytics"
    __table_args__ = {'extend_existing': True}
    {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    governance_score = Column(Float)
    compliance_score = Column(Float)
    overall_risk_level = Column(String)
