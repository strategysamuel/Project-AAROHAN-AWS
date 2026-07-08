import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class GSTProfile(Base):
    __tablename__ = "gst_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    gstin = Column(String(15), unique=True, nullable=False, index=True)
    legal_name = Column(String(200), nullable=False)
    trade_name = Column(String(200), nullable=True)
    registration_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="ACTIVE") # ACTIVE, SUSPENDED, CANCELLED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    returns = relationship("GSTReturn", back_populates="profile", cascade="all, delete-orphan")
    analytics = relationship("GSTAnalytics", back_populates="profile", cascade="all, delete-orphan")

class GSTReturn(Base):
    __tablename__ = "gst_returns"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("gst_profiles.id"), nullable=False)
    return_type = Column(String(10), nullable=False) # GSTR1, GSTR3B
    financial_year = Column(String(10), nullable=False) # e.g. "2025-26"
    tax_period = Column(String(10), nullable=False) # e.g. "042025" (MMYYYY)
    filing_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="FILED") # FILED, PENDING
    gross_turnover = Column(Float, default=0.0)
    tax_paid = Column(Float, default=0.0)
    filing_delay_days = Column(Integer, default=0)
    
    profile = relationship("GSTProfile", back_populates="returns")

class GSTAnalytics(Base):
    __tablename__ = "gst_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("gst_profiles.id"), nullable=False)
    avg_monthly_turnover = Column(Float, default=0.0)
    peak_turnover_month = Column(String(10), nullable=True)
    revenue_growth_rate = Column(Float, default=0.0) # MoM or YoY change (%)
    revenue_stability = Column(Float, default=1.0) # Coefficient of variation or similar score (0.0 to 1.0)
    compliance_score = Column(Float, default=100.0) # 0 to 100 based on filings
    filing_delay_score = Column(Float, default=100.0) # 0 to 100 based on delays
    seasonality_index = Column(Float, default=0.0) # 0 to 1 based on variance
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    profile = relationship("GSTProfile", back_populates="analytics")
