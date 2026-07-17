from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db_helper import Base

class ESECustomer(Base):
    __tablename__ = "ese_customers"
    
    id = Column(Integer, primary_key=True, index=True)
    pan = Column(String(50), unique=True, index=True)
    legal_name = Column(String(150))
    mobile_number = Column(String(50))
    email = Column(String(100))
    persona_name = Column(String(100))
    scenario_id = Column(String(50))

class ESEBusiness(Base):
    __tablename__ = "ese_businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("ese_customers.id"))
    trade_name = Column(String(150))
    gstin = Column(String(50), unique=True, index=True)
    cin = Column(String(50), nullable=True)
    annual_turnover = Column(Float)
    industry_segment = Column(String(100))

class ESEGSTRecord(Base):
    __tablename__ = "ese_gst_records"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("ese_customers.id"))
    gstin = Column(String(50))
    filing_month = Column(String(50)) # e.g. "-1 month", "-2 months" or YYYY-MM
    revenue = Column(Float)
    gst_paid = Column(Float)
    filing_status = Column(String(50)) # "FILED", "PENDING"

class ESETransaction(Base):
    __tablename__ = "ese_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("ese_customers.id"))
    account_ref_num = Column(String(50))
    transaction_date = Column(String(50))
    amount = Column(Float)
    type = Column(String(50)) # "CREDIT", "DEBIT"
    balance = Column(Float)
    description = Column(String(200))

class ESECKYCRecord(Base):
    __tablename__ = "ese_ckyc_records"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("ese_customers.id"))
    pan = Column(String(50))
    ckyc_number = Column(String(50))
    full_name = Column(String(150))
    dob = Column(String(50))
    kyc_status = Column(String(50)) # "CLEAN", "EXPIRED", "INCOMPLETE"

class ESEEPFORecord(Base):
    __tablename__ = "ese_epfo_records"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("ese_customers.id"))
    establishment_id = Column(String(100))
    employee_count = Column(Integer)
    pf_compliance_score = Column(Float)
    last_month_contribution = Column(Float)

class ESEMCARecord(Base):
    __tablename__ = "ese_mca_records"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("ese_customers.id"))
    cin = Column(String(50))
    company_name = Column(String(150))
    date_of_incorporation = Column(String(50))
    status = Column(String(50)) # "ACTIVE", "INACTIVE"

class ESELoanApplication(Base):
    __tablename__ = "ese_loan_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("ese_customers.id"))
    requested_amount = Column(Float)
    tenure_months = Column(Integer)
    status = Column(String(50)) # "OFFERS_GENERATED", "ACCEPTED", "DISBURSED", "REJECTED"
    interest_rate = Column(Float)
