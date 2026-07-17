"""
AAROHAN CAM Service – Database Models (v2)
==========================================
Comprehensive ORM for the Credit Appraisal Memo service with:
  • Full 18-section CAM record
  • Version history with section snapshots
  • Approval log
  • Template registry
  • CAM configuration
"""
import datetime

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class CAMRecord(Base):
    """Master CAM record storing all 18 sections and scoring."""
    __tablename__ = "cam_records"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    cam_reference = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(50), default="DRAFT")       # DRAFT|PENDING_APPROVAL|APPROVED|REJECTED|ARCHIVED
    current_version = Column(Integer, default=1)
    template = Column(String(50), default="IDBI_BANK") # template key

    # ── Identification ──────────────────────────────────────────────────────
    section_executive_summary = Column(Text, nullable=False, default="")
    section_applicant_profile = Column(Text, nullable=False, default="")
    section_business_profile = Column(Text, nullable=False, default="")
    section_loan_requirement = Column(Text, nullable=False, default="")

    # ── Verification ────────────────────────────────────────────────────────
    section_identity_verification = Column(Text, nullable=False, default="")
    section_gst_compliance = Column(Text, nullable=False, default="")
    section_banking_behaviour = Column(Text, nullable=False, default="")
    section_workforce_stability = Column(Text, nullable=False, default="")
    section_corporate_governance = Column(Text, nullable=False, default="")

    # ── Scoring / AI ────────────────────────────────────────────────────────
    section_fhc_summary = Column(Text, nullable=False, default="")
    section_credit_decision = Column(Text, nullable=False, default="")
    section_fraud_screening = Column(Text, nullable=False, default="")
    section_ocen_marketplace = Column(Text, nullable=False, default="")

    # ── Recommendation ──────────────────────────────────────────────────────
    section_recommended_offer = Column(Text, nullable=False, default="")
    section_key_risks = Column(Text, nullable=False, default="")
    section_risk_mitigation = Column(Text, nullable=False, default="")
    section_banker_recommendation = Column(Text, nullable=False, default="")
    section_approval_matrix = Column(Text, nullable=False, default="")

    # ── Scoring Summary ─────────────────────────────────────────────────────
    overall_credit_score = Column(Float, nullable=True)
    financial_health_rating = Column(String(10), nullable=True)   # AAA..C
    risk_grade = Column(String(10), nullable=True)                 # Low|Medium|High|Critical
    fraud_status = Column(String(20), nullable=True)              # CLEAR|FLAGGED|BLOCKED
    eligibility_status = Column(String(20), nullable=True)        # ELIGIBLE|CONDITIONAL|INELIGIBLE
    recommended_loan_amount = Column(Float, nullable=True)
    recommended_interest_rate = Column(Float, nullable=True)
    recommended_tenure_months = Column(Integer, nullable=True)

    # ── AI Narrative ────────────────────────────────────────────────────────
    narrative_customer_strengths = Column(Text, nullable=True)
    narrative_business_strengths = Column(Text, nullable=True)
    narrative_financial_observations = Column(Text, nullable=True)
    narrative_key_risks = Column(Text, nullable=True)
    narrative_mitigating_factors = Column(Text, nullable=True)
    narrative_lending_recommendation = Column(Text, nullable=True)
    narrative_monitoring_actions = Column(Text, nullable=True)

    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    versions = relationship("CAMVersion", back_populates="cam", cascade="all, delete-orphan")
    approvals = relationship("CAMApprovalLog", back_populates="cam", cascade="all, delete-orphan")


class CAMVersion(Base):
    """Section snapshots per version."""
    __tablename__ = "cam_versions"

    id = Column(Integer, primary_key=True, index=True)
    cam_id = Column(Integer, ForeignKey("cam_records.id"), nullable=False)
    version_num = Column(Integer, nullable=False)
    edited_by = Column(String(100), nullable=False, default="SYSTEM")
    edited_at = Column(DateTime, default=utc_now)
    change_summary = Column(String(500), nullable=True)

    # Snapshot (key sections)
    section_executive_summary = Column(Text, nullable=False, default="")
    section_banker_recommendation = Column(Text, nullable=False, default="")
    section_recommended_offer = Column(Text, nullable=False, default="")
    section_key_risks = Column(Text, nullable=False, default="")
    overall_credit_score = Column(Float, nullable=True)
    status = Column(String(50), nullable=False, default="DRAFT")

    cam = relationship("CAMRecord", back_populates="versions")


class CAMApprovalLog(Base):
    """Multi-level approval chain."""
    __tablename__ = "cam_approvals"

    id = Column(Integer, primary_key=True, index=True)
    cam_id = Column(Integer, ForeignKey("cam_records.id"), nullable=False)
    approver_id = Column(String(100), nullable=False)
    approver_role = Column(String(100), nullable=False, default="Branch Manager")
    action = Column(String(50), nullable=False)    # APPROVED|REJECTED|RETURNED
    level = Column(Integer, default=1)             # 1=BM, 2=ZM, 3=Credit Committee
    comments = Column(String(1000), nullable=True)
    signed_at = Column(DateTime, default=utc_now)

    cam = relationship("CAMRecord", back_populates="approvals")


class CAMTemplate(Base):
    """Template registry for bank-specific CAM formats."""
    __tablename__ = "cam_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_key = Column(String(50), unique=True, nullable=False)
    template_name = Column(String(200), nullable=False)
    bank_name = Column(String(200), nullable=False)
    logo_placeholder = Column(String(200), nullable=True)
    color_primary = Column(String(10), default="#003366")
    color_secondary = Column(String(10), default="#E8F0FE")
    header_text = Column(String(300), nullable=True)
    footer_text = Column(String(300), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)


class CAMConfig(Base):
    """Service-level configuration."""
    __tablename__ = "cam_config"

    id = Column(Integer, primary_key=True, index=True)
    default_template = Column(String(50), default="IDBI_BANK")
    auto_generate_on_ocen = Column(Boolean, default=True)
    require_fraud_clear = Column(Boolean, default=True)
    sections_enabled = Column(Text, nullable=True)   # JSON list of enabled sections
    created_at = Column(DateTime, default=utc_now)
