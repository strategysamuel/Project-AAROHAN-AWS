import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_validation_error():
    # Attempt search with incorrect PAN format
    response = client.post("/ckyc/search", json={"pan": "BADPAN"})
    assert response.status_code == 422 # Schema check trigger

def test_ckyc_search_and_verify():
    pan = "ABCDE1234F"
    customer_id = 125
    
    # 1. Search registry
    search_res = client.post("/ckyc/search", json={"pan": pan})
    assert search_res.status_code == 200
    data = search_res.json()
    assert data["ckyc_number"] == "30049281726354"
    assert data["pan"] == pan
    
    # 2. Trigger identity verification check
    ver_payload = {
        "customer_id": customer_id,
        "checked_by": "RM-KUMAR-99"
    }
    ver_res = client.post(f"/ckyc/verify/{customer_id}", json=ver_payload)
    assert ver_res.status_code == 200
    ver_data = ver_res.json()
    assert ver_data["match_confidence"] == 100.0
    assert ver_data["verification_status"] == "VERIFIED"
    
    # 3. Retrieve record details
    get_res = client.get(f"/ckyc/records/{customer_id}")
    assert get_res.status_code == 200
    assert get_res.json()["ckyc_number"] == "30049281726354"
