import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Table, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "onboarding_customers"
    
    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String(200), nullable=False)
    mobile_number = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    pan = Column(String(10), unique=True, nullable=False, index=True) # Permanent Account Number
    aadhaar_masked = Column(String(12), nullable=True)  # XXXXXXXX1234 format
    district = Column(String(100), nullable=True)
    workflow_id = Column(String(50), nullable=True)     # Last triggered workflow
    persona_name = Column(String(200), nullable=True)   # ESE persona linked
    onboarding_status = Column(String(50), default="DRAFT")  # DRAFT, SUBMITTED, VERIFIED, ACTIVE
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    businesses = relationship("BusinessEntity", back_populates="customer", cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    documents = relationship("OnboardingDocument", back_populates="customer", cascade="all, delete-orphan")

class BusinessEntity(Base):
    __tablename__ = "onboarding_businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("onboarding_customers.id"), nullable=False)
    trade_name = Column(String(200), nullable=False)
    gstin = Column(String(15), unique=True, nullable=False, index=True) # Goods and Services Tax Identification Number
    udyam_number = Column(String(20), nullable=True, index=True)  # UDYAM-XX-00-0000000
    cin = Column(String(21), unique=True, nullable=True, index=True) # Corporate Identification Number (Optional for proprietorships)
    constitution_type = Column(String(50), nullable=False) # Proprietorship, Partnership, Private Limited
    annual_turnover = Column(Float, default=0.0)
    industry_segment = Column(String(100), nullable=False) # e.g. Textile, Retail, Auto Components
    business_vintage_years = Column(Integer, default=0)  # Years in operation
    employee_count = Column(Integer, default=0)
    existing_banking = Column(String(200), nullable=True)  # e.g. "SBI, HDFC Bank"
    lifecycle_state = Column(String(50), default="REGISTERED") # REGISTERED, VERIFIED, IN_PROGRESS, ACTIVE
    
    customer = relationship("Customer", back_populates="businesses")
    directors = relationship("ProprietorDirector", back_populates="business", cascade="all, delete-orphan")

class ProprietorDirector(Base):
    __tablename__ = "onboarding_directors"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("onboarding_businesses.id"), nullable=False)
    full_name = Column(String(150), nullable=False)
    pan = Column(String(10), nullable=False)
    aadhaar_masked = Column(String(12), nullable=False) # Masked Aadhaar number (e.g. XXXXXXXX1234)
    mobile = Column(String(15), nullable=False)
    
    business = relationship("BusinessEntity", back_populates="directors")

class Address(Base):
    __tablename__ = "onboarding_addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("onboarding_customers.id"), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(6), nullable=False)
    address_type = Column(String(50), default="OFFICE") # OFFICE, RESIDENCE, FACTORY
    
    customer = relationship("Customer", back_populates="addresses")


class OnboardingDocument(Base):
    """Tracks simulated document uploads per customer."""
    __tablename__ = "onboarding_documents"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("onboarding_customers.id"), nullable=False)
    doc_type = Column(String(50), nullable=False)   # PAN, AADHAAR, GST_CERT, UDYAM, BANK_STMT, FINANCIALS, COI
    doc_name = Column(String(200), nullable=False)
    source = Column(String(50), default="UPLOAD")   # UPLOAD | SIMULATION_DATASET
    status = Column(String(30), default="PENDING")  # PENDING | VERIFIED | REJECTED
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="documents")
