from services.shared.database import Base
"""
AAROHAN OCEN Marketplace – Database Models (v2)
================================================
Extends the original scaffolding with:
  • Rich Lender Registry (10 lenders, full policy attributes)
  • Loan Product catalogue
  • Marketplace Match Records (match score + explainability)
  • Offer Rejection tracking
  • Marketplace configuration
"""
import datetime

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


# ---------------------------------------------------------------------------
# Lender Registry (rich policy attributes)
# ---------------------------------------------------------------------------
class Lender(Base):
    __tablename__ = "ocen_lenders"
    __table_args__ = {'extend_existing': True}
    {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    lender_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    lender_type = Column(String(50), default="BANK")          # BANK | NBFC | FINTECH | MFI
    base_interest_rate = Column(Float, default=10.5)           # % p.a. minimum
    max_interest_rate = Column(Float, default=18.0)            # % p.a. maximum
    max_loan_amount = Column(Float, default=5_000_000.0)       # ₹
    min_loan_amount = Column(Float, default=50_000.0)          # ₹
    min_credit_score = Column(Integer, default=650)
    processing_fee_pct = Column(Float, default=1.0)            # % of loan amount
    max_tenure_months = Column(Integer, default=60)
    min_tenure_months = Column(Integer, default=6)
    risk_appetite = Column(String(20), default="MEDIUM")       # LOW | MEDIUM | HIGH
    collateral_required = Column(Boolean, default=False)
    preferred_industries = Column(String(500), default="ALL")  # comma-separated
    geographic_coverage = Column(String(200), default="PAN_INDIA")
    tat_days = Column(Integer, default=3)                      # turnaround time
    loan_products = Column(String(500), default="Working Capital Loan,Term Loan")
    women_entrepreneur_scheme = Column(Boolean, default=False)
    startup_friendly = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)


# ---------------------------------------------------------------------------
# Loan Products
# ---------------------------------------------------------------------------
class LoanProduct(Base):
    __tablename__ = "ocen_loan_products"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(50), unique=True, nullable=False, index=True)
    product_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)


# ---------------------------------------------------------------------------
# Partner Registry (LSPs, Tech Providers)
# ---------------------------------------------------------------------------
class Partner(Base):
    __tablename__ = "ocen_partners"
    __table_args__ = {'extend_existing': True}
    {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    partner_type = Column(String(50), default="LSP")
    is_active = Column(Boolean, default=True)


# ---------------------------------------------------------------------------
# Loan Application
# ---------------------------------------------------------------------------
class LoanApplication(Base):
    __tablename__ = "ocen_loan_applications"
    __table_args__ = {'extend_existing': True}
    {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    uli_reference = Column(String(100), unique=True, nullable=False, index=True)
    requested_amount = Column(Float, nullable=False)
    requested_tenure_months = Column(Integer, default=12)
    product_type = Column(String(100), default="Working Capital Loan")
    purpose = Column(String(250), nullable=True)
    status = Column(String(50), default="APPLIED")
    selected_offer_id = Column(Integer, nullable=True)

    # Upstream intelligence inputs
    fhc_score = Column(Float, nullable=True)               # Financial Health Card composite
    credit_decision = Column(String(50), nullable=True)    # APPROVE | CONDITIONAL | REJECT
    fraud_score = Column(Float, nullable=True)             # RBI fraud risk score
    fraud_risk_level = Column(String(20), nullable=True)   # Low | Medium | High | Critical

    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    offers = relationship("LoanOffer", back_populates="application")


# ---------------------------------------------------------------------------
# Loan Offer (enriched with match score and explainability)
# ---------------------------------------------------------------------------
class LoanOffer(Base):
    __tablename__ = "ocen_loan_offers"
    __table_args__ = {'extend_existing': True}
    {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("ocen_loan_applications.id"), nullable=False)
    lender_id = Column(String(50), nullable=False, index=True)
    lender_name = Column(String(200), nullable=False)
    lender_type = Column(String(50), default="BANK")
    product_type = Column(String(100), default="Working Capital Loan")

    offered_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    processing_fee = Column(Float, default=0.0)
    monthly_installment = Column(Float, nullable=False)
    total_interest = Column(Float, default=0.0)
    approval_probability = Column(Float, default=0.8)       # 0–1
    expected_disbursal_days = Column(Integer, default=3)

    match_score = Column(Float, default=0.0)               # 0–100
    rank = Column(Integer, default=1)
    conditions = Column(Text, nullable=True)
    match_explanation = Column(Text, nullable=True)         # JSON string

    status = Column(String(50), default="PENDING")          # PENDING | ACCEPTED | REJECTED | EXPIRED
    rejection_reason = Column(String(300), nullable=True)
    created_at = Column(DateTime, default=utc_now)

    application = relationship("LoanApplication", back_populates="offers")


# ---------------------------------------------------------------------------
# Marketplace Match Record
# ---------------------------------------------------------------------------
class MarketplaceMatch(Base):
    __tablename__ = "ocen_marketplace_matches"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("ocen_loan_applications.id"), nullable=False)
    lenders_screened = Column(Integer, default=0)
    lenders_matched = Column(Integer, default=0)
    lenders_rejected = Column(Integer, default=0)
    best_offer_id = Column(Integer, nullable=True)
    best_rate = Column(Float, nullable=True)
    best_match_score = Column(Float, nullable=True)
    status = Column(String(50), default="COMPLETED")
    created_at = Column(DateTime, default=utc_now)


# ---------------------------------------------------------------------------
# Marketplace Config
# ---------------------------------------------------------------------------
class MarketplaceConfig(Base):
    __tablename__ = "ocen_marketplace_config"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    active_adapter = Column(String(50), default="SIMULATION")
    match_params = Column(Text, nullable=True)              # JSON
    created_at = Column(DateTime, default=utc_now)


# ---------------------------------------------------------------------------
# Audit Log
# ---------------------------------------------------------------------------
class AuditLog(Base):
    __tablename__ = "ocen_audit_logs"
    __table_args__ = {'extend_existing': True}
    {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    correlation_id = Column(String(100), index=True)
    event_type = Column(String(100), nullable=False, index=True)
    actor = Column(String(100), default="SYSTEM")
    message = Column(String(500), nullable=False)
    details = Column(String(2000), nullable=True)
    timestamp = Column(DateTime, default=utc_now)
