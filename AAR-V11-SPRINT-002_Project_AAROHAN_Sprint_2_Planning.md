# AAR-V11-SPRINT-002: Project AAROHAN Sprint 2 Planning

---

## 1. Executive Summary

This document specifies the Sprint 2 Planning targets for **Project AAROHAN Version 1.1**. Based on the actual velocity measured in Sprint 1 (6 Story Points), this planning board structures resource allocation, task breakdowns, testing strategies, and risk mitigations for the second sprint iteration. Sprint 2 focuses on integrating external public registries (RBI Central Fraud Registry) to enhance credit underwriting decision safety.

---

## 2. Sprint Goal

Deliver the automated RBI Central Fraud Registry verification API and sync capabilities in the credit evaluation engine to eliminate credit risk from blacklisted MSME borrowers.

---

## 3. Sprint Scope

Sprint 2 scope is prioritized based on the team's measured capacity and backlog importance:
* **US-11-202**: Query RBI Central Fraud Registry (5 Story Points)
* **Retrospective Action Integration**: Resolve monorepo Python package/pytest path lookup configurations and set up Secret Manager notifications.

---

## 4. Sprint Capacity Planning

Following Scrum best practices, the team capacity for Sprint 2 is strictly constrained to the actual velocity achieved during Sprint 1:
* **Sprint 1 Actual Velocity**: 6 Story Points
* **Sprint 2 Target Load**: 5 Story Points (Conserving 1 Story Point buffer for the integration of Retrospective improvement actions)
* **Resource Allocation**:
  * 1 Product Owner, 1 Scrum Master
  * 2 Backend Developers (80 Hours)
  * 1 Frontend Developer (40 Hours)
  * 1 AI Engineer (40 Hours)
  * 1 QA Engineer (40 Hours)
  * 1 DevOps Engineer (40 Hours)

---

## 5. Sprint 1 Retrospective Action Review

Each of the improvement opportunities identified in the Sprint 1 Retrospective is mapped to Sprint 2 tasks:
1. **Pytest Path Collection Issue**:
   * *Resolution Plan*: Create a root `pytest.ini` config file to declare all service directories in the path, allowing unified test suite execution (`pytest`) without custom import hacks.
2. **Secret Manager Notification Pipeline**:
   * *Resolution Plan*: Configure Secret Manager to publish to a Pub/Sub topic when keys are rotated, which Eventarc handles to push notifications/reload signals.

---

## 6. Selected User Stories

### Story ID: US-11-202
* **Feature ID**: F-11-002
* **Epic ID**: EP-11-008 (Compliance Automation)
* **Story Points**: 5
* **Priority**: Critical (Must Have)
* **Story Statement**: As a Credit Officer, I want the system to check applicant details against the RBI Central Fraud Registry so that blacklisted borrowers are flagged and rejected immediately.
* **Acceptance Criteria**:
  - *Given*: An RM submits a loan application for PAN "ABCDE1234F".
  - *When*: The credit engine queries the RBI Registry API.
  - *Then*: If blacklisted, the application status is set to `REJECTED_FRAUD_FLAG` and logged in audit trails.
* **Dependencies**: RBI Central Fraud Registry mock/sandbox endpoints.

---

## 7. Sprint Backlog

Total Selected Backlog: **5 Story Points** (under the 6 SP velocity baseline).

* **US-11-202**: Query RBI Central Fraud Registry (5 SP)
* **Process Action**: Monorepo pytest path configuration (0 SP - Technical Debt Buffer)
* **DevOps Action**: Secret Manager Pub/Sub Event Notification Setup (0 SP - Technical Debt Buffer)

---

## 8. Engineering Task Breakdown

### Tasks for US-11-202 (RBI Registry Integration)
* **Task 1.1**: Design RBI Central Fraud Registry API client adapter and mock response payloads. (4h)
* **Task 1.2**: Implement verification check block in the `credit-engine` service logic. (6h)
* **Task 1.3**: Update database schemas to support the `REJECTED_FRAUD_FLAG` status code and audit trail logging. (4h)
* **Task 1.4**: Modify Relationship Manager workspace dashboard to show fraud-specific rejection flags. (4h)

### Retrospective Action Tasks
* **Task Ret-1**: Add root `pytest.ini` and structure pythonpath for monorepo modules. (3h)
* **Task Ret-2**: Set up Pub/Sub topic and Eventarc routing for secret change events. (3h)

---

## 9. Definition of Ready (DoR)

* User stories must be estimated in Story Points.
* Target external API schemas (RBI) must be defined or simulated.
* Clear business value and functional acceptance criteria must be documented.

---

## 10. Definition of Done (DoD)

* All code compiled cleanly with zero warnings.
* All regression and unit tests passed with 100% success.
* Branch reviewed and approved by another engineer.
* Continuous Integration pipeline run succeeds on the main branch.
* Deployed to the Staging/QA environments.

---

## 11. Risks & Mitigations

* **Risk**: High latency or downtime of the third-party RBI Registry API.
* **Mitigation**: Implement a 2000ms request timeout limit, caching strategies, and fallback status (`PENDING_MANUAL_FRAUD_CHECK`) to avoid blocking the user flow.

---

## 12. Sprint KPIs

* **Velocity**: Target 5 Story Points completed.
* **Story Completion Rate**: 100%.
* **Defect Leakage**: Zero bugs leaked to production.
* **Backend Code Coverage**: Maintain >= 80% coverage.

---

## 13. AI Engineering Activities

* Ensure that Gemini and Vertex AI integrations are updated to correctly handle the new `REJECTED_FRAUD_FLAG` status inside CAM (Credit Assessment Memo) and SWOT summary generations.

---

## 14. Google Cloud Activities

* Provision Cloud Pub/Sub topics for Secret Manager update notifications.
* Map Eventarc routing rules to trigger Cloud Run container environment checks.

---

## 15. Testing Strategy

* **Unit Tests**: Mock the RBI Central Fraud Registry response to validate success/failure/blacklist logic.
* **Integration/E2E Tests**: Update the monorepo integration test file (`tests/test_regression_e2e.py`) to run verification checks including blacklisted PAN states.
* **Regression Tests**: Ensure previous Pydantic v2 migrations and secret rotation endpoints function properly under load.

---

## 16. Sprint Deliverables

* Updated `credit-engine` service with RBI Central Fraud Registry connector.
* Configured `pytest.ini` root testing framework.
* Cloud Pub/Sub and Eventarc rotation message channels.

---

## 17. Approval Matrix

* **Product Owner**: APPROVED
* **Scrum Master**: APPROVED
* **CTO / Enterprise Architect**: APPROVED
* **Engineering Manager**: APPROVED

---

## 18. Appendix

* Backlog Reference Board.
* Staging API Sandbox Endpoints for mock registries.
