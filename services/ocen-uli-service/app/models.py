import datetime
def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Lender(Base):
    __tablename__ = "ocen_lenders"
    
    id = Column(Integer, primary_key=True, index=True)
    lender_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    lender_type = Column(String(50), default="BANK") # BANK, NBFC, FINTECH
    base_interest_rate = Column(Float, default=10.5)
    max_loan_amount = Column(Float, default=5000000.0)
    min_credit_score = Column(Integer, default=650)
    is_active = Column(Boolean, default=True)

class Partner(Base):
    __tablename__ = "ocen_partners"
    
    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    partner_type = Column(String(50), default="LSP") # LSP, Tech Provider, Broker
    is_active = Column(Boolean, default=True)

class LoanApplication(Base):
    __tablename__ = "ocen_loan_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    uli_reference = Column(String(100), unique=True, nullable=False, index=True)
    requested_amount = Column(Float, nullable=False)
    requested_tenure_months = Column(Integer, default=12)
    purpose = Column(String(250), nullable=True)
    status = Column(String(50), default="APPLIED") # APPLIED, OFFERS_GENERATED, ACCEPTED, DISBURSED, REJECTED
    selected_offer_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class LoanOffer(Base):
    __tablename__ = "ocen_loan_offers"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("ocen_loan_applications.id"), nullable=False)
    lender_id = Column(String(50), nullable=False, index=True)
    lender_name = Column(String(200), nullable=False)
    offered_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    processing_fee = Column(Float, default=0.0)
    monthly_installment = Column(Float, nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, ACCEPTED, EXPIRED
    created_at = Column(DateTime, default=utc_now)

class AuditLog(Base):
    __tablename__ = "ocen_audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    correlation_id = Column(String(100), index=True)
    event_type = Column(String(100), nullable=False, index=True)
    actor = Column(String(100), default="SYSTEM")
    message = Column(String(500), nullable=False)
    details = Column(String(2000), nullable=True) # JSON or descriptive string
    timestamp = Column(DateTime, default=utc_now)
