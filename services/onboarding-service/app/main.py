import logging
import sys
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Customer, BusinessEntity, ProprietorDirector, Address
from app.schemas import CustomerCreate, CustomerResponse, CustomerBase
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "onboarding-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("onboarding-service")

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
        
    # 2. Map customer properties
    customer = Customer(
        legal_name=payload.legal_name,
        mobile_number=payload.mobile_number,
        email=payload.email,
        pan=payload.pan
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
        
    # 4. Create business entities and directors
    for bus in payload.businesses:
        business = BusinessEntity(
            customer_id=customer.id,
            trade_name=bus.trade_name,
            gstin=bus.gstin,
            cin=bus.cin,
            constitution_type=bus.constitution_type,
            annual_turnover=bus.annual_turnover,
            industry_segment=bus.industry_segment,
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
