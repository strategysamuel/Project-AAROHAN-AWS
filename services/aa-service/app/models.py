import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class LinkedAccount(Base):
    __tablename__ = "aa_linked_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    account_ref_num = Column(String(100), unique=True, nullable=False, index=True) # e.g. "SB-100293"
    masked_acc_num = Column(String(50), nullable=False) # e.g. "XXXXXX4321"
    bank_name = Column(String(100), nullable=False) # e.g. "State Bank of India"
    account_type = Column(String(50), nullable=False) # e.g. "CURRENT", "SAVINGS"
    balance = Column(Float, default=0.0)
    currency = Column(String(10), default="INR")
    is_active = Column(Boolean, default=True)
    last_synced_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    transactions = relationship("AATransaction", back_populates="account", cascade="all, delete-orphan")

class AATransaction(Base):
    __tablename__ = "aa_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("aa_linked_accounts.id"), nullable=False)
    txn_ref_num = Column(String(100), unique=True, nullable=False, index=True)
    txn_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    txn_type = Column(String(10), nullable=False) # DEBIT, CREDIT
    narration = Column(String(255), nullable=True)
    category = Column(String(100), default="OTHERS") # INCOME, UTILITY, RENT, PAYROLL, VENDOR
    is_recurring = Column(Boolean, default=False)
    
    account = relationship("LinkedAccount", back_populates="transactions")

class AAAnalytics(Base):
    __tablename__ = "aa_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, unique=True, index=True)
    total_inflow = Column(Float, default=0.0)
    total_outflow = Column(Float, default=0.0)
    net_cash_flow = Column(Float, default=0.0)
    avg_balance = Column(Float, default=0.0)
    income_score = Column(Float, default=100.0)
    debt_service_ratio = Column(Float, default=0.0)
    last_calculated_at = Column(DateTime, default=datetime.datetime.utcnow)
