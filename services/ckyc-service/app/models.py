import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class CKYCRecord(Base):
    __tablename__ = "ckyc_records"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, unique=True, nullable=False, index=True)
    ckyc_number = Column(String(50), unique=True, nullable=False, index=True) # 14-digit CKYC Identifier
    full_name = Column(String(200), nullable=False)
    dob = Column(String(20), nullable=False) # DD-MM-YYYY
    pan = Column(String(10), nullable=False, index=True)
    kyc_status = Column(String(50), default="VERIFIED") # VERIFIED, PENDING_REFRESH
    image_url = Column(String(255), nullable=True) # Mock GCS profile image
    last_synced_at = Column(DateTime, default=datetime.datetime.utcnow)

class CKYCVerificationLog(Base):
    __tablename__ = "ckyc_verification_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    checked_by = Column(String(100), nullable=False) # RM staff ID
    match_confidence = Column(Float, default=100.0) # Identity match confidence percentage (0 to 100)
    anomaly_detected = Column(Boolean, default=False)
    verification_status = Column(String(50), default="MATCHED") # MATCHED, EXCEPTION_QUEUE
    verified_at = Column(DateTime, default=datetime.datetime.utcnow)
