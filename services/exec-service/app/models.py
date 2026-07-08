import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class ExecKPI(Base):
    __tablename__ = "exec_kpis"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), unique=True, nullable=False, index=True) # e.g. "TOTAL_PORTFOLIO_VOLUME", "ACTIVE_MSME_COUNT"
    metric_value = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ExecBranchPerformance(Base):
    __tablename__ = "exec_branch_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    branch_name = Column(String(100), unique=True, nullable=False, index=True) # e.g. "Mumbai Corporate", "Coimbatore MSME"
    region = Column(String(50), nullable=False) # West, South, North, East
    loan_disbursed_amt = Column(Float, default=0.0)
    active_accounts = Column(Integer, default=0)
    average_health_score = Column(Float, default=0.0)
