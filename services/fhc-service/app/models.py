import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class FinancialHealthCard(Base):
    __tablename__ = "fhc_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, unique=True, index=True)
    
    # Composite Score
    overall_score = Column(Float, default=0.0) # Overall rating (0 to 100)
    rating = Column(String(10), default="D") # AAA, AA, A, BBB, BB, B, CCC, CC, C, D
    
    # 10 Sub-Scores (Value, Weight, Reason, Recommendation)
    identity_score = Column(Float, default=0.0)
    identity_weight = Column(Float, default=0.10)
    identity_reason = Column(String(500), nullable=True)
    identity_recommendation = Column(String(500), nullable=True)
    
    compliance_score = Column(Float, default=0.0)
    compliance_weight = Column(Float, default=0.10)
    compliance_reason = Column(String(500), nullable=True)
    compliance_recommendation = Column(String(500), nullable=True)
    
    liquidity_score = Column(Float, default=0.0)
    liquidity_weight = Column(Float, default=0.15)
    liquidity_reason = Column(String(500), nullable=True)
    liquidity_recommendation = Column(String(500), nullable=True)
    
    revenue_score = Column(Float, default=0.0)
    revenue_weight = Column(Float, default=0.10)
    revenue_reason = Column(String(500), nullable=True)
    revenue_recommendation = Column(String(500), nullable=True)
    revenue_health_score = Column(Float, default=0.0)
    
    cash_flow_score = Column(Float, default=0.0)
    cash_flow_weight = Column(Float, default=0.15)
    cash_flow_reason = Column(String(500), nullable=True)
    cash_flow_recommendation = Column(String(500), nullable=True)
    
    business_stability_score = Column(Float, default=0.0)
    business_stability_weight = Column(Float, default=0.10)
    business_stability_reason = Column(String(500), nullable=True)
    business_stability_recommendation = Column(String(500), nullable=True)
    
    governance_score = Column(Float, default=0.0)
    governance_weight = Column(Float, default=0.05)
    governance_reason = Column(String(500), nullable=True)
    governance_recommendation = Column(String(500), nullable=True)
    
    workforce_score = Column(Float, default=0.0)
    workforce_weight = Column(Float, default=0.05)
    workforce_reason = Column(String(500), nullable=True)
    workforce_recommendation = Column(String(500), nullable=True)
    
    banking_behaviour_score = Column(Float, default=0.0)
    banking_behaviour_weight = Column(Float, default=0.10)
    banking_behaviour_reason = Column(String(500), nullable=True)
    banking_behaviour_recommendation = Column(String(500), nullable=True)
    
    growth_score = Column(Float, default=0.0)
    growth_weight = Column(Float, default=0.10)
    growth_reason = Column(String(500), nullable=True)
    growth_recommendation = Column(String(500), nullable=True)
    
    # 14 Financial Dimensions
    identity_trust_score = Column(Float, default=0.0)
    business_compliance_score = Column(Float, default=0.0)
    gst_health_score = Column(Float, default=0.0)
    banking_behaviour_dim_score = Column(Float, default=0.0)
    cash_flow_stability_score = Column(Float, default=0.0)
    liquidity_dim_score = Column(Float, default=0.0)
    revenue_growth_score = Column(Float, default=0.0)
    working_capital_score = Column(Float, default=0.0)
    profitability_score = Column(Float, default=0.0)
    payroll_stability_score = Column(Float, default=0.0)
    corporate_governance_score = Column(Float, default=0.0)
    operational_stability_score = Column(Float, default=0.0)
    business_continuity_score = Column(Float, default=0.0)
    digital_adoption_score = Column(Float, default=0.0)
    overall_financial_strength_score = Column(Float, default=0.0)
    
    # AI Explainability details
    key_strengths = Column(String(500), nullable=True) # Semi-colon separated key positive factors
    risk_concerns = Column(String(500), nullable=True) # Semi-colon separated risk triggers
    opportunities = Column(String(500), nullable=True)
    risk_factors = Column(String(500), nullable=True)
    ai_explanation = Column(Text, nullable=True)
    
    # Administration and Override Controls
    is_overridden = Column(Boolean, default=False)
    overridden_score = Column(Float, nullable=True)
    override_reason = Column(String(500), nullable=True)
    overridden_by = Column(String(100), nullable=True)
    override_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    history = relationship("ScoreHistory", back_populates="card", cascade="all, delete-orphan")

