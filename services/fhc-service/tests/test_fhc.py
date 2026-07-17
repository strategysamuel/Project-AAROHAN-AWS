import sys
import os
# Fix pythonpath shadowing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_card_calculation_and_history():
    customer_id = 110
    
    # 1. Trigger initial calculation
    calc_res = client.post(f"/fhc/calculate/{customer_id}")
    assert calc_res.status_code == 200
    calc_data = calc_res.json()
    
    # Verify overall score bounds and components
    assert 0.0 <= calc_data["overall_score"] <= 100.0
    assert calc_data["revenue_health_score"] == 88.0
    assert calc_data["compliance_score"] == 95.0
    assert "Strong compliance consistency" in calc_data["key_strengths"]
    
    # 2. Get health card details
    get_res = client.get(f"/fhc/{customer_id}")
    assert get_res.status_code == 200
    assert get_res.json()["overall_score"] == calc_data["overall_score"]
    
    # 3. Retrieve history logs
    hist_res = client.get(f"/fhc/history/{customer_id}")
    assert hist_res.status_code == 200
    assert len(hist_res.json()) >= 1
    assert hist_res.json()[0]["score_value"] == calc_data["overall_score"]
