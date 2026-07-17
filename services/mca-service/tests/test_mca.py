import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_cin_validation_error():
    # Attempt sync with incorrect CIN format
    response = client.post("/mca/sync/125", json={"cin": "BADCIN"})
    assert response.status_code == 422 # Schema check trigger

def test_mca_sync_and_retrieval():
    customer_id = 125
    cin = "U12345MH2020PTC123456" # Valid CIN format
    
    # 1. Sync data
    sync_res = client.post(f"/mca/sync/{customer_id}", json={"cin": cin})
    assert sync_res.status_code == 200
    data = sync_res.json()
    assert "Textiles" in data["company_name"] or "Production" in data["company_name"]
    assert len(data["directors"]) == 2
    assert len(data["charges"]) == 2
    assert len(data["filings"]) == 2
    
    # 2. Get profile
    profile_res = client.get(f"/mca/profile/{customer_id}")
    assert profile_res.status_code == 200
    assert profile_res.json()["cin"] == cin
