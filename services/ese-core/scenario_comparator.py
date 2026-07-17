import logging
from typing import Dict, Any

logger = logging.getLogger("ese-scenario-comparator")

class ScenarioComparisonEngine:
    @staticmethod
    def compare_scenarios(left_id: str, right_id: str) -> Dict[str, Any]:
        """
        Compare two simulation configurations or business profiles side-by-side.
        """
        left_id = left_id.upper()
        right_id = right_id.upper()
        
        comparison_data = {
            "left_id": left_id,
            "right_id": right_id,
            "metrics_comparison": {},
            "visual_explanations": ""
        }

        if "EXCELLENT_BORROWER" in left_id and "CASH_FLOW_STRESS" in right_id:
            comparison_data["metrics_comparison"] = {
                "dscr": {"left": 2.1, "right": 0.85, "diff": -1.25, "impact": "CRITICAL DEGRADATION"},
                "credit_score": {"left": 780, "right": 520, "diff": -260, "impact": "HIGH DEFAULT RISK"},
                "npa_status": {"left": "PERFORMING", "right": "SUBSTANDARD", "diff": "N/A", "impact": "PROVISIONS REQUIRED"},
                "approval_probability": {"left": "95%", "right": "12%", "diff": "-83%", "impact": "REJECTION RECOMMENDED"}
            }
            comparison_data["visual_explanations"] = (
                "Under 'Cash Flow Stress', the borrower exhibits high cash flow variance due to payment defaults. "
                "The DSCR drops below the critical 1.0 threshold (to 0.85), forcing the credit score down by 260 points. "
                "Lenders reject or demand high risk premiums."
            )
        elif "STARTUP" in left_id and "MANUFACTURING" in right_id:
            comparison_data["metrics_comparison"] = {
                "dscr": {"left": 1.2, "right": 1.75, "diff": 0.55, "impact": "HIGHER SERVICE CAPACITY"},
                "credit_score": {"left": 610, "right": 740, "diff": 130, "impact": "ESTABLISHED RUNTRACK"},
                "business_age_months": {"left": 8, "right": 48, "diff": 40, "impact": "LOWER MORTALITY RATE"},
                "collateral_coverage": {"left": "0%", "right": "120%", "diff": "120%", "impact": "SECURED RECOVERY"}
            }
            comparison_data["visual_explanations"] = (
                "The Manufacturing MSME possesses long operational history (48 months) and substantial asset coverage, "
                "supporting an elevated 740 credit score. In contrast, the Startup is in its launch phase (8 months) "
                "with minimal cash buffer and zero collateral, limiting approvals to FinTech lenders."
            )
        elif "CLEAN" in left_id and "BLACKLIST" in right_id:
            comparison_data["metrics_comparison"] = {
                "fraud_flag": {"left": "CLEAN", "right": "BLACKLISTED", "diff": "CRITICAL", "impact": "IMMEDIATE REJECTION"},
                "credit_score": {"left": 720, "right": 300, "diff": -420, "impact": "SYSTEM SUSPENSION"},
                "repayment_status": {"left": "REGULAR", "right": "SUSPENDED", "diff": "N/A", "impact": "LEGAL AUDIT"}
            }
            comparison_data["visual_explanations"] = (
                "A RBI Blacklisted status triggers security alerts across all API checkpoints. "
                "The Credit score drops to the minimum threshold of 300, suspending all active marketplace offers."
            )
        elif "PSB" in left_id and "NBFC" in right_id:
            comparison_data["metrics_comparison"] = {
                "minimum_score_req": {"left": 750, "right": 620, "diff": -130, "impact": "ACCESSIBLE TARGET"},
                "interest_rate": {"left": "8.5%", "right": "14.0%", "diff": "+5.5%", "impact": "HIGHER BORROWING COST"},
                "sla_days": {"left": 15.0, "right": 1.0, "diff": -14.0, "impact": "RAPID APPROVAL"}
            }
            comparison_data["visual_explanations"] = (
                "Public Sector Banks offer low interest rates (8.5%) but enforce conservative criteria (min score 750, 15 days SLA). "
                "NBFCs provide rapid, automated loan access (1 day SLA) with higher risk pricing (14.0%)."
            )
        else:
            comparison_data["metrics_comparison"] = {
                "comparison_status": {"left": "ACTIVE", "right": "ACTIVE", "diff": "None", "impact": "NEUTRAL"}
            }
            comparison_data["visual_explanations"] = "Neutral comparative profiles. No critical discrepancies detected."

        return comparison_data
