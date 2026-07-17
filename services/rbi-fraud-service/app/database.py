import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, FraudWatchlist

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("rbi-fraud-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for rbi-fraud-service...")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables_to_drop = []
        
        if "rbi_fraud_records" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["rbi_fraud_records"])
        if "rbi_fraud_watchlist" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["rbi_fraud_watchlist"])
        if "rbi_fraud_config" in inspector.get_table_names():
            tables_to_drop.append(Base.metadata.tables["rbi_fraud_config"])
            
        if tables_to_drop:
            logger.info("Dropping existing rbi-fraud-service tables to update column schema...")
            Base.metadata.drop_all(bind=engine, tables=tables_to_drop)
            
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
        
        # Seed default watchlist values
        db = SessionLocal()
        try:
            if db.query(FraudWatchlist).count() == 0:
                logger.info("Seeding default watchlist records...")
                watchlist_items = [
                    FraudWatchlist(watchlist_type="PAN", value="FRAUD1234F", reason="Involved in corporate credit siphon case"),
                    FraudWatchlist(watchlist_type="PAN", value="BLACKLIST1F", reason="Director blacklisted by SEBI"),
                    FraudWatchlist(watchlist_type="PAN", value="RBI999999F", reason="Matches fraud identity indicator"),
                    FraudWatchlist(watchlist_type="GSTIN", value="27FRAUD0001K1Z5", reason="Linked to circular fake invoicing network"),
                    FraudWatchlist(watchlist_type="ACCOUNT", value="9999999999", reason="Flagged money laundering cash withdrawal account"),
                    FraudWatchlist(watchlist_type="DIRECTOR", value="DIN888888", reason="Disqualified director associated with shell entities")
                ]
                db.add_all(watchlist_items)
                db.commit()
                logger.info("Seeding completed.")
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
