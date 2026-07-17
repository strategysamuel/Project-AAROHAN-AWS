from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship


class EWSWatchlist(Base):
    __tablename__ = "ews_watchlist"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, unique=True, nullable=False, index=True)
    risk_level = Column(String(50), default="MEDIUM") # HIGH, MEDIUM, LOW
    added_at = Column(DateTime, default=datetime.datetime.utcnow)
    reason_code = Column(String(100), nullable=False) # e.g. "GST_DELAY", "CASHFLOW_DROP"

class EWSAlert(Base):
    __tablename__ = "ews_alerts"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    trigger_rule = Column(String(100), nullable=False) # e.g. "RULE_LIQUIDITY_DROP"
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

class EWSRiskCase(Base):
    __tablename__ = "ews_risk_cases"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    status = Column(String(50), default="OPEN") # OPEN, ESCALATED, RESOLVED
    ai_risk_narrative = Column(String(1000), nullable=False) # Gemini generated risk summary
    mitigation_action = Column(String(500), nullable=True) # Recommended mitigations
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
