import os
import re

SERVICES_DIR = "services"

for root, dirs, files in os.walk(SERVICES_DIR):
    if "app" in dirs:
        app_dir = os.path.join(root, "app")
        srv_name = os.path.basename(root)
        if srv_name == "shared" or srv_name.startswith('.'):
            continue
            
        models_path = os.path.join(app_dir, "models.py")
        if os.path.exists(models_path):
            with open(models_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Remove Base = declarative_base() and its import if they exist
            content = re.sub(r'^Base\s*=\s*declarative_base\(\)\s*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'from\s+sqlalchemy\.ext\.declarative\s+import\s+declarative_base', '', content)
            
            # It might be from sqlalchemy.orm import declarative_base
            if "from sqlalchemy.orm import declarative_base" in content:
                content = content.replace("from sqlalchemy.orm import declarative_base", "")
            elif "from sqlalchemy.orm import relationship, declarative_base" in content:
                content = content.replace("from sqlalchemy.orm import relationship, declarative_base", "from sqlalchemy.orm import relationship")
            
            # Check if we already import Base from shared
            if "from services.shared.database import Base" not in content:
                content = "from services.shared.database import Base\n" + content
                
            with open(models_path, "w", encoding="utf-8") as f:
                f.write(content)

        db_path = os.path.join(app_dir, "database.py")
        if os.path.exists(db_path):
            new_db_content = f"""import logging
from services.shared.database import engine, SessionLocal, get_db, Base

logger = logging.getLogger("{srv_name}")

def init_db():
    try:
        import app.models
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {{str(e)}}")
"""
            with open(db_path, "w", encoding="utf-8") as f:
                f.write(new_db_content)

print("Phase 2: Shared database module refactoring applied to all services.")
