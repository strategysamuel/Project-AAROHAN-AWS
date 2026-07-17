import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESELoanApplication

def seed_loans(db, customers):
    print("[SEEDER] Seeding loan application records...")
    db.query(ESELoanApplication).delete()
    db.commit()
    
    count = 0
    for customer in customers:
        # Check defaults
        if "Kirana" in customer.legal_name:
            amt = 500000.0
            tenure = 12
        elif "Textile" in customer.legal_name:
            amt = 5000000.0
            tenure = 36
        elif "Exports" in customer.legal_name:
            amt = 4000000.0
            tenure = 24
        else:
            amt = 1500000.0
            tenure = 24
            
        record = ESELoanApplication(
            customer_id=customer.id,
            requested_amount=amt,
            tenure_months=tenure,
            status="OFFERS_GENERATED",
            interest_rate=10.5
        )
        db.add(record)
        count += 1
        
    db.commit()
    print(f"[SEEDER] Successfully seeded {count} loan applications.")
    return count
