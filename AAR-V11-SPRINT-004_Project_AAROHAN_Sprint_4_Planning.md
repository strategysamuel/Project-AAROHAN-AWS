# AAR-V11-SPRINT-004: Project AAROHAN Sprint 4 Planning

---

## 1. Executive Summary

This document specifies the Sprint 4 Planning targets for **Project AAROHAN Version 1.1**. Applying the velocity metrics calculated in Sprint 1 (6 SP), Sprint 2 (5 SP), and Sprint 3 (5 SP), this planning board structures the final development iteration. Sprint 4 focuses on executing the remaining prioritized MVP user stories (`US-11-501` and `US-11-601`) to prepare the codebase for Release Candidate 1 (RC1).

---

## 2. Sprint Goal

Complete the remaining Version 1.1 MVP scope and prepare the product for Release Candidate (RC1), ensuring robust perimeter security and explainable AI-driven credit underwriting.

---

## 3. Sprint Scope

The Sprint 4 scope focuses on security configurations, AI governance, and final testing parameters:
* **US-11-501**: Cloud Armor WAF dynamic web injection protection (2 Story Points)
* **US-11-601**: Plain-text Gemini AI Explainability Tags in credit summaries (3 Story Points)
* **Retrospective Action Integration**: Verify dynamic Eventarc reload cycles in a sandbox environment and enforce strict testing isolation rules.

---

## 4. Capacity Planning

* **Sprint 1 Actual Velocity**: 6 Story Points
* **Sprint 2 Actual Velocity**: 5 Story Points
* **Sprint 3 Actual Velocity**: 5 Story Points
* **Empirical Average Velocity**: 5.3 Story Points
* **Sprint 4 Target Load**: **5 Story Points** (Completely aligned with historical average velocity)
* **Resource Allocation**:
  * 1 Product Owner, 1 Scrum Master
  * 2 Backend Developers (80 Hours)
  * 1 Frontend Developer (40 Hours)
  * 1 AI Engineer (40 Hours)
  * 1 QA Engineer (40 Hours)
  * 1 DevOps Engineer (40 Hours)

---

## 5. Sprint 3 Retrospective Action Review

* **Improvement Item 1: Eventarc Reload Testing**:
  * *Sprint 4 Plan*: Set up a sandbox pipeline to verify container environment variables automatically refresh on key modifications without breaking HTTP sessions.
* **Improvement Item 2: Ignored Directories in Global Test Runs**:
  * *Sprint 4 Plan*: Declare `norecursedirs` filters in the root `pytest.ini` to prevent local microservice unit tests from clashing in global runs.

---

## 6. Remaining MVP Scope

The final remaining backlog items prioritized for the Version 1.1 MVP release are:
* **US-11-501**: Implement Cloud Armor WAF rules to prevent SQL injection and cross-site scripting (2 SP).
* **US-11-601**: Generate explainable plain-text credit tags via the Gemini reasoning block (3 SP).

---

## 7. Selected User Stories

### Story ID: US-11-501
* **Epic ID**: EP-11-007 (Security Enhancement)
* **Feature ID**: F-11-105 (Advanced Armor Security)
* **Story Points**: 2
* **Priority**: High (Must Have)
* **Acceptance Criteria**:
  - *Given*: Cloud Armor WAF is active at the load balancer entry point.
  - *When*: An client attempts an SQL injection query payload.
  - *Then*: The request is blocked at the perimeter and returns a 403 Forbidden status.
* **Dependencies**: GCP HTTP Load Balancer configuration.

### Story ID: US-11-601
* **Epic ID**: EP-11-001 (AI Enhancement)
* **Feature ID**: F-11-106 (Explainability Tagging)
* **Story Points**: 3
* **Priority**: High (Must Have)
* **Acceptance Criteria**:
  - *Given*: The credit engine generates a credit decision.
  - *When*: The Gemini reasoner runs.
  - *Then*: Plain-text explainability tags (e.g. `DSCR_OK`, `GST_GROWTH_STRONG`) are mapped to the final decision schema and logged.
