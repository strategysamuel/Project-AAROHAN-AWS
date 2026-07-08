import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_cam_draft_edit_approval_flow():
    customer_id = 120
    
    # 1. Trigger initial generation
    gen_res = client.post(f"/cam/generate/{customer_id}")
    assert gen_res.status_code == 201
    gen_data = gen_res.json()
    assert gen_data["current_version"] == 1
    assert "SWOT Assessment:" in gen_data["swot_analysis"]
    
    cam_id = gen_data["id"]
    
    # 2. Put manual edit updates
    edit_payload = {
        "edited_by": "STAFF-COOPER-99",
        "change_summary": "Manual adjustment to risk indicators",
        "executive_summary": "Adjusted executive details showing strong collateral backup.",
        "business_profile": gen_data["business_profile"],
        "financial_analysis": gen_data["financial_analysis"],
        "swot_analysis": gen_data["swot_analysis"],
        "risk_assessment": "Adjusted Risk Assessment. Level: Minimal Risk.",
        "collateral_assessment": "Hypothecation of machinery valued at ₹65 Lakhs"
    }
    
    edit_res = client.put(f"/cam/{cam_id}", json=edit_payload)
    assert edit_res.status_code == 200
    edit_data = edit_res.json()
    assert edit_data["current_version"] == 2
    assert edit_data["collateral_assessment"] == "Hypothecation of machinery valued at ₹65 Lakhs"
    assert len(edit_data["versions"]) == 2
    
    # 3. Submit final approval
    app_payload = {
        "approver_id": "MANAGER-SMITH-88",
        "action": "APPROVED",
        "comments": "Reviewed financial and collateral records. Approved Working Capital enhancement."
    }
    app_res = client.post(f"/cam/{cam_id}/approve", json=app_payload)
    assert app_res.status_code == 200
    assert app_res.json()["status"] == "APPROVED"
    
    # 4. Export PDF
    exp_res = client.get(f"/cam/{cam_id}/export")
    assert exp_res.status_code == 200
    assert "download_url" in exp_res.json()
