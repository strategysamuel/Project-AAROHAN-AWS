import os
import sys
import pytest
from fastapi.testclient import TestClient

# Helper to load apps dynamically from directories with dashes
def load_app(service_name: str):
    path = os.path.abspath(f"services/{service_name}")
    if path not in sys.path:
        sys.path.insert(0, path)
    
    # Clear all cached modules under 'app' root package to avoid monorepo crossover
    for k in list(sys.modules.keys()):
        if k == "app" or k.startswith("app."):
            sys.modules.pop(k, None)
            
    try:
        module = __import__("app.main", fromlist=["app"])
        return module.app
    finally:
        if path in sys.path:
            sys.path.remove(path)

def test_onboarding_and_consent_journey():
    # 1. Onboarding Service
    onboarding_app = load_app("onboarding-service")
    client_onboarding = TestClient(onboarding_app)
    
    res = client_onboarding.get("/customers")
    assert res.status_code == 200
    
    # 2. Consent Service
    consent_app = load_app("consent-service")
    client_consent = TestClient(consent_app)
    
    res = client_consent.get("/consents/purposes")
    assert res.status_code == 200
    assert len(res.json()) > 0

def test_financial_evaluation_and_health():
    # 1. GST Service
    gst_app = load_app("gst-service")
    client_gst = TestClient(gst_app)
    
    # Sync first
    sync_res = client_gst.post("/gst/sync/120", json={"gstin": "27AAAAA1111A1Z1"})
    assert sync_res.status_code == 200
    
    # Retrieve profile
    profile_res = client_gst.get("/gst/profile/120")
    assert profile_res.status_code == 200
    assert profile_res.json()["gstin"] == "27AAAAA1111A1Z1"
    
    # 2. Account Aggregator
    aa_app = load_app("aa-service")
    client_aa = TestClient(aa_app)
    
    # Link first
    link_payload = [{
        "account_ref_num": "ACC-001",
        "masked_acc_num": "XXXX1234",
        "bank_name": "IDBI Bank",
        "account_type": "SAVINGS"
    }]
    link_res = client_aa.post("/aa/link/120", json=link_payload)
    assert link_res.status_code == 200
    
    # Sync transactions
    sync_aa_res = client_aa.post("/aa/sync/120", json={"consent_id": 12345})
    assert sync_aa_res.status_code == 200
    
    # Get accounts
    acc_res = client_aa.get("/aa/accounts/120")
    assert acc_res.status_code == 200
    
    # 3. Financial Health Card
    fhc_app = load_app("fhc-service")
    client_fhc = TestClient(fhc_app)
    
    # Calculate score
    calc_res = client_fhc.post("/fhc/calculate/120")
    assert calc_res.status_code == 200
    
    # Retrieve card
    card_res = client_fhc.get("/fhc/120")
    assert card_res.status_code == 200

def test_credit_and_cam_generation():
    # 1. Credit Decision Engine
    credit_app = load_app("credit-engine")
    client_credit = TestClient(credit_app)
    
    eval_res = client_credit.post("/credit/evaluate/120")
    assert eval_res.status_code == 200
    assert eval_res.json()["approval_status"] == "PENDING_HUMAN_REVIEW"
    
    # 2. CAM Generator
    cam_app = load_app("cam-service")
    client_cam = TestClient(cam_app)
    
    generate_res = client_cam.post("/cam/generate/120")
    assert generate_res.status_code == 201
    
    doc_res = client_cam.get("/cam/120")
    assert doc_res.status_code == 200

def test_rm_and_exec_workspace():
    # 1. Relationship Manager Workspace
    rm_app = load_app("rm-workspace-service")
    client_rm = TestClient(rm_app)
    
    res = client_rm.get("/rm/tasks")
    assert res.status_code == 200
    assert len(res.json()) >= 2
    assert res.json()[0]["status"] == "PENDING"
    
    # 2. Executive Dashboard
    exec_app = load_app("exec-service")
    client_exec = TestClient(exec_app)
    
    res = client_exec.get("/exec/kpis")
    assert res.status_code == 200
    
    # 3. Early Warning System
    ews_app = load_app("ews-service")
    client_ews = TestClient(ews_app)
    
    # Evaluate
    eval_res = client_ews.post("/ews/evaluate/120")
    assert eval_res.status_code == 200
    
    # Get Watchlist
    watchlist_res = client_ews.get("/ews/watchlist")
    assert watchlist_res.status_code == 200

