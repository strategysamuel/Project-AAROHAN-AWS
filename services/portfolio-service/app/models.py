from services.shared.database import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship


class PortfolioSimulation(Base):
    __tablename__ = "portfolio_simulations"
    __table_args__ = {'extend_existing': True}
        
    id = Column(Integer, primary_key=True, index=True)
    scenario_name = Column(String(100), nullable=False)
    interest_rate_change = Column(Float, default=0.0)
    inflation_change = Column(Float, default=0.0)
    sector_slowdown = Column(String(50), nullable=True) # e.g. "Textiles", "Automotive"
    
    # Expected Impacts
    expected_portfolio_value = Column(Float, default=0.0)
    expected_npa_exposure = Column(Float, default=0.0)
    average_fhc_score = Column(Float, default=0.0)
    
    ai_advisor_text = Column(String(1000), nullable=False) # Gemini generated advisory note
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
