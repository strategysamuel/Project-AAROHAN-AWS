import datetime
import logging
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Password Hash Context
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT Sign Parameters (Injectable via Secret Manager in production)
SECRET_KEY = "aarohan-secure-encryption-key-for-local-development"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
logger = logging.getLogger("auth-service")

class TokenData(BaseModel):
    user_id: int
    mobile_number: str
    role: str
    permissions: List[str]

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int, mobile_number: str, role: str, permissions: List[str]) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(user_id),
        "mobile": mobile_number,
        "role": role,
        "permissions": permissions,
        "exp": expire
      }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        mobile: str = payload.get("mobile")
        role: str = payload.get("role")
        permissions: List[str] = payload.get("permissions", [])
        
        if user_id is None or mobile is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token validation failed: missing claims."
            )
        return TokenData(user_id=int(user_id), mobile_number=mobile, role=role, permissions=permissions)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or token invalid."
        )

# Dependency injection validator to check active permissions
class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, token: str = Depends(oauth2_scheme)) -> TokenData:
        token_data = verify_access_token(token)
        if self.required_permission not in token_data.permissions:
            logger.warning(f"Access Denied: User {token_data.user_id} lacks permission {self.required_permission}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access permissions for this action."
            )
        return token_data
