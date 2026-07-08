import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class TReDSBuyer(Base):
    __tablename__ = "treds_buyers"
    
    id = Column(Integer, primary_key=True, index=True)
    buyer_pan = Column(String(10), unique=True, nullable=False, index=True)
    buyer_name = Column(String(200), nullable=False)
    credit_rating = Column(String(10), default="AA") # AAA, AA, A, BBB
    payment_behaviour_days = Column(Integer, default=45) # Average days to clear payments

class TReDSInvoice(Base):
    __tablename__ = "treds_invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    buyer_pan = Column(String(10), nullable=False, index=True)
    buyer_name = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    tenure_days = Column(Integer, default=90)
    issue_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="ELIGIBLE") # ELIGIBLE, DISCOUNTED, SETTLED
    last_synced_at = Column(DateTime, default=datetime.datetime.utcnow)
