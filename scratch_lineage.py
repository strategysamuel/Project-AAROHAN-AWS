import os
import ast
import json
import re

SERVICES_DIR = "services"

audit = []

for srv in os.listdir(SERVICES_DIR):
    srv_path = os.path.join(SERVICES_DIR, srv)
    if not os.path.isdir(srv_path) or srv.startswith('.'):
        continue
    
    app_dir = os.path.join(srv_path, "app")
    if not os.path.isdir(app_dir):
        app_dir = srv_path
        
    db_file = os.path.join(app_dir, "database.py")
    models_file = os.path.join(app_dir, "models.py")
    main_file = os.path.join(app_dir, "main.py")
    
    srv_info = {
        "service": srv,
        "database_used": "Unknown",
        "database_file": "Unknown",
        "orm": "Unknown",
        "customer_table": "None",
        "foreign_keys": [],
        "seed_source": "Unknown",
        "report_source": "Unknown"
    }

    if os.path.exists(db_file):
        with open(db_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "sqlite" in content:
                srv_info["database_used"] = "SQLite"
                match = re.search(r'sqlite:///(\S+)', content)
                if match:
                    srv_info["database_file"] = match.group(1).strip("'\"")
            if "sqlalchemy" in content:
                srv_info["orm"] = "SQLAlchemy"

    if os.path.exists(models_file):
        with open(models_file, "r", encoding="utf-8") as f:
            content = f.read()
            tables = re.findall(r'__tablename__\s*=\s*[\'"]([^\'"]+)[\'"]', content)
            if tables:
                srv_info["customer_table"] = tables[0] if "customers" in tables or "business" in tables else tables[0]
            fks = re.findall(r'ForeignKey\([\'"]([^\'"]+)[\'"]\)', content)
            srv_info["foreign_keys"] = fks

    if os.path.exists(main_file):
        with open(main_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "seed" in content.lower():
                srv_info["seed_source"] = "main.py / seed logic"
                
    audit.append(srv_info)

with open("AAR-DATA-LINEAGE.md", "w", encoding="utf-8") as f:
    f.write("# AAR-DATA-LINEAGE\n\n")
    for info in audit:
        f.write(f"## {info['service']}\n")
        f.write(f"- **Database used**: {info['database_used']}\n")
        f.write(f"- **Database file/path**: {info['database_file']}\n")
        f.write(f"- **ORM model**: {info['orm']}\n")
        f.write(f"- **Customer table**: {info['customer_table']}\n")
        f.write(f"- **Foreign keys**: {', '.join(info['foreign_keys'])}\n")
        f.write(f"- **Seed source**: {info['seed_source']}\n")
        f.write(f"- **Report source**: {info['report_source']}\n\n")

    f.write("## Dependency Graph\n\n")
    f.write("Customer\n↓\nGST\n↓\nCKYC\n↓\nAA\n↓\nEPFO\n↓\nMCA\n↓\nCredit\n↓\nCAM\n↓\nExecutive\n↓\nReports\n")

print("Done generating lineage.")
