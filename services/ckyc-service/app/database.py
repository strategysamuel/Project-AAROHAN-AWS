import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("ckyc-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for ckyc-service...")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables_to_drop = []
        if "ckyc_records" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["ckyc_records"])
        if "ckyc_verification_logs" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["ckyc_verification_logs"])
        
        if tables_to_drop:
            Base.metadata.drop_all(bind=engine, tables=tables_to_drop)
            
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
