import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESEBusiness

def seed_businesses(db, customers):
    print("[SEEDER] Seeding businesses...")
    db.query(ESEBusiness).delete()
    db.commit()
    
    businesses_seeded = []
    for customer in customers:
        # Build gstin
        gstin = f"27{customer.pan}1Z5" # Format matched to PAN
        
        business = ESEBusiness(
            customer_id=customer.id,
            trade_name=f"{customer.legal_name} Group",
            gstin=gstin,
            cin=f"U72900KA2020PTC{customer.id:06d}",
            annual_turnover=15000000.0, # Default turnover tier
            industry_segment=customer.persona_name
        )
        db.add(business)
        businesses_seeded.append(business)
        
    db.commit()
    print(f"[SEEDER] Successfully seeded {len(businesses_seeded)} businesses.")
    return businesses_seeded
