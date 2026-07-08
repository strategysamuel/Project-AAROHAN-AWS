import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, EWSWatchlist, EWSAlert, EWSRiskCase

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("ews-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for ews-service...")
        Base.metadata.create_all(bind=engine)
        
        # Seed default watchlist & alerts if empty
        db = SessionLocal()
        if not db.query(EWSWatchlist).first():
            w1 = EWSWatchlist(customer_id=120, risk_level="MEDIUM", reason_code="CASHFLOW_DROP")
            w2 = EWSWatchlist(customer_id=115, risk_level="LOW", reason_code="GST_DELAY")
            db.add_all([w1, w2])
            
        if not db.query(EWSAlert).first():
            a1 = EWSAlert(customer_id=120, trigger_rule="RULE_CASHFLOW_DROP", message="Current Account deposits dropped 15% MoM.")
            a2 = EWSAlert(customer_id=115, trigger_rule="RULE_GST_DELAY", message="GST filing was delayed by 5 days in Q2.")
            db.add_all([a1, a2])
            
        if not db.query(EWSRiskCase).first():
            c1 = EWSRiskCase(
                customer_id=120,
                status="OPEN",
                ai_risk_narrative="AI Risk Analysis: Customer 120 displays moderate risk due to current account cash flow volatility. Average balances dropped by 15% MoM, reducing debt service buffer.",
                mitigation_action="Send SMS invitation for account aggregator consent renewal; Schedule RM verification call."
            )
            db.add(c1)
            
        db.commit()
        db.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
