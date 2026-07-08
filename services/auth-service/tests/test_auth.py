import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import hash_password, verify_password, create_access_token, verify_access_token

client = TestClient(app)

def test_password_hashing():
    raw_pass = "SecurePass123!"
    hashed = hash_password(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPass", hashed) is False

def test_jwt_token_flow():
    user_id = 42
    mobile = "9876543210"
    role = "RELATIONSHIP_MANAGER"
    permissions = ["loan:read", "loan:create"]
    
    token = create_access_token(user_id, mobile, role, permissions)
    assert isinstance(token, str)
    
    data = verify_access_token(token)
    assert data.user_id == user_id
    assert data.mobile_number == mobile
    assert data.role == role
    assert "loan:read" in data.permissions
    assert "loan:create" in data.permissions

def test_login_success():
    # Rajesh RM Kumar matches mobile_number 9876543210 and password AarohanPass123! from seeder
    response = client.post(
        "/auth/login",
        json={"mobile_number": "9876543210", "password": "AarohanPass123!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["role"] == "RELATIONSHIP_MANAGER"

def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={"mobile_number": "9876543210", "password": "WrongPassword!"}
    )
    assert response.status_code == 401
    assert "errorCode" in response.json()
