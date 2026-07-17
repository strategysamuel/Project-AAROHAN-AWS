import os
from abc import ABC, abstractmethod
from typing import Dict, Any

class CKYCAdapter(ABC):
    @abstractmethod
    def fetch_record(self, pan: str) -> Dict[str, Any]:
        pass

class DemoDatasetAdapter(CKYCAdapter):
    def fetch_record(self, pan: str) -> Dict[str, Any]:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # Connect to the local shared database
        engine = create_engine("sqlite:///./aarohan_local.db")
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        try:
            # Query the ESE CKYC simulation table directly
            res = db.execute(
                "SELECT ckyc_number, full_name, dob, pan, kyc_status FROM ese_ckyc_records WHERE pan = :pan", 
                {"pan": pan}
            ).fetchone()
            if res:
                return {
                    "ckyc_number": res[0],
                    "full_name": res[1],
                    "dob": res[2],
                    "pan": res[3],
                    "kyc_status": res[4]
                }
        except Exception:
            pass
        finally:
            db.close()
            
        # Fallback default mock
        return {
            "ckyc_number": "30049281726354",
            "full_name": "Aditya Patel",
            "dob": "12-08-1988",
            "pan": pan,
            "kyc_status": "VERIFIED"
        }

class SandboxCKYCAdapter(CKYCAdapter):
    def fetch_record(self, pan: str) -> Dict[str, Any]:
        # Simulates Sandbox CKYC Endpoint
        return {
            "ckyc_number": "99998888777766",
            "full_name": "Sandbox MSME Customer",
            "dob": "01-01-1990",
            "pan": pan,
            "kyc_status": "VERIFIED_WITH_WARNING"
        }

class RealCKYCAdapter(CKYCAdapter):
    def fetch_record(self, pan: str) -> Dict[str, Any]:
        # Simulates Real Production CKYC Registry Endpoint
        return {
            "ckyc_number": "11112222333344",
            "full_name": "Real Registry Name",
            "dob": "15-05-1985",
            "pan": pan,
            "kyc_status": "VERIFIED"
        }

def get_ckyc_adapter() -> CKYCAdapter:
    profile = os.getenv("CKYC_ADAPTER_PROFILE", "DEMO_DATASET").upper()
    if profile == "REAL":
        return RealCKYCAdapter()
    elif profile == "SANDBOX":
        return SandboxCKYCAdapter()
    else:
        return DemoDatasetAdapter()
