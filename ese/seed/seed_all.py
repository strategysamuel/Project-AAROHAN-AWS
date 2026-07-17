import os
import sys
import glob

# Bootstrap virtualenv site-packages to support running without explicit poetry activation
def bootstrap_virtualenv():
    possible_paths = [
        "C:\\Users\\DELL\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\aarohan-backend-*\\Lib\\site-packages",
        "C:\\Users\\DELL\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\aarohan-backend-*\\lib\\site-packages"
    ]
    for pattern in possible_paths:
        for path in glob.glob(pattern):
            if path not in sys.path:
                sys.path.insert(0, path)
                # Suppress output to keep logs clean unless debugging

bootstrap_virtualenv()

import json
import hashlib
import time
from datetime import datetime

# Adjust path to find ese-core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from db_helper import get_active_dataset_path, get_engine, Base, get_sim_db_session
from models import ESECustomer, ESEBusiness, ESEGSTRecord, ESETransaction, ESECKYCRecord, ESEEPFORecord, ESEMCARecord, ESELoanApplication

# Import seeders
from seed_customers import seed_customers
from seed_businesses import seed_businesses
from seed_transactions import seed_transactions
from seed_gst import seed_gst
from seed_ckyc import seed_ckyc
from seed_epfo import seed_epfo
from seed_mca import seed_mca
from seed_loans import seed_loans
from validator import validate_referential_integrity

def load_json_files(directory):
    items = []
    if not os.path.exists(directory):
        return items
    for f in os.listdir(directory):
        if f.endswith(".json") and f != "schema.json":
            with open(os.path.join(directory, f), "r") as fh:
                items.append(json.load(fh))
    return items

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def main():
    start_time = time.time()
    print("====================================================")
    print("PROJECT AAROHAN - SEED ALL SIMULATION DATASETS")
    print("====================================================")
    
    # 1. Resolve workspace paths
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    personas_dir = os.path.join(workspace_root, "ese", "personas")
    scenarios_dir = os.path.join(workspace_root, "ese", "scenarios")
    
    # Load metadata configs
    personas_data = load_json_files(personas_dir)
    scenarios_data = load_json_files(scenarios_dir)
    
    scenarios_map = {s["scenario_id"]: s for s in scenarios_data}
    personas_map = {p["scenario_id"]: p for p in personas_data}
    
    # 2. Get active database file
    db_path = get_active_dataset_path()
    print(f"[INIT] Active simulation database target: {db_path}")
    
    # Clean previous if exists
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception as e:
            print(f"[WARNING] Could not remove existing DB file: {e}")
            
    # 3. Create schema
    engine = get_engine()
    print("[INIT] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Start Session
    db = get_sim_db_session()
    
    try:
        # 4. Execute modular seeders in order
        customers = seed_customers(db, personas_data)
        seed_businesses(db, customers)
        tx_count = seed_transactions(db, customers, scenarios_map)
        gst_count = seed_gst(db, customers, scenarios_map)
        seed_ckyc(db, customers, personas_map)
        seed_epfo(db, customers, personas_map, scenarios_map)
        seed_mca(db, customers, scenarios_map)
        seed_loans(db, customers)
        
        # 5. Referential integrity checks
        validate_referential_integrity(db)
        
        # Close connection to flush
        db.close()
        
        # 6. Generate checksum & dataset_manifest.json
        checksum = calculate_sha256(db_path)
        
        manifest = {
            "dataset_name": f"{os.path.basename(os.path.dirname(db_path)).upper()} Domain Dataset Package",
            "dataset_version": "1.0.0",
            "compatibility_version": "v3.0",
            "generated_timestamp": datetime.utcnow().isoformat() + "Z",
            "checksum": checksum,
            "personas": [p["persona_name"] for p in personas_data],
            "scenarios": [s["scenario_name"] for s in scenarios_data],
            "supported_demo_journeys": [
                "MSME Lending Journey", 
                "Customer Onboarding", 
                "Financial Health Card", 
                "Fraud Detection"
            ],
            "record_counts": {
                "ese_customers": len(personas_data),
                "ese_businesses": len(personas_data),
                "ese_gst_records": gst_count,
                "ese_transactions": tx_count,
                "ese_ckyc_records": len(personas_data),
                "ese_epfo_records": len(personas_data),
                "ese_mca_records": len(personas_data),
                "ese_loan_applications": len(personas_data)
            },
            "seed_modules_used": [
                "seed_customers",
                "seed_businesses",
                "seed_transactions",
                "seed_gst",
                "seed_ckyc",
                "seed_epfo",
                "seed_mca",
                "seed_loans"
            ]
        }
        
        manifest_path = os.path.join(os.path.dirname(db_path), "dataset_manifest.json")
        with open(manifest_path, "w") as mf:
            json.dump(manifest, mf, indent=2)
            
        duration = time.time() - start_time
        print("====================================================")
        print(f"[SEED COMPLETE] {len(personas_data)} personas, {gst_count} GST records, {tx_count} transactions seeded in {duration:.2f}s")
        print(f"Manifest output: {manifest_path}")
        print("====================================================")
        
    except Exception as e:
        db.rollback()
        db.close()
        print(f"[FATAL] Seeding failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
