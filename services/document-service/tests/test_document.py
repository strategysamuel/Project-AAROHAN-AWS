import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_document_upload_and_delete():
    # 1. Create document metadata record
    payload = {
        "customer_id": 102,
        "document_type": "PAN",
        "file_name": "pan_card.pdf",
        "file_size_bytes": 150000,
        "content_type": "application/pdf",
        "storage_path": "gs://aarohan-documents/102/pan_card.pdf",
        "metadata_fields": [
            {"meta_key": "pan_number", "meta_value": "ABCDE1234F"},
            {"meta_key": "ocr_status", "meta_value": "SUCCESS"}
        ]
    }
    
    response = client.post("/documents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["file_name"] == "pan_card.pdf"
    assert len(data["metadata_fields"]) == 2
    
    doc_id = data["id"]
    
    # 2. Get document metadata
    get_res = client.get(f"/documents/{doc_id}")
    assert get_res.status_code == 200
    
    # 3. Soft Delete document
    del_res = client.delete(f"/documents/{doc_id}")
    assert del_res.status_code == 200
    
    # 4. Confirm document is hidden
    get_hidden = client.get(f"/documents/{doc_id}")
    assert get_hidden.status_code == 404

def test_digilocker_import():
    import_payload = {
        "customer_id": 102,
        "document_type": "AADHAAR",
        "digilocker_uri": "in.gov.uidai-adr-XXXXXXXX9999",
        "consent_id": 42
    }
    
    response = client.post("/documents/digilocker/import", json=import_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["source_origin"] == "DIGILOCKER"
    assert len(data["metadata_fields"]) == 3
    assert data["metadata_fields"][2]["meta_value"] == "in.gov.uidai-adr-XXXXXXXX9999"
