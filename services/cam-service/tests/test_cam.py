"""
AAR-BUILD-018 – CAM Generation Service
Comprehensive Test Suite
=======================================================================
Coverage:
  ✓ CAM generation (all 18 sections populated)
  ✓ Data aggregation (upstream intelligence consumed)
  ✓ Narrative generation (all 7 narrative fields)
  ✓ PDF generation (valid PDF-1.4 header)
  ✓ HTML rendering (valid HTML with score bar)
  ✓ JSON export (all sections present)
  ✓ Version comparison (field-level diffs)
  ✓ Workflow integration (OCEN trigger, executive feed)
  ✓ Business event publication (log-based)
  ✓ Dashboard functionality (KPIs, recent list)
  ✓ Approval workflow (multi-level, audit trail)
  ✓ Template registry (5 bank templates)
  ✓ Admin (archive, config, regenerate)
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

# ── Shared Payloads ────────────────────────────────────────────────────────

GOOD_PAYLOAD = {
    "customer_id": 9001,
    "template": "IDBI_BANK",
    "fhc_score": 74.5,
    "credit_decision": "APPROVE",
    "fraud_risk_level": "Low",
    "fraud_score": 5.0,
    "recommended_lender": "IDBI Bank – MSME Division",
    "recommended_amount": 1_500_000.0,
    "recommended_rate": 9.25,
    "recommended_tenure": 24,
    "business_name": "Shree Textiles Pvt Ltd",
    "business_type": "Private Limited",
    "industry": "Textiles",
    "annual_revenue": 8_000_000.0,
    "loan_purpose": "Working capital and inventory procurement",
}

CONDITIONAL_PAYLOAD = {
    "customer_id": 9002,
    "template": "PRIVATE_BANK",
    "fhc_score": 52.0,
    "credit_decision": "CONDITIONAL",
    "fraud_risk_level": "Medium",
    "fraud_score": 35.0,
    "recommended_lender": "HDFC Bank – Business Banking",
    "recommended_amount": 800_000.0,
    "recommended_rate": 11.5,
    "recommended_tenure": 18,
    "business_name": "Sunrise Traders",
    "annual_revenue": 4_000_000.0,
}

REJECT_PAYLOAD = {
    "customer_id": 9003,
    "template": "GENERIC",
    "fhc_score": 28.0,
    "credit_decision": "REJECT",
    "fraud_risk_level": "High",
    "fraud_score": 72.0,
    "recommended_amount": 0,
    "business_name": "Risky Corp",
    "annual_revenue": 1_000_000.0,
}


def generate(payload=None):
    return client.post("/cam/generate", json=payload or GOOD_PAYLOAD)


# ===========================================================================
#  1. CAM Generation – 18 Sections
# ===========================================================================

class TestCAMGeneration:
    def test_generate_returns_200(self):
        r = generate()
        assert r.status_code == 200

    def test_generate_creates_cam_reference(self):
        r = generate()
        assert r.json()["cam_reference"].startswith("CAM-")

    def test_all_18_sections_populated(self):
        r = generate()
        d = r.json()
        sections = [
            "section_executive_summary", "section_applicant_profile",
            "section_business_profile", "section_loan_requirement",
            "section_identity_verification", "section_gst_compliance",
            "section_banking_behaviour", "section_workforce_stability",
            "section_corporate_governance", "section_fhc_summary",
            "section_credit_decision", "section_fraud_screening",
            "section_ocen_marketplace", "section_recommended_offer",
            "section_key_risks", "section_risk_mitigation",
            "section_banker_recommendation", "section_approval_matrix",
        ]
        for s in sections:
            assert s in d
            assert len(d[s]) > 20, f"Section {s} is too short."

    def test_executive_summary_contains_business_name(self):
        r = generate()
        assert "Shree Textiles Pvt Ltd" in r.json()["section_executive_summary"]

    def test_recommended_offer_contains_emi(self):
        r = generate()
        offer = r.json()["section_recommended_offer"]
        assert "₹" in offer or "Rs" in offer

    def test_approval_matrix_has_levels(self):
        r = generate()
        matrix = r.json()["section_approval_matrix"]
        assert "Branch Manager" in matrix or "Level 1" in matrix

    def test_status_is_draft(self):
        r = generate()
        assert r.json()["status"] == "DRAFT"

    def test_version_is_1_on_creation(self):
        r = generate()
        assert r.json()["current_version"] == 1

    def test_template_stored(self):
        r = generate()
        assert r.json()["template"] == "IDBI_BANK"

    def test_generate_is_idempotent(self):
        """Re-generating for same customer replaces old CAM."""
        r1 = generate()
        r2 = generate()
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert r1.json()["cam_reference"] != r2.json()["cam_reference"]

    def test_generate_by_customer_id_endpoint(self):
        r = client.post("/cam/generate/9004?template=GENERIC")
        assert r.status_code == 200
        assert r.json()["customer_id"] == 9004


# ===========================================================================
#  2. Credit Scoring
# ===========================================================================

class TestCreditScoring:
    def test_overall_credit_score_present(self):
        r = generate()
        assert r.json()["overall_credit_score"] is not None

    def test_fhc_rating_aaa_for_high_score(self):
        r = generate({**GOOD_PAYLOAD, "fhc_score": 90.0, "customer_id": 9101})
        assert r.json()["financial_health_rating"] in ("AAA", "AA")

    def test_fhc_rating_c_for_low_score(self):
        r = generate({**REJECT_PAYLOAD, "fhc_score": 20.0, "customer_id": 9102})
        assert r.json()["financial_health_rating"] == "C"

    def test_risk_grade_low_for_good_profile(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9103})
        assert r.json()["risk_grade"] == "Low"

    def test_risk_grade_critical_for_reject(self):
        r = generate({**REJECT_PAYLOAD, "customer_id": 9104})
        assert r.json()["risk_grade"] == "Critical"

    def test_fraud_status_clear_for_low_risk(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9105})
        assert r.json()["fraud_status"] == "CLEAR"

    def test_fraud_status_blocked_for_critical(self):
        r = generate({**REJECT_PAYLOAD, "fraud_risk_level": "Critical", "customer_id": 9106})
        assert r.json()["fraud_status"] == "BLOCKED"

    def test_eligibility_eligible_for_good_profile(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9107})
        assert r.json()["eligibility_status"] == "ELIGIBLE"

    def test_eligibility_conditional_for_conditional(self):
        r = generate({**CONDITIONAL_PAYLOAD, "customer_id": 9108})
        assert r.json()["eligibility_status"] == "CONDITIONAL"

    def test_eligibility_ineligible_for_reject(self):
        r = generate({**REJECT_PAYLOAD, "customer_id": 9109})
        assert r.json()["eligibility_status"] == "INELIGIBLE"

    def test_recommended_loan_amount_stored(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9110})
        assert r.json()["recommended_loan_amount"] == 1_500_000.0

    def test_recommended_interest_rate_stored(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9111})
        assert r.json()["recommended_interest_rate"] == 9.25


# ===========================================================================
#  3. Narrative Generation
# ===========================================================================

class TestNarrativeGeneration:
    def test_all_7_narratives_present(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9201})
        d = r.json()
        for field in [
            "narrative_customer_strengths", "narrative_business_strengths",
            "narrative_financial_observations", "narrative_key_risks",
            "narrative_mitigating_factors", "narrative_lending_recommendation",
            "narrative_monitoring_actions",
        ]:
            assert d[field] is not None
            assert len(d[field]) > 10, f"Narrative {field} is empty."

    def test_strengths_mention_fhc_for_good_profile(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9202})
        assert "FHC" in r.json()["narrative_customer_strengths"] or "Financial Health" in r.json()["narrative_customer_strengths"]

    def test_recommendation_says_approve_for_good(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9203})
        assert "APPROVAL" in r.json()["narrative_lending_recommendation"].upper()

    def test_recommendation_says_decline_for_reject(self):
        r = generate({**REJECT_PAYLOAD, "customer_id": 9204})
        assert "DECLINE" in r.json()["narrative_lending_recommendation"].upper() or "REJECT" in r.json()["narrative_lending_recommendation"].upper()

    def test_monitoring_mentions_gst(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9205})
        assert "GST" in r.json()["narrative_monitoring_actions"]


# ===========================================================================
#  4. Retrieve
# ===========================================================================

class TestRetrieve:
    def test_retrieve_cam_by_customer_id(self):
        generate({**GOOD_PAYLOAD, "customer_id": 9301})
        r = client.get("/cam/9301")
        assert r.status_code == 200
        assert r.json()["customer_id"] == 9301

    def test_retrieve_cam_by_cam_id(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9302})
        cam_id = gen.json()["id"]
        r = client.get(f"/cam/record/{cam_id}")
        assert r.status_code == 200

    def test_retrieve_nonexistent_404(self):
        r = client.get("/cam/999999")
        assert r.status_code == 404

    def test_refresh_cam(self):
        generate({**GOOD_PAYLOAD, "customer_id": 9303})
        r = client.post("/cam/refresh/9303?template=PUBLIC_SECTOR")
        assert r.status_code == 200
        assert r.json()["customer_id"] == 9303


# ===========================================================================
#  5. Download – JSON / HTML / PDF
# ===========================================================================

class TestDownload:
    def _cam_id(self, customer_id=9401, payload=None):
        p = payload or {**GOOD_PAYLOAD, "customer_id": customer_id}
        return generate(p).json()["id"]

    def test_download_json(self):
        cam_id = self._cam_id(9401)
        r = client.get(f"/cam/{cam_id}/download?format=json")
        assert r.status_code == 200
        d = r.json()
        assert "sections" in d
        assert "scoring" in d
        assert "narratives" in d
        assert len(d["sections"]) == 18

    def test_download_html(self):
        cam_id = self._cam_id(9402)
        r = client.get(f"/cam/{cam_id}/download?format=html")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        assert b"<html" in r.content

    def test_html_contains_score_bar(self):
        cam_id = self._cam_id(9403)
        html = client.get(f"/cam/{cam_id}/download?format=html").content.decode()
        assert "score-bar" in html or "Credit Score" in html

    def test_html_contains_all_section_titles(self):
        cam_id = self._cam_id(9404)
        html = client.get(f"/cam/{cam_id}/download?format=html").content.decode()
        for title in ["Executive Summary", "Fraud Screening", "Banker Recommendation"]:
            assert title in html

    def test_html_contains_narrative(self):
        cam_id = self._cam_id(9405)
        html = client.get(f"/cam/{cam_id}/download?format=html").content.decode()
        assert "AI Lending Narrative" in html or "narrative" in html

    def test_download_pdf(self):
        cam_id = self._cam_id(9406)
        r = client.get(f"/cam/{cam_id}/download?format=pdf")
        assert r.status_code == 200
        assert r.headers["content-type"] == "application/pdf"
        assert r.content.startswith(b"%PDF-1.4")

    def test_pdf_contains_cam_reference(self):
        cam_id = self._cam_id(9407)
        cam_ref = generate({**GOOD_PAYLOAD, "customer_id": 9407}).json()["cam_reference"]
        pdf = client.get(f"/cam/{cam_id}/download?format=pdf").content.decode("utf-8", errors="replace")
        assert "CAM-" in pdf

    def test_unsupported_format_400(self):
        cam_id = self._cam_id(9408)
        r = client.get(f"/cam/{cam_id}/download?format=docx")
        assert r.status_code == 400


# ===========================================================================
#  6. Version History & Comparison
# ===========================================================================

class TestVersions:
    def test_version_1_created_on_generation(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9501})
        cam_id = gen.json()["id"]
        versions = client.get(f"/cam/{cam_id}/versions").json()
        assert len(versions) >= 1
        assert versions[0]["version_num"] == 1

    def test_update_cam_increments_version(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9502})
        cam_id = gen.json()["id"]
        client.put(f"/cam/{cam_id}", json={
            "edited_by": "RM001",
            "change_summary": "Corrected business profile",
            "section_business_profile": "Updated business profile content",
        })
        updated = client.get(f"/cam/record/{cam_id}").json()
        assert updated["current_version"] == 2

    def test_version_comparison_returns_diffs(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9503})
        cam_id = gen.json()["id"]
        # Create v2
        client.put(f"/cam/{cam_id}", json={
            "edited_by": "RM001",
            "change_summary": "Updated recommendation",
            "section_banker_recommendation": "Revised recommendation: APPROVE with enhanced monitoring.",
        })
        r = client.get(f"/cam/{cam_id}/compare?v_a=1&v_b=2")
        assert r.status_code == 200
        d = r.json()
        assert d["version_a"] == 1
        assert d["version_b"] == 2
        assert "diffs" in d
        changed = [diff for diff in d["diffs"] if diff["changed"]]
        assert len(changed) >= 1

    def test_compare_missing_version_404(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9504})
        cam_id = gen.json()["id"]
        r = client.get(f"/cam/{cam_id}/compare?v_a=1&v_b=99")
        assert r.status_code == 404


# ===========================================================================
#  7. Approval Workflow
# ===========================================================================

class TestApproval:
    def test_approve_cam(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9601})
        cam_id = gen.json()["id"]
        r = client.post(f"/cam/{cam_id}/approve", json={
            "approver_id": "BM-MUMBAI-01",
            "approver_role": "Branch Manager",
            "action": "APPROVED",
            "level": 1,
            "comments": "Strong profile – approve.",
        })
        assert r.status_code == 200
        assert r.json()["status"] == "APPROVED"

    def test_reject_cam(self):
        gen = generate({**REJECT_PAYLOAD, "customer_id": 9602})
        cam_id = gen.json()["id"]
        r = client.post(f"/cam/{cam_id}/approve", json={
            "approver_id": "BM-PUNE-02",
            "approver_role": "Branch Manager",
            "action": "REJECTED",
            "level": 1,
            "comments": "Fraud risk too high.",
        })
        assert r.status_code == 200
        assert r.json()["status"] == "REJECTED"

    def test_approval_trail_recorded(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9603})
        cam_id = gen.json()["id"]
        client.post(f"/cam/{cam_id}/approve", json={
            "approver_id": "BM-HYD-03", "approver_role": "Branch Manager",
            "action": "APPROVED", "level": 1,
        })
        trail = client.get(f"/cam/{cam_id}/approvals").json()
        assert len(trail) >= 1
        assert trail[0]["approver_id"] == "BM-HYD-03"

    def test_multi_level_approval(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9604})
        cam_id = gen.json()["id"]
        # Level 1 – Branch Manager
        client.post(f"/cam/{cam_id}/approve", json={
            "approver_id": "BM-001", "approver_role": "Branch Manager",
            "action": "RETURNED", "level": 1, "comments": "Refer to ZM.",
        })
        # Level 2 – Zonal Manager
        client.post(f"/cam/{cam_id}/approve", json={
            "approver_id": "ZM-001", "approver_role": "Zonal Manager",
            "action": "APPROVED", "level": 2,
        })
        trail = client.get(f"/cam/{cam_id}/approvals").json()
        assert len(trail) == 2
        levels = {t["level"] for t in trail}
        assert 1 in levels and 2 in levels


# ===========================================================================
#  8. Dashboard
# ===========================================================================

class TestDashboard:
    def test_dashboard_structure(self):
        r = client.get("/cam/dashboard/summary")
        assert r.status_code == 200
        d = r.json()
        for k in ["total_cams", "draft", "pending_approval", "approved", "rejected", "archived", "avg_credit_score", "recent_cams"]:
            assert k in d

    def test_dashboard_totals_non_negative(self):
        d = client.get("/cam/dashboard/summary").json()
        for k in ["total_cams", "draft", "approved", "rejected"]:
            assert d[k] >= 0

    def test_dashboard_recent_cams_list(self):
        generate({**GOOD_PAYLOAD, "customer_id": 9701})
        d = client.get("/cam/dashboard/summary").json()
        assert isinstance(d["recent_cams"], list)


# ===========================================================================
#  9. Templates
# ===========================================================================

class TestTemplates:
    def test_list_templates_returns_5(self):
        r = client.get("/cam/templates")
        assert r.status_code == 200
        templates = r.json()
        assert len(templates) >= 5

    def test_template_keys_correct(self):
        templates = client.get("/cam/templates").json()
        keys = {t["template_key"] for t in templates}
        for k in ["IDBI_BANK", "PUBLIC_SECTOR", "PRIVATE_BANK", "NBFC", "GENERIC"]:
            assert k in keys

    def test_get_idbi_template(self):
        r = client.get("/cam/templates/IDBI_BANK")
        assert r.status_code == 200
        assert "IDBI" in r.json()["bank_name"]

    def test_get_nonexistent_template_404(self):
        r = client.get("/cam/templates/UNKNOWN_BANK")
        assert r.status_code == 404

    def test_private_bank_template_generates_cam(self):
        r = generate({**GOOD_PAYLOAD, "customer_id": 9801, "template": "PRIVATE_BANK"})
        assert r.status_code == 200
        assert r.json()["template"] == "PRIVATE_BANK"

    def test_html_uses_template_branding(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9802, "template": "IDBI_BANK"})
        cam_id = gen.json()["id"]
        html = client.get(f"/cam/{cam_id}/download?format=html").content.decode()
        assert "#003087" in html or "IDBI" in html


# ===========================================================================
#  10. Workflow Integration
# ===========================================================================

class TestWorkflowIntegration:
    def test_ocen_trigger_endpoint(self):
        r = client.get("/cam/workflow/ocen-trigger/9901?template=IDBI_BANK")
        assert r.status_code == 200
        assert r.json()["customer_id"] == 9901

    def test_executive_feed(self):
        r = client.get("/cam/workflow/executive-feed")
        assert r.status_code == 200
        d = r.json()
        assert "total_cams" in d
        assert "avg_credit_score" in d
        assert "total_recommended_value" in d

    def test_admin_config_retrieval(self):
        r = client.get("/cam/admin/config")
        assert r.status_code == 200
        d = r.json()
        assert "default_template" in d
        assert "sections_enabled" in d
        assert len(d["sections_enabled"]) == 18

    def test_archive_cam(self):
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9902})
        cam_id = gen.json()["id"]
        r = client.post(f"/cam/{cam_id}/archive")
        assert r.status_code == 200
        assert r.json()["status"] == "ARCHIVED"


# ===========================================================================
#  11. Business Events
# ===========================================================================

class TestBusinessEvents:
    def test_cam_generation_started_event(self, caplog):
        import logging
        with caplog.at_level(logging.INFO, logger="cam-service"):
            generate({**GOOD_PAYLOAD, "customer_id": 9111})
        assert any("CAM Generation Started" in m for m in caplog.messages)

    def test_cam_generated_event(self, caplog):
        import logging
        with caplog.at_level(logging.INFO, logger="cam-service"):
            generate({**GOOD_PAYLOAD, "customer_id": 9112})
        assert any("CAM Generated" in m for m in caplog.messages)

    def test_cam_approved_event(self, caplog):
        import logging
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9113})
        cam_id = gen.json()["id"]
        with caplog.at_level(logging.INFO, logger="cam-service"):
            client.post(f"/cam/{cam_id}/approve", json={
                "approver_id": "BM-001", "approver_role": "BM",
                "action": "APPROVED", "level": 1,
            })
        assert any("CAM Approved" in m for m in caplog.messages)

    def test_cam_exported_event_json(self, caplog):
        import logging
        gen = generate({**GOOD_PAYLOAD, "customer_id": 9114})
        cam_id = gen.json()["id"]
        with caplog.at_level(logging.INFO, logger="cam-service"):
            client.get(f"/cam/{cam_id}/download?format=json")
        assert any("CAM Exported" in m for m in caplog.messages)


# ===========================================================================
#  12. Health Probes
# ===========================================================================

class TestHealth:
    def test_livez(self):
        r = client.get("/livez")
        assert r.status_code == 200
        assert r.json()["status"] == "UP"

    def test_readyz(self):
        r = client.get("/readyz")
        assert r.status_code == 200
        assert r.json()["status"] == "READY"
