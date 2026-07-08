import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class RMTask(Base):
    __tablename__ = "rm_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    due_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, IN_PROGRESS, COMPLETED
    priority = Column(String(20), default="MEDIUM") # HIGH, MEDIUM, LOW
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RMLead(Base):
    __tablename__ = "rm_leads"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    contact_person = Column(String(100), nullable=False)
    mobile = Column(String(15), nullable=False)
    pipeline_stage = Column(String(50), default="QUALIFICATION") # QUALIFICATION, UNDERWRITING, SANCTIONED, DISBURSED
    estimated_loan_amt = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RMAlert(Base):
    __tablename__ = "rm_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    alert_type = Column(String(50), nullable=False) # e.g. "GST_DELAY", "LIQUIDITY_DROP", "CONSENT_EXPIRY"
    message = Column(String(255), nullable=False)
    severity = Column(String(20), default="WARNING") # INFO, WARNING, CRITICAL
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RMInteraction(Base):
    __tablename__ = "rm_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    staff_id = Column(String(100), nullable=False)
    interaction_type = Column(String(50), nullable=False) # CALL, MEETING, EMAIL
    notes = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
