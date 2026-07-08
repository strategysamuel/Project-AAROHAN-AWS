import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class MCACompanyProfile(Base):
    __tablename__ = "mca_company_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, unique=True, nullable=False, index=True)
    cin = Column(String(21), unique=True, nullable=False, index=True) # 21-character CIN
    company_name = Column(String(200), nullable=False)
    incorporation_date = Column(DateTime, nullable=False)
    company_status = Column(String(50), default="ACTIVE") # ACTIVE, STRUCK_OFF, LIQUIDATED
    class_of_company = Column(String(50), nullable=False) # e.g. Private Limited, Public Limited
    authorized_capital = Column(Float, default=0.0)
    paid_up_capital = Column(Float, default=0.0)
    last_synced_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    directors = relationship("MCADirector", back_populates="company", cascade="all, delete-orphan")
    charges = relationship("MCACharge", back_populates="company", cascade="all, delete-orphan")
    filings = relationship("MCACompanyFiling", back_populates="company", cascade="all, delete-orphan")

class MCADirector(Base):
    __tablename__ = "mca_directors"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mca_company_profiles.id"), nullable=False)
    din = Column(String(8), nullable=False) # 8-character DIN
    full_name = Column(String(150), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    
    company = relationship("MCACompanyProfile", back_populates="directors")

class MCACharge(Base):
    __tablename__ = "mca_charges"
    
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
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mca_company_profiles.id"), nullable=False)
    form_name = Column(String(50), nullable=False) # e.g. "AOC-4", "MGT-7"
    filing_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="APPROVED")
    
    company = relationship("MCACompanyProfile", back_populates="filings")
class MCALink(Base):
    __tablename__ = "mca_links"
    id = Column(Integer, primary_key=True)
