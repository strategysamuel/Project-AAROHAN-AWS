import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESECKYCRecord

def seed_ckyc(db, customers, personas_map):
    print("[SEEDER] Seeding CKYC records...")
    db.query(ESECKYCRecord).delete()
    db.commit()
    
    count = 0
    for customer in customers:
        # Determine status from persona definition
        persona = personas_map.get(customer.scenario_id, {})
        ckyc_status = persona.get("ckyc_status", "CLEAN")
        
        record = ESECKYCRecord(
            customer_id=customer.id,
            pan=customer.pan,
            ckyc_number=f"30049281726{customer.id:03d}",
            full_name=customer.legal_name,
            dob="1988-08-12",
            kyc_status=ckyc_status
        )
        db.add(record)
        count += 1
        
    db.commit()
    print(f"[SEEDER] Successfully seeded {count} CKYC records.")
    return count
