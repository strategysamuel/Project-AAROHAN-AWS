"""
OCEN Marketplace – Database Bootstrap
"""
import json
import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.models import Base, Lender, LoanProduct, Partner, MarketplaceConfig

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("ocen-uli-service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    try:
        logger.info("Initializing OCEN marketplace database tables...")
        inspector = inspect(engine)
        existing = inspector.get_table_names()

        # Drop and recreate all OCEN-specific tables to apply schema changes
        ocen_tables = [
            "ocen_lenders", "ocen_loan_products", "ocen_marketplace_matches",
            "ocen_marketplace_config", "ocen_loan_applications",
            "ocen_loan_offers", "ocen_audit_logs", "ocen_partners",
        ]

        tables_to_drop = [
            Base.metadata.tables[t] for t in ocen_tables if t in existing and t in Base.metadata.tables
        ]
        if tables_to_drop:
            Base.metadata.drop_all(bind=engine, tables=tables_to_drop)

        Base.metadata.create_all(bind=engine)
        logger.info("OCEN tables created successfully.")
        _seed(SessionLocal())
    except Exception as exc:
        logger.error(f"Failed to initialize OCEN database: {exc}")


def _seed(db):
    from app.adapters import LENDER_SEED_DATA, LOAN_PRODUCTS_SEED, DEFAULT_MATCH_PARAMS

    try:
        if db.query(Lender).count() == 0:
            logger.info("Seeding 10 lenders into OCEN registry...")
            for d in LENDER_SEED_DATA:
                db.add(Lender(**d))
            db.commit()
            logger.info("Lender seed complete.")

        if db.query(LoanProduct).count() == 0:
            logger.info("Seeding loan products...")
            for code, name, desc in LOAN_PRODUCTS_SEED:
                db.add(LoanProduct(product_code=code, product_name=name, description=desc))
            db.commit()

        if db.query(Partner).count() == 0:
            partners = [
                Partner(partner_id="PART-GSTN", name="GSTN Portal Service", partner_type="Tech Provider"),
                Partner(partner_id="PART-ONDC", name="ONDC Credit LSP App", partner_type="LSP"),
            ]
            db.add_all(partners)
            db.commit()

        if db.query(MarketplaceConfig).count() == 0:
            db.add(MarketplaceConfig(
                active_adapter="SIMULATION",
                match_params=json.dumps(DEFAULT_MATCH_PARAMS),
            ))
            db.commit()

    finally:
        db.close()
