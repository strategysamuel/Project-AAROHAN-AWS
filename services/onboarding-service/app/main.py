import json
import logging
import os
import sys
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Customer, BusinessEntity, ProprietorDirector, Address, OnboardingDocument
from app.schemas import (
    CustomerCreate, CustomerResponse, CustomerBase,
    DocumentResponse, DocumentUploadRequest,
    PersonaLoadRequest, WorkflowTriggerResponse,
    ValidationResult, ValidationResponse,
    CustomerValidateRequest,
)
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "onboarding-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("onboarding-service")

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PERSONAS_DIR = os.path.join(WORKSPACE_ROOT, "ese", "personas")
DATASET_DIR = os.path.join(WORKSPACE_ROOT, "ese", "datasets", "msme")

PERSONA_ALIASES = {
    "GreenAgro Cooperative": "Green Valley Farms",
    "QuickLogistics Services": "TechBoost Solutions",
}

def _load_persona_templates() -> dict:
    templates: dict = {}
    if os.path.isdir(PERSONAS_DIR):
        for entry in os.listdir(PERSONAS_DIR):
            if not entry.endswith(".json") or entry == "schema.json":
                continue
            file_path = os.path.join(PERSONAS_DIR, entry)
            try:
                with open(file_path, "r", encoding="utf-8") as handle:
                    persona = json.load(handle)
                persona_name = persona.get("persona_name")
                if persona_name:
                    templates[persona_name] = {
                        "legal_name": persona.get("legal_name", persona_name),
                        "mobile_number": persona.get("mobile_number", ""),
                        "email": persona.get("email", ""),
                        "pan": persona.get("pan", ""),
                        "aadhaar_masked": persona.get("aadhaar_masked", ""),
                        "district": persona.get("district", ""),
                        "address_line1": persona.get("address_line1", ""),
                        "state": persona.get("state", ""),
                        "pincode": persona.get("pincode", ""),
                        "persona_name": persona_name,
                        "business": persona.get("business", {}),
                    }
            except Exception:
                logger.warning(f"WARNING | Failed to load persona template: {file_path}")

    return templates


PERSONA_TEMPLATES = _load_persona_templates()


def _resolve_persona_name(persona_name: str) -> str:
    if persona_name in PERSONA_TEMPLATES:
        return persona_name
    return PERSONA_ALIASES.get(persona_name, persona_name)

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN MSME Onboarding & Lifecycle Service",
    description="Customer management, validation, registration pipelines, and search operations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom auditing and Correlation ID middleware
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

@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Registering Customer: {payload.legal_name} | PAN: {payload.pan}")
    
    # 1. Duplicate checks
    existing = db.query(Customer).filter(
        (Customer.pan == payload.pan) | (Customer.mobile_number == payload.mobile_number)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A customer with this PAN or Mobile Number is already registered."
        )
        
    # 2. Map customer properties (including AAR-BUILD-008 fields)
    customer = Customer(
        legal_name=payload.legal_name,
        mobile_number=payload.mobile_number,
        email=payload.email,
        pan=payload.pan,
        aadhaar_masked=payload.aadhaar_masked,
        district=payload.district,
        persona_name=payload.persona_name,
        onboarding_status=payload.onboarding_status,
    )
    db.add(customer)
    db.flush() # Populate customer ID
    
    # 3. Create addresses
    for addr in payload.addresses:
        address = Address(
            customer_id=customer.id,
            address_line1=addr.address_line1,
            address_line2=addr.address_line2,
            city=addr.city,
            state=addr.state,
            pincode=addr.pincode,
            address_type=addr.address_type
        )
        db.add(address)
        
    # 4. Create business entities and directors (including AAR-BUILD-008 fields)
    for bus in payload.businesses:
        business = BusinessEntity(
            customer_id=customer.id,
            trade_name=bus.trade_name,
            gstin=bus.gstin,
            udyam_number=bus.udyam_number,
            cin=bus.cin,
            constitution_type=bus.constitution_type,
            annual_turnover=bus.annual_turnover,
            industry_segment=bus.industry_segment,
            business_vintage_years=bus.business_vintage_years,
            employee_count=bus.employee_count,
            existing_banking=bus.existing_banking,
            lifecycle_state=bus.lifecycle_state
        )
        db.add(business)
        db.flush() # Populate business ID
        
        for dir in bus.directors:
            director = ProprietorDirector(
                business_id=business.id,
                full_name=dir.full_name,
                pan=dir.pan,
                aadhaar_masked=dir.aadhaar_masked,
                mobile=dir.mobile
            )
            db.add(director)
            
    db.commit()
    db.refresh(customer)
    logger.info(f"AUDIT | Customer registered successfully | ID: {customer.id}")
    return customer

