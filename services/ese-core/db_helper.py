import os
import logging
from services.shared.database import SessionLocal, engine, Base, get_db

logger = logging.getLogger("ese-core")

def get_active_dataset_path() -> str:
    from services.shared.database import DATABASE_URL
    # Extract path from sqlite:///path
    if DATABASE_URL.startswith("sqlite:///"):
        return DATABASE_URL[10:]
    return DATABASE_URL

def get_db_url() -> str:
    # Deprecated: URL is now managed by shared database layer
    return "sqlite:///../../aarohan_local.db"

def get_engine():
    return engine

def get_sim_db_session():
    return SessionLocal()

def get_sim_db():
    db = get_sim_db_session()
    try:
        yield db
    finally:
        db.close()
