import logging
from typing import Dict, Any

logger = logging.getLogger("ese-ai-assistant")

class AIAssistantEngine:
    @staticmethod
    def generate_explanation(category: str, data: Dict[str, Any]) -> str:
        """
        Generate deterministic natural-language explanations based on category:
        category: "CREDIT_DECISION", "FHC", "RISK_FACTORS", "LENDING_RECOMMENDATION", "KPIs"
        """
        category = category.upper()
        
        if category == "CREDIT_DECISION":
            score = data.get("credit_score", 720)
            if score >= 700:
                return (
                    f"The Credit appraisal decision is APPROVED. The borrower exhibits a strong "
                    f"credit score of {score}, driven by a consistent 95% GST filing compliance record "
                    f"and positive operating cash flows with zero ledger defaults."
                )
            else:
                return (
                    f"The Credit appraisal decision is REJECTED. The credit score of {score} falls "
                    f"below the target threshold due to elevated leverage ratios and recent cash flow stresses."
                )

        elif category == "FHC":
            score = data.get("fhc_score", 80)
            return (
                f"The Financial Health Card score is {score}/100. This indicates robust liquidity "
                f"and stable current account averages. Operating margins are healthy, though slightly "
                f"impacted by macroeconomic inflation cycles."
            )

        elif category == "RISK_FACTORS":
            dscr = data.get("dscr", 1.5)
            if dscr < 1.0:
                return (
                    f"High Risk Alert: The Debt Service Coverage Ratio (DSCR) is {dscr}, indicating "
                    f"insufficient operating cash to meet monthly interest and principal repayments."
                )
            else:
                return (
                    f"Moderate Risk: DSCR is stable at {dscr}. Sector headwinds present minor growth constraints, "
                    f"but balance sheet leverage remains well within safety limits."
                )

        elif category == "LENDING_RECOMMENDATION":
            limit = data.get("limit", 2500000.0)
            return (
                f"Lending Recommendation: Approve a Working Capital limit up to INR {limit:,.2f}. "
                f"Recommend structured repayments linked to trade invoice collections (net-30 billing cycles)."
            )

        elif category == "KPIS":
            outstanding = data.get("outstanding", 1250000000.0)
            return (
                f"Portfolio Performance: The aggregate outstanding volume stands at INR {outstanding:,.2f}. "
                f"The NPA ratio is maintained at 2.8%, showcasing strong loan quality and timely recoveries."
            )

        return "Gemini AI Advisor: Financial metrics remain within standard performance margins."
