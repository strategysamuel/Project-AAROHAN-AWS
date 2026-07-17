import pytest
import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_consent_lifecycle():
    # 1. Create a pending consent request
    future_date = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30)).isoformat()
    payload = {
        "customer_id": 101,
        "provider_type": "ACCOUNT_AGGREGATOR",
        "purpose_code": "CREDIT_APPRAISAL",
        "valid_until": future_date
    }
    
    response = client.post("/consents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PENDING"
    assert data["provider_type"] == "ACCOUNT_AGGREGATOR"
    
    consent_id = data["id"]
    
    # 2. Approve the consent request
    sig_payload = {
        "signature_hash": "sha256-digital-signature-approval-verification-string-123"
    }
    app_response = client.post(f"/consents/{consent_id}/approve", json=sig_payload)
    assert app_response.status_code == 200
    app_data = app_response.json()
    assert app_data["status"] == "APPROVED"
    assert len(app_data["artifacts"]) == 1
    assert app_data["artifacts"][0]["signature_hash"] == sig_payload["signature_hash"]
    
    # 3. Revoke the approved consent
    rev_response = client.post(f"/consents/{consent_id}/revoke")
    assert rev_response.status_code == 200
    assert rev_response.json()["status"] == "REVOKED"
    
    # 4. Attempt to approve a revoked consent (should fail)
    fail_response = client.post(f"/consents/{consent_id}/approve", json=sig_payload)
    assert fail_response.status_code == 400
