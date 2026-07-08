import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_executive_kpis_and_briefings():
    # 1. Fetch executive dashboard KPIs
    kpis_res = client.get("/exec/kpis")
    assert kpis_res.status_code == 200
    assert len(kpis_res.json()) >= 4
    
    # 2. Fetch Branch performance ranking lists
    branch_res = client.get("/exec/branches")
    assert branch_res.status_code == 200
    assert len(branch_res.json()) >= 3
    assert branch_res.json()[0]["loan_disbursed_amt"] >= branch_res.json()[1]["loan_disbursed_amt"]
    
    # 3. Call AI daily executive brief mock
    brief_res = client.get("/exec/briefing")
    assert brief_res.status_code == 200
    data = brief_res.json()
    assert "Total disbursed volume has reached ₹245 Crores" in data["summary_text"]
    assert len(data["risk_warnings"]) > 0
    assert len(data["strategic_recommendations"]) > 0
