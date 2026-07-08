import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class EPFOEstablishmentProfile(Base):
    __tablename__ = "epfo_profiles"
    
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

class EPFOContribution(Base):
    __tablename__ = "epfo_contributions"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("epfo_profiles.id"), nullable=False)
    wage_month = Column(String(10), nullable=False) # e.g. "042025" (MMYYYY)
    amount_paid = Column(Float, default=0.0)
    employees_count = Column(Integer, default=0)
    payment_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="PAID")
    
    profile = relationship("EPFOEstablishmentProfile", back_populates="contributions")
