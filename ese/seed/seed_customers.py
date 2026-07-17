import os
import sys

# Adjust path to find ese-core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESECustomer

def seed_customers(db, personas):
    print("[SEEDER] Seeding customers...")
    customers_seeded = []
    
    # We delete existing customers to ensure idempotency
    db.query(ESECustomer).delete()
    db.commit()
    
    for idx, persona in enumerate(personas, start=120): # Start ID at 120 matching test suite
        # Build legal name
        name_parts = persona["persona_name"].split(" ")
        legal_name = persona["persona_name"]
        
        customer = ESECustomer(
            id=idx,
            pan=persona["pan"],
            legal_name=legal_name,
            mobile_number=f"98765{idx:05d}",
            email=f"{name_parts[0].lower()}@domain.com",
            persona_name=persona["persona_name"],
            scenario_id=persona["scenario_id"]
        )
        db.add(customer)
        customers_seeded.append(customer)
        
    db.commit()
    print(f"[SEEDER] Successfully seeded {len(customers_seeded)} customers.")
    return customers_seeded
