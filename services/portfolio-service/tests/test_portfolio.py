import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_portfolio_macro_simulation():
    # 1. Post a macro stress simulation request
    payload = {
        "scenario_name": "Interest Rate Spike & Textile Slowdown",
        "interest_rate_change": 1.5,
        "inflation_change": 1.0,
        "sector_slowdown": "Textiles"
    }
    
    response = client.post("/portfolio/simulate", json=payload)
    assert response.status_code == 201
    data = response.json()
    
    assert data["scenario_name"] == "Interest Rate Spike & Textile Slowdown"
    assert data["expected_portfolio_value"] < 2450000000.0 # Volume should decline
    assert data["expected_npa_exposure"] > 45000000.0 # Default exposures should rise
    assert data["average_fhc_score"] < 82.4
    assert "Gemini Portfolio Risk Advisory:" in data["ai_advisor_text"]
    
    # 2. Get simulations history list
    list_res = client.get("/portfolio/simulations")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
    assert list_res.json()[0]["scenario_name"] == "Interest Rate Spike & Textile Slowdown"
