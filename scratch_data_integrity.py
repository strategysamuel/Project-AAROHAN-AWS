import os
import sqlite3
import json

SERVICES_DIR = "services"

services_dbs = []

for srv in os.listdir(SERVICES_DIR):
    srv_path = os.path.join(SERVICES_DIR, srv)
    if not os.path.isdir(srv_path) or srv.startswith('.'):
        continue
    db_path = os.path.join(srv_path, "aarohan_local.db")
    if os.path.exists(db_path):
        services_dbs.append({
            "service": srv,
            "db_path": db_path
        })
    elif os.path.exists(os.path.join(srv_path, "app", "aarohan_local.db")):
        services_dbs.append({
            "service": srv,
            "db_path": os.path.join(srv_path, "app", "aarohan_local.db")
        })

tables_to_check = {
    "ckyc-service": ("ckyc_records", "customer_id"),
    "gst-service": ("gst_profiles", "customer_id"),
    "aa-service": ("aa_linked_accounts", "customer_id"),
    "epfo-service": ("epfo_profiles", "customer_id"),
    "mca-service": ("mca_company_profiles", "customer_id"),
    "credit-engine": ("ai_credit_decisions", "customer_id"),
    "cam-service": ("cam_records", "customer_id"),
    "exec-service": ("exec_kpis", "customer_id"),
    "onboarding-service": ("onboarding_customers", "id")
}

with open("AAR-DATA-INTEGRITY-REPORT.md", "w", encoding="utf-8") as f:
    f.write("# AAR-DATA-INTEGRITY-REPORT\n\n")
    f.write("## Data Integrity Checks\n\n")
    
    for srv_info in services_dbs:
        srv = srv_info["service"]
        db_path = srv_info["db_path"]
        
        f.write(f"### {srv}\n")
        f.write(f"- Database: `{db_path}`\n")
        
        if srv in tables_to_check:
            table, id_col = tables_to_check[srv]
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(f"SELECT {id_col} FROM {table}")
                rows = cursor.fetchall()
                ids = [str(r[0]) for r in rows]
                f.write(f"- Table `{table}` has records for IDs: {', '.join(ids)}\n")
                conn.close()
            except Exception as e:
                f.write(f"- Error querying `{table}`: {e}\n")
        f.write("\n")
        
    f.write("## Findings: Broken Relationships\n\n")
    f.write("- **Customer ID Mismatch:** The core customer ID is likely duplicated or disjoint across the different `aarohan_local.db` files in each service directory. Because each microservice has its own isolated SQLite DB, there is no shared relational integrity. For the system to have a single customer journey, all microservices must point to the same logical Customer ID and ideally the same shared database file (or we must migrate them to a central SQLite DB instance for the hackathon/demo).\n")

print("Done.")
