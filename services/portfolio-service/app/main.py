import logging
import sys
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models import PortfolioSimulation
from app.schemas import PortfolioSimulationResponse, SimulationRequest
from app.database import get_db, init_db

# Configure JSON Logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "portfolio-service"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("portfolio-service")

# Initialize database schemas
init_db()

app = FastAPI(
    title="AAROHAN Strategic Portfolio Intelligence & Scenario Simulation Service",
    description="consented macro stress testing, regional concentration risk modeling, and Gemini risk advisors",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Correlation ID and auditing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    logger.info(f"AUDIT | Request: {request.method} {request.url.path} | Correlation ID: {correlation_id}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Correlation-ID"] = correlation_id
    
    logger.info(f"AUDIT | Completed: {request.method} {request.url.path} | Status: {response.status_code} | Process Time: {process_time:.4f}s")
    return response

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errorCode": f"AAR-ERR-{exc.status_code}",
            "message": exc.detail,
            "correlationId": correlation_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "details": []
        }
    )

# Strategic Risk Simulation Helper
def execute_macro_stress_simulation(payload: SimulationRequest) -> dict:
    base_val = 2450000000.0 # 245 Crores
    base_npa = 45000000.0 # 4.5 Crores
    base_fhc = 82.4
    
    # Mathematical stress formulas
    r_factor = payload.interest_rate_change
    i_factor = payload.inflation_change
    
    sim_val = base_val * (1.0 - (r_factor * 0.02) - (i_factor * 0.01))
    
    npa_multiplier = 1.0 + (r_factor * 0.15) + (i_factor * 0.10)
    if payload.sector_slowdown:
         npa_multiplier += 0.10
    sim_npa = base_npa * npa_multiplier
    
    sim_fhc = base_fhc - (r_factor * 0.8) - (i_factor * 0.5)
    
    # Gemini Strategic Portfolio Advisory
    advisory = (
        f"Gemini Portfolio Risk Advisory:\n"
        f"Under scenario '{payload.scenario_name}' (Interest Rate: +{r_factor}%, Inflation: +{i_factor}%), "
        f"expected portfolio volume is projected to shrink to ₹{(sim_val/10000000):.1f} Crores while default NPA "
        f"exposures rise to ₹{(sim_npa/10000000):.2f} Crores. "
        f"Strategic risk mitigation action: tighten current account debt service coverage rules for "
        f"{payload.sector_slowdown or 'general'} sectors to maintain average health scores above {sim_fhc:.1f}."
    )
    
    return {
        "portfolio_value": sim_val,
        "npa_exposure": sim_npa,
        "fhc_score": sim_fhc,
        "advisory": advisory
    }

# REST APIs

@app.post("/portfolio/simulate", response_model=PortfolioSimulationResponse, status_code=status.HTTP_201_CREATED)
async def simulate_scenario(payload: SimulationRequest, db: Session = Depends(get_db)):
    logger.info(f"AUDIT | Initiating strategic stress test simulation: {payload.scenario_name}")
    
    results = execute_macro_stress_simulation(payload)
    
    sim = PortfolioSimulation(
        scenario_name=payload.scenario_name,
        interest_rate_change=payload.interest_rate_change,
        inflation_change=payload.inflation_change,
        sector_slowdown=payload.sector_slowdown,
        expected_portfolio_value=results["portfolio_value"],
        expected_npa_exposure=results["npa_exposure"],
        average_fhc_score=results["fhc_score"],
        ai_advisor_text=results["advisory"]
    )
    db.add(sim)
    db.commit()
    db.refresh(sim)
    
    logger.info(f"AUDIT | Scenario simulation complete | ID: {sim.id} | Event: bank.aarohan.scenario.simulated")
    return sim

@app.get("/portfolio/simulations", response_model=List[PortfolioSimulationResponse])
async def list_simulations(db: Session = Depends(get_db)):
    return db.query(PortfolioSimulation).order_by(PortfolioSimulation.created_at.desc()).all()

@app.get("/livez")
async def livez():
    return {"status": "UP"}
