import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_gst_validation_error():
    # Attempt sync with incorrect GSTIN format
    response = client.post("/gst/sync/42", json={"gstin": "INVALIDGSTIN"})
    assert response.status_code == 422 # Schema format validation check trigger

def test_gst_sync_and_analytics():
    customer_id = 99
    # 27ABCDE1234F1Z5 is a valid GSTIN format
    sync_response = client.post(
        f"/gst/sync/{customer_id}",
        json={"gstin": "27ABCDE1234F1Z5"}
    )
    assert sync_response.status_code == 200
    data = sync_response.json()
    assert data["customer_id"] == customer_id
    assert len(data["returns"]) > 0
    assert len(data["analytics"]) == 1
    
    # Verify calculated values in response
    analytics = data["analytics"][0]
    assert analytics["avg_monthly_turnover"] > 0
    assert analytics["compliance_score"] == 75.0
    assert analytics["filing_delay_score"] <= 100.0
    assert analytics["seasonality_index"] > 0.0
    
    # Query analytics directly
    query_response = client.get(f"/gst/analytics/{customer_id}")
    assert query_response.status_code == 200
    query_data = query_response.json()
    assert query_data["avg_monthly_turnover"] == analytics["avg_monthly_turnover"]