def test_regulatory_and_trade_finance():
    # 1. CKYC
    ckyc_app = load_app("ckyc-service")
    client_ckyc = TestClient(ckyc_app)
    
    # Search first
    search_res = client_ckyc.post("/ckyc/search", json={"pan": "ABCDE1234F"})
    assert search_res.status_code == 200
    
    # Verify
    verify_res = client_ckyc.post("/ckyc/verify/125", json={"customer_id": 125, "checked_by": "RM-101"})
    assert verify_res.status_code == 200
    
    # 2. MCA
    mca_app = load_app("mca-service")
    client_mca = TestClient(mca_app)
    
    # Sync first
    sync_mca_res = client_mca.post("/mca/sync/120", json={"cin": "U72900KA2020P134567"})
    assert sync_mca_res.status_code == 200
    
    res = client_mca.get("/mca/profile/120")
    assert res.status_code == 200
    
    # 3. EPFO
    epfo_app = load_app("epfo-service")
    client_epfo = TestClient(epfo_app)
    
    # Sync first
    sync_epfo_res = client_epfo.post("/epfo/sync/120", json={"establishment_id": "MHBAN00000000000000000", "esic_registration_num": "55000123450000101"})
    assert sync_epfo_res.status_code == 200
    
    res = client_epfo.get("/epfo/profile/120")
    assert res.status_code == 200
    
    # 4. TReDS
    treds_app = load_app("treds-service")
    client_treds = TestClient(treds_app)
    
    # Sync first
    sync_treds_res = client_treds.post("/treds/sync/125", json={"seller_pan": "ABCDE1234F"})
    assert sync_treds_res.status_code == 200
    
    res = client_treds.get("/treds/invoices/125")
    assert res.status_code == 200

def test_ocen_uli_loan_disbursement_journey():
    # 1. OCEN Gateway Service
    ocen_app = load_app("ocen-uli-service")
    client_ocen = TestClient(ocen_app)
    
    # Check health check endpoint
    res = client_ocen.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
    
    # Eligibility check
    eligibility_payload = {
        "customer_id": 125,
        "annual_revenue": 10000000.0,
        "credit_score": 780,
        "requested_amount": 1000000.0
    }
    res = client_ocen.post("/ocen/eligibility", json=eligibility_payload)
    assert res.status_code == 200
    assert res.json()["eligible"] is True
    
    # Application & offer matching
    apply_payload = {
        "customer_id": 125,
        "requested_amount": 500000.0,
        "requested_tenure_months": 12,
        "purpose": "Inventory purchase"
    }
    res = client_ocen.post("/ocen/apply", json=apply_payload)
    assert res.status_code == 200
    app_data = res.json()
    assert app_data["status"] == "OFFERS_GENERATED"
    app_id = app_data["id"]
    
    # Offers list
    res = client_ocen.get(f"/ocen/applications/{app_id}/offers")
    assert res.status_code == 200
    offers = res.json()
    assert len(offers) > 0
    offer_id = offers[0]["id"]
    
    # Accept
    res = client_ocen.post("/ocen/offers/accept", json={"offer_id": offer_id})
    assert res.status_code == 200
    assert res.json()["status"] == "ACCEPTED"
    
    # Disburse
    res = client_ocen.post(f"/ocen/disburse/{app_id}")
    assert res.status_code == 200
    assert res.json()["status"] == "DISBURSED"

def test_rbi_fraud_registry_blacklist():
    # Clean up any existing customer with FRAUD1234F PAN or conflicting GSTIN
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine("sqlite:///./aarohan_local.db")
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM onboarding_customers WHERE pan = 'FRAUD1234F'"))
            conn.execute(text("DELETE FROM onboarding_businesses WHERE gstin = '27FRAUD1234F1Z1'"))
            conn.commit()
    except Exception:
        pass

    # 1. Onboard a customer with blacklisted PAN
    onboarding_app = load_app("onboarding-service")
    client_onboarding = TestClient(onboarding_app)
    
    import random
    rand_suffix = random.randint(10000, 99999)
    mobile_number = "9" + "".join(random.choices("0123456789", k=9))
    
    payload = {
        "legal_name": f"Fraudulent Merchant {rand_suffix} Ltd",
        "mobile_number": mobile_number,
        "email": f"fraud_{rand_suffix}@merchant.com",
        "pan": "FRAUD1234F", # Blacklisted PAN
        "businesses": [
            {
                "trade_name": "Fraud Goods",
                "gstin": "27FRAUD1234F1Z1",
                "cin": None,
                "constitution_type": "Private Limited",
                "annual_turnover": 1000000.0,
                "industry_segment": "Retail"
            }
        ],
        "addresses": [
            {
                "address_line1": "123 Fraud St",
                "city": "Mumbai",
                "state": "Maharashtra",
                "pincode": "400001",
                "address_type": "OFFICE"
            }
        ]
    }
    
    onboard_res = client_onboarding.post("/customers", json=payload)
    assert onboard_res.status_code == 201, f"Failed to onboard: {onboard_res.status_code} - {onboard_res.text}"
    customer_id = onboard_res.json()["id"]
        
    # 2. Query credit-engine for evaluation
    credit_app = load_app("credit-engine")
    client_credit = TestClient(credit_app)
    
    eval_res = client_credit.post(f"/credit/evaluate/{customer_id}")
    assert eval_res.status_code == 200
    data = eval_res.json()
    assert data["rbi_fraud_status"] == "BLACKLISTED"
    assert data["recommendation"] == "REJECTED"
    assert data["approval_status"] == "REJECTED"
