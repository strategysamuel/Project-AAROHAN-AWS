import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../services/ese-core")))

from models import ESECustomer, ESEBusiness, ESEGSTRecord, ESETransaction, ESECKYCRecord, ESEEPFORecord, ESEMCARecord, ESELoanApplication

def validate_referential_integrity(db):
    print("[VALIDATOR] Validating database referential integrity...")
    
    customers = db.query(ESECustomer).all()
    customer_ids = {c.id for c in customers}
    
    # 1. Businesses
    for biz in db.query(ESEBusiness).all():
        if biz.customer_id not in customer_ids:
            raise AssertionError(f"Referential integrity failure: Business {biz.id} references invalid customer {biz.customer_id}")
            
    # 2. GST Records
    for gst in db.query(ESEGSTRecord).all():
        if gst.customer_id not in customer_ids:
            raise AssertionError(f"Referential integrity failure: GST record {gst.id} references invalid customer {gst.customer_id}")
            
    # 3. Transactions
    for tx in db.query(ESETransaction).all():
        if tx.customer_id not in customer_ids:
            raise AssertionError(f"Referential integrity failure: Transaction {tx.id} references invalid customer {tx.customer_id}")
            
    # 4. CKYC Records
    for ckyc in db.query(ESECKYCRecord).all():
        if ckyc.customer_id not in customer_ids:
            raise AssertionError(f"Referential integrity failure: CKYC record {ckyc.id} references invalid customer {ckyc.customer_id}")
            
    # 5. EPFO Records
    for epfo in db.query(ESEEPFORecord).all():
        if epfo.customer_id not in customer_ids:
            raise AssertionError(f"Referential integrity failure: EPFO record {epfo.id} references invalid customer {epfo.customer_id}")
            
    # 6. MCA Records
    for mca in db.query(ESEMCARecord).all():
        if mca.customer_id not in customer_ids:
            raise AssertionError(f"Referential integrity failure: MCA record {mca.id} references invalid customer {mca.customer_id}")
            
    # 7. Loan Applications
    for loan in db.query(ESELoanApplication).all():
        if loan.customer_id not in customer_ids:
            raise AssertionError(f"Referential integrity failure: Loan Application {loan.id} references invalid customer {loan.customer_id}")
            
    print("[VALIDATOR] Referential integrity validation passed successfully.")
    return True
