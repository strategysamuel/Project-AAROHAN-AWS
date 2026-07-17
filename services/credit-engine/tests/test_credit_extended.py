import sys
import os
# Fix pythonpath shadowing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_credit_extended_flow():
    customer_id = 888
    
    # 1. Trigger initial evaluation
    eval_res = client.post(f"/credit/evaluate/{customer_id}")
    assert eval_res.status_code == 200
    eval_data = eval_res.json()
    assert eval_data["customer_id"] == customer_id
    assert "recommendation" in eval_data
    assert "eligible_loan_amount" in eval_data
    
    # 2. Get history
    hist_res = client.get(f"/credit/history/{customer_id}")
    assert hist_res.status_code == 200
    assert len(hist_res.json()) >= 1
    
    # 3. Get latest decision
    dec_res = client.get(f"/credit/decision/{customer_id}")
    assert dec_res.status_code == 200
    assert dec_res.json()["id"] == eval_data["id"]
    
    # 4. Get config
    cfg_res = client.get("/credit/config")
    assert cfg_res.status_code == 200
    cfg_data = cfg_res.json()
    assert cfg_data["active_adapter"] == "RULE_ENGINE"
    
    # 5. Switch to VERTEX_AI adapter
    cfg_data["active_adapter"] = "VERTEX_AI"
    up_res = client.post("/credit/config", json=cfg_data)
    assert up_res.status_code == 200
    
    # 6. Recalculate with VERTEX_AI adapter
    recalc_res = client.post(f"/credit/recalculate/{customer_id}")
    assert recalc_res.status_code == 200
    recalc_data = recalc_res.json()
    assert "Vertex AI" in recalc_data["ai_narrative"]
    
    # 7. Compare decisions
    comp_res = client.post("/credit/compare", json={
        "customer_ids": [customer_id, 115]
    })
    assert comp_res.status_code == 200
    assert len(comp_res.json()) >= 2
    
    # 8. Export JSON
    exp_json = client.get(f"/credit/export/{customer_id}?format=json")
    assert exp_json.status_code == 200
    assert "recommendation" in exp_json.json()
    
    # 9. Export PDF
    exp_pdf = client.get(f"/credit/export/{customer_id}?format=pdf")
    assert exp_pdf.status_code == 200
    assert exp_pdf.headers["content-type"] == "application/pdf"
    assert b"%PDF-1.4" in exp_pdf.content
