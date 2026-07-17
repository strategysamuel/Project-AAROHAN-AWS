import logging
from typing import Dict, Any

logger = logging.getLogger("ese-causal-model")

class MacroeconomicState:
    def __init__(self):
        self.repo_rate: float = 6.5       # %
        self.inflation: float = 5.0       # %
        self.exchange_rate: float = 83.5   # USD/INR
        self.fuel_price: float = 96.0     # INR/Ltr
        self.commodity_price_index: float = 100.0
        self.government_subsidies_active: bool = False
        self.monsoon_impact: str = "NORMAL" # "NORMAL", "DEFICIT", "EXCESS"
        self.sector_growth_rates: Dict[str, float] = {
            "Textiles": 5.0,
            "Retail": 8.0,
            "Agriculture": 3.0,
            "Logistics": 6.5,
            "Healthcare": 7.5,
            "Services": 9.0
        }

    def update(self, parameters: Dict[str, Any]):
        self.repo_rate = parameters.get("repo_rate", self.repo_rate)
        self.inflation = parameters.get("inflation", self.inflation)
        self.exchange_rate = parameters.get("exchange_rate", self.exchange_rate)
        self.fuel_price = parameters.get("fuel_price", self.fuel_price)
        self.commodity_price_index = parameters.get("commodity_price_index", self.commodity_price_index)
        self.government_subsidies_active = parameters.get("government_subsidies_active", self.government_subsidies_active)
        self.monsoon_impact = parameters.get("monsoon_impact", self.monsoon_impact).upper()
        if "sector_growth_rates" in parameters:
            self.sector_growth_rates.update(parameters["sector_growth_rates"])

class RegionalBankingProfile:
    def __init__(self, name: str, industry_mix: list, gst_behavior: str, risk_characteristics: str):
        self.name = name
        self.industry_mix = industry_mix
        self.gst_behavior = gst_behavior # "HIGH_COMPLIANCE", "MODERATE_COMPLIANCE", "VARYING"
        self.risk_characteristics = risk_characteristics

REGIONAL_PROFILES = {
    "Tamil Nadu": RegionalBankingProfile("Tamil Nadu", ["Textiles", "Manufacturing", "Automotive"], "HIGH_COMPLIANCE", "LOW_RISK"),
    "Karnataka": RegionalBankingProfile("Karnataka", ["Services", "FinTech", "AgroProcessing"], "HIGH_COMPLIANCE", "LOW_RISK"),
    "Maharashtra": RegionalBankingProfile("Maharashtra", ["Manufacturing", "Logistics", "Retail"], "HIGH_COMPLIANCE", "LOW_RISK"),
    "Gujarat": RegionalBankingProfile("Gujarat", ["Textiles", "Chemicals", "Manufacturing"], "HIGH_COMPLIANCE", "MODERATE_RISK"),
    "Telangana": RegionalBankingProfile("Telangana", ["Services", "Logistics", "Retail"], "MODERATE_COMPLIANCE", "MODERATE_RISK"),
    "Kerala": RegionalBankingProfile("Kerala", ["Tourism", "AgroProcessing", "Retail"], "MODERATE_COMPLIANCE", "LOW_RISK")
}

class FinancialCausalModel:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FinancialCausalModel, cls).__new__(cls, *args, **kwargs)
            cls._instance.macro_state = MacroeconomicState()
            cls._instance.active_region = "Maharashtra"
        return cls._instance

    def set_region(self, region_name: str):
        if region_name in REGIONAL_PROFILES:
            self.active_region = region_name
            logger.info(f"Active region set to: {region_name}")

    def get_macro_state(self) -> MacroeconomicState:
        return self.macro_state

    def calculate_fhc(self, ocf: float, interest: float = 50000.0, principal: float = 100000.0) -> Dict[str, Any]:
        # Macroeconomic factors influence costs
        cogs_inflation_factor = 1.0 + (self.macro_state.inflation - 5.0) * 0.015
        fuel_transport_factor = 1.0 + (self.macro_state.fuel_price - 96.0) * 0.005

        # Operating Cash Flow adjusted by macroeconomic factors
        adjusted_ocf = ocf / (cogs_inflation_factor * fuel_transport_factor)

        # Region specific adjustments
        region_profile = REGIONAL_PROFILES.get(self.active_region)
        if region_profile and region_profile.gst_behavior == "HIGH_COMPLIANCE":
            gst_compliance_score = 95.0
        else:
            gst_compliance_score = 80.0

        # DSCR calculation
        total_debt_service = principal + interest
        if total_debt_service <= 0:
            dscr = 3.0
        else:
            dscr = max(0.1, adjusted_ocf / total_debt_service)

        # Scores out of 100
        liquidity_score = min(100.0, max(20.0, 50.0 + dscr * 15.0))
        profitability_score = min(100.0, max(20.0, 75.0 - (self.macro_state.inflation - 5.0) * 2.0))
        leverage_score = min(100.0, max(20.0, 80.0 - (self.macro_state.repo_rate - 6.5) * 5.0))
        debt_service_score = min(100.0, max(10.0, dscr * 40.0))

        overall_score = (
            (liquidity_score * 0.30) +
            (profitability_score * 0.25) +
            (leverage_score * 0.25) +
            (debt_service_score * 0.20)
        )

        return {
            "overall_score": round(overall_score, 2),
            "liquidity_score": round(liquidity_score, 2),
            "profitability_score": round(profitability_score, 2),
            "leverage_score": round(leverage_score, 2),
            "debt_service_score": round(debt_service_score, 2),
            "dscr": round(dscr, 2),
            "gst_compliance_score": gst_compliance_score
        }

    def calculate_credit_score(self, fhc_score: float, fraud_alert: bool = False) -> int:
        if fraud_alert:
            return 300
        
        base_score = 300
        range_points = 600

        # regional risk modifier
        region_profile = REGIONAL_PROFILES.get(self.active_region)
        risk_modifier = 0.0
        if region_profile:
            if region_profile.risk_characteristics == "LOW_RISK":
                risk_modifier = 0.05
            elif region_profile.risk_characteristics == "HIGH_RISK":
                risk_modifier = -0.05

        fhc_ratio = fhc_score / 100.0
        # Calculate Credit Score
        score = base_score + range_points * (0.80 * fhc_ratio + 0.20 + risk_modifier)
        return int(min(900, max(300, score)))
