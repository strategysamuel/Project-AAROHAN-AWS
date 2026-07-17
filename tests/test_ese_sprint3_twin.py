import pytest
import os
import sys

# Adjust path to find ese-core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/ese-core")))

from scenario_comparator import ScenarioComparisonEngine
from report_generator import EnterpriseReportGenerator
from ai_assistant import AIAssistantEngine
from branding import brandingEngine

def test_scenario_comparison():
    comparator = ScenarioComparisonEngine()
    
    # Excellent vs Stress
    res = comparator.compare_scenarios("EXCELLENT_BORROWER", "CASH_FLOW_STRESS")
    assert "dscr" in res["metrics_comparison"]
    assert "credit_score" in res["metrics_comparison"]
    assert res["metrics_comparison"]["dscr"]["left"] == 2.1
    assert res["metrics_comparison"]["dscr"]["right"] == 0.85
    assert "Cash Flow Stress" in res["visual_explanations"]

    # Startup vs Manufacturing
    res_type = comparator.compare_scenarios("STARTUP", "MANUFACTURING")
    assert "business_age_months" in res_type["metrics_comparison"]
    assert res_type["metrics_comparison"]["business_age_months"]["left"] == 8
    assert res_type["metrics_comparison"]["business_age_months"]["right"] == 48

def test_report_generation():
    generator = EnterpriseReportGenerator()
    data = {"customer_id": 120, "score": 90, "status": "EXCELLENT", "value": "1,000,000"}
    
    # Markdown
    md = generator.generate_report("FHC", "MARKDOWN", data)
    assert b"# PROJECT AAROHAN - FHC REPORT" in md
    assert b"Customer ID: 120" in md

    # Excel
    xls = generator.generate_report("CAM", "EXCEL", data)
    assert b"Report Title,PROJECT AAROHAN - CAM REPORT" in xls
    assert b"Score,90,OK" in xls

    # PDF
    pdf = generator.generate_report("RISK", "PDF", data)
    assert pdf.startswith(b"%PDF-1.4")

def test_ai_presentation_assistant():
    assistant = AIAssistantEngine()
    
    # Approved Credit Decision
    narr_approve = assistant.generate_explanation("CREDIT_DECISION", {"credit_score": 750})
    assert "APPROVED" in narr_approve
    assert "750" in narr_approve

    # Rejected Credit Decision
    narr_reject = assistant.generate_explanation("CREDIT_DECISION", {"credit_score": 500})
    assert "REJECTED" in narr_reject
    assert "500" in narr_reject

    # Risk factors
    narr_risk = assistant.generate_explanation("RISK_FACTORS", {"dscr": 0.8})
    assert "High Risk Alert" in narr_risk

def test_branding_engine():
    engine = brandingEngine()
    
    # Default
    assert engine.get_brand()["theme"] == "dark"
    
    # Switch to IDBI
    engine.set_brand("IDBI")
    assert engine.get_brand()["theme"] == "glassmorphic-teal"
    
    # Switch to Hackathon
    engine.set_brand("HACKATHON")
    assert engine.get_brand()["theme"] == "cyberpunk-neon"
