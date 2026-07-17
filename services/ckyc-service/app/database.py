import logging
from services.shared.database import engine, SessionLocal, get_db, Base

logger = logging.getLogger("ckyc-service")

def init_db():
    try:
        import app.models
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
