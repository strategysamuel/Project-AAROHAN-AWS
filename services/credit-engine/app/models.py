import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class AICreditDecision(Base):
    __tablename__ = "ai_credit_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    recommendation = Column(String(50), nullable=False) # APPROVED, REJECTED, REQUEST_MORE_INFO
    confidence_score = Column(Float, default=0.0) # 0.0 to 100.0
    ai_narrative = Column(String(1000), nullable=False) # Gemini generated analytical commentary
    policy_status = Column(String(50), default="COMPLIANT") # COMPLIANT, VIOLATION
    approval_status = Column(String(50), default="PENDING_HUMAN_REVIEW") # PENDING_HUMAN_REVIEW, APPROVED, REJECTED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    approvals = relationship("HumanApprovalLog", back_populates="decision", cascade="all, delete-orphan")

class HumanApprovalLog(Base):
    __tablename__ = "human_approval_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("ai_credit_decisions.id"), nullable=False)
    approver_id = Column(String(100), nullable=False) # Staff/Underwriter ID
    action = Column(String(50), nullable=False) # APPROVED, REJECTED, REQUEST_MORE_INFO
    comments = Column(String(500), nullable=True) # Text feedback capturing underwriting notes
    signed_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    decision = relationship("AICreditDecision", back_populates="approvals")
