import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class CAMRecord(Base):
    __tablename__ = "cam_records"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, unique=True, index=True)
    status = Column(String(50), default="DRAFT") # DRAFT, PENDING_APPROVAL, APPROVED, REJECTED
    current_version = Column(Integer, default=1)
    
    # Core CAM Sections
    executive_summary = Column(String(2000), nullable=False)
    business_profile = Column(String(1000), nullable=False)
    financial_analysis = Column(String(2000), nullable=False)
    swot_analysis = Column(String(1000), nullable=False)
    risk_assessment = Column(String(1500), nullable=False)
    collateral_assessment = Column(String(1000), nullable=True)
    ai_recommendation = Column(String(1000), nullable=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    versions = relationship("CAMVersion", back_populates="cam", cascade="all, delete-orphan")

class CAMVersion(Base):
    __tablename__ = "cam_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    cam_id = Column(Integer, ForeignKey("cam_records.id"), nullable=False)
    version_num = Column(Integer, nullable=False)
    edited_by = Column(String(100), nullable=False) # Staff ID
    edited_at = Column(DateTime, default=datetime.datetime.utcnow)
    change_summary = Column(String(255), nullable=True)
    
    # Snapshot of sections at this version
    executive_summary = Column(String(2000), nullable=False)
    business_profile = Column(String(1000), nullable=False)
    financial_analysis = Column(String(2000), nullable=False)
    swot_analysis = Column(String(1000), nullable=False)
    risk_assessment = Column(String(1500), nullable=False)
    
    cam = relationship("CAMRecord", back_populates="versions")
    
class CAMApprovalLog(Base):
    __tablename__ = "cam_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    cam_id = Column(Integer, nullable=False, index=True)
    approver_id = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False) # APPROVED, REJECTED
    comments = Column(String(500), nullable=True)
    signed_at = Column(DateTime, default=datetime.datetime.utcnow)
