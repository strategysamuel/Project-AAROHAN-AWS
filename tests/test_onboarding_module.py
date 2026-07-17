"""
Tests for the Enterprise Customer Onboarding Module.
AAR-BUILD-008 – Customer Onboarding
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/onboarding-service")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.models import Base
from app.database import get_db
from app.main import app

# ── In-memory DB with StaticPool ─────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Autouse fixture: apply override for this module only, clear on teardown ──
@pytest.fixture(scope="module", autouse=True)
def apply_db_override():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)   # restore for subsequent test files

client = TestClient(app)


# ============================================================
# Fixtures
# ============================================================

VALID_CUSTOMER = {
    "legal_name": "Test MSME Enterprise Ltd",
    "mobile_number": "9111222333",
    "email": "test@msmeltd.in",
    "pan": "TESTM0001A",
    "aadhaar_masked": "XXXXXXXX4321",
    "district": "Mumbai",
    "persona_name": None,
    "onboarding_status": "DRAFT",
    "businesses": [
        {
            "trade_name": "Test MSME Pvt Ltd",
            "gstin": "27TESTM0001A1Z9",
            "udyam_number": "UDYAM-MH-01-0099999",
            "cin": None,
            "constitution_type": "Private Limited",
            "annual_turnover": 12000000.0,
            "industry_segment": "Manufacturing",
            "business_vintage_years": 5,
            "employee_count": 45,
            "existing_banking": "SBI",
            "lifecycle_state": "REGISTERED",
            "directors": [
                {
                    "full_name": "Test Director",
                    "pan": "DIRTM0001B",
                    "aadhaar_masked": "XXXXXXXX7890",
                    "mobile": "9222333444"
                }
            ]
        }
    ],
    "addresses": [
        {
            "address_line1": "123 Enterprise Road",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400001",
            "address_type": "OFFICE"
        }
    ]
}


@pytest.fixture(scope="module")
def created_customer_id():
    res = client.post("/customers", json=VALID_CUSTOMER)
    assert res.status_code == 201, res.text
    return res.json()["id"]


# ============================================================
# 1. Customer Registration
# ============================================================

def test_register_customer():
    unique = dict(VALID_CUSTOMER)
    unique["mobile_number"] = "9555666777"
    unique["email"] = "unique@msmeltd2.in"
    unique["pan"] = "UNIQM0002C"
    unique["businesses"] = [dict(VALID_CUSTOMER["businesses"][0])]
    unique["businesses"][0]["gstin"] = "27UNIQM0002C1Z4"
    res = client.post("/customers", json=unique)
    assert res.status_code == 201
    data = res.json()
    assert data["legal_name"] == unique["legal_name"]
    assert data["aadhaar_masked"] == "XXXXXXXX4321"
    assert data["district"] == "Mumbai"


def test_customer_list():
    res = client.get("/customers")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_customer_get_by_id(created_customer_id):
    res = client.get(f"/customers/{created_customer_id}")
    assert res.status_code == 200
    assert res.json()["id"] == created_customer_id


# ============================================================
# 2. Business Registration Fields
# ============================================================

def test_business_udyam_field(created_customer_id):
    res = client.get(f"/customers/{created_customer_id}")
    businesses = res.json()["businesses"]
    assert len(businesses) == 1
    b = businesses[0]
    assert b["udyam_number"] == "UDYAM-MH-01-0099999"
    assert b["business_vintage_years"] == 5
    assert b["employee_count"] == 45
    assert b["existing_banking"] == "SBI"


# ============================================================
# 3. Validation
# ============================================================

def test_validate_valid_customer():
    payload = {
        "legal_name": "Valid Test Co",
        "mobile_number": "9100200300",
        "email": "valid@testco.in",
        "pan": "VALID0001X",
        "onboarding_status": "DRAFT"
    }
    res = client.post("/customers/validate", json=payload)
    assert res.status_code == 200
    data = res.json()
    pan_result = next(r for r in data["results"] if r["field"] == "pan")
    mobile_result = next(r for r in data["results"] if r["field"] == "mobile_number")
    assert pan_result["valid"] is True
    assert mobile_result["valid"] is True


def test_validate_invalid_pan():
    payload = {
        "legal_name": "Bad PAN Co",
        "mobile_number": "9100200300",
        "email": "bad@pan.in",
        "pan": "BADPAN",
        "onboarding_status": "DRAFT"
    }
    res = client.post("/customers/validate", json=payload)
    assert res.status_code == 200
    results = res.json()["results"]
    pan_result = next(r for r in results if r["field"] == "pan")
    assert pan_result["valid"] is False


def test_validate_invalid_mobile():
    payload = {
        "legal_name": "Bad Mobile Co",
        "mobile_number": "123",
        "email": "bad@mobile.in",
        "pan": "BMOBL0001Z",
        "onboarding_status": "DRAFT"
    }
    res = client.post("/customers/validate", json=payload)
    assert res.status_code == 200
    results = res.json()["results"]
    mob_result = next(r for r in results if r["field"] == "mobile_number")
    assert mob_result["valid"] is False


# ============================================================
# 4. Duplicate Detection
# ============================================================

def test_duplicate_pan_rejected():
    dup = dict(VALID_CUSTOMER)
    dup["mobile_number"] = "9888777666"
    dup["email"] = "dup@pan.in"
    # Same PAN as VALID_CUSTOMER – already registered
    res = client.post("/customers", json=dup)
    assert res.status_code == 409


def test_duplicate_detection_via_validate(created_customer_id):
    payload = {
        "legal_name": "Dup Check Co",
        "mobile_number": "9111222333",   # already registered
        "email": "dup2@test.in",
        "pan": "TESTM0001A",             # already registered
        "onboarding_status": "DRAFT"
    }
    res = client.post("/customers/validate", json=payload)
    assert res.status_code == 200
    results = res.json()["results"]
    dup_pan = next(r for r in results if r["field"] == "pan_duplicate")
    dup_mob = next(r for r in results if r["field"] == "mobile_duplicate")
    assert dup_pan["valid"] is False
    assert dup_mob["valid"] is False


# ============================================================
# 5. Persona Loading
# ============================================================

def test_load_persona_priya():
    res = client.post("/customers/load-persona", json={"persona_name": "Priya Textile Works"})
    assert res.status_code == 200
    p = res.json()["persona"]
    assert p["legal_name"] == "Priya Textile Works"
    assert p["business"]["gstin"] == "27SIMPT0001K1Z5"
    assert p["business"]["udyam_number"] == "UDYAM-GJ-05-0023456"
    assert p["business"]["business_vintage_years"] == 12


def test_load_persona_not_found():
    res = client.post("/customers/load-persona", json={"persona_name": "NonExistent Persona"})
    assert res.status_code == 404


# ============================================================
# 6. Document Upload
# ============================================================

def test_upload_document(created_customer_id):
    res = client.post(f"/customers/{created_customer_id}/documents", json={
        "doc_type": "PAN",
        "doc_name": "PAN_TESTM0001A.pdf",
        "source": "UPLOAD"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["doc_type"] == "PAN"
    assert data["status"] == "PENDING"


def test_upload_document_from_dataset(created_customer_id):
    res = client.post(f"/customers/{created_customer_id}/documents", json={
        "doc_type": "BANK_STMT",
        "doc_name": "Bank_Statement_6M.csv",
        "source": "SIMULATION_DATASET"
    })
    assert res.status_code == 201
    assert res.json()["source"] == "SIMULATION_DATASET"


def test_list_documents(created_customer_id):
    res = client.get(f"/customers/{created_customer_id}/documents")
    assert res.status_code == 200
    docs = res.json()
    assert len(docs) >= 2


# ============================================================
# 7. Workflow Trigger + Event Publishing
# ============================================================

def test_start_workflow(created_customer_id):
    res = client.post(f"/customers/{created_customer_id}/start-workflow")
    assert res.status_code == 200
    data = res.json()
    assert data["template_name"] == "MSME Lending Journey"
    assert data["status"] == "STARTED"
    assert "Customer Registered" in data["events_published"]
    assert "Business Registered" in data["events_published"]
    assert "Workflow Started" in data["events_published"]
    assert data["workflow_id"].startswith("wf_")


def test_workflow_id_persisted(created_customer_id):
    # Trigger workflow first (may already be triggered)
    client.post(f"/customers/{created_customer_id}/start-workflow")
    res = client.get(f"/customers/{created_customer_id}")
    assert res.status_code == 200
    assert res.json()["onboarding_status"] == "SUBMITTED"
    assert res.json()["workflow_id"].startswith("wf_")


# ============================================================
# 8. Admin – Update & Soft Delete
# ============================================================

def test_update_customer(created_customer_id):
    res = client.put(f"/customers/{created_customer_id}", json={
        "legal_name": "Test MSME Enterprise Ltd (Updated)",
        "mobile_number": "9111222333",
        "email": "test@msmeltd.in",
        "pan": "TESTM0001A",
        "onboarding_status": "ACTIVE"
    })
    assert res.status_code == 200
    assert "Updated" in res.json()["legal_name"]


def test_delete_customer():
    # Register temp customer then delete
    temp = dict(VALID_CUSTOMER)
    temp["mobile_number"] = "9700800900"
    temp["email"] = "temp@delete.in"
    temp["pan"] = "TEMPM0099Z"
    temp["businesses"] = [dict(VALID_CUSTOMER["businesses"][0])]
    temp["businesses"][0]["gstin"] = "27TEMPM0099Z1Z7"
    create_res = client.post("/customers", json=temp)
    assert create_res.status_code == 201
    cid = create_res.json()["id"]
    del_res = client.delete(f"/customers/{cid}")
    assert del_res.status_code == 200
    get_res = client.get(f"/customers/{cid}")
    assert get_res.status_code == 404


# ============================================================
# 9. Search
# ============================================================

def test_search_by_name():
    res = client.get("/customers?search=Test+MSME")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
