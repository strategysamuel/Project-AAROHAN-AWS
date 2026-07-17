import os
import re

SERVICES_DIR = "services"

schema_details = []

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
            
            tables = re.findall(r'__tablename__\s*=\s*[\'"]([^\'"]+)[\'"]', content)
            
            pks = re.findall(r'(\w+)\s*=\s*Column\(.*primary_key=True', content)
            fks = re.findall(r'(\w+)\s*=\s*Column\(.*ForeignKey\([\'"]([^\'"]+)[\'"]\)', content)
            
            # rough heuristic for finding columns
            
            schema_details.append({
                "service": srv_name,
                "tables": tables,
                "pks": pks,
                "fks": fks
            })

with open("AAR-DATABASE-SCHEMA.md", "w", encoding="utf-8") as f:
    f.write("# AAR-DATABASE-SCHEMA\n\n")
    
    dup_customer_tables = []
    
    for info in schema_details:
        f.write(f"## {info['service']}\n")
        f.write(f"- Tables: {', '.join(info['tables'])}\n")
        f.write(f"- Primary Keys: {', '.join(info['pks'])}\n")
        
        fk_strs = [f"{fk[0]} -> {fk[1]}" for fk in info['fks']]
        f.write(f"- Foreign Keys: {', '.join(fk_strs)}\n\n")
        
        for t in info['tables']:
            if "customer" in t.lower() or "profile" in t.lower() or "business" in t.lower():
                dup_customer_tables.append(f"{info['service']}.{t}")
                
    f.write("## Duplicated Customer Tables\n")
    for d in dup_customer_tables:
        f.write(f"- {d}\n")
    
    f.write("\n## Isolated Datasets\n")
    f.write("All services previously had isolated SQLite DBs. With Phase 2, they all share `aarohan_local.db` but they still use duplicated tables (e.g., `ckyc_records`, `gst_profiles`) representing the same logical entity without a central unified `customer` table enforcing foreign keys globally.\n")
    
    f.write("\n## Broken Relationships\n")
    f.write("Because there is no central `customers` table that `ckyc_records.customer_id` or `gst_profiles.customer_id` strictly references via a database constraint across all microservices, the relationship is logical. If `customer_id` does not match exactly across these tables, the dashboard breaks. This is identified as a broken relationship.\n")

print("Generated AAR-DATABASE-SCHEMA.md")
