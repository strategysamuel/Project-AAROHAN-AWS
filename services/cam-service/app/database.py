"""
AAROHAN CAM Service – Database Bootstrap
"""
import json
import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.models import Base, CAMTemplate, CAMConfig
from app.cam_engine import TEMPLATES

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger = logging.getLogger("cam-service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    try:
        logger.info("Initializing CAM service database tables...")
        inspector = inspect(engine)
        existing = inspector.get_table_names()

        # Drop old CAM tables to apply new schema
        cam_tables = ["cam_records", "cam_versions", "cam_approvals",
                      "cam_templates", "cam_config"]
        tables_to_drop = [
            Base.metadata.tables[t]
            for t in cam_tables if t in existing and t in Base.metadata.tables
        ]
        if tables_to_drop:
            Base.metadata.drop_all(bind=engine, tables=tables_to_drop)

        Base.metadata.create_all(bind=engine)
        logger.info("CAM tables created.")
        _seed(SessionLocal())
    except Exception as exc:
        logger.error(f"CAM DB init failed: {exc}")


def _seed(db):
    try:
        from app.cam_engine import ALL_SECTIONS
        if db.query(CAMTemplate).count() == 0:
            for key, t in TEMPLATES.items():
                db.add(CAMTemplate(
                    template_key=key,
                    template_name=t["header_text"],
                    bank_name=t["bank_name"],
                    logo_placeholder=t["logo_placeholder"],
                    color_primary=t["color_primary"],
                    color_secondary=t["color_secondary"],
                    header_text=t["header_text"],
                    footer_text=t["footer_text"],
                ))
            db.commit()
            logger.info("CAM templates seeded.")

        if db.query(CAMConfig).count() == 0:
            db.add(CAMConfig(
                default_template="IDBI_BANK",
                auto_generate_on_ocen=True,
                require_fraud_clear=True,
                sections_enabled=json.dumps(ALL_SECTIONS),
            ))
            db.commit()
    finally:
        db.close()
