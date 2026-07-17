import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("credit-engine")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for credit-engine...")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables_to_drop = []
        
        # We need to drop these tables to recreate them with the correct columns
        if "ai_credit_decisions" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["ai_credit_decisions"])
        if "human_approval_logs" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["human_approval_logs"])
        if "credit_engine_config" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["credit_engine_config"])
            
        if tables_to_drop:
            logger.info("Dropping existing credit-engine tables to update column schema...")
            Base.metadata.drop_all(bind=engine, tables=tables_to_drop)
            
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
