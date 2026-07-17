import os
import re

SERVICES_DIR = "services"

for root, dirs, files in os.walk(SERVICES_DIR):
    if "database.py" in files:
        filepath = os.path.join(root, "database.py")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content.replace('"sqlite:///./aarohan_local.db"', 'import os\nos.getenv("DATABASE_URL", "sqlite:///../../aarohan_local.db")')
        new_content = new_content.replace('import os\nimport os', 'import os')
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

print("Updated all database paths to point to shared DB.")
