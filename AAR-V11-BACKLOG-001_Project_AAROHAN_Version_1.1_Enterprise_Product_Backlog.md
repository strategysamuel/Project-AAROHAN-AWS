# AAR-V11-BACKLOG-001: Project AAROHAN Version 1.1 Enterprise Product Backlog

---

## 1. Executive Summary

This document specifies the Version 1.1 Enterprise Product Backlog for Project AAROHAN. It maps priorities, business values, technical efforts, and dependencies across all development epics planned for the upcoming product cycle.

---

## 2. Product Vision Alignment

The Version 1.1 backlog targets scaling AAROHAN's digital lending pipelines, introducing native mobile support, expanding AI-driven decision safety, and integrating new public registries.

---

## 3. Backlog Management Strategy

The backlog is managed by the Product Management Board. Items are refined bi-weekly during sprint planning and prioritize feature stability, security compliance, and user satisfaction.

---

## 4. Prioritization Framework

Prioritization is governed by the **WSJF (Weighted Shortest Job First)** and **MoSCoW** frameworks, weighing business value, risk reduction, opportunity enablement, and development complexity.

---

## 5. Epic Backlog

* **Epic 1: AI Enhancement**: Fine-tune Gemini scorecards and SWOT compilers.
* **Epic 2: Mobile Banking Experience**: Cross-platform mobile client app for RMs.
* **Epic 3: Advanced Analytics**: Real-time portfolio dashboards.
* **Epic 4: Multi-language Support**: Localizing portal interfaces.
* **Epic 5: AI Agent Evolution**: Task routing automation via ADK.
* **Epic 6: Performance Optimization**: Cache engines and API gateway optimization.
* **Epic 7: Security Enhancement**: Automatic secret rotations.
* **Epic 8: Compliance Automation**: RBI reporting pipelines.
* **Epic 9: Operational Excellence**: Multi-region database replication.
* **Epic 10: Platform Modernization**: Kubernetes orchestration profiles.

---

## 6. Feature Backlog

### Feature ID: F-11-001
* **Title**: Auto Secret Key Rotation
* **Description**: Implement Secret Manager cron job to rotate DB and JWT keys every 90 days.
* **Business Value**: Mitigates security compromise risks and satisfies banking audits.
* **Acceptance Criteria**: Keys rotate automatically, services reload configuration without downtime.
* **Priority**: Must Have (Critical)
* **Estimated Effort**: 3 Story Points
* **Dependencies**: Secret Manager configuration.
* **Risks**: Temporary connectivity lag during rolling restarts.

### Feature ID: F-11-002
* **Title**: RBI Central Fraud Registry Sync
* **Description**: Connect the underwriting engine to the RBI Fraud database to auto-check applicant history.
* **Business Value**: Lowers defaults and flags high-risk accounts early.
* **Acceptance Criteria**: The system queries the registry and rejects blacklisted borrowers.
* **Priority**: Must Have (Critical)
* **Estimated Effort**: 5 Story Points
* **Dependencies**: RBI API credentials.
* **Risks**: Response delay on RBI external APIs.

---

## 7. Technical Debt Backlog

* **TD-11-001**: Complete Pydantic v2 `ConfigDict` schemas migrations across remaining auxiliary services.
* **TD-11-002**: Remove SQLite file fallback from all production environment configurations.

---

## 8. Defect Backlog

* **DF-11-001**: Resolve session timeout alerts for long document review actions.

---

## 9. Innovation Backlog

* Explore blockchain-based invoice registration for TReDS to prevent double-discounting fraud.

---

## 10. Research & Spike Backlog

* **Spike SP-11-001**: Research Google Cloud Spanner multi-region active-active database scaling costs and migration paths.

---

## 11. Infrastructure Backlog

* Configure GKE deployment manifests for microservices.

---

## 12. AI Enhancement Backlog

* Implement offline fine-tuning for CAM SWOT summaries.

---

## 13. Security Enhancement Backlog

* Deploy Advanced Cloud Armor policies to block dynamic web injections.

---

## 14. Google Cloud Modernization Backlog

* Setup Google Cloud Eventarc triggers to automate backend messaging routes.

---

## 15. Release Planning

* **Release v1.1.0 (Q1)**: F-11-001 (Auto Secret Key Rotation) + TD-11-001 (Pydantic Migration).
* **Release v1.1.1 (Q2)**: F-11-002 (RBI Fraud Registry Sync).
* **Release v1.2.0 (Q3)**: Launch GKE clusters and the RM Mobile App.

---

## 16. Product Metrics

* **Approval Cycle Time**: Target under 60 seconds.
* **Default Rate**: Maintain below 1%.
* **User Adoption**: 100% active RM usage.

---

## 17. Risks & Assumptions

* **Assumption**: Downstream live registries maintain stable schemas.
* **Risk**: High latency on Vertex AI endpoints during peak periods.

---

## 18. Governance & Approval

Backlog modifications require authorization from the CPO and CTO during the monthly review.

---

## 19. Appendix

* WSJF calculation spreadsheets.
* Story Points estimation tables.
