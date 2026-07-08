import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, ConsentPurpose

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("consent-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for consent-service...")
        Base.metadata.create_all(bind=engine)
        
        # Seed default purposes if missing
        db = SessionLocal()
        if not db.query(ConsentPurpose).first():
            p1 = ConsentPurpose(
                code="CREDIT_APPRAISAL",
                description="Retrieve bank ledger transactions and tax history to calculate credit eligibility limits.",
                data_minimization_rules="Only access transactions from last 12 months; delete after underwriting decision."
            )
            p2 = ConsentPurpose(
                code="MONITORING",
                description="Retrieve financial health metrics monthly to detect early warning triggers.",
                data_minimization_rules="Only access monthly aggregate values; retain throughout loan tenure."
            )
            db.add_all([p1, p2])
            db.commit()
            logger.info("Default consent purposes seeded.")
        db.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
