import logging
from typing import List, Dict, Any

logger = logging.getLogger("ese-lenders")

class Lender:
    def __init__(self, name: str, category: str, min_score: int, interest_rate: float, sla_days: float, max_ticket_size: float):
        self.name = name
        self.category = category
        self.min_score = min_score
        self.interest_rate = interest_rate
        self.sla_days = sla_days
        self.max_ticket_size = max_ticket_size
        self.capital_allocated = 500000000.0 # 50 Crores
        self.capital_deployed = 0.0
        self.sector_concentration: Dict[str, float] = {}

    def can_approve(self, credit_score: int, request_amount: float, sector: str) -> bool:
        if credit_score < self.min_score:
            return False
        if request_amount > self.max_ticket_size:
            return False
        # Check concentration limit (e.g. max 30% in any sector)
        current_sector_ratio = self.sector_concentration.get(sector, 0.0)
        if current_sector_ratio > 0.30:
            return False
        return True

    def deploy_capital(self, amount: float, sector: str):
        self.capital_deployed += amount
        # Update sector concentration
        current_sector_volume = self.sector_concentration.get(sector, 0.0) * self.capital_deployed
        new_sector_volume = current_sector_volume + amount
        for s in self.sector_concentration:
            # Recompute ratios
            self.sector_concentration[s] = (self.sector_concentration[s] * (self.capital_deployed - amount)) / self.capital_deployed
        self.sector_concentration[sector] = new_sector_volume / self.capital_deployed

class BankingNetworkSimulator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BankingNetworkSimulator, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_network()
        return cls._instance

    def _init_network(self):
        self.lenders: Dict[str, Lender] = {
            "PSB": Lender("State Bank of Simulation", "Public Sector Bank", 750, 8.5, 15.0, 10000000.0),
            "PVT": Lender("Dynamic Finance Bank", "Private Bank", 700, 10.5, 3.0, 5000000.0),
            "NBFC": Lender("Capital Growth NBFC", "NBFC", 620, 14.0, 1.0, 2000000.0),
            "FINTECH": Lender("InstantCredit FinTech", "FinTech", 580, 16.0, 0.1, 1000000.0),
            "COOPERATIVE": Lender("Cooperative Agro Trust", "Cooperative Bank", 600, 11.0, 5.0, 500000.0)
        }

    def generate_offers(self, persona_id: str, credit_score: int, request_amount: float = 1000000.0, sector: str = "Retail") -> List[Dict[str, Any]]:
        offers = []
        for code, lender in self.lenders.items():
            if lender.can_approve(credit_score, request_amount, sector):
                # Calculate risk-adjusted interest rate
                risk_premium = 0.0
                if credit_score < 650:
                    risk_premium = 2.5
                elif credit_score < 750:
                    risk_premium = 1.0
                
                final_rate = lender.interest_rate + risk_premium
                offers.append({
                    "id": f"OFFER-{code}-{persona_id[:5].upper()}",
                    "bank_name": lender.name,
                    "category": lender.category,
                    "interest_rate": round(final_rate, 2),
                    "tenure_months": 12,
                    "sla_days": lender.sla_days,
                    "approved_amount": request_amount
                })
        return offers
