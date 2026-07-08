import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_customer_invalid_formats():
    # Attempt creation with invalid PAN and GSTIN formats
    payload = {
        "legal_name": "ABC Enterprises",
        "mobile_number": "12345", # Invalid mobile length
        "email": "invalid-email", # Invalid email format
        "pan": "INVALIDPAN", # Invalid characters
        "businesses": [
            {
                "trade_name": "ABC Trade",
                "gstin": "12345GSTIN", # Invalid GSTIN format
                "constitution_type": "Proprietorship",
                "annual_turnover": -50.0, # Turnover cannot be negative
                "industry_segment": "Manufacturing"
            }
        ],
        "addresses": [
            {
                "address_line1": "Road 1",
                "city": "Pune",
                "state": "MH",
                "pincode": "411" # Invalid pincode length
            }
        ]
    }
    
    response = client.post("/customers", json=payload)
    assert response.status_code == 422 # Unprocessable Entity due to validation rules

def test_create_customer_success():
    payload = {
        "legal_name": "Aditya Garments Private Limited",
        "mobile_number": "9000000001",
        "email": "aditya@garments.com",
        "pan": "ABCDE1234F",
        "businesses": [
            {
                "trade_name": "Aditya Weaving Mills",
                "gstin": "27ABCDE1234F1Z5",
                "cin": "U12345MH2020PTC123456",
                "constitution_type": "Private Limited",
                "annual_turnover": 45000000.0,
                "industry_segment": "Textiles",
                "directors": [
                    {
                        "full_name": "Aditya Patel",
                        "pan": "FGHIJ5678K",
                        "aadhaar_masked": "XXXXXXXX9876",
                        "mobile": "9999988888"
                    }
                ]
            }
        ],
        "addresses": [
            {
                "address_line1": "Plot 42, MIDC Industrial Area",
                "city": "Coimbatore",
                "state": "Tamil Nadu",
                "pincode": "641001",
                "address_type": "OFFICE"
            }
        ]
    }
    
    # 1. Post new customer
    response = client.post("/customers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["legal_name"] == "Aditya Garments Private Limited"
    assert data["pan"] == "ABCDE1234F"
    assert len(data["businesses"]) == 1
    assert data["businesses"][0]["trade_name"] == "Aditya Weaving Mills"
    
    customer_id = data["id"]
    
    # 2. Retrieve customer details
    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == 200
    assert get_response.json()["legal_name"] == "Aditya Garments Private Limited"
    
    # 3. Soft Delete customer
    delete_response = client.delete(f"/customers/{customer_id}")
    assert delete_response.status_code == 200
    
    # 4. Confirm deleted customer is no longer accessible
    get_deleted = client.get(f"/customers/{customer_id}")
    assert get_deleted.status_code == 404
