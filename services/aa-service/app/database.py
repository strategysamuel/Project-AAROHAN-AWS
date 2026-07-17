import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("aa-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for aa-service...")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables_to_drop = []
        if "aa_linked_accounts" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["aa_linked_accounts"])
        if "aa_transactions" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["aa_transactions"])
        if "aa_analytics" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["aa_analytics"])
        if "aa_consents" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["aa_consents"])
        
        if tables_to_drop:
            Base.metadata.drop_all(bind=engine, tables=tables_to_drop)
            
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
