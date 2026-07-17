import pytest
import os
import json
import sys
import importlib.util
from fastapi.testclient import TestClient

# Ensure ACTIVE_DATASET is set to msme for tests
os.environ["ACTIVE_DATASET"] = "msme"

# Adjust path to find ese-core and seeders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/ese-core")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ese/seed")))

# Programmatic seeder execution to ensure fresh data in any test runner environment
try:
    import seed_all
    seed_all.main()
except Exception as e:
    print(f"Test seeder bootstrap warning: {e}")

from adapter_factory import AdapterFactory, CKYC, VERTEX_AI, DEMO, PRODUCTION
from adapters.base import AdapterRequest
from journey_engine import DemoJourneyEngine

def load_app(service_name: str):
    file_path = os.path.abspath(f"services/{service_name}/app/main.py")
    module_name = f"dynamic_{service_name.replace('-', '_')}"
    
    # Clear sys.modules cache for 'app' to prevent crossover imports
    for k in list(sys.modules.keys()):
        if k == "app" or k.startswith("app."):
            sys.modules.pop(k, None)
            
    if module_name in sys.modules:
        return sys.modules[module_name].app
        
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    
    service_path = os.path.abspath(f"services/{service_name}")
    sys.path.insert(0, service_path)
    try:
        spec.loader.exec_module(module)
        return module.app
    finally:
        if service_path in sys.path:
            sys.path.remove(service_path)

def test_active_profile_detection():
    profile = AdapterFactory.get_active_profile()
    assert profile in {"DEMO", "TRAINING", "UAT", "PERFORMANCE", "PRODUCTION"}

def test_adapter_registry_lookup():
    if AdapterFactory.get_active_profile() != "PRODUCTION":
        adapter = AdapterFactory.get_adapter(CKYC)
        assert adapter.__class__.__name__ == "SimulationCKYCAdapter"
        assert adapter.health_check() is True

def test_ckyc_fetch_simulation():
    # Clean up conflicting local DB record with customer_id=125 or target PAN to prevent unique constraint failure
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine("sqlite:///./aarohan_local.db")
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM ckyc_records WHERE customer_id = 125 OR pan = 'SIMPT0001K'"))
            conn.commit()
    except Exception as e:
        print(f"Conflicting record cleanup warning: {e}")

    ckyc_app = load_app("ckyc-service")
    client = TestClient(ckyc_app)
    
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    state_file = os.path.join(workspace_root, "ese", "ese_active_state.json")
    
    original_state = {}
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            original_state = json.load(f)
            
    # Set to DEMO
    with open(state_file, "w") as f:
        json.dump({"active_profile": "DEMO"}, f)
        
    try:
        res = client.post("/ckyc/search", json={"pan": "SIMPT0001K"})
        assert res.status_code == 200, f"CKYC search failed. Status: {res.status_code}, Body: {res.text}"
        data = res.json()
        assert data["pan"] == "SIMPT0001K"
        assert data["full_name"] == "Priya Textile Works"
        assert data["kyc_status"] == "CLEAN"
    finally:
        if original_state:
            with open(state_file, "w") as f:
                json.dump(original_state, f)

def test_demo_journey_engine():
    engine = DemoJourneyEngine(mode="LOCAL")
    
    # Onboarding
    res1 = engine.run_journey("Customer Onboarding", customer_id=120)
    assert res1["status"] == "SUCCESS"
    
    # Financial Health Card
    res2 = engine.run_journey("Financial Health Card", customer_id=120)
    assert res2["status"] == "SUCCESS"

def test_admin_api_endpoints():
    admin_app = load_app("ese-admin-service")
    client = TestClient(admin_app)
    
    res = client.get("/ese/health")
    assert res.status_code == 200
    assert "ese_mode" in res.json()
    
    res = client.get("/ese/control/status")
    assert res.status_code == 200
    assert res.json()["status"] == "UP"
