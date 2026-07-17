import pytest
import os
import sys

# Adjust path to find ese-core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/ese-core")))

from clock import SimulationClock
from causal_model import FinancialCausalModel, REGIONAL_PROFILES
from event_engine import BusinessEventEngine
from lenders import BankingNetworkSimulator
from replay_engine import ExecutiveReplayEngine

def test_simulation_clock():
    clock = SimulationClock()
    clock.set_date("2026-06-01")
    assert clock.get_date_string() == "2026-06-01"
    
    clock.tick("day")
    assert clock.get_date_string() == "2026-06-02"
    
    clock.tick("week")
    assert clock.get_date_string() == "2026-06-09"

def test_financial_causal_model():
    fcm = FinancialCausalModel()
    fcm.set_region("Tamil Nadu")
    
    # Excellent financial health
    res_good = fcm.calculate_fhc(ocf=1500000.0, interest=20000.0, principal=50000.0)
    assert res_good["overall_score"] > 80.0
    assert res_good["dscr"] > 2.0
    
    # Bad financial health
    res_bad = fcm.calculate_fhc(ocf=10000.0, interest=20000.0, principal=50000.0)
    assert res_bad["overall_score"] < 60.0
    assert res_bad["dscr"] < 1.0

    # Credit score computation
    cs_good = fcm.calculate_credit_score(res_good["overall_score"])
    cs_bad = fcm.calculate_credit_score(res_bad["overall_score"])
    assert cs_good > cs_bad
    
    # Fraud alert credit score degradation
    cs_fraud = fcm.calculate_credit_score(res_good["overall_score"], fraud_alert=True)
    assert cs_fraud == 300

def test_lenders_and_offers():
    simulator = BankingNetworkSimulator()
    
    # Excellent score gets public bank offer
    offers_good = simulator.generate_offers("per_good", credit_score=800, request_amount=500000.0)

    bank_names_good = [o["bank_name"] for o in offers_good]
    assert "State Bank of Simulation" in bank_names_good
    assert "InstantCredit FinTech" in bank_names_good
    
    # Poor score gets only fintech/high-risk offer
    offers_poor = simulator.generate_offers("per_poor", credit_score=590, request_amount=500000.0)
    bank_names_poor = [o["bank_name"] for o in offers_poor]
    assert "State Bank of Simulation" not in bank_names_poor
    assert "InstantCredit FinTech" in bank_names_poor

def test_event_engine_cascade():
    bee = BusinessEventEngine()
    bee.clear_history()
    
    # Dispatch initial GST return filed event
    bee.dispatch("GST_RETURN_FILED", "per_testile_001", {"reported_turnover": 5000000.0})
    
    history = bee.get_history()
    event_types = [e["event_type"] for e in history]
    
    # Verify cascade events were generated
    assert "GST_RETURN_FILED" in event_types
    assert "TURNOVER_UPDATED" in event_types
    assert "CASH_FLOW_UPDATED" in event_types
    assert "FHC_RECALCULATED" in event_types
    assert "CREDIT_SCORE_UPDATED" in event_types
    assert "OCEN_ELIGIBILITY_UPDATED" in event_types
    assert "LOAN_OFFERS_REGENERATED" in event_types
    assert "EXEC_DASHBOARD_REFRESHED" in event_types

def test_replay_engine():
    engine = ExecutiveReplayEngine()
    rec_id = engine.start_recording("Test Journey")
    
    engine.log_step("STEP_1", {"param": "value"})
    engine.log_event("TEST_EVENT", {"data": 123})
    engine.capture_portfolio_snapshot({"outstanding": 100000.0})
    
    rec = engine.stop_recording()
    assert rec["recording_id"] == rec_id
    assert len(rec["steps"]) == 1
    assert len(rec["events_captured"]) == 1
    assert len(rec["portfolio_snapshots"]) == 1
    
    summary = engine.export_summary(rec_id)
    assert "Test Journey" in summary
    assert "Steps Executed: 1" in summary
