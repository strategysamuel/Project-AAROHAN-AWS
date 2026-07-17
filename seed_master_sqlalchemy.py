import os
import sys
import importlib

# Ensure we can import services
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from services.shared.database import SessionLocal, engine, Base

def load_module(name):
    return importlib.import_module(name)

onboarding_models = load_module("services.onboarding-service.app.models")
gst_models = load_module("services.gst-service.app.models")
ckyc_models = load_module("services.ckyc-service.app.models")
aa_models = load_module("services.aa-service.app.models")
epfo_models = load_module("services.epfo-service.app.models")
mca_models = load_module("services.mca-service.app.models")
fhc_models = load_module("services.fhc-service.app.models")
credit_models = load_module("services.credit-engine.app.models")
cam_models = load_module("services.cam-service.app.models")
exec_models = load_module("services.exec-service.app.models")

# Create tables skipped because microservices create them on startup

def seed_data():
    db = SessionLocal()
    print("====================================================")
    print("PHASE 4: MASTER SEED ORCHESTRATOR (DYNAMIC IDs)")
    print("====================================================")
    
    print("\n--- 1. Creating Customer ---")
    customer = onboarding_models.Customer(
        id=99,
        legal_name="Priya Textile Works",
        mobile_number="9876543210",
        email="priya@textileworks.in",
        pan="PRXPT0001K",
        aadhaar_masked="XXXXXXXX1234",
        district="Surat",
        persona_name="Priya Textile Works",
        onboarding_status="SUBMITTED"
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    customer_id = customer.id
    pan = customer.pan
    print(f"✅ Created Customer! ID: {customer_id} | PAN: {pan}")

    print("\n--- 2. Seeding GST ---")
    gst = gst_models.GSTProfile(
        customer_id=customer_id,
        gstin="27SIMPT0001K1Z5",
        legal_name="Priya Textile Works",
        registration_date="2015-05-20",
        status="Active",
        taxpayer_type="Regular"
    )
    db.add(gst)
    db.commit()
    print("✅ GST Synced")

    print("\n--- 3. Seeding CKYC ---")
    ckyc = ckyc_models.CKYCRecord(
        customer_id=customer_id,
        ckyc_number="30049281726355",
        full_name="Priya Textile Works",
        dob="12-08-1988",
        pan=pan,
        aadhaar_masked="XXXXXXXX1234",
        address="123 Demo St",
        mobile="9876543210",
        email="priya@textileworks.in",
        kyc_status="CLEAN"
    )
    db.add(ckyc)
    db.commit()
    print("✅ CKYC Seeded")

    print("\n--- 4. Seeding Account Aggregator ---")
    aa = aa_models.LinkedAccount(
        customer_id=customer_id,
        account_ref_num="REF123456",
        masked_acc_num="XXXX-XXXX-1234",
        bank_name="HDFC Bank",
        account_type="CURRENT",
        link_status="ACTIVE",
        balance=250000.00
    )
    db.add(aa)
    db.commit()
    print("✅ AA Linked")

    print("\n--- 5. Seeding EPFO ---")
    epfo = epfo_models.EPFOProfile(
        customer_id=customer_id,
        uan="100123456789",
        establishment_id="MHBAN0000012000",
        establishment_name="Priya Textile Works",
        active_employees=87,
        total_remittance_ytd=1500000.0,
        last_remittance_date="2024-03-15",
        compliance_status="REGULAR"
    )
    db.add(epfo)
    db.commit()
    print("✅ EPFO Synced")

    print("\n--- 6. Seeding MCA ---")
    mca = mca_models.MCACompanyProfile(
        customer_id=customer_id,
        cin="U12345MH2020P123456",
        company_name="Priya Textile Works Pvt Ltd",
        date_of_incorporation="2012-05-15",
        roc_code="RoC-Mumbai",
        company_status="Active",
        authorized_capital=1000000.0,
        paid_up_capital=500000.0
    )
    db.add(mca)
    db.commit()
    print("✅ MCA Synced")

    print("\n--- 7. Generating Financial Health Card ---")
    fhc = fhc_models.FinancialHealthCard(
        customer_id=customer_id,
        overall_score=85.5,
        rating="Excellent",
        cash_flow_score=88.0,
        compliance_score=92.0,
        business_stability_score=80.0
    )
    db.add(fhc)
    db.commit()
    print("✅ Financial Health Card Generated")

    print("\n--- 8. Credit Decision ---")
    credit = credit_models.CreditDecision(
        customer_id=customer_id,
        application_id="APP-12345",
        confidence_score=91.0,
        recommendation="APPROVED",
        max_sanction_limit=5000000.0,
        suggested_roi=10.5
    )
    db.add(credit)
    db.commit()
    print("✅ Credit Evaluated")

    print("\n--- 9. CAM Service ---")
    cam = cam_models.CAMRecord(
        customer_id=customer_id,
        cam_reference="CAM-DEMO-001",
        proposed_facility="Working Capital",
        recommended_amount=5000000.0,
        final_roi=10.5,
        tenor_months=36,
        status="APPROVED"
    )
    db.add(cam)
    db.commit()
    print("✅ CAM Generated")
    
    print("\n[SUCCESS] Master Seeding Completed using Dynamic IDs via SQLAlchemy.")
    db.close()

if __name__ == "__main__":
    seed_data()
