from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


class EPFOEstablishmentProfile(Base):
    __tablename__ = "epfo_profiles"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, unique=True, nullable=False, index=True)
    establishment_id = Column(String(50), unique=True, nullable=False, index=True) # 15-character EPFO Code
    establishment_name = Column(String(200), nullable=False)
    esic_registration_num = Column(String(50), nullable=True) # 17-digit ESIC Code
    status = Column(String(50), default="ACTIVE")
    number_of_employees = Column(Integer, default=0)
    average_monthly_payroll = Column(Float, default=0.0)
    last_synced_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    contributions = relationship("EPFOContribution", back_populates="profile", cascade="all, delete-orphan")
    employees = relationship("EPFOEmployee", back_populates="profile", cascade="all, delete-orphan")
    analytics = relationship("EPFOAnalytics", back_populates="profile", cascade="all, delete-orphan")

class EPFOContribution(Base):
    __tablename__ = "epfo_contributions"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("epfo_profiles.id"), nullable=False)
    wage_month = Column(String(10), nullable=False) # e.g. "042025" (MMYYYY)
    amount_paid = Column(Float, default=0.0)
    employer_share = Column(Float, default=0.0)
    employees_count = Column(Integer, default=0)
    payment_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="PAID") # PAID, LATE, MISSING
    
    profile = relationship("EPFOEstablishmentProfile", back_populates="contributions")

class EPFOEmployee(Base):
    __tablename__ = "epfo_employees"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("epfo_profiles.id"), nullable=False)
    uan = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    joining_date = Column(DateTime, nullable=False)
    exit_date = Column(DateTime, nullable=True)
    salary = Column(Float, default=0.0)
    designation = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    
    profile = relationship("EPFOEstablishmentProfile", back_populates="employees")

class EPFOAnalytics(Base):
    __tablename__ = "epfo_analytics"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("epfo_profiles.id"), nullable=False)
    active_employees = Column(Integer, default=0)
    attrition_rate = Column(Float, default=0.0)
    avg_employee_tenure = Column(Float, default=0.0)
    monthly_payroll = Column(Float, default=0.0)
    payroll_growth = Column(Float, default=0.0)
    hiring_trend = Column(String(100), default="Stable")
    workforce_growth = Column(Float, default=0.0)
    payroll_stability_index = Column(Float, default=100.0)
    compliance_score = Column(Float, default=100.0)
    
    # Workforce Risk Indicators
    payroll_risk = Column(String(50), default="Low") # Low, Medium, High, Critical
    compliance_risk = Column(String(50), default="Low")
    attrition_risk = Column(String(50), default="Low")
    workforce_stability_risk = Column(String(50), default="Low")
    business_continuity_risk = Column(String(50), default="Low")
    
    ai_insights = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    profile = relationship("EPFOEstablishmentProfile", back_populates="analytics")
