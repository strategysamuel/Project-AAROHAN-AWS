from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


class LinkedAccount(Base):
    __tablename__ = "aa_linked_accounts"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    account_ref_num = Column(String(100), unique=True, nullable=False, index=True) # e.g. "SB-100293"
    masked_acc_num = Column(String(50), nullable=False) # e.g. "XXXXXX4321"
    bank_name = Column(String(100), nullable=False) # e.g. "State Bank of India"
    account_type = Column(String(50), nullable=False) # e.g. "CURRENT", "SAVINGS", "LOAN", "FD", "CC"
    balance = Column(Float, default=0.0)
    currency = Column(String(10), default="INR")
    is_active = Column(Boolean, default=True)
    last_synced_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    transactions = relationship("AATransaction", back_populates="account", cascade="all, delete-orphan")

class AATransaction(Base):
    __tablename__ = "aa_transactions"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("aa_linked_accounts.id"), nullable=False)
    txn_ref_num = Column(String(100), unique=True, nullable=False, index=True)
    txn_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    txn_type = Column(String(10), nullable=False) # DEBIT, CREDIT
    narration = Column(String(255), nullable=True)
    category = Column(String(100), default="OTHERS") # INCOME, UTILITY, RENT, PAYROLL, VENDOR, EMI, TAX
    is_recurring = Column(Boolean, default=False)
    
    account = relationship("LinkedAccount", back_populates="transactions")

class AAAnalytics(Base):
    __tablename__ = "aa_analytics"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, unique=True, index=True)
    total_inflow = Column(Float, default=0.0)
    total_outflow = Column(Float, default=0.0)
    net_cash_flow = Column(Float, default=0.0)
    avg_balance = Column(Float, default=0.0)
    median_balance = Column(Float, default=0.0)
    income_score = Column(Float, default=100.0)
    debt_service_ratio = Column(Float, default=0.0)
    
    # Cash Flow Intelligence
    monthly_credits = Column(Float, default=0.0)
    monthly_debits = Column(Float, default=0.0)
    cash_flow_stability = Column(Float, default=100.0)
    seasonality = Column(Float, default=1.0)
    income_stability = Column(Float, default=100.0)
    expense_ratio = Column(Float, default=0.0)
    working_capital_estimate = Column(Float, default=0.0)
    savings_behaviour = Column(String(100), default="Steady")
    
    # Behaviour Analytics
    salary_regularity = Column(String(100), default="Regular")
    business_revenue_stability = Column(String(100), default="Stable")
    cheque_bounce_indicator = Column(Boolean, default=False)
    emi_discipline = Column(String(100), default="Excellent")
    overdraft_usage = Column(String(100), default="None")
    high_cash_dependency = Column(Boolean, default=False)
    large_cash_withdrawals = Column(Boolean, default=False)
    frequent_low_balance = Column(Boolean, default=False)
    dormant_account = Column(Boolean, default=False)
    
    # Financial Risk Indicators
    liquidity_risk = Column(String(50), default="Low") # Low, Medium, High, Critical
    cash_flow_risk = Column(String(50), default="Low")
    behaviour_risk = Column(String(50), default="Low")
    income_risk = Column(String(50), default="Low")
    expense_risk = Column(String(50), default="Low")
    banking_stability_score = Column(Float, default=100.0)
    overall_score = Column(Float, default=100.0)
    
    ai_insights = Column(Text, default="")
    last_calculated_at = Column(DateTime, default=datetime.datetime.utcnow)

class AAConsent(Base):
    __tablename__ = "aa_consents"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    consent_artefact_id = Column(String(100), unique=True, nullable=False, index=True)
    purpose = Column(String(200), nullable=False)
    data_requested = Column(String(200), nullable=False)
    validity = Column(String(100), nullable=False)
    frequency = Column(String(50), default="ONCE")
    accounts_included = Column(String(200), nullable=True) # Comma-separated masked account numbers
    status = Column(String(50), default="PENDING") # PENDING, APPROVED, REJECTED, EXPIRED, REVOKED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
