import sys
import os
# Fix pythonpath shadowing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_fhc_extended_lifecycle():
    customer_id = 999
    
    # 1. Trigger initial calculation
    calc_res = client.post(f"/fhc/calculate/{customer_id}")
    assert calc_res.status_code == 200
    calc_data = calc_res.json()
    assert calc_data["customer_id"] == customer_id
    assert "overall_score" in calc_data
    assert "rating" in calc_data
    assert "identity_score" in calc_data
    assert "compliance_score" in calc_data
    
    # 2. Get health card
    get_res = client.get(f"/fhc/{customer_id}")
    assert get_res.status_code == 200
    assert get_res.json()["overall_score"] == calc_data["overall_score"]
    
    # 3. Refresh health card
    ref_res = client.post(f"/fhc/refresh/{customer_id}")
    assert ref_res.status_code == 200
    
    # 4. Get config
    cfg_res = client.get("/fhc/config")
    assert cfg_res.status_code == 200
    cfg_data = cfg_res.json()
    assert "weights" in cfg_data
    assert "thresholds" in cfg_data
    
    # 5. Update config
    new_weights = dict(cfg_data["weights"])
    new_weights["identity_score"] = 0.20
    new_weights["compliance_score"] = 0.00 # reduce compliance to balance sum
    
    up_res = client.post("/fhc/config", json={
        "weights": new_weights,
        "thresholds": cfg_data["thresholds"]
    })
    assert up_res.status_code == 200
    
    # 6. Recalculate after config update
    recalc_res = client.post(f"/fhc/recalculate/{customer_id}")
    assert recalc_res.status_code == 200
    
    # 7. Override score
    override_res = client.post(f"/fhc/override/{customer_id}", json={
        "overridden_score": 92.5,
        "override_reason": "Audited premium client status",
        "overridden_by": "RM-102"
    })
    assert override_res.status_code == 200
    override_data = override_res.json()
    assert override_data["is_overridden"] is True
    assert override_data["overall_score"] == 92.5
    assert override_data["rating"] == "AAA" # 92.5 should map to AAA
    
    # 8. Compare health cards
    comp_res = client.post("/fhc/compare", json={
        "customer_ids": [customer_id, 110]
    })
    assert comp_res.status_code == 200
    assert len(comp_res.json()) >= 2
    
    # 9. Get trend analysis
    trend_res = client.get(f"/fhc/trend/{customer_id}?interval=monthly")
    assert trend_res.status_code == 200
    trend_data = trend_res.json()
    assert "history" in trend_data
    assert "trend_direction" in trend_data
    
    # 10. Export JSON
    exp_json = client.get(f"/fhc/export/{customer_id}?format=json")
    assert exp_json.status_code == 200
    assert exp_json.json()["overall_score"] == 92.5
    
    # 11. Export PDF
    exp_pdf = client.get(f"/fhc/export/{customer_id}?format=pdf")
    assert exp_pdf.status_code == 200
    assert exp_pdf.headers["content-type"] == "application/pdf"
    assert b"%PDF-1.4" in exp_pdf.content
