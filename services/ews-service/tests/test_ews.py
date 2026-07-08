import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ews_full_flow():
    customer_id = 125
    
    # 1. Trigger evaluation
    eval_res = client.post(f"/ews/evaluate/{customer_id}")
    assert eval_res.status_code == 200
    eval_data = eval_res.json()
    assert eval_data["status"] == "OPEN"
    assert "Gemini Early Warning Risk Report" in eval_data["ai_risk_narrative"]
    
    case_id = eval_data["id"]
    
    # 2. Get watchlist registry list
    watch_res = client.get("/ews/watchlist")
    assert watch_res.status_code == 200
    assert any(w["customer_id"] == customer_id for w in watch_res.json())
    
    # 3. Escalate risk case
    esc_payload = {
        "comments": "Escalating due to overlap of deposit drop with GSTR filing warning."
    }
    esc_res = client.post(f"/ews/cases/{case_id}/escalate", json=esc_payload)
    assert esc_res.status_code == 200
    assert esc_res.json()["status"] == "ESCALATED"
    assert "Escalated action:" in esc_res.json()["mitigation_action"]
