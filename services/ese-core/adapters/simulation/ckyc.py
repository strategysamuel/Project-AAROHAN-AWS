import time
import random
import sys
import os

# Bootstrap virtualenv
def bootstrap_virtualenv():
    import glob
    possible_paths = [
        "C:\\Users\\DELL\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\aarohan-backend-*\\Lib\\site-packages",
        "C:\\Users\\DELL\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\aarohan-backend-*\\lib\\site-packages"
    ]
    for pattern in possible_paths:
        for path in glob.glob(pattern):
            if path not in sys.path:
                sys.path.insert(0, path)

bootstrap_virtualenv()

# Import base classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from adapters.base import ExternalIntegrationAdapter, AdapterRequest, AdapterResponse
from adapter_factory import register_adapter, CKYC, DEMO, TRAINING, UAT, PERFORMANCE
from db_helper import get_sim_db_session
from models import ESECKYCRecord

@register_adapter(CKYC, DEMO)
@register_adapter(CKYC, TRAINING)
@register_adapter(CKYC, UAT)
@register_adapter(CKYC, PERFORMANCE)
class SimulationCKYCAdapter(ExternalIntegrationAdapter):
    """
    SimulationCKYCAdapter (Reference Implementation)
    
    DEVELOPER GUIDE FOR ADDING SIMULATION ADAPTERS:
    1. Inherit from ExternalIntegrationAdapter.
    2. Register your adapter using the @register_adapter(INTEGRATION_NAME, PROFILE) decorator.
    3. Implement fetch(self, request: AdapterRequest) -> AdapterResponse:
       - Connect to the ESE simulation database via get_sim_db_session().
       - Retrieve the target records (e.g. GST, AA, EPFO) matching request.customer_id.
       - Simulate latency if the active profile is DEMO or TRAINING.
       - Return a standard AdapterResponse with data, status code, and simulated=True.
    4. Implement health_check() -> bool.
    """

    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        active_profile = os.getenv("INTEGRATION_PROFILE", "DEMO").upper()
        
        # Simulate latency in DEMO or TRAINING profiles
        latency = 0.0
        if active_profile in (DEMO, TRAINING):
            latency = random.uniform(200.0, 400.0)
            time.sleep(latency / 1000.0)
            
        pan = request.params.get("pan")
        customer_id = request.customer_id
        
        db = get_sim_db_session()
        try:
            # Query the central CKYC simulation record
            record = None
            if pan:
                record = db.query(ESECKYCRecord).filter(ESECKYCRecord.pan == pan).first()
            elif customer_id:
                record = db.query(ESECKYCRecord).filter(ESECKYCRecord.customer_id == customer_id).first()
                
            if not record:
                # Fallback to defaults or return 404
                return AdapterResponse(
                    data={},
                    status_code=404,
                    simulated=True,
                    latency_ms=latency,
                    message=f"CKYC record not found for PAN: {pan} or Customer ID: {customer_id}"
                )
                
            response_data = {
                "kycId": record.ckyc_number,
                "name": record.full_name,
                "pan": record.pan,
                "aadhaar_masked": "XXXX-XXXX-1234",
                "dob": record.dob,
                "address": "123 MSME Road, City, State - 400001",
                "kyc_status": record.kyc_status
            }
            
            return AdapterResponse(
                data=response_data,
                status_code=200,
                simulated=True,
                latency_ms=latency
            )
        finally:
            db.close()

    def health_check(self) -> bool:
        db = get_sim_db_session()
        try:
            # Simply check table connectivity
            db.query(ESECKYCRecord).limit(1).all()
            return True
        except Exception:
            return False
        finally:
            db.close()
