import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_lenders_and_partners_endpoints():
    # Test Lenders Listing
    res = client.get("/ocen/lenders")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 3 # seeded lenders
    
    # Test Partners Listing
    res = client.get("/ocen/partners")
    assert res.status_code == 200
    assert len(res.json()) >= 2 # seeded partners

def test_eligibility_engine():
    # Eligible case
    payload = {
        "customer_id": 125,
        "annual_revenue": 10000000.0,
        "credit_score": 780,
        "requested_amount": 1000000.0
    }
    res = client.post("/ocen/eligibility", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["eligible"] is True
    assert data["max_eligible_amount"] == 3000000.0
    assert "ULI-" in data["uli_reference"]

    # Ineligible case - requested amount too high
    payload["requested_amount"] = 5000000.0
    res = client.post("/ocen/eligibility", json=payload)
    assert res.status_code == 200
    assert res.json()["eligible"] is False

def test_complete_loan_journey():
    # 1. Submit Application
    payload = {
        "customer_id": 125,
        "requested_amount": 500000.0,
        "requested_tenure_months": 12,
        "purpose": "Machinery purchase financing"
    }
    app_res = client.post("/ocen/apply", json=payload)
    assert app_res.status_code == 200
    app_data = app_res.json()
    assert app_data["status"] == "OFFERS_GENERATED"
    app_id = app_data["id"]
    
    # 2. Get Offers
    offers_res = client.get(f"/ocen/applications/{app_id}/offers")
    assert offers_res.status_code == 200
    offers = offers_res.json()
    assert len(offers) > 0
    offer_id = offers[0]["id"]
    
    # 3. Compare Offers
    comp_res = client.get(f"/ocen/offers/compare/{app_id}")
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    assert comp_data["best_rate_offer_id"] is not None
    
    # 4. Get AI Recommendations
    ai_res = client.get(f"/ocen/ai-advisor/{app_id}")
    assert ai_res.status_code == 200
    ai_data = ai_res.json()
    assert ai_data["suitability_score"] > 90.0
    assert ai_data["recommended_offer_id"] is not None
    
    # 5. Accept Offer
    accept_res = client.post("/ocen/offers/accept", json={"offer_id": offer_id})
    assert accept_res.status_code == 200
    assert accept_res.json()["status"] == "ACCEPTED"
    
    # 6. Disburse Loan
    disb_res = client.post(f"/ocen/disburse/{app_id}")
    assert disb_res.status_code == 200
    assert disb_res.json()["status"] == "DISBURSED"
    
    # 7. Check Audit Logs
    logs_res = client.get("/ocen/audit-logs")
    assert logs_res.status_code == 200
    logs = logs_res.json()
    assert any(log["event_type"] == "LOAN_DISBURSED" for log in logs)
