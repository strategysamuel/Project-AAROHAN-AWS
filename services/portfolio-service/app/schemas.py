from pydantic import BaseModel
import datetime
from typing import List, Optional

class SimulationRequest(BaseModel):
    scenario_name: str
    interest_rate_change: float = 0.0 # e.g. +1.5%
    inflation_change: float = 0.0 # e.g. +1.0%
    sector_slowdown: Optional[str] = None # e.g. "Textiles"

class PortfolioSimulationResponse(BaseModel):
    id: int
    scenario_name: str
    interest_rate_change: float
    inflation_change: float
    sector_slowdown: Optional[str]
    expected_portfolio_value: float
    expected_npa_exposure: float
    average_fhc_score: float
    ai_advisor_text: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