@app.get("/customers", response_model=List[CustomerResponse])
async def list_customers(
    search: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Customer).filter(Customer.is_deleted == False)
    
    if search:
        query = query.filter(
            or_(
                Customer.legal_name.ilike(f"%{search}%"),
                Customer.pan.ilike(f"%{search}%"),
                Customer.mobile_number.ilike(f"%{search}%")
            )
        )
        
    return query.offset(offset).limit(limit).all()

@app.get("/customers/{id}", response_model=CustomerResponse)
async def get_customer(id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == id, Customer.is_deleted == False).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer file not found."
        )
    return customer

@app.put("/customers/{id}", response_model=CustomerResponse)
async def update_customer(id: int, payload: CustomerBase, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Updating Customer Profile ID: {id}")
    customer = db.query(Customer).filter(Customer.id == id, Customer.is_deleted == False).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found."
        )
        
    customer.legal_name = payload.legal_name
    customer.mobile_number = payload.mobile_number
    customer.email = payload.email
    customer.pan = payload.pan
    db.commit()
    db.refresh(customer)
    logger.info(f"AUDIT | Customer Profile ID: {id} updated successfully")
    return customer

@app.delete("/customers/{id}", status_code=status.HTTP_200_OK)
async def delete_customer(id: int, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Soft Deleting Customer Profile ID: {id}")
    customer = db.query(Customer).filter(Customer.id == id, Customer.is_deleted == False).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found."
        )
        
    customer.is_deleted = True
    customer.is_active = False
    db.commit()
    logger.info(f"AUDIT | Customer Profile ID: {id} successfully soft-deleted")
    return {"message": f"Customer Profile ID {id} has been soft-deleted successfully."}

@app.get("/livez")
async def livez():
    return {"status": "UP"}


# ============================================================
# NEW ENTERPRISE ROUTES (AAR-BUILD-008)
# ============================================================

# --- Persona Load: populate form from ESE persona name ---
PERSONA_TEMPLATES = {
    "Priya Textile Works": {
        "legal_name": "Priya Textile Works",
        "mobile_number": "9876543210",
        "email": "priya@textileworks.in",
        "pan": "PRXPT0001K",
        "aadhaar_masked": "XXXXXXXX1234",
        "district": "Surat",
        "address_line1": "123 Textile Market",
        "state": "Gujarat",
        "pincode": "395002",
        "persona_name": "Priya Textile Works",
        "business": {
            "trade_name": "Priya Textile Works Pvt Ltd",
            "gstin": "27SIMPT0001K1Z5",
            "udyam_number": "UDYAM-GJ-05-0023456",
            "cin": None,
            "constitution_type": "Private Limited",
            "annual_turnover": 45000000.0,
            "industry_segment": "Manufacturing – Textiles",
            "business_vintage_years": 12,
            "employee_count": 87,
            "existing_banking": "SBI, HDFC Bank"
        }
    },
    "GreenAgro Cooperative": {
        "legal_name": "GreenAgro Cooperative Society",
        "mobile_number": "9834567890",
        "email": "admin@greenagro.coop",
        "pan": "GRNAG0002B",
        "aadhaar_masked": "XXXXXXXX5678",
        "district": "Nashik",
        "address_line1": "Plot 45, MIDC Area",
        "state": "Maharashtra",
        "pincode": "422007",
        "persona_name": "GreenAgro Cooperative",
        "business": {
            "trade_name": "GreenAgro Cooperative Society",
            "gstin": "27SIMGA0002B1Z8",
            "udyam_number": "UDYAM-MH-11-0087654",
            "cin": None,
            "constitution_type": "Cooperative",
            "annual_turnover": 28000000.0,
            "industry_segment": "Agriculture",
            "business_vintage_years": 8,
            "employee_count": 34,
            "existing_banking": "Bank of Maharashtra"
        }
    },
    "QuickLogistics Services": {
        "legal_name": "Quick Logistics Services Pvt Ltd",
        "mobile_number": "9900112233",
        "email": "ops@quicklogistics.in",
        "pan": "QKLOG0003C",
        "aadhaar_masked": "XXXXXXXX9012",
        "district": "Pune",
        "address_line1": "Logistics Park, Hinjewadi",
        "state": "Maharashtra",
        "pincode": "411057",
        "persona_name": "QuickLogistics Services",
        "business": {
            "trade_name": "Quick Logistics Services Pvt Ltd",
            "gstin": "27SIMQL0003C1Z1",
            "udyam_number": "UDYAM-MH-20-0034521",
            "cin": "U72900MH2015PTC000003",
            "constitution_type": "Private Limited",
            "annual_turnover": 84000000.0,
            "industry_segment": "Logistics & Supply Chain",
            "business_vintage_years": 9,
            "employee_count": 215,
            "existing_banking": "ICICI Bank, Axis Bank"
        }
    }
}

