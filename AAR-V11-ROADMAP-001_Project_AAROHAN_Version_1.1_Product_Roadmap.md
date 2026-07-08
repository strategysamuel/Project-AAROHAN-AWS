# AAR-V11-ROADMAP-001: Project AAROHAN Version 1.1 Product Roadmap

---

## 1. Executive Summary

This document specifies the Version 1.1 Product Roadmap for Project AAROHAN. Following the successful closure of Version 1.0, this strategic blueprint maps future capabilities, technical debt resolutions, architectural upgrades, AI agent integrations, and new Digital Public Infrastructure (DPI) channels.

---

## 2. Vision for Version 1.1

Our vision for Version 1.1 is to evolve Project AAROHAN from a semi-automated embedded lending tool into an active, multi-agent AI lending ecosystem. Version 1.1 will support live, active-active multi-region database operations, native mobile client support, and direct connections to public registries.

---

## 3. Lessons Learned from Version 1.0

* **Environment Separation**: Decoupling sandbox mock configurations from production files prevents manual test adjustments.
* **Module Cache Conflicts**: Isolating dynamic app loaders in python tests avoids import collisions.

---

## 4. Business Drivers

* **Reduced Processing Friction**: Target instant loan approvals for larger credit values.
* **Proactive Risk Management**: Prevent defaults through real-time portfolio alert triggers.
* **Lower Operating Costs**: Save compute resources by automatically scaling services to zero during off-peak windows.

---

## 5. Customer Feedback Themes

* **Session Persistence**: Relationship Managers request extended session timeouts for detailed document checks.
* **Document Auto-parsing**: Desire for automated extraction of unstructured PDF files (e.g., bank statements).

---

## 6. Technical Debt Backlog

* **TD-001 (Pydantic Migration)**: Complete the Pydantic v2 `ConfigDict` upgrades across all auxiliary services.
* **TD-002 (Database Fallbacks)**: Disable SQLite database fallback mechanisms in production runtimes.

---

## 7. Architecture Evolution

Migrate databases to Google Cloud Spanner to enable active-active multi-region setups, replacing the current single-region AlloyDB clusters.

---

## 8. AI Enhancement Roadmap

* **Vertex AI Tuning**: Fine-tune Gemini models using the historical underwriting override datasets.
* **Agentic Workflows**: Integrate custom Agent Development Kit (ADK) pipelines to automate task assignments.

---

## 9. Google Cloud Enhancement Roadmap

* Deploy Google Cloud Armor Advanced rules for DDoS protection.
* Integrate Google Cloud Eventarc triggers to automate messaging workflows.

---

## 10. Security Enhancement Roadmap

Enforce monthly automated IAM permission audits and integrate Secret Manager key rotation pipelines.

---

## 11. Scalability Roadmap

Configure Kubernetes clusters (GKE) to run microservices, replacing Cloud Run for larger scale operations.

---

## 12. Performance Optimization Roadmap

Integrate Redis Cache instances to store static registry queries (such as CKYC lookups) and reduce API latency.

---

## 13. Product Enhancement Backlog

* Build native mobile applications for Relationship Managers.
* Support real-time chat assistants for borrowers.

---

## 14. New Digital Public Infrastructure Integrations

* **RBI Central Fraud Registry**: Auto-check borrower flags.
* **Sahamati Consent Architecture**: Complete compliance updates.
* **ONDC Financial Services**: Join open discount lending networks.

---

## 15. API Modernization

Deploy Apigee Gateway policies to handle advanced rate limiting and client token metrics.

---

## 16. Mobile Application Strategy

Deliver cross-platform React Native apps targeting Android and iOS, enabling RMs to complete registrations on-site.

---

## 17. Analytics & Reporting Enhancements

Integrate Looker dashboards to visualize portfolio default alerts.

---

## 18. Multi-language Support Strategy

Localize portal screens to support regional Indian languages (Hindi, Kannada, Tamil, Telugu, Marathi).

---

## 19. AI Agent Evolution

Deploy autonomous agents to follow up on pending consent requests.

---

## 20. Proposed Epics

* **Epic 1**: Multi-Agent Integration Framework.
* **Epic 2**: Active-Active Database Operations.
* **Epic 3**: RM Mobile App.
* **Epic 4**: Regional Language Support.

---

## 21. Prioritized Feature Backlog

1. **Feature 1**: Rotate Secret Manager keys automatically. (High Priority)
2. **Feature 2**: Connect to RBI Central Fraud Registry. (High Priority)
3. **Feature 3**: Implement GKE deployment profiles. (Medium Priority)
4. **Feature 4**: Localize portals to regional languages. (Low Priority)

---

## 22. Release Planning

* **Version 1.1-M1 (Month 1)**: Complete Pydantic v2 upgrades and Secret Manager auto-rotations.
* **Version 1.1-M2 (Month 3)**: Integrate ONDC and RBI Fraud Registries.
* **Version 1.1-M3 (Month 6)**: Deploy GKE clusters and launch the RM Mobile App.

---

## 23. Risks

* **API Scheme Disruptions**: Downstream live registries changing schemas during active runs.
* **AI Hallucinations**: Gemini generating inaccurate SWOT summaries on incomplete customer data.

---

## 24. Success Metrics

* **Disbursal Latency**: p99 under 5 seconds.
* **System Uptime**: 99.99% availability.
* **Adoption Rate**: 100% RM active usage.

---

## 25. Executive Approval Matrix

| Title | Name | Decision | Signature | Date |
| :--- | :--- | :---: | :---: | :---: |
| **Chief Product Officer (CPO)** | *CPO Name* | **APPROVED** | *Signed* | 2026-07-08 |
| **Chief Technology Officer (CTO)** | *CTO Name* | **APPROVED** | *Signed* | 2026-07-08 |
| **Chief Information Officer (CIO)** | *CIO Name* | **APPROVED** | *Signed* | 2026-07-08 |
| **Chief AI Officer (CAIO)** | *CAIO Name* | **APPROVED** | *Signed* | 2026-07-08 |
| **Enterprise Architect** | *Architect Name* | **APPROVED** | *Signed* | 2026-07-08 |
| **Google Cloud Architect** | *Architect Name* | **APPROVED** | *Signed* | 2026-07-08 |
