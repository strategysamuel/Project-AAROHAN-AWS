from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


class CKYCRecord(Base):
    __tablename__ = "ckyc_records"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, unique=True, nullable=False, index=True)
    ckyc_number = Column(String(50), unique=True, nullable=False, index=True) # 14-digit CKYC Identifier
    full_name = Column(String(200), nullable=False)
    dob = Column(String(20), nullable=False) # DD-MM-YYYY
    pan = Column(String(10), nullable=False, index=True)
    aadhaar_masked = Column(String(12), nullable=True) # XXXXXXXX1234
    address = Column(String(500), nullable=True)
    mobile = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    kyc_status = Column(String(50), default="VERIFIED") # VERIFIED, VERIFIED_WITH_WARNING, PENDING, MANUAL_REVIEW, FAILED, DUPLICATE_RECORD, DATA_MISMATCH
    image_url = Column(String(255), nullable=True) # Mock GCS profile image
    last_synced_at = Column(DateTime, default=datetime.datetime.utcnow)

class CKYCVerificationLog(Base):
    __tablename__ = "ckyc_verification_logs"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    checked_by = Column(String(100), nullable=False) # RM staff ID or "SYSTEM"
    match_confidence = Column(Float, default=100.0) # Identity match confidence percentage (0 to 100)
    risk_indicators = Column(String(500), default="") # Comma-separated indicators
    anomaly_detected = Column(Boolean, default=False)
    verification_status = Column(String(50), default="VERIFIED") # VERIFIED, VERIFIED_WITH_WARNING, PENDING, MANUAL_REVIEW, FAILED, DUPLICATE_RECORD, DATA_MISMATCH
    comments = Column(Text, nullable=True) # Audit override comments
    verified_at = Column(DateTime, default=datetime.datetime.utcnow)

# Mapping to Onboarding tables in the shared database
class OnboardingCustomer(Base):
    __tablename__ = "onboarding_customers"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String(200), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False)
    pan = Column(String(10), nullable=False)
    aadhaar_masked = Column(String(12), nullable=True)
    district = Column(String(100), nullable=True)
    onboarding_status = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

class OnboardingAddress(Base):
    __tablename__ = "onboarding_addresses"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False)
    address_line1 = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(6), nullable=False)
