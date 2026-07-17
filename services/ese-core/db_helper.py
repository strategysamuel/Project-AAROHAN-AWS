import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger("ese-core")

Base = declarative_base()

def get_active_dataset_path() -> str:
    """
    Returns the absolute path to the active simulation database (banking.db).
    Resolves using ACTIVE_DATASET env variable, defaulting to 'msme'.
    """
    active_dataset = os.getenv("ACTIVE_DATASET", os.getenv("ACTIVE_DATASET_VERSION", "msme")).lower()
    
    # We look for datasets in 'ese/datasets/' (relative to workspace root)
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    dataset_dir = os.path.join(workspace_root, "ese", "datasets", active_dataset)
    
    # Ensure directory exists
    os.makedirs(dataset_dir, exist_ok=True)
    
    db_path = os.path.join(dataset_dir, "banking.db")
    return db_path

def get_db_url() -> str:
    return f"sqlite:///{get_active_dataset_path()}"

def get_engine():
    db_url = get_db_url()
    # Use WAL mode for concurrency
    engine = create_engine(
        db_url, 
        connect_args={"check_same_thread": False}
    )
    return engine

def get_sim_db_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_sim_db():
    db = get_sim_db_session()
    try:
        yield db
    finally:
        db.close()
