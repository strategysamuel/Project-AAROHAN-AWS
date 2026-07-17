import os
import re
import json

SERVICES_DIR = "services"

audit = []

for root, dirs, files in os.walk(SERVICES_DIR):
    if "app" in dirs:
        app_dir = os.path.join(root, "app")
        srv_name = os.path.basename(root)
        if srv_name.startswith('.'): continue
        
        info = {
            "service": srv_name,
            "has_database_py": os.path.exists(os.path.join(app_dir, "database.py")),
            "has_models_py": os.path.exists(os.path.join(app_dir, "models.py")),
            "database_url": "Unknown",
            "sqlalchemy_engine": False,
            "sessionlocal": False,
            "base": False,
            "models": [],
            "seed_scripts": [],
            "health_endpoint": False
        }
        
        db_path = os.path.join(app_dir, "database.py")
        if os.path.exists(db_path):
            with open(db_path, "r", encoding="utf-8") as f:
                content = f.read()
                info["sqlalchemy_engine"] = "create_engine(" in content
                info["sessionlocal"] = "SessionLocal" in content
                info["base"] = "Base = declarative_base()" in content or "from app.models import Base" in content
                
                url_match = re.search(r'DATABASE_URL\s*=\s*(.+)', content)
                if url_match:
                    info["database_url"] = url_match.group(1).strip()
        
        models_path = os.path.join(app_dir, "models.py")
        if os.path.exists(models_path):
            with open(models_path, "r", encoding="utf-8") as f:
                content = f.read()
                tables = re.findall(r'__tablename__\s*=\s*[\'"]([^\'"]+)[\'"]', content)
                info["models"] = tables

        main_path = os.path.join(app_dir, "main.py")
        if os.path.exists(main_path):
            with open(main_path, "r", encoding="utf-8") as f:
                content = f.read()
                if "/livez" in content or "/health" in content:
                    info["health_endpoint"] = True
                
        # checking seed logic
        if os.path.exists(main_path):
            with open(main_path, "r", encoding="utf-8") as f:
                if "seed" in f.read().lower():
                    info["seed_scripts"].append("main.py")
                    
        audit.append(info)

with open("AAR-DATABASE-AUDIT.md", "w", encoding="utf-8") as f:
    f.write("# AAR-DATABASE-AUDIT\n\n")
    for info in audit:
        f.write(f"## {info['service']}\n")
        f.write(f"- database.py: {'Yes' if info['has_database_py'] else 'No'}\n")
        f.write(f"- DATABASE_URL: {info['database_url']}\n")
        f.write(f"- SQLAlchemy Engine: {'Yes' if info['sqlalchemy_engine'] else 'No'}\n")
        f.write(f"- SessionLocal: {'Yes' if info['sessionlocal'] else 'No'}\n")
        f.write(f"- Base: {'Yes' if info['base'] else 'No'}\n")
        f.write(f"- ORM Models: {', '.join(info['models'])}\n")
        f.write(f"- Seed Scripts: {', '.join(info['seed_scripts'])}\n")
        f.write(f"- Health Endpoint: {'Yes' if info['health_endpoint'] else 'No'}\n\n")

print("Generated AAR-DATABASE-AUDIT.md")