class ScoreHistory(Base):
    __tablename__ = "fhc_score_history"
    
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("fhc_cards.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
    score_value = Column(Float, nullable=False)
    rating = Column(String(10), default="D")
    
    card = relationship("FinancialHealthCard", back_populates="history")

class FHCConfig(Base):
    __tablename__ = "fhc_config"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), unique=True, default="default")
    weights = Column(Text, nullable=False) # JSON string for weights
    thresholds = Column(Text, nullable=False) # JSON string for thresholds and ratings
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


# ============================================================
# Mapping models for Aggregated Services (Read-Only)
# ============================================================

class OnboardingCustomer(Base):
    __tablename__ = "onboarding_customers"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    legal_name = Column(String)
    mobile_number = Column(String)
    email = Column(String)
    pan = Column(String)
    onboarding_status = Column(String)

class OnboardingBusiness(Base):
    __tablename__ = "onboarding_businesses"
    __table_args__ = {'extend_existing': True}
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
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    ckyc_number = Column(String)
    kyc_status = Column(String)

class CKYCVerificationLog(Base):
    __tablename__ = "ckyc_verification_logs"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    match_confidence = Column(Float)
    risk_indicators = Column(String)
    anomaly_detected = Column(Boolean)
    verification_status = Column(String)

class GSTProfile(Base):
    __tablename__ = "gst_profiles"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    gstin = Column(String)
    status = Column(String)

class GSTAnalytics(Base):
    __tablename__ = "gst_analytics"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer)
    avg_monthly_turnover = Column(Float)
    revenue_growth_rate = Column(Float)
    revenue_stability = Column(Float)
    compliance_score = Column(Float)
    filing_delay_score = Column(Float)
    working_capital_estimate = Column(Float)
    revenue_volatility = Column(Float)
    business_stability_score = Column(Float)
    risk_indicators = Column(String)
    risk_level = Column(String)
    ai_insights = Column(Text)

class AAAnalytics(Base):
    __tablename__ = "aa_analytics"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    total_inflow = Column(Float)
    total_outflow = Column(Float)
    net_cash_flow = Column(Float)
    avg_balance = Column(Float)
    income_score = Column(Float)
    cash_flow_stability = Column(Float)
    overdraft_usage = Column(String)
    cheque_bounce_indicator = Column(Boolean)
    emi_discipline = Column(String)
    frequent_low_balance = Column(Boolean)
    dormant_account = Column(Boolean)
    liquidity_risk = Column(String)
    cash_flow_risk = Column(String)
    banking_stability_score = Column(Float)
    overall_score = Column(Float)

class EPFOProfile(Base):
    __tablename__ = "epfo_profiles"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    number_of_employees = Column(Integer)

class EPFOAnalytics(Base):
    __tablename__ = "epfo_analytics"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer)
    active_employees = Column(Integer)
    attrition_rate = Column(Float)
    payroll_growth = Column(Float)
    workforce_growth = Column(Float)
    payroll_stability_index = Column(Float)
    compliance_score = Column(Float)
    workforce_stability_risk = Column(String)
    business_continuity_risk = Column(String)

class MCACompanyProfile(Base):
    __tablename__ = "mca_company_profiles"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    cin = Column(String)
    company_status = Column(String)
    authorized_capital = Column(Float)
    paid_up_capital = Column(Float)

class MCAGovernanceAnalytics(Base):
    __tablename__ = "mca_governance_analytics"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    compliance_score = Column(Float)
    governance_score = Column(Float)
    overall_risk_level = Column(String)

class MCADirector(Base):
    __tablename__ = "mca_directors"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    is_disqualified = Column(Boolean)

class MCACharge(Base):
    __tablename__ = "mca_charges"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    charge_amount = Column(Float)
    status = Column(String)
