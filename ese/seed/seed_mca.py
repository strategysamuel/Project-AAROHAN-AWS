import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESEMCARecord

def seed_mca(db, customers, scenarios_map):
    print("[SEEDER] Seeding MCA records...")
    db.query(ESEMCARecord).delete()
    db.commit()
    
    count = 0
    for customer in customers:
        scenario = scenarios_map.get(customer.scenario_id, {})
        mca_status = scenario.get("mca_status", "ACTIVE_COMPLIANT")
        
        record = ESEMCARecord(
            customer_id=customer.id,
            cin=f"U72900KA2020PTC{customer.id:06d}",
            company_name=f"{customer.legal_name} Private Limited",
            date_of_incorporation="2020-04-15",
            status="ACTIVE" if mca_status != "INACTIVE" else "INACTIVE"
        )
        db.add(record)
        count += 1
        
    db.commit()
    print(f"[SEEDER] Successfully seeded {count} MCA records.")
    return count