@app.post("/customers/load-persona", response_model=dict)
async def load_persona(payload: PersonaLoadRequest):
    """Return prefilled form data for a named ESE persona."""
    resolved_name = payload.persona_name
    tmpl = PERSONA_TEMPLATES.get(resolved_name)
    if not tmpl:
        raise HTTPException(status_code=404, detail=f"Persona '{payload.persona_name}' not found in dataset.")
    logger.info(f"AUDIT | Persona form populated: {payload.persona_name} -> {resolved_name}")
    return {"status": "ok", "persona": {**tmpl, "requested_persona_name": payload.persona_name, "resolved_persona_name": resolved_name}}


# --- Field Validation ---
@app.post("/customers/validate", response_model=ValidationResponse)
async def validate_customer_fields(payload: CustomerValidateRequest, db: Session = Depends(get_db)):
    """Validate individual fields and detect duplicates before full registration."""
    import re
    PAN_RE = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")
    MOBILE_RE = re.compile(r"^\d{10}$")

    results = []

    # PAN format
    results.append(ValidationResult(
        field="pan", valid=bool(PAN_RE.match(payload.pan)),
        message="PAN format valid." if PAN_RE.match(payload.pan) else "PAN must be 5 letters + 4 digits + 1 letter."
    ))
    # Mobile
    results.append(ValidationResult(
        field="mobile_number", valid=bool(MOBILE_RE.match(payload.mobile_number)),
        message="Mobile valid." if MOBILE_RE.match(payload.mobile_number) else "Mobile must be exactly 10 digits."
    ))
    # Duplicate PAN
    dup_pan = db.query(Customer).filter(Customer.pan == payload.pan, Customer.is_deleted == False).first()
    results.append(ValidationResult(
        field="pan_duplicate", valid=dup_pan is None,
        message="PAN is unique." if dup_pan is None else f"Duplicate PAN found: Customer ID {dup_pan.id}."
    ))
    # Duplicate Mobile
    dup_mob = db.query(Customer).filter(Customer.mobile_number == payload.mobile_number, Customer.is_deleted == False).first()
    results.append(ValidationResult(
        field="mobile_duplicate", valid=dup_mob is None,
        message="Mobile is unique." if dup_mob is None else f"Duplicate Mobile found: Customer ID {dup_mob.id}."
    ))

    all_valid = all(r.valid for r in results)
    return ValidationResponse(all_valid=all_valid, results=results)


# --- Document Upload (Simulated) ---
@app.post("/customers/{id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(id: int, payload: DocumentUploadRequest, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == id, Customer.is_deleted == False).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    doc = OnboardingDocument(
        customer_id=id,
        doc_type=payload.doc_type,
        doc_name=payload.doc_name,
        source=payload.source,
        status="PENDING"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    logger.info(f"AUDIT | Document uploaded | Customer: {id} | Type: {payload.doc_type} | Source: {payload.source}")
    return doc


@app.get("/customers/{id}/documents", response_model=List[DocumentResponse])
async def list_documents(id: int, db: Session = Depends(get_db)):
    return db.query(OnboardingDocument).filter(OnboardingDocument.customer_id == id).all()


# --- Workflow Trigger (publishes Business Events + starts MSME Lending Journey) ---
@app.post("/customers/{id}/start-workflow", response_model=WorkflowTriggerResponse)
async def start_lending_workflow(id: int, db: Session = Depends(get_db)):
    """Publish onboarding events and launch the MSME Lending Journey workflow."""
    import uuid as _uuid
    customer = db.query(Customer).filter(Customer.id == id, Customer.is_deleted == False).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    # Publish business events (logged to audit trail)
    events_published = ["Customer Registered", "Business Registered", "Workflow Started"]
    wf_id = f"wf_{_uuid.uuid4().hex[:12]}"

    for evt in events_published:
        logger.info(
            f"AUDIT | EVENT_BUS | Published: {evt} "
            f"| Customer: {id} | Persona: {customer.persona_name or customer.legal_name} "
            f"| WorkflowID: {wf_id}"
        )

    # Persist workflow reference
    customer.workflow_id = wf_id
    customer.onboarding_status = "SUBMITTED"
    db.commit()

    logger.info(f"AUDIT | MSME Lending Journey launched | Customer: {id} | WorkflowID: {wf_id}")
    return WorkflowTriggerResponse(
        workflow_id=wf_id,
        template_name="MSME Lending Journey",
        status="STARTED",
        customer_id=id,
        events_published=events_published
    )
