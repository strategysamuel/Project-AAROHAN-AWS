import sys
import os
# Fix pythonpath shadowing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_credit_evaluation_and_human_approval():
    customer_id = 115
    
    # 1. Trigger AI Evaluation request
    eval_res = client.post(f"/credit/evaluate/{customer_id}")
    assert eval_res.status_code == 200
    eval_data = eval_res.json()
    
    assert eval_data["recommendation"] == "APPROVED"
    assert eval_data["confidence_score"] == 86.4
    assert "Gemini Credit Intelligence Report" in eval_data["ai_narrative"]
    assert eval_data["approval_status"] == "PENDING_HUMAN_REVIEW"
    
    decision_id = eval_data["id"]
    
    # 2. Submit human approval
    app_payload = {
        "approver_id": "RM-KUMAR-99",
        "action": "APPROVED",
        "comments": "GST returns verified and cash flows look solid. Sanctioning ₹50 Lakhs limit."
    }
    app_res = client.post(f"/credit/approve/{decision_id}", json=app_payload)
    assert app_res.status_code == 200
    app_data = app_res.json()
    assert app_data["approval_status"] == "APPROVED"
    assert len(app_data["approvals"]) == 1
    assert app_data["approvals"][0]["approver_id"] == "RM-KUMAR-99"
    
    # 3. Attempt duplicate sign-off (should fail)
    fail_res = client.post(f"/credit/approve/{decision_id}", json=app_payload)
    assert fail_res.status_code == 400
