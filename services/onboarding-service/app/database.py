import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("onboarding-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _safe_add_column(conn, table: str, column: str, col_def: str):
    """Add a column only if it doesn't already exist (SQLite has no IF NOT EXISTS for ALTER)."""
    try:
        result = conn.execute(text(f"PRAGMA table_info({table})"))
        existing = [row[1] for row in result.fetchall()]
        if column not in existing:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}"))
            logger.info(f"DB migration: added column {table}.{column}")
    except Exception as e:
        logger.warning(f"DB migration skipped {table}.{column}: {e}")

def init_db():
    """Initialise onboarding schemas and run safe column migrations."""
    try:
        logger.info("Initializing database tables for onboarding-service...")
        # Create any tables that don't yet exist (including onboarding_documents)
        Base.metadata.create_all(bind=engine)

        # Safe ALTER migrations for columns added in AAR-BUILD-008
        with engine.begin() as conn:
            # Customer new fields
            _safe_add_column(conn, "onboarding_customers", "aadhaar_masked",    "VARCHAR(12)")
            _safe_add_column(conn, "onboarding_customers", "district",          "VARCHAR(100)")
            _safe_add_column(conn, "onboarding_customers", "workflow_id",       "VARCHAR(50)")
            _safe_add_column(conn, "onboarding_customers", "persona_name",      "VARCHAR(200)")
            _safe_add_column(conn, "onboarding_customers", "onboarding_status", "VARCHAR(50) DEFAULT 'DRAFT'")
            # Business new fields
            _safe_add_column(conn, "onboarding_businesses", "udyam_number",          "VARCHAR(20)")
            _safe_add_column(conn, "onboarding_businesses", "business_vintage_years", "INTEGER DEFAULT 0")
            _safe_add_column(conn, "onboarding_businesses", "employee_count",         "INTEGER DEFAULT 0")
            _safe_add_column(conn, "onboarding_businesses", "existing_banking",       "VARCHAR(200)")

        logger.info("Database tables and migrations completed successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
