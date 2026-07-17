import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("mca-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for mca-service...")
        from sqlalchemy import text
        with engine.connect() as conn:
            for tbl in ["mca_company_profiles", "mca_directors", "mca_charges", "mca_company_filings", "mca_financial_statements", "mca_governance_analytics", "mca_links"]:
                conn.execute(text(f"DROP TABLE IF EXISTS {tbl}"))
                conn.commit()
            
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
