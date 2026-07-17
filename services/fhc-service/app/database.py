import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("fhc-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for fhc-service...")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables_to_drop = []
        
        # We need to drop these tables to update their schemas to support the new FHC parameters
        if "fhc_cards" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["fhc_cards"])
        if "fhc_score_history" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["fhc_score_history"])
        if "fhc_config" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["fhc_config"])
            
        if tables_to_drop:
            logger.info("Dropping existing fhc-service tables to update column schema...")
            Base.metadata.drop_all(bind=engine, tables=tables_to_drop)
            
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
