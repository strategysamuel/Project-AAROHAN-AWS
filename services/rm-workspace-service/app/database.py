import logging
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, RMLead, RMTask, RMAlert

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("rm-workspace-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for rm-workspace-service...")
        Base.metadata.create_all(bind=engine)
        
        # Seed default tasks & leads if empty
        db = SessionLocal()
        if not db.query(RMLead).first():
            l1 = RMLead(company_name="Aditya Garments Pvt Ltd", contact_person="Aditya Patel", mobile="9000000001", pipeline_stage="UNDERWRITING", estimated_loan_amt=5000000.0)
            l2 = RMLead(company_name="Balaji Weaving Mills", contact_person="Balaji Rao", mobile="9000000002", pipeline_stage="QUALIFICATION", estimated_loan_amt=3500000.0)
            db.add_all([l1, l2])
            
        if not db.query(RMTask).first():
            t1 = RMTask(customer_id=120, title="Review GSTR-1 Seasonality File", description="Check October peak margins.", due_date=datetime.datetime.utcnow() + datetime.timedelta(days=2), priority="HIGH")
            t2 = RMTask(customer_id=120, title="Request AA consent renewal", description="Existing consent valid for 5 more days.", due_date=datetime.datetime.utcnow() + datetime.timedelta(days=4), priority="MEDIUM")
            db.add_all([t1, t2])
            
        if not db.query(RMAlert).first():
            a1 = RMAlert(customer_id=120, alert_type="CONSENT_EXPIRY", message="Account Aggregator consent expiring in 5 days.", severity="WARNING")
            a2 = RMAlert(customer_id=120, alert_type="LIQUIDITY_DROP", message="Current Account average balance dropped by 15% MoM.", severity="CRITICAL")
            db.add_all([a1, a2])
            
        db.commit()
        db.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
