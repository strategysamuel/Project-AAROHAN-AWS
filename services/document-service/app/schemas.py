from pydantic import BaseModel, Field
import datetime
from typing import List, Optional

class DocumentMetadataBase(BaseModel):
    meta_key: str
    meta_value: str

class DocumentMetadataCreate(DocumentMetadataBase):
    pass

class DocumentMetadataResponse(DocumentMetadataBase):
    id: int

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    customer_id: int
    document_type: str = Field(..., description="e.g. PAN, AADHAAR, GST_CERT, ITR_RETURN, BANK_STATEMENT")
    file_name: str
    file_size_bytes: int
    content_type: str
    storage_path: str
    source_origin: str = "UPLOAD"

class DocumentCreate(DocumentBase):
    metadata_fields: List[DocumentMetadataCreate] = []

class DocumentResponse(DocumentBase):
    id: int
    is_active: bool
    created_at: datetime.datetime
    metadata_fields: List[DocumentMetadataResponse] = []

    class Config:
        from_attributes = True

class DigiLockerImportRequest(BaseModel):
    customer_id: int
    document_type: str
    digilocker_uri: str # e.g. "in.gov.uidai-adr-XXXXXXXX1234"
    consent_id: int
