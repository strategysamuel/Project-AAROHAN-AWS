import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_discovery_invalid_mobile():
    # Attempt discovery with invalid mobile length
    response = client.post("/aa/discover/102", json={"customer_mobile": "123"})
    assert response.status_code == 422

def test_aa_full_flow():
    customer_id = 105
    # 1. Discover accounts
    disc_res = client.post(f"/aa/discover/{customer_id}", json={"customer_mobile": "9876543210"})
    assert disc_res.status_code == 200
    disc_data = disc_res.json()
    assert len(disc_data) == 2
    
    # 2. Link accounts
    link_payload = [
        {
            "account_ref_num": disc_data[0]["account_ref_num"],
            "bank_name": disc_data[0]["bank_name"],
            "account_type": disc_data[0]["account_type"],
            "masked_acc_num": disc_data[0]["masked_acc_num"]
        }
    ]
    
    link_res = client.post(f"/aa/link/{customer_id}", json=link_payload)
    assert link_res.status_code == 200
    
    # 3. Synchronize statements and calculate analytics
    sync_res = client.post(f"/aa/sync/{customer_id}", json={"consent_id": 42})
    assert sync_res.status_code == 200
    sync_data = sync_res.json()
    
    assert sync_data["total_inflow"] > 0
    assert sync_data["total_outflow"] > 0
    assert sync_data["net_cash_flow"] != 0.0
    
    # 4. Query cash flow metrics
    analytics_res = client.get(f"/aa/analytics/{customer_id}")
    assert analytics_res.status_code == 200
    assert analytics_res.json()["net_cash_flow"] == sync_data["net_cash_flow"]
