import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_establishment_validation_error():
    # Attempt sync with incorrect establishment ID format
    response = client.post("/epfo/sync/125", json={"establishment_id": "BADESTID"})
    assert response.status_code == 422 # Schema check trigger

def test_epfo_sync_and_retrieval():
    customer_id = 125
    establishment_id = "ABCDE1234567000" # Valid 15-char format
    
    # 1. Sync data
    sync_res = client.post(f"/epfo/sync/{customer_id}", json={"establishment_id": establishment_id})
    assert sync_res.status_code == 200
    data = sync_res.json()
    assert "Textiles" in data["establishment_name"] or "EPFO" in data["establishment_name"]
    assert data["number_of_employees"] > 0
    assert len(data["contributions"]) > 0
    
    # 2. Get profile
    profile_res = client.get(f"/epfo/profile/{customer_id}")
    assert profile_res.status_code == 200
    assert profile_res.json()["establishment_id"] == establishment_id
