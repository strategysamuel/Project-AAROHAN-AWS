import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class FinancialHealthCard(Base):
    __tablename__ = "fhc_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, unique=True, index=True)
    overall_score = Column(Float, default=0.0) # Overall rating (0 to 100)
    
    # Sub-Score metrics
    revenue_health_score = Column(Float, default=0.0)
    cash_flow_score = Column(Float, default=0.0)
    liquidity_score = Column(Float, default=0.0)
    banking_behaviour_score = Column(Float, default=0.0)
    compliance_score = Column(Float, default=0.0)
    growth_score = Column(Float, default=0.0)
    
    # Explainability details
    key_strengths = Column(String(500), nullable=True) # Semi-colon separated key positive factors
    risk_concerns = Column(String(500), nullable=True) # Semi-colon separated risk triggers
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    history = relationship("ScoreHistory", back_populates="card", cascade="all, delete-orphan")

class ScoreHistory(Base):
    __tablename__ = "fhc_score_history"
    
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("fhc_cards.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
    score_value = Column(Float, nullable=False)
    
    card = relationship("FinancialHealthCard", back_populates="history")
