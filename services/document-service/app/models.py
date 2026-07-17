from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    document_type = Column(String(50), nullable=False) # e.g. "PAN", "AADHAAR", "GST_CERT", "ITR_RETURN", "BANK_STATEMENT"
    file_name = Column(String(200), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False) # e.g. "application/pdf"
    storage_path = Column(String(255), nullable=False) # GCS bucket file path (e.g. gs://aarohan-documents/101/pan.pdf)
    source_origin = Column(String(50), default="UPLOAD") # UPLOAD, DIGILOCKER, CKYC
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    metadata_fields = relationship("DocumentMetadata", back_populates="document", cascade="all, delete-orphan")

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    meta_key = Column(String(100), nullable=False) # e.g. "document_number", "expiry_date", "ocr_confidence"
    meta_value = Column(String(255), nullable=False)
    
    document = relationship("Document", back_populates="metadata_fields")
