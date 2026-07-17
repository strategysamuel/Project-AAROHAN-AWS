from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


class MCACompanyProfile(Base):
    __tablename__ = "mca_company_profiles"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, unique=True, nullable=False, index=True)
    cin = Column(String(21), unique=True, nullable=False, index=True) # 21-character CIN
    company_name = Column(String(200), nullable=False)
    incorporation_date = Column(DateTime, nullable=False)
    company_status = Column(String(50), default="ACTIVE") # ACTIVE, STRUCK_OFF, LIQUIDATED
    class_of_company = Column(String(50), nullable=False) # e.g. Private Limited, Public Limited
    authorized_capital = Column(Float, default=0.0)
    paid_up_capital = Column(Float, default=0.0)
    registered_office = Column(String(300), default="101, Textile Tower, Bandra East, Mumbai - 400051")
    roc = Column(String(100), default="ROC Mumbai")
    last_synced_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    directors = relationship("MCADirector", back_populates="company", cascade="all, delete-orphan")
    charges = relationship("MCACharge", back_populates="company", cascade="all, delete-orphan")
    filings = relationship("MCACompanyFiling", back_populates="company", cascade="all, delete-orphan")
    financials = relationship("MCAFinancialStatement", back_populates="company", cascade="all, delete-orphan")
    analytics = relationship("MCAGovernanceAnalytics", back_populates="company", cascade="all, delete-orphan")

class MCADirector(Base):
    __tablename__ = "mca_directors"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mca_company_profiles.id"), nullable=False)
    din = Column(String(8), nullable=False) # 8-character DIN
    full_name = Column(String(150), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    is_disqualified = Column(Boolean, default=False)
    
    company = relationship("MCACompanyProfile", back_populates="directors")

class MCACharge(Base):
    __tablename__ = "mca_charges"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mca_company_profiles.id"), nullable=False)
    charge_id = Column(String(50), nullable=False) # Charge registration ID
    holder_name = Column(String(200), nullable=False) # Lending Bank/FI
    charge_amount = Column(Float, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="OPEN") # OPEN, SATISFIED
    
    company = relationship("MCACompanyProfile", back_populates="charges")

class MCACompanyFiling(Base):
    __tablename__ = "mca_company_filings"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mca_company_profiles.id"), nullable=False)
    form_name = Column(String(50), nullable=False) # e.g. "AOC-4", "MGT-7"
    filing_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="APPROVED")
    financial_year = Column(String(20), default="2024-25")
    filing_delay_days = Column(Integer, default=0)
    
    company = relationship("MCACompanyProfile", back_populates="filings")

class MCAFinancialStatement(Base):
    __tablename__ = "mca_financial_statements"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mca_company_profiles.id"), nullable=False)
    financial_year = Column(String(20), nullable=False) # e.g. "2024-25"
    revenue = Column(Float, default=0.0)
    net_worth = Column(Float, default=0.0)
    profit_after_tax = Column(Float, default=0.0)
    debt = Column(Float, default=0.0)
    
    company = relationship("MCACompanyProfile", back_populates="financials")

class MCAGovernanceAnalytics(Base):
    __tablename__ = "mca_governance_analytics"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mca_company_profiles.id"), nullable=False)
    company_age = Column(Float, default=0.0)
    filing_consistency = Column(String(100), default="Consistent")
    director_stability = Column(String(100), default="Stable")
    capital_structure = Column(String(100), default="Sufficient")
    net_worth_trend = Column(String(100), default="Increasing")
    revenue_trend = Column(String(100), default="Increasing")
    profit_trend = Column(String(100), default="Increasing")
    debt_trend = Column(String(100), default="Stable")
    compliance_history = Column(String(300), default="")
    
    compliance_score = Column(Float, default=100.0)
    governance_score = Column(Float, default=100.0)
    
    # Risks
    governance_risk = Column(String(50), default="Low")
    regulatory_risk = Column(String(50), default="Low")
    financial_reporting_risk = Column(String(50), default="Low")
    director_risk = Column(String(50), default="Low")
    legal_risk = Column(String(50), default="Low")
    overall_risk_level = Column(String(50), default="Low")
    
    ai_insights = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    company = relationship("MCACompanyProfile", back_populates="analytics")
