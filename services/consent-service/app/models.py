from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship


class ConsentPurpose(Base):
    __tablename__ = "consent_purposes"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True) # e.g. "CREDIT_APPRAISAL", "MONITORING"
    description = Column(String(255), nullable=False)
    data_minimization_rules = Column(String(500), nullable=True) # JSON rule description

class Consent(Base):
    __tablename__ = "consents"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    provider_type = Column(String(50), nullable=False) # e.g. "ACCOUNT_AGGREGATOR", "GSTN", "CKYC", "DIGILOCKER"
    purpose_code = Column(String(50), nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, APPROVED, REVOKED, EXPIRED
    valid_until = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    artifacts = relationship("ConsentArtifact", back_populates="consent", cascade="all, delete-orphan")

class ConsentArtifact(Base):
    __tablename__ = "consent_artifacts"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    consent_id = Column(Integer, ForeignKey("consents.id"), nullable=False)
    signature_hash = Column(String(255), nullable=False) # Digital signature validating customer approval
    artifact_path = Column(String(255), nullable=True) # GCS bucket file path if applicable
    signed_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    consent = relationship("Consent", back_populates="artifacts")
