import os
import sys
import json
import subprocess
import logging
import time
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware

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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "ese-admin-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ese-admin-service")

# Resolve paths
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
STATE_FILE_PATH = os.path.join(WORKSPACE_ROOT, "ese", "ese_active_state.json")

# Ensure ese folder exists
os.makedirs(os.path.join(WORKSPACE_ROOT, "ese"), exist_ok=True)

# Add ese-core to path
sys.path.append(os.path.join(WORKSPACE_ROOT, "services", "ese-core"))
from adapter_factory import AdapterFactory, SUPPORTED_PROFILES
from db_helper import get_active_dataset_path
from journey_engine import DemoJourneyEngine

# Import Sprint 2 Twin Modules
from clock import SimulationClock
from causal_model import FinancialCausalModel, REGIONAL_PROFILES
from event_engine import BusinessEventEngine
from lenders import BankingNetworkSimulator
from replay_engine import ExecutiveReplayEngine

# Import Sprint 3 Modules
from scenario_comparator import ScenarioComparisonEngine
from report_generator import EnterpriseReportGenerator
from ai_assistant import AIAssistantEngine
from branding import brandingEngine


app = FastAPI(
    title="Project AAROHAN Enterprise Simulation Control Center",
    description="Control panel and admin orchestrator for the Digital Banking Twin",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize state file helper
def get_state() -> Dict[str, Any]:
    if os.path.exists(STATE_FILE_PATH):
        try:
            with open(STATE_FILE_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    # Defaults
    default_state = {
        "active_profile": "DEMO",
        "active_dataset": "msme",
        "active_persona": "Priya Textile Works",
        "active_scenario": "EXCELLENT_BORROWER",
        "active_journey": "None",
        "last_journey_status": "None"
    }
    save_state(default_state)
    return default_state

def save_state(state: Dict[str, Any]):
    with open(STATE_FILE_PATH, "w") as f:
        json.dump(state, f, indent=2)

# Existing Endpoints

@app.get("/ese/control")
def get_control_settings():
    state = get_state()
    # Merge clock info
    clock = SimulationClock()
    state["simulated_date"] = clock.get_date_string()
    return state

@app.post("/ese/control/profile")
def set_active_profile(payload: Dict[str, str]):
    profile = payload.get("profile", "").upper()
    if profile not in SUPPORTED_PROFILES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid profile. Supported: {list(SUPPORTED_PROFILES)}"
        )
    state = get_state()
    state["active_profile"] = profile
    save_state(state)
    logger.info(f"AUDIT | Control Center | Active profile switched to {profile}")
    return {"status": "success", "active_profile": profile}

@app.post("/ese/control/persona")
def set_active_persona(payload: Dict[str, str]):
    persona = payload.get("persona", "")
    state = get_state()
    state["active_persona"] = persona
    save_state(state)
    logger.info(f"AUDIT | Control Center | Active persona switched to {persona}")
    return {"status": "success", "active_persona": persona}

@app.post("/ese/control/scenario")
def set_active_scenario(payload: Dict[str, str]):
    scenario = payload.get("scenario", "")
    state = get_state()
    state["active_scenario"] = scenario
    save_state(state)
    logger.info(f"AUDIT | Control Center | Active scenario switched to {scenario}")
    return {"status": "success", "active_scenario": scenario}

@app.post("/ese/control/dataset")
def set_active_dataset(payload: Dict[str, str]):
    dataset = payload.get("dataset", "").lower()
    # Check if dataset package exists in marketplace
    marketplace_dir = os.path.join(WORKSPACE_ROOT, "ese", "datasets", dataset)
    if not os.path.exists(marketplace_dir):
        os.makedirs(marketplace_dir, exist_ok=True)
    
    state = get_state()
    state["active_dataset"] = dataset
    save_state(state)
    logger.info(f"AUDIT | Control Center | Active dataset switched to {dataset}")
    return {"status": "success", "active_dataset": dataset}

# Sprint 2 Clock & Macro Simulation routes

@app.get("/ese/control/clock")
def get_clock_state():
    clock = SimulationClock()
    return {"simulated_date": clock.get_date_string()}

@app.post("/ese/control/clock/tick")
def tick_clock(payload: Dict[str, str]):
    interval = payload.get("interval", "day")
    clock = SimulationClock()
    try:
        new_date = clock.tick(interval)
        return {"status": "success", "simulated_date": new_date}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ese/control/clock/set")
def set_clock_date(payload: Dict[str, str]):
    date_str = payload.get("date", "")
    clock = SimulationClock()
    clock.set_date(date_str)
    return {"status": "success", "simulated_date": clock.get_date_string()}

@app.get("/ese/control/macro")
def get_macro_parameters():
    fcm = FinancialCausalModel()
    macro = fcm.get_macro_state()
    return {
        "repo_rate": macro.repo_rate,
        "inflation": macro.inflation,
        "exchange_rate": macro.exchange_rate,
        "fuel_price": macro.fuel_price,
        "commodity_price_index": macro.commodity_price_index,
        "government_subsidies_active": macro.government_subsidies_active,
        "monsoon_impact": macro.monsoon_impact,
        "sector_growth_rates": macro.sector_growth_rates
    }

@app.post("/ese/control/macro")
def update_macro_parameters(payload: Dict[str, Any]):
    fcm = FinancialCausalModel()
    macro = fcm.get_macro_state()
    macro.update(payload)
    return {"status": "success", "message": "Macroeconomic state updated."}

@app.post("/ese/control/region")
def set_region(payload: Dict[str, str]):
    region = payload.get("region", "Maharashtra")
    if region not in REGIONAL_PROFILES:
        raise HTTPException(status_code=400, detail=f"Unsupported region. Choose from: {list(REGIONAL_PROFILES.keys())}")
    fcm = FinancialCausalModel()
    fcm.set_region(region)
    return {"status": "success", "region": region}

# Events routes

@app.get("/ese/control/events")
def list_events():
    bee = BusinessEventEngine()
    return bee.get_history()

@app.post("/ese/control/event")
def post_event(payload: Dict[str, Any]):
    event_type = payload.get("event_type", "")
    persona_id = payload.get("persona_id", "per_unknown")
    event_payload = payload.get("payload", {})
    bee = BusinessEventEngine()
    res = bee.dispatch(event_type, persona_id, event_payload)
    return res

# Banking network and portfolio routes

@app.get("/ese/control/lenders")
def get_banking_network():
    simulator = BankingNetworkSimulator()
    lenders_info = {}
    for code, lender in simulator.lenders.items():
        lenders_info[code] = {
            "name": lender.name,
            "category": lender.category,
            "min_score": lender.min_score,
            "interest_rate": lender.interest_rate,
            "sla_days": lender.sla_days,
            "capital_allocated": lender.capital_allocated,
            "capital_deployed": lender.capital_deployed,
            "sector_concentration": lender.sector_concentration
        }
    return lenders_info

@app.get("/ese/control/analytics")
def get_portfolio_analytics():
    # Model high-fidelity portfolio evolution data
    simulator = BankingNetworkSimulator()
    outstanding = sum(l.capital_deployed for l in simulator.lenders.values())
    if outstanding == 0:
        # Seed mock outstanding data if fresh db
        outstanding = 1250000000.0 # 125 Crores baseline
        
    return {
        "portfolio_outstanding": outstanding,
        "npa_ratio": 2.8, # Simulated NPA ratio
        "recovery_ratio": 76.5,
        "sector_exposure": {
            "Textiles": 28.5,
            "Retail": 22.0,
            "Agriculture": 15.5,
            "Logistics": 18.0,
            "Healthcare": 16.0
        },
        "approval_rate": 84.2,
        "average_ticket_size": 2500000.0,
        "portfolio_profitability": 12.8,
        "district_wise_lending": {
            "Mumbai": 45.0,
            "Pune": 25.0,
            "Nashik": 15.0,
            "Nagpur": 15.0
        },
        "state_wise_lending": {
            "Maharashtra": 60.0,
            "Gujarat": 20.0,
            "Karnataka": 20.0
        },
        "women_led_business_lending_pct": 32.5
    }

# Replay routes

@app.get("/ese/control/replay")
def list_replays():
    engine = ExecutiveReplayEngine()
    return engine.list_recordings()

@app.post("/ese/control/replay/start")
def start_replay(payload: Dict[str, str]):
    journey_name = payload.get("journey_name", "Demo Journey")
    engine = ExecutiveReplayEngine()
    rec_id = engine.start_recording(journey_name)
    return {"status": "success", "recording_id": rec_id}

@app.post("/ese/control/replay/stop")
def stop_replay():
    engine = ExecutiveReplayEngine()
    res = engine.stop_recording()
    return {"status": "success", "recording": res}

@app.get("/ese/control/replay/{id}")
def get_replay_details(id: str):
    engine = ExecutiveReplayEngine()
    rec = engine.get_recording(id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recording not found")
    return rec

@app.get("/ese/control/replay/{id}/export")
def export_replay(id: str):
    engine = ExecutiveReplayEngine()
    summary = engine.export_summary(id)
    if summary == "No recording found.":
        raise HTTPException(status_code=404, detail=summary)
    return {"summary": summary}

# Journey orchestration execution endpoint

@app.post("/ese/control/journey")
def execute_demo_journey(payload: Dict[str, Any]):
    journey_name = payload.get("journey_name", "")
    customer_id = payload.get("customer_id", 120)
    
    # Track replay engine recording if active
    replay = ExecutiveReplayEngine()
    replay.log_step(f"Trigger Demo Journey: {journey_name}", {"customer_id": customer_id})

    engine = DemoJourneyEngine(mode="LOCAL")
    try:
        result = engine.run_journey(journey_name, customer_id=customer_id)
        state = get_state()
        state["active_journey"] = journey_name
        state["last_journey_status"] = result["status"]
        save_state(state)
        
        replay.log_step(f"Journey completed: {journey_name}", {"status": result["status"]})
        return result
    except Exception as e:
        replay.log_step(f"Journey failed: {journey_name}", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Journey execution failed: {str(e)}"
        )

@app.post("/ese/control/reset")
def reset_database(payload: Optional[Dict[str, Any]] = None):
    state = get_state()
    env = os.environ.copy()
    env["ACTIVE_DATASET"] = state["active_dataset"]
    
    seed_script = os.path.join(WORKSPACE_ROOT, "ese", "seed", "seed_all.py")
    
    logger.info(f"AUDIT | Control Center | DB reset initiated for dataset: {state['active_dataset']}")
    
    start_time = time.time()
    try:
        res = subprocess.run(
            [sys.executable, seed_script],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        duration = time.time() - start_time
        logger.info(f"AUDIT | Control Center | DB reset completed successfully in {duration:.2f}s")
        return {
            "status": "complete",
            "personas_seeded": 6,
            "duration_seconds": round(duration, 2),
            "log": res.stdout
        }
    except subprocess.CalledProcessError as e:
        logger.error(f"AUDIT | Control Center | DB reset failed: {e.stderr}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reset seeder script failed: {e.stderr}"
        )

@app.get("/ese/control/status")
def get_control_status():
    state = get_state()
    adapters = AdapterFactory.get_registered_adapters_status()
    db_path = get_active_dataset_path()
    
    manifest = {}
    manifest_path = os.path.join(os.path.dirname(db_path), "dataset_manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r") as mf:
                manifest = json.load(mf)
        except Exception:
            pass
            
    clock = SimulationClock()
    return {
        "status": "UP",
        "active_profile": state["active_profile"],
        "active_dataset": state["active_dataset"],
        "active_persona": state["active_persona"],
        "active_scenario": state["active_scenario"],
        "active_journey": state["active_journey"],
        "simulated_date": clock.get_date_string(),
        "db_path": db_path,
        "manifest": manifest,
        "adapters_loaded": len(adapters),
        "adapters": adapters
    }

@app.get("/ese/health")
def get_ese_health():
    state = get_state()
    adapters_status = AdapterFactory.get_registered_adapters_status()
    all_healthy = all(a["is_healthy"] for a in adapters_status)
    return {
        "ese_mode": state["active_profile"],
        "status": "healthy" if all_healthy else "unhealthy",
        "active_dataset": state["active_dataset"],
        "adapters_loaded": len(adapters_status)
    }

@app.get("/ese/datasets")
def get_ese_datasets():
    datasets_dir = os.path.join(WORKSPACE_ROOT, "ese", "datasets")
    if not os.path.exists(datasets_dir):
        return []
    return [d for d in os.listdir(datasets_dir) if os.path.isdir(os.path.join(datasets_dir, d))]

@app.get("/ese/profiles")
def get_ese_profiles():
    return list(SUPPORTED_PROFILES)

@app.get("/ese/scenarios")
def get_ese_scenarios():
    scenarios_dir = os.path.join(WORKSPACE_ROOT, "ese", "scenarios")
    if not os.path.exists(scenarios_dir):
        return []
    return [f.replace(".json", "") for f in os.listdir(scenarios_dir) if f.endswith(".json")]

@app.get("/ese/personas")
def get_ese_personas():
    personas_dir = os.path.join(WORKSPACE_ROOT, "ese", "personas")
    if not os.path.exists(personas_dir):
        return []
    return [f.replace(".json", "") for f in os.listdir(personas_dir) if f.endswith(".json")]

@app.get("/ese/adapters")
def get_ese_adapters():
    return AdapterFactory.get_registered_adapters_status()

# Sprint 3 Executive Demo, Reports & AI routes


@app.post("/ese/control/compare")
def compare_scenarios(payload: Dict[str, str]):
    left = payload.get("left_scenario", "")
    right = payload.get("right_scenario", "")
    res = ScenarioComparisonEngine.compare_scenarios(left, right)
    return res

@app.post("/ese/control/report")
def generate_report(payload: Dict[str, Any]):
    report_type = payload.get("report_type", "FHC")
    format_type = payload.get("format_type", "markdown")
    data = payload.get("data", {})
    res_bytes = EnterpriseReportGenerator.generate_report(report_type, format_type, data)
    # Return as base64 or string depending on format
    if format_type.upper() in ("PDF", "EXCEL"):
        import base64
        return {"report_type": report_type, "format": format_type, "content_b64": base64.b64encode(res_bytes).decode("utf-8")}
    return {"report_type": report_type, "format": format_type, "content": res_bytes.decode("utf-8")}

@app.post("/ese/control/narrate")
def narrate_metrics(payload: Dict[str, Any]):
    category = payload.get("category", "FHC")
    data = payload.get("data", {})
    explanation = AIAssistantEngine.generate_explanation(category, data)
    return {"category": category, "narration": explanation}

@app.get("/ese/control/branding")
def get_branding():
    engine = brandingEngine()
    return engine.get_brand()

@app.post("/ese/control/branding")
def set_branding(payload: Dict[str, str]):
    brand = payload.get("brand", "STANDARD")
    engine = brandingEngine()
    try:
        brand_info = engine.set_brand(brand)
        return {"status": "success", "brand": brand, "config": brand_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def get_health():
    state = get_state()
    return {
        "ese_mode": state["active_profile"],
        "adapters_loaded": len(AdapterFactory.get_registered_adapters_status())
    }

@app.get("/livez")
def livez():
    return {"status": "UP"}
