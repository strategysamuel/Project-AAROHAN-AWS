import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import pathlib
import os

# Get the absolute path of the workspace root (two levels up from services/shared)
workspace_root = pathlib.Path(__file__).parent.parent.parent.resolve()
data_dir = workspace_root / "data"

if data_dir.exists() and data_dir.is_dir():
    db_path = data_dir / "aarohan_local.db"
else:
    db_path = workspace_root / "aarohan_local.db"

# Ensure the URL is correctly formatted for SQLAlchemy
db_url = f"sqlite:///{db_path.as_posix()}"

DATABASE_URL = os.getenv("DATABASE_URL", db_url)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
