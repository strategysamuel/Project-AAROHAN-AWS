import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESEEPFORecord

def seed_epfo(db, customers, personas_map, scenarios_map):
    print("[SEEDER] Seeding EPFO records...")
    db.query(ESEEPFORecord).delete()
    db.commit()
    
    count = 0
    for customer in customers:
        persona = personas_map.get(customer.scenario_id, {})
        scenario = scenarios_map.get(customer.scenario_id, {})
        
        # Base employee count by business segment
        if "Kirana" in customer.legal_name:
            employee_count = 3
        elif "Textile" in customer.legal_name:
            employee_count = 45
        elif "Exports" in customer.legal_name:
            employee_count = 30
        else:
            employee_count = 12
            
        epfo_status = scenario.get("epfo_compliance", "COMPLIANT")
        
        pf_compliance_score = 100.0 if epfo_status == "COMPLIANT" else 45.5
        last_month_contribution = employee_count * 1800.0 # INR 1800 average per employee contribution
        
        record = ESEEPFORecord(
            customer_id=customer.id,
            establishment_id=f"MHBAN00000000000000{customer.id:04d}",
            employee_count=employee_count,
            pf_compliance_score=pf_compliance_score,
            last_month_contribution=round(last_month_contribution, 2)
        )
        db.add(record)
        count += 1
        
    db.commit()
    print(f"[SEEDER] Successfully seeded {count} EPFO records.")
    return count
