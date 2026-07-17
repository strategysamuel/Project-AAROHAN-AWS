# AAR-V11-SPRINT-003: Project AAROHAN Sprint 3 Planning

---

## 1. Executive Summary

This document specifies the Sprint 3 Planning targets for **Project AAROHAN Version 1.1**. Applying the velocity metrics calculated in Sprint 1 (6 SP) and Sprint 2 (5 SP), and incorporating the recommendations of the Increment Planning Board (**AAR-V11-INC-PLAN-001**), this sprint is scheduled to translate the approved designs for the RBI Central Fraud Registry Sync (**US-11-202**) into production-grade source code. 

Furthermore, this sprint implements the key retrospective action item to resolve monorepo unit test collection and path parameters.

---

## 2. Sprint Goal

Deliver the next highest-priority Version 1.1 capabilities while reducing technical debt and improving production readiness, specifically implementing the automated RBI Central Fraud Registry integration in the credit evaluation engine.

---

## 3. Sprint Scope

The Sprint 3 scope targets code compilation and testing of the deferred compliance and technical debt features:
* **US-11-202**: Query RBI Central Fraud Registry (5 Story Points - Live Code Integration)
* **Technical Debt Action**: Complete global pathing configuration via `pytest.ini` to resolve ModuleNotFoundError test collection bugs.
* **Alert Notifications Setup**: Configure GCP Pub/Sub notification logs for Secret Manager rotation triggers.

---

## 4. Capacity Planning

* **Sprint 1 Actual Velocity**: 6 Story Points
* **Sprint 2 Actual Velocity**: 5 Story Points
* **Average Team Velocity**: 5.5 Story Points
* **Sprint 3 Target Capacity**: **5 Story Points** (Reserving 0.5 Story Points buffer for Monorepo pathing and Alert setup)
* **Resource Allocation**:
  * 1 Product Owner, 1 Scrum Master
  * 2 Backend Developers (80 Hours)
  * 1 Frontend Developer (40 Hours)
  * 1 AI Engineer (40 Hours)
  * 1 QA Engineer (40 Hours)
  * 1 DevOps Engineer (40 Hours)

---

## 5. Sprint 2 Retrospective Action Review

* **Improvement Item 1: Pytest Collection Failure**:
  * *Sprint 3 Resolution*: Add a global `pytest.ini` configuration at the root of the workspace directory. Declare all microservices paths under `pythonpath = services/ckyc-service services/mca-service services/epfo-service services/credit-engine` to prevent import failures.
* **Improvement Item 2: Dynamic Container Reload Alerts**:
  * *Sprint 3 Resolution*: Set up automatic Pub/Sub message triggers when secrets are updated in Secret Manager.

---

## 6. Selected User Stories

### Story ID: US-11-202
* **Epic ID**: EP-11-008 (Compliance Automation)
* **Feature ID**: F-11-002 (RBI Central Fraud Registry Sync)
* **Story Points**: 5
* **Priority**: Critical (Must Have)
* **Acceptance Criteria**:
  - *Given*: An RM submits a loan application for PAN "ABCDE1234F".
  - *When*: The credit engine queries the RBI Registry API.
  - *Then*: If blacklisted, the application status is set to `REJECTED_FRAUD_FLAG` and logged in audit trails.
* **Dependencies**: RBI mock registries sandbox endpoints.

---

## 7. Sprint Backlog

* **US-11-202**: Query RBI Central Fraud Registry (5 SP)
* **Tech Debt**: Setup global `pytest.ini` configurations (0 SP - Technical Debt Buffer)
* **DevOps**: Secret Manager update Pub/Sub alerting triggers (0 SP - Technical Debt Buffer)

---

## 8. Engineering Task Breakdown

### Tasks for US-11-202 (Code Integration)
* **Task 1.1**: Write the HTTP Client connector for the RBI Central Fraud Registry API inside `services/credit-engine/app/main.py`. (4h)
* **Task 1.2**: Update the `AICreditDecision` model and `ai_credit_decisions` database tables to store `rbi_fraud_status` and `rbi_verification_log`. (4h)
* **Task 1.3**: Configure the credit evaluation logic to check customer PANs, flag matches with `REJECTED_FRAUD_FLAG`, and write audit trails. (6h)
* **Task 1.4**: Update the Relationship Manager workspace dashboard to retrieve and display specific fraud-flag indicators. (4h)

### Retrospective Action Tasks
* **Task Ret-1**: Add root `pytest.ini` file and verify that the global `pytest` command executes successfully across all service directories. (3h)
* **Task Ret-2**: Provision the Cloud Pub/Sub topics and Eventarc routing rules for secret change signals. (3h)

---

## 9. Definition of Ready (DoR)

* Stories must have estimated Story Points.
* Interface models and mock schemas for external APIs (RBI) must be finalized.
* Acceptance criteria must be reviewed and agreed upon by the Product Owner.

---

## 10. Definition of Done (DoD)

* All unit, integration, and E2E regression tests pass successfully.
* Code has been committed, reviewed, and approved.
* Backend test coverage meets or exceeds the 80% baseline requirement.
* Docker images compile successfully and deploy to the Staging/QA environments.

---

## 11. Sprint Risks

* **Risk**: Latency delays from external third-party registry query calls during underwriting evaluation.
* **Mitigation**: Implement a 2000ms request timeout SLA limit, client-side caching, and fallback status (`PENDING_MANUAL_FRAUD_CHECK`) to preserve continuous system availability.

---

## 12. Sprint KPIs

* **Velocity**: Target 5 Story Points completed.
* **Story Completion Rate**: 100%.
* **Defect Leakage**: Zero defects leak to UAT/Staging.
* **Backend Code Coverage**: >= 80% coverage maintained.

---

## 13. AI Engineering Activities

* Update Vertex AI / Gemini prompt directives inside the credit engine to recognize the `REJECTED_FRAUD_FLAG` status, preventing model hallucinations when compiling CAM summaries.

---

## 14. Google Cloud Activities

* Configure Secret Manager dynamic event publishers.
* Deploy Eventarc triggers to automate backend container reloading.

---

## 15. Security Activities

* Verify that all credentials rotated using `scripts/rotate_secrets.py` continue to update the active environment configuration smoothly.
* Confirm that WAF security policies block unauthorized access attempts.

---

## 16. Testing Strategy

* **Unit Tests**: Add tests verifying the mock adapter’s output for success, failure, and blacklisted PAN scenarios.
* **Integration Tests**: Update `tests/test_regression_e2e.py` to ensure that checks against blacklisted accounts return the correct rejection states.
* **Regression Tests**: Ensure previous updates to Pydantic v2 schemas and key rotation schedules remain fully functional.

---

## 17. Sprint Deliverables

* Live source code implementation for the RBI Central Fraud Registry client adapter.
* Verified root-level `pytest.ini` testing framework configuration.
* Automated GCP Pub/Sub alert publishers for secret updates.

---

## 18. Approval Matrix

* **Product Owner**: APPROVED
* **Scrum Master**: APPROVED
* **Engineering Manager**: APPROVED
* **Technical Lead**: APPROVED

---

## 19. Appendix

* Sprint Planning spreadsheet.
* Target API endpoints documentation.
