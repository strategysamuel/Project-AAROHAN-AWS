import os
import sys
import random
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESETransaction

def seed_transactions(db, customers, scenarios_map):
    print("[SEEDER] Seeding transactions...")
    db.query(ESETransaction).delete()
    db.commit()
    
    count = 0
    base_date = datetime.date(2026, 7, 8)
    
    for customer in customers:
        scenario = scenarios_map.get(customer.scenario_id, {})
        flow_profile = scenario.get("cash_flow_stability", "STRONG")
        
        # Decide monthly turnover scale
        if "Kirana" in customer.legal_name:
            monthly_turnover = 500000.0 # Retail MSME Kirana Store
        elif "Textile" in customer.legal_name:
            monthly_turnover = 2500000.0 # Manufacturing Priya Textile Works
        elif "Exports" in customer.legal_name:
            monthly_turnover = 4000000.0 # Exporter Kavitha Exports
        else:
            monthly_turnover = 1500000.0 # Others default
            
        balance = 500000.0 # starting balance
        
        # Generate 50 transactions spread over past 30 days
        for i in range(50):
            tx_date = base_date - datetime.timedelta(days=random.randint(1, 30))
            # Determine debit or credit
            is_credit = random.random() > 0.45
            
            # Adjust flow stability multipliers based on cash flow profile
            if flow_profile == "WEAK":
                is_credit = random.random() > 0.6 # more debits than credits
                
            amount = random.uniform(5000, monthly_turnover / 5)
            
            if is_credit:
                balance += amount
                tx_type = "CREDIT"
                description = f"INWARD FT / GST CR / {customer.id:04d}"
            else:
                balance -= amount
                tx_type = "DEBIT"
                description = f"OUTWARD CHG / SALARY DR / {customer.id:04d}"
                
            transaction = ESETransaction(
                customer_id=customer.id,
                account_ref_num=f"ACC-{customer.id:03d}",
                transaction_date=tx_date.isoformat(),
                amount=round(amount, 2),
                type=tx_type,
                balance=round(balance, 2),
                description=description
            )
            db.add(transaction)
            count += 1
            
    db.commit()
    print(f"[SEEDER] Successfully seeded {count} transactions.")
    return count
