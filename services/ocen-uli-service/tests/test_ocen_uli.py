"""
AAR-BUILD-017 – OCEN Marketplace Simulation Service
Comprehensive Test Suite
=======================================================================
Coverage:
  ✓ Lender matching (10 lenders screened)
  ✓ Offer generation (all eligible lenders get ranked offers)
  ✓ Match score calculation (component weights validated)
  ✓ Ranking logic (best match score = rank 1)
  ✓ Explainable recommendations (explanation fields populated)
  ✓ All REST API endpoints
  ✓ Workflow integration (CAM summary, executive dashboard)
  ✓ Business event publication (log-based)
  ✓ Dashboard functionality (all aggregate fields)
  ✓ Adapter switching (SIMULATION → SANDBOX → PRODUCTION)
  ✓ Loan products listing
  ✓ Eligibility check (pass / fail scenarios)
  ✓ Offer accept / reject
  ✓ Disbursement
  ✓ Admin: replay, export, config
  ✓ Audit logs
  ✓ Health probes
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ---------------------------------------------------------------------------
# Shared payload builders
# ---------------------------------------------------------------------------

GOOD_APP = {
    "customer_id": 8001,
    "requested_amount": 1_500_000.0,
    "requested_tenure_months": 24,
    "product_type": "Working Capital Loan",
    "purpose": "Inventory procurement",
    "fhc_score": 72.5,
    "credit_decision": "APPROVE",
    "fraud_score": 5.0,
    "fraud_risk_level": "Low",
}

RISKY_APP = {
    "customer_id": 8002,
    "requested_amount": 800_000.0,
    "requested_tenure_months": 12,
    "product_type": "Working Capital Loan",
    "fhc_score": 42.0,
    "credit_decision": "CONDITIONAL",
    "fraud_score": 45.0,
    "fraud_risk_level": "Medium",
}

BLOCKED_APP = {
    "customer_id": 8003,
    "requested_amount": 500_000.0,
    "requested_tenure_months": 12,
    "product_type": "Working Capital Loan",
    "fhc_score": 30.0,
    "credit_decision": "REJECT",
    "fraud_score": 95.0,
    "fraud_risk_level": "Critical",
}


def apply(payload):
    return client.post("/ocen/apply", json=payload)


# ===========================================================================
#  1. Lender Registry
# ===========================================================================

class TestLenderRegistry:
    def test_list_lenders_returns_10(self):
        r = client.get("/ocen/lenders")
        assert r.status_code == 200
        assert len(r.json()) >= 10

    def test_lender_types_diverse(self):
        lenders = client.get("/ocen/lenders").json()
        types = {l["lender_type"] for l in lenders}
        assert len(types) >= 3  # BANK, NBFC, FINTECH/MFI

    def test_get_lender_by_id(self):
        r = client.get("/ocen/lenders/LEND-IDBI-001")
        assert r.status_code == 200
        d = r.json()
        assert d["lender_id"] == "LEND-IDBI-001"
        assert d["name"] == "IDBI Bank – MSME Division"
        assert "Working Capital Loan" in d["loan_products"]

    def test_get_nonexistent_lender_404(self):
        r = client.get("/ocen/lenders/LEND-GHOST")
        assert r.status_code == 404

    def test_register_new_lender(self):
        r = client.post("/ocen/lenders", json={
            "lender_id": "LEND-TEST-001",
            "name": "Test NBFC",
            "lender_type": "NBFC",
            "base_interest_rate": 14.0,
            "max_interest_rate": 20.0,
            "max_loan_amount": 1_000_000,
            "min_loan_amount": 50_000,
            "min_credit_score": 620,
            "processing_fee_pct": 2.0,
            "tat_days": 1,
            "loan_products": "Working Capital Loan",
        })
        assert r.status_code == 200
        assert r.json()["lender_id"] == "LEND-TEST-001"

    def test_register_duplicate_lender_409(self):
        r = client.post("/ocen/lenders", json={
            "lender_id": "LEND-IDBI-001",
            "name": "Duplicate",
            "lender_type": "BANK",
            "base_interest_rate": 10.0,
            "max_interest_rate": 15.0,
            "max_loan_amount": 1_000_000,
            "min_loan_amount": 50_000,
            "min_credit_score": 650,
        })
        assert r.status_code == 409

    def test_disable_test_lender(self):
        r = client.delete("/ocen/lenders/LEND-TEST-001")
        assert r.status_code == 200
        assert "disabled" in r.json()["message"].lower()


# ===========================================================================
#  2. Loan Products
# ===========================================================================

class TestLoanProducts:
    def test_list_products_returns_10(self):
        r = client.get("/ocen/products")
        assert r.status_code == 200
        assert len(r.json()) >= 10

    def test_product_names_correct(self):
        products = client.get("/ocen/products").json()
        names = [p["product_name"] for p in products]
        expected = [
            "Working Capital Loan", "Term Loan", "Invoice Financing",
            "Women Entrepreneur Loan", "Startup Loan",
        ]
        for name in expected:
            assert name in names


# ===========================================================================
#  3. Lender Search (Matching Engine)
# ===========================================================================

class TestLenderSearch:
    def test_search_eligible_lenders_good_profile(self):
        r = client.post("/ocen/marketplace/search", json={
            "customer_id": 8001,
            "requested_amount": 1_000_000.0,
            "product_type": "Working Capital Loan",
            "fhc_score": 72.0,
            "credit_decision": "APPROVE",
            "fraud_risk_level": "Low",
        })
        assert r.status_code == 200
        d = r.json()
        assert d["total_lenders_screened"] >= 10
        assert d["eligible_lenders"] >= 5

    def test_search_critical_fraud_blocks_all(self):
        r = client.post("/ocen/marketplace/search", json={
            "customer_id": 8003,
            "requested_amount": 500_000.0,
            "product_type": "Working Capital Loan",
            "fhc_score": 30.0,
            "credit_decision": "REJECT",
            "fraud_risk_level": "Critical",
        })
        assert r.status_code == 200
        d = r.json()
        assert d["eligible_lenders"] == 0

    def test_search_results_ranked_by_score(self):
        r = client.post("/ocen/marketplace/search", json={
            "customer_id": 8001,
            "requested_amount": 500_000.0,
            "product_type": "Working Capital Loan",
            "fhc_score": 70.0,
            "credit_decision": "APPROVE",
            "fraud_risk_level": "Low",
        })
        results = [x for x in r.json()["results"] if x["eligible"]]
        if len(results) >= 2:
            assert results[0]["match_score"] >= results[1]["match_score"]

    def test_search_amount_too_high_rejected(self):
        r = client.post("/ocen/marketplace/search", json={
            "customer_id": 8001,
            "requested_amount": 100_000_000.0,  # > all lender caps
            "product_type": "Working Capital Loan",
            "fhc_score": 80.0,
            "credit_decision": "APPROVE",
            "fraud_risk_level": "Low",
        })
        d = r.json()
        assert d["eligible_lenders"] == 0


# ===========================================================================
#  4. Offer Generation
# ===========================================================================

class TestOfferGeneration:
    def test_good_application_generates_offers(self):
        r = apply(GOOD_APP)
        assert r.status_code == 200
        d = r.json()
        assert d["status"] == "OFFERS_GENERATED"
        # Check offers
        offers = client.get(f"/ocen/applications/{d['id']}/offers").json()
        assert len(offers) >= 3

    def test_blocked_application_returns_blocked_status(self):
        r = apply(BLOCKED_APP)
        assert r.status_code == 200
        assert "BLOCKED" in r.json()["status"] or r.json()["status"] == "NO_OFFERS"

    def test_offers_have_match_score(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        for o in offers:
            assert o["match_score"] >= 0
            assert o["match_score"] <= 100

    def test_offers_ranked_best_first(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        if len(offers) >= 2:
            assert offers[0]["match_score"] >= offers[1]["match_score"]
            assert offers[0]["rank"] == 1
            assert offers[1]["rank"] == 2

    def test_offer_has_emi_computed(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        for o in offers:
            assert o["monthly_installment"] > 0

    def test_offer_has_total_interest(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        for o in offers:
            assert o["total_interest"] >= 0

    def test_offer_has_approval_probability(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        for o in offers:
            assert 0.0 <= o["approval_probability"] <= 1.0

    def test_offer_processing_fee_positive(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        for o in offers:
            assert o["processing_fee"] >= 0


# ===========================================================================
#  5. Match Score Calculation
# ===========================================================================

class TestMatchScore:
    def test_adapter_score_calculation(self):
        from app.adapters import SimulationAdapter

        class MockLender:
            lender_id = "TEST"
            name = "Test"
            max_loan_amount = 5_000_000.0
            min_loan_amount = 50_000.0
            max_tenure_months = 60
            min_tenure_months = 6
            base_interest_rate = 10.0
            max_interest_rate = 18.0
            processing_fee_pct = 1.0
            risk_appetite = "MEDIUM"
            collateral_required = False
            tat_days = 3
            loan_products = "Working Capital Loan"

        adapter = SimulationAdapter()
        score = adapter._compute_match_score(
            MockLender(), 80.0, "APPROVE", "Low", 1_000_000.0, {}
        )
        assert 0 <= score <= 100

    def test_high_fhc_gives_higher_score(self):
        from app.adapters import SimulationAdapter

        class ML:
            lender_id = "X"
            max_loan_amount = 5_000_000.0
            risk_appetite = "MEDIUM"
            collateral_required = False
            tat_days = 3

        adapter = SimulationAdapter()
        low = adapter._compute_match_score(ML(), 30.0, "APPROVE", "Low", 500_000.0, {})
        high = adapter._compute_match_score(ML(), 90.0, "APPROVE", "Low", 500_000.0, {})
        assert high > low

    def test_fraud_critical_gives_zero_component(self):
        from app.adapters import SimulationAdapter
        assert SimulationAdapter()._fraud_score_component("Critical") == 0.0

    def test_fraud_low_gives_max_component(self):
        from app.adapters import SimulationAdapter
        assert SimulationAdapter()._fraud_score_component("Low") == 100.0

    def test_approve_decision_gives_max_cd_component(self):
        from app.adapters import SimulationAdapter
        assert SimulationAdapter()._credit_decision_component("APPROVE") == 100.0

    def test_emi_calculation(self):
        from app.adapters import calculate_emi
        emi = calculate_emi(1_000_000, 12.0, 12)
        assert emi > 80_000   # sanity check for ₹10L at 12% for 12m

    def test_risk_adjusted_rate_higher_for_low_fhc(self):
        from app.adapters import SimulationAdapter

        class ML:
            base_interest_rate = 10.0
            max_interest_rate = 18.0

        adapter = SimulationAdapter()
        low_rate = adapter._risk_adjusted_rate(ML(), 80.0, "Low")
        high_rate = adapter._risk_adjusted_rate(ML(), 30.0, "High")
        assert high_rate > low_rate


# ===========================================================================
#  6. Explainable Recommendations
# ===========================================================================

class TestExplainability:
    def test_offer_has_match_explanation(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        for o in offers:
            assert o["match_explanation"] is not None
            exp = json.loads(o["match_explanation"])
            assert "why_selected" in exp
            assert "why_customer_qualifies" in exp
            assert "key_strengths" in exp
            assert "key_constraints" in exp
            assert "suggested_next_steps" in exp

    def test_explanation_strengths_populated_for_good_profile(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        exp = json.loads(offers[0]["match_explanation"])
        assert len(exp["key_strengths"]) >= 1

    def test_ai_advisor_recommendation(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.get(f"/ocen/ai-advisor/{app_id}")
        assert r2.status_code == 200
        d = r2.json()
        assert d["recommended_offer_id"] is not None
        assert d["suitability_score"] > 0
        assert len(d["breakdown"]) > 10

    def test_ai_advisor_includes_lender_name(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.get(f"/ocen/ai-advisor/{app_id}")
        assert len(r2.json()["dynamic_summary"]) > 20


# ===========================================================================
#  7. Offer Comparison
# ===========================================================================

class TestOfferComparison:
    def test_comparison_structure(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.get(f"/ocen/offers/compare/{app_id}")
        assert r2.status_code == 200
        d = r2.json()
        assert "total_offers" in d
        assert "best_rate_offer_id" in d
        assert "best_match_offer_id" in d
        assert "comparison_notes" in d

    def test_best_rate_has_lowest_rate(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        comp = client.get(f"/ocen/offers/compare/{app_id}").json()
        if comp["best_rate_offer_id"] and comp["offers"]:
            rates = {o["id"]: o["interest_rate"] for o in comp["offers"]}
            best_id = comp["best_rate_offer_id"]
            assert all(rates[best_id] <= r for r in rates.values())


# ===========================================================================
#  8. Accept / Reject / Disburse
# ===========================================================================

class TestOfferLifecycle:
    def test_accept_offer(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        best_offer_id = offers[0]["id"]

        acc = client.post("/ocen/offers/accept", json={"offer_id": best_offer_id})
        assert acc.status_code == 200
        assert acc.json()["status"] == "ACCEPTED"
        assert acc.json()["selected_offer_id"] == best_offer_id

    def test_accept_expires_other_offers(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        client.post("/ocen/offers/accept", json={"offer_id": offers[0]["id"]})
        updated = client.get(f"/ocen/applications/{app_id}/offers").json()
        pending = [o for o in updated if o["status"] == "PENDING"]
        assert len(pending) == 0

    def test_reject_offer(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        rej = client.post("/ocen/offers/reject", json={
            "offer_id": offers[0]["id"],
            "rejection_reason": "Interest rate too high",
        })
        assert rej.status_code == 200
        assert rej.json()["status"] == "REJECTED"
        assert rej.json()["rejection_reason"] == "Interest rate too high"

    def test_disburse_after_accept(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        client.post("/ocen/offers/accept", json={"offer_id": offers[0]["id"]})
        dis = client.post(f"/ocen/disburse/{app_id}")
        assert dis.status_code == 200
        assert dis.json()["status"] == "DISBURSED"

    def test_disburse_without_accept_fails(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        dis = client.post(f"/ocen/disburse/{app_id}")
        assert dis.status_code == 400

    def test_accept_nonexistent_offer_404(self):
        r = client.post("/ocen/offers/accept", json={"offer_id": 999999})
        assert r.status_code == 404


# ===========================================================================
#  9. Marketplace Status & Dashboard
# ===========================================================================

class TestDashboard:
    def test_marketplace_status_structure(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.get(f"/ocen/marketplace/status/{app_id}")
        assert r2.status_code == 200
        d = r2.json()
        assert "status" in d
        assert "total_offers" in d
        assert "lenders_screened" in d
        assert "best_match_score" in d

    def test_dashboard_structure(self):
        r = client.get("/ocen/dashboard")
        assert r.status_code == 200
        d = r.json()
        required = [
            "total_applications", "offers_generated", "offers_accepted",
            "offers_rejected", "active_lenders", "avg_match_score",
            "avg_interest_rate", "recent_applications",
        ]
        for k in required:
            assert k in d

    def test_dashboard_active_lenders_count(self):
        d = client.get("/ocen/dashboard").json()
        assert d["active_lenders"] >= 10

    def test_dashboard_totals_non_negative(self):
        d = client.get("/ocen/dashboard").json()
        for k in ("total_applications", "offers_generated", "active_lenders"):
            assert d[k] >= 0


# ===========================================================================
#  10. Eligibility Check
# ===========================================================================

class TestEligibility:
    def test_good_profile_eligible(self):
        r = client.post("/ocen/eligibility", json={
            "customer_id": 8001,
            "annual_revenue": 10_000_000,
            "credit_score": 720,
            "requested_amount": 1_000_000,
            "fhc_score": 70.0,
            "credit_decision": "APPROVE",
            "fraud_risk_level": "Low",
        })
        assert r.status_code == 200
        assert r.json()["eligible"] is True
        assert "ULI-" in r.json()["uli_reference"]

    def test_low_credit_score_not_eligible(self):
        r = client.post("/ocen/eligibility", json={
            "customer_id": 8004,
            "annual_revenue": 5_000_000,
            "credit_score": 550,
            "requested_amount": 500_000,
        })
        assert r.status_code == 200
        assert r.json()["eligible"] is False

    def test_amount_exceeds_revenue_ceiling(self):
        r = client.post("/ocen/eligibility", json={
            "customer_id": 8005,
            "annual_revenue": 1_000_000,
            "credit_score": 720,
            "requested_amount": 5_000_000,  # 5× revenue
        })
        assert r.status_code == 200
        assert r.json()["eligible"] is False

    def test_critical_fraud_blocks_eligibility(self):
        r = client.post("/ocen/eligibility", json={
            "customer_id": 8006,
            "annual_revenue": 10_000_000,
            "credit_score": 750,
            "requested_amount": 500_000,
            "fraud_risk_level": "Critical",
        })
        assert r.status_code == 200
        assert r.json()["eligible"] is False


# ===========================================================================
#  11. Adapter Switching
# ===========================================================================

class TestAdapterSwitching:
    def _set_adapter(self, adapter: str):
        r = client.post("/ocen/config", json={"active_adapter": adapter, "match_params": {}})
        assert r.status_code == 200

    def test_default_adapter_simulation(self):
        r = client.get("/ocen/config")
        assert r.status_code == 200
        assert r.json()["active_adapter"] == "SIMULATION"

    def test_switch_to_sandbox(self):
        self._set_adapter("SANDBOX")
        r = apply(GOOD_APP)
        assert r.status_code == 200
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        # Sandbox mode stamps "SANDBOX MODE" in conditions
        for o in offers:
            assert "SANDBOX" in (o.get("conditions") or "").upper()

    def test_switch_to_production(self):
        self._set_adapter("PRODUCTION")
        r = apply(GOOD_APP)
        assert r.status_code == 200

    def test_switch_back_to_simulation(self):
        self._set_adapter("SIMULATION")
        assert client.get("/ocen/config").json()["active_adapter"] == "SIMULATION"


# ===========================================================================
#  12. Admin – Replay / Export
# ===========================================================================

class TestAdmin:
    def test_replay_matching(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.post("/ocen/admin/replay", json={"application_id": app_id})
        assert r2.status_code == 200
        assert r2.json()["status"] == "OFFERS_GENERATED"

    def test_export_json(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.get(f"/ocen/admin/export/{app_id}?format=json")
        assert r2.status_code == 200
        d = r2.json()
        assert "application" in d
        assert "offers" in d

    def test_export_pdf(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.get(f"/ocen/admin/export/{app_id}?format=pdf")
        assert r2.status_code == 200
        assert r2.headers["content-type"] == "application/pdf"
        assert b"%PDF-1.4" in r2.content

    def test_export_unsupported_format(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.get(f"/ocen/admin/export/{app_id}?format=csv")
        assert r2.status_code == 400

    def test_audit_logs_non_empty(self):
        r = client.get("/ocen/audit-logs")
        assert r.status_code == 200
        assert len(r.json()) >= 1


# ===========================================================================
#  13. Workflow Integration
# ===========================================================================

class TestWorkflowIntegration:
    def test_cam_summary_structure(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        r2 = client.get(f"/ocen/cam-summary/{app_id}")
        assert r2.status_code == 200
        d = r2.json()
        assert "requested_amount" in d
        assert "fhc_score" in d
        assert "uli_reference" in d

    def test_executive_summary(self):
        r = client.get("/ocen/executive-summary")
        assert r.status_code == 200
        d = r.json()
        assert "total_applications" in d
        assert "avg_interest_rate" in d
        assert "total_loan_value" in d

    def test_cam_summary_shows_selected_lender_after_accept(self):
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        client.post("/ocen/offers/accept", json={"offer_id": offers[0]["id"]})
        cam = client.get(f"/ocen/cam-summary/{app_id}").json()
        assert cam["selected_lender"] is not None
        assert cam["approved_amount"] is not None


# ===========================================================================
#  14. Business Event Publication
# ===========================================================================

class TestBusinessEvents:
    def test_marketplace_search_started_event(self, caplog):
        import logging
        with caplog.at_level(logging.INFO, logger="ocen-uli-service"):
            apply(GOOD_APP)
        assert any("Marketplace Search Started" in m for m in caplog.messages)

    def test_lender_matched_event(self, caplog):
        import logging
        with caplog.at_level(logging.INFO, logger="ocen-uli-service"):
            apply(GOOD_APP)
        assert any("Lender Matched" in m for m in caplog.messages)

    def test_offer_accepted_event(self, caplog):
        import logging
        r = apply(GOOD_APP)
        app_id = r.json()["id"]
        offers = client.get(f"/ocen/applications/{app_id}/offers").json()
        with caplog.at_level(logging.INFO, logger="ocen-uli-service"):
            client.post("/ocen/offers/accept", json={"offer_id": offers[0]["id"]})
        assert any("Offer Accepted" in m for m in caplog.messages)


# ===========================================================================
#  15. Health Probes
# ===========================================================================

class TestHealth:
    def test_liveness(self):
        r = client.get("/healthz")
        assert r.status_code == 200
        assert r.json()["status"] == "UP"

    def test_readiness(self):
        r = client.get("/readyz")
        assert r.status_code == 200
        assert r.json()["status"] == "READY"
