import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sync_validation_error():
    # Attempt sync with incorrect PAN format
    response = client.post("/treds/sync/125", json={"seller_pan": "BADPAN"})
    assert response.status_code == 422 # Schema check trigger

def test_treds_sync_and_discounting():
    customer_id = 125
    seller_pan = "ABCDE1234F"
    
    # 1. Sync invoices
    sync_res = client.post(f"/treds/sync/{customer_id}", json={"seller_pan": seller_pan})
    assert sync_res.status_code == 200
    data = sync_res.json()
    assert len(data) == 2
    assert data[0]["invoice_number"] == "INV-2025-001"
    
    invoice_id = data[0]["id"]
    
    # 2. Get list
    list_res = client.get(f"/treds/invoices/{customer_id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 2
    
    # 3. Discount invoice
    disc_res = client.post(f"/treds/discount/{invoice_id}")
    assert disc_res.status_code == 200
    assert disc_res.json()["status"] == "DISCOUNTED"
