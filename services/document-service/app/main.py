import logging
import sys
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import Document, DocumentMetadata
from app.schemas import DocumentCreate, DocumentResponse, DigiLockerImportRequest
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "document-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("document-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN Document Management & DigiLocker Gateway Service",
    description="Secure file repository metadata mapping, GCS links, and DigiLocker import channels",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Correlation ID and auditing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    logger.info(f"AUDIT | Request: {request.method} {request.url.path} | Correlation ID: {correlation_id}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Correlation-ID"] = correlation_id
    
    logger.info(f"AUDIT | Completed: {request.method} {request.url.path} | Status: {response.status_code} | Process Time: {process_time:.4f}s")
    return response

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorCode": f"AAR-ERR-{exc.status_code}",
            "message": exc.detail,
            "correlationId": correlation_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "details": []
        }
    )

# REST APIs

@app.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Registering Document: {payload.file_name} | Customer: {payload.customer_id}")
    
    doc = Document(
        customer_id=payload.customer_id,
        document_type=payload.document_type,
        file_name=payload.file_name,
        file_size_bytes=payload.file_size_bytes,
        content_type=payload.content_type,
        storage_path=payload.storage_path,
        source_origin=payload.source_origin
    )
    db.add(doc)
    db.flush() # Populate document ID
    
    for m in payload.metadata_fields:
        metadata = DocumentMetadata(
            document_id=doc.id,
            meta_key=m.meta_key,
            meta_value=m.meta_value
        )
        db.add(metadata)
        
    db.commit()
    db.refresh(doc)
    logger.info(f"AUDIT | Document uploaded successfully | ID: {doc.id} | Path: {doc.storage_path}")
    return doc

@app.post("/documents/digilocker/import", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def import_digilocker_document(payload: DigiLockerImportRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Importing DigiLocker Document | Customer: {payload.customer_id} | URI: {payload.digilocker_uri}")
    
    # Simulates pulling a verified PDF file from DigiLocker API
    file_name = f"digilocker_{payload.document_type.lower()}_{payload.customer_id}.pdf"
    storage_path = f"gs://aarohan-documents/{payload.customer_id}/{file_name}"
    
    doc = Document(
        customer_id=payload.customer_id,
        document_type=payload.document_type,
        file_name=file_name,
        file_size_bytes=245000, # Mock size
        content_type="application/pdf",
        storage_path=storage_path,
        source_origin="DIGILOCKER"
    )
    db.add(doc)
    db.flush()
    
    # Seed verification metadata returned from DigiLocker
    m1 = DocumentMetadata(document_id=doc.id, meta_key="issuer", meta_value="Govt of India")
    m2 = DocumentMetadata(document_id=doc.id, meta_key="verification_status", meta_value="VERIFIED_DIGITAL_SIGNATURE")
    m3 = DocumentMetadata(document_id=doc.id, meta_key="digilocker_uri", meta_value=payload.digilocker_uri)
    db.add_all([m1, m2, m3])
    
    db.commit()
    db.refresh(doc)
    logger.info(f"AUDIT | DigiLocker import successful | Doc ID: {doc.id} | Event: bank.aarohan.document.imported")
    return doc

@app.get("/documents", response_model=List[DocumentResponse])
async def list_documents(
    customer_id: Optional[int] = None,
    document_type: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Document).filter(Document.is_deleted == False)
    if customer_id is not None:
        query = query.filter(Document.customer_id == customer_id)
    if document_type is not None:
        query = query.filter(Document.document_type == document_type)
        
    return query.offset(offset).limit(limit).all()

@app.get("/documents/{id}", response_model=DocumentResponse)
async def get_document(id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == id, Document.is_deleted == False).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document record not found."
        )
    return doc

@app.delete("/documents/{id}", status_code=status.HTTP_200_OK)
async def delete_document(id: int, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Soft Deleting Document Profile ID: {id}")
    doc = db.query(Document).filter(Document.id == id, Document.is_deleted == False).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document profile not found."
        )
        
    doc.is_deleted = True
    doc.is_active = False
    db.commit()
    logger.info(f"AUDIT | Document Profile ID: {id} successfully soft-deleted")
    return {"message": f"Document Profile ID {id} has been soft-deleted successfully."}

@app.get("/livez")
async def livez():
    return {"status": "UP"}
