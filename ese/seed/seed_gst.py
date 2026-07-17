import os
import sys
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESEGSTRecord

def seed_gst(db, customers, scenarios_map):
    print("[SEEDER] Seeding GST records...")
    db.query(ESEGSTRecord).delete()
    db.commit()
    
    count = 0
    base_date = datetime.date(2026, 7, 8)
    
    for customer in customers:
        scenario = scenarios_map.get(customer.scenario_id, {})
        gst_profile = scenario.get("gst_compliance", "COMPLIANT")
        rev_multiplier = scenario.get("gst_revenue_multiplier", 1.0)
        
        # Determine monthly base revenue
        if "Kirana" in customer.legal_name:
            base_monthly_rev = 500000.0
        elif "Textile" in customer.legal_name:
            base_monthly_rev = 2500000.0
        elif "Exports" in customer.legal_name:
            base_monthly_rev = 4000000.0
        else:
            base_monthly_rev = 1500000.0
            
        gstin = f"27{customer.pan}1Z5"
        
        # Seed 12 months
        for m in range(12):
            month_date = base_date - datetime.timedelta(days=30 * m)
            month_str = month_date.strftime("%Y-%m")
            
            # Apply multiplier and minor random variance (within 10%)
            import random
            revenue = base_monthly_rev * rev_multiplier * random.uniform(0.9, 1.1)
            gst_paid = revenue * 0.18 # 18% GST default
            
            # Scenario non-compliance rules
            filing_status = "FILED"
            if gst_profile == "NON_COMPLIANT" and m < 3: # Missed last 3 months
                filing_status = "PENDING"
                
            record = ESEGSTRecord(
                customer_id=customer.id,
                gstin=gstin,
                filing_month=month_str,
                revenue=round(revenue, 2),
                gst_paid=round(gst_paid, 2),
                filing_status=filing_status
            )
            db.add(record)
            count += 1
            
    db.commit()
    print(f"[SEEDER] Successfully seeded {count} GST filing records.")
    return count