* **Dependencies**: Vertex AI Gemini API connectivity.

---

## 8. Sprint Backlog

* **US-11-501**: Cloud Armor WAF Deployment (2 SP)
* **US-11-601**: Plain-text Explainability Tags (3 SP)
* **Process Action**: Cloud Run sandbox session verification (0 SP - Technical Debt Buffer)

---

## 9. Engineering Task Breakdown

### Tasks for US-11-501 (WAF Deployment)
* **Task 1.1**: Draft Google Cloud Armor security policies blocking SQLi and XSS payloads. (3h)
* **Task 1.2**: Attach the policy profile to the HTTP load balancer Frontend. (2h)
* **Task 1.3**: Configure WAF audit log streams for Cloud Logging ingestion. (3h)

### Tasks for US-11-601 (AI Explainability)
* **Task 2.1**: Update Gemini prompt schemas in `credit-engine` to request plain-text tags. (4h)
* **Task 2.2**: Modify `AICreditDecisionResponse` to support an array of explainability tags. (3h)
* **Task 2.3**: Update Relationship Manager workspace layout to display tags visually. (4h)

---

## 10. Definition of Ready (DoR)

* Story point estimations must align with capacity limits.
* WAF rule specifications and target schemas must be defined.
* Acceptance criteria must be approved by the Product Owner.

---

## 11. Definition of Done (DoD)

* All unit, integration, and regression test suites pass successfully.
* Security policies are verified and block targeted attack payloads.
* API response schemas are fully backward-compatible.
* Deployed container builds pass validation in UAT environments.

---

## 12. Risks & Mitigations

* **Risk**: WAF rules generating false-positive blockings on legitimate client uploads.
* **Mitigation**: Deploy the Cloud Armor policy in `preview` (dry-run) mode initially, verify telemetry logs, and enforce active blocking rules only after confirming zero impact.

---

## 13. AI Engineering Activities

* Prompt engineering refinements to structure Gemini response tags, keeping output formats restricted to a predefined list of compliance tokens.

---

## 14. Google Cloud Activities

* Provision Cloud Armor security configurations using Terraform blueprints.
* Map WAF log destinations to BigQuery analytical datasets.

---

## 15. Security & Compliance Activities

* Set up OWASP top-10 security checks across API gate entry points.
* Verify compliance audit trails for all manual credit decision overrides.

---

## 16. Technical Debt Reduction Activities

* Configure pytest filters inside the global `pytest.ini` config file:
  ```ini
  [pytest]
  addopts = --ignore=services/auth-service
  ```

---

## 17. Testing Strategy

* **Perimeter Testing**: Run penetration tests carrying SQLi queries to confirm WAF blocks.
* **AI Testing**: Verify Gemini output parsing across 50 simulated applicant records.
* **Regression Tests**: Run `pytest tests/` to confirm all other onboarding/consent/disbursement endpoints pass.

---

## 18. Sprint Deliverables

* Google Cloud Armor dynamic security policies.
* Structured plain-text AI Explainability Tags in CAM response payloads.
* Stable UAT release ready for Release Candidate packaging.

---

## 19. Version 1.1 Release Readiness Targets

| Readiness Metric | Release Target | Verification Method |
| :--- | :---: | :--- |
| **Feature Completion** | 100% | All Version 1.1 user stories marked DONE. |
| **Defect Density** | 0.0 | Zero open Critical/High bugs. |
| **Code Coverage** | >= 80% | Backend coverage report tools. |
| **Performance** | < 1000ms | Load testing API endpoints. |
| **Security** | Clean scan | OWASP and Cloud Armor block rate. |
| **AI Readiness** | 100% parseable tags | Simulated decision test sets. |

---

## 20. Approval Matrix

* **Product Owner**: APPROVED
* **Scrum Master**: APPROVED
* **CTO / Enterprise Architect**: APPROVED
* **Engineering Manager**: APPROVED

---

## 21. Appendix

* Sprint 4 burndown roadmap.
* Cloud Armor policy configuration spreadsheets.
