# Enterprise AI Architecture & Operating Model

**Document ID:** AAR-AIA-007  
**Document Name:** Enterprise AI Architecture & Operating Model  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 (ERDA), AAR-EAV-002 (EAV), AAR-BAR-003 (Business Architecture), AAR-BKA-004 (Banking Architecture), AAR-INA-005 (Information Architecture), AAR-DTA-006 (Data Architecture)  
**Next Artifact:** AAR-APA-008 (Enterprise Application Architecture)  
**Target Audience:** IDBI Bank Board, MD & CEO, Executive Directors, Chief AI Officer, CIO, CTO, Chief Risk Officer, and AI Governance Committee  
**Document Owner:** Chief AI Officer (CAIO)  
**Approval Authority:** AI Governance Committee (AIGC)  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief AI Officer | Initial Release of Enterprise AI Architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Document Metadata & Scope](#document-metadata--scope)
3. [PART 1: Enterprise AI Vision](#part-1-enterprise-ai-vision)
4. [PART 2: AI Strategy for MSME Banking](#part-2-ai-strategy-for-msme-banking)
5. [PART 3: Enterprise AI Principles](#part-3-enterprise-ai-principles)
6. [PART 4: AI Operating Model](#part-4-ai-operating-model)
7. [PART 5: Enterprise AI Capability Model](#part-5-enterprise-ai-capability-model)
8. [PART 6: Enterprise AI Use Case Catalogue](#part-6-enterprise-ai-use-case-catalogue)
9. [PART 7: Enterprise AI Agent Architecture](#part-7-enterprise-ai-agent-architecture)
10. [PART 8: Enterprise Decision Intelligence Framework](#part-8-enterprise-decision-intelligence-framework)
11. [PART 9: AI Governance Framework](#part-9-ai-governance-framework)
12. [PART 10: Responsible AI Framework](#part-10-responsible-ai-framework)
13. [PART 11: Enterprise Prompt Governance](#part-11-enterprise-prompt-governance)
14. [PART 12: Enterprise AI Data Consumption](#part-12-enterprise-ai-data-consumption)
15. [PART 13: Enterprise Explainability Framework](#part-13-enterprise-explainability-framework)
16. [PART 14: AI Security Architecture](#part-14-ai-security-architecture)
17. [PART 15: Enterprise AI Monitoring](#part-15-enterprise-ai-monitoring)
18. [PART 16: Enterprise AI KPIs](#part-16-enterprise-ai-kpis)
19. [PART 17: Regulatory AI Architecture](#part-17-regulatory-ai-architecture)
20. [PART 18: Enterprise AI Risks](#part-18-enterprise-ai-risks)
21. [PART 19: Enterprise AI Assumptions](#part-19-enterprise-ai-assumptions)
22. [PART 20: Five-Year Enterprise AI Roadmap](#part-20-five-year-enterprise-ai-roadmap)
23. [PART 21: Enterprise AI Reference Architecture](#part-21-enterprise-ai-reference-architecture)
24. [PART 22: Conclusion](#part-22-conclusion)

---

## Executive Summary
This document establishes the Enterprise AI Reference Architecture and Operating Model (AAR-AIA-007) for Project AAROHAN. It defines the governance frameworks, specialized agent coordinates, decision intelligence boundaries, explainability models, and MLOps metrics needed to operate an AI-native banking ecosystem. The ERDA guidelines ensure that all AI models, prompts, and agentic tools remain explainable, auditable, safe, and aligned with RBI digital lending directives.

---

## Document Metadata & Scope
*   **Purpose:** Establish the banking reference guidelines for AI models, prompts, agentic tools, and MLOps monitoring.
*   **Scope:** Governs all Large Language Models (LLMs), machine learning models, prompt databases, and automated workflows.
*   **Audience:** Board members, MD & CEO, Chief AI Officer, CIO, CTO, risk heads, and compliance auditors.
*   **AI Vision Statement:** Transition credit operations from rule-based automation to a self-learning, autonomous banking ecosystem under human audit control.

---

## PART 1: Enterprise AI Vision
*   **Purpose:** Align technology developments with the bank's long-term business goals.
*   **Business Objective:** Drive credit volume growth in priority sector manufacturing and services.
*   **Banking Objective:** Move to self-optimizing risk underwriting engines.
*   **Regulatory Considerations:** Aligns with national data protection and safety laws.
*   **Inputs:** Strategic bank directions, regulatory mandates.
*   **Outputs:** Target state AI operating models.
*   **Dependencies:** Executive sponsor sign-off.
*   **Deliverables:** AI Strategy & Vision Document.
*   **Owner:** Chief AI Officer (CAIO).
*   **Review Authority:** AI Governance Committee.
*   **Success Criteria:** AI target models aligned with national safety guidelines.

---

## PART 2: AI Strategy for MSME Banking
*   **Purpose:** Outline how artificial intelligence supports commercial lending operations.
*   **Business Objective:** Lower operational transaction costs.
*   **Banking Objective:** Underwrite loans using alternate, transaction-level records.
*   **Regulatory Considerations:** Aligns with RBI digital lending guidelines on automated credit.
*   **Inputs:** System telemetry, credit scoring reports.
*   **Outputs:** AI model registries.
*   **Dependencies:** Model registry connections.
*   **Deliverables:** AI Banking Strategy.
*   **Owner:** Chief AI Officer (CAIO).
*   **Review Authority:** Chief Credit Officer (CCO).
*   **Success Criteria:** Underwriting decision turnaround times reduced to minutes.

---

## PART 3: Enterprise AI Principles
1.  **Human Accountability (HITL):** Final lending authorizations, policy adjustments, and risk parameters must remain under human control.
2.  **Explainability:** AI recommendations must generate a natural-language reason chain mapping back to verified policy databases.
3.  **Bias Prevention:** Models must undergo weekly fairness checks to prevent demographic or regional discrimination.
4.  **Security by Default:** Restrict model access and protect pipelines from prompt-injection threats.

---

## PART 4: AI Operating Model
*   **Model Ownership:** The Chief AI Officer owns all active models and prompt files.
*   **Operations Rhythm:** The AI Governance Committee meets weekly to review safety logs and performance metrics.
*   **Lifecycles:** Standard pipelines for model training, testing, promotion, and archiving.

---

## PART 5: Enterprise AI Capability Model

AAROHAN uses a structured, three-level capability layout:

### L1: Cognitive Underwriting & Analytics
*   **L2: Natural Language Parsing**
    *   *L3: Document Intelligence Summarization*
        *   *Purpose:* Summarize complex tax and financial files into structured text.
        *   *Business Objective:* Lower operational transaction costs.
        *   *Banking Objective:* Automate the compilation of underwriting files.
        *   *AI Owner:* Lead AI Engineer.
        *   *Inputs:* Scanned PDFs, balance sheets.
        *   *Outputs:* Structured JSON text summaries.
        *   *Human Oversight:* Underwriters must review and confirm summary accuracy.
        *   *Explainability Requirement:* Summaries must cite specific page and line numbers.
        *   *Regulatory Mapping:* RBI digital lending and compliance rules.
        *   *Risks:* Model hallucinations or data truncation.
        *   *KPIs:* Translation accuracy index.
        *   *Success Criteria:* Summaries completed in < 1 minute with zero discrepancies.
*   **L2: Risk Forecasting**
    *   *L3: Dynamic Risk Scoring*
        *   *Purpose:* Recalculate credit ratings based on current transaction logs.
        *   *Business Objective:* Lower credit defaults.
        *   *Banking Objective:* Provide real-time early warning signal updates.
        *   *AI Owner:* Lead Data Scientist.
        *   *Inputs:* GST tax logs, bank statement transactions.
        *   *Outputs:* Updated risk index metrics.
        *   *Human Oversight:* Risk managers approve rate or limit adjustments.
        *   *Explainability Requirement:* Output must list key factors driving risk shifts.
        *   *Regulatory Mapping:* RBI model risk management guidelines.
        *   *Risks:* Concepts drift or incorrect data inputs.
        *   *KPIs:* NPA reduction, prediction accuracy.
        *   *Success Criteria:* Risk shifts identified 45 days before default.

---

## PART 6: Enterprise AI Use Case Catalogue
*   **Financial Health Card Generator:** Evaluates tax and bank logs to build a live business health card.
*   **Credit Memo Assistant (CAM):** Compiles pre-underwritten loan files with grounding citations.
*   **EWS Risk Engine:** Checks transaction variations daily to flag early warning signals (EWS).
*   **Fraud Detection Engine:** Document AI runs metadata checks on uploads to identify potential forgery.

---

## PART 7: Enterprise AI Agent Architecture

Specialized agents coordinate to resolve underwriting tasks:

```
  [ Customer Assistant Agent ] ──> [ Fraud & Identity Agent ] ──> [ Underwriter Agent ]
                                                                        │
  [ Executive Advisor Agent ] <── [ Portfolio Risk Agent ] <────────────┘
```

*   **Relationship Manager Agent:** Generates client reports, status alerts, and drafts proposals.
*   **Underwriter Agent:** Runs the underwriting rule checks and compiles credit memos.
*   **Risk Agent:** Reviews transaction logs and flags early warning signal (EWS) alerts.
*   **Executive Advisor Agent:** Translates Looker dashboard metrics into qualitative briefings.

---

## PART 8: Enterprise Decision Intelligence Framework
*   **Fully Automated Decisions:** Auto-approvals for low-ticket micro loans where GST and bank statement records are verified.
*   **Assisted AI Decisions:** Underwriting agents compile credit dossiers for underwriters to review and approve.
*   **Human Override:** Underwriters can override AI scores with written justifications.
*   **Audit Trail:** Decisional chains are logged in write-once audit databases.

---

## PART 9: AI Governance Framework
*   **Governance Committee:** Meets weekly to review drift alerts, safety triggers, and compliance performance.
*   **Prompt Governance:** All prompts must pass unit testing and safety audits before production release.
*   **Recertification:** Models are retrained and recertified quarterly to align with active market conditions.

---

## PART 10: Responsible AI Framework
*   **Fairness:** Enforce weekly checks to ensure scoring models do not apply demographic bias.
*   **Transparency:** All decisions must present natural-language reason chains.
*   **Human Oversight:** High-risk files, overrides, and customer appeals route directly to human experts.

---

## PART 11: Enterprise Prompt Governance
*   **Standard Categorization:** System prompts, Risk check prompts, Credit spreading prompts.
*   **Version Control:** Prompts are managed in Git and tagged with semantic version numbers (Major.Minor.Patch).
*   **Testing Pipelines:** Automated verification of prompt outputs before release.

---

## PART 12: Enterprise AI Data Consumption
*   **GSTN & AA Feeds:** Ingested daily to update risk profiles and cash flow projections.
*   **EPFO & ESIC Logs:** Checked to confirm active employer payroll contributions.
*   **Internal Core Ledgers:** Ingested to track active loan repayment histories.

---

## PART 13: Enterprise Explainability Framework
*   **Feature Importance:** Output must show which parameters (e.g., invoice value, utility delay) drove the credit decision.
*   **Audit Evidence:** Explanation trails are saved as read-only metadata records for external regulators.

---

## PART 14: AI Security Architecture
*   **Prompt Injection Defense:** Verify and sanitize inputs on all client-facing text portals.
*   **Data Leakage Prevention:** Mask and block sensitive customer PII from model logs.
*   **Abuse Monitoring:** Tracks API transaction spikes to block potential denial of service attacks.

---

## PART 15: Enterprise AI Monitoring
*   **MLOps Dashboard:** Vertex AI monitors track data drift, conceptual changes, and accuracy metrics.
*   **Automatic Rollbacks:** System triggers automatic rollbacks to stable model versions when drift thresholds are breached.

---

## PART 16: Enterprise AI KPIs

AAROHAN monitors and reports KPIs across four AI dimensions:

| Category | KPI | Target Baseline | Formula |
| :--- | :--- | :---: | :--- |
| **Model Quality** | Drift Index | < 0.1 | $\text{Drift Deviation} / \text{Baseline Deviation}$ |
| **Safety** | Safety Filter Triggers | 0 | $\text{safety violations} / \text{Total Queries}$ |
| **Performance** | Recommendation Acceptance | > 85% | $\text{Accepted AI Recs} / \text{Total AI Recs}$ |
| **Explainability**| Explanation Availability | 100% | $\text{Explained Decisions} / \text{Total Decisions}$ |

---

## PART 17: Regulatory AI Architecture
*   **RBI Guidelines:** Direct fund routing; only consented data pulled from registries.
*   **Data Privacy (DPDP Act):** Secure consent profiles stored in database registries.
*   **Model Governance:** Grounded, explainable decision paths logged for audit.

---

## PART 18: Enterprise AI Risks
*   **Hallucination Risk:** Models may generate incorrect recommendations.
*   **Data Drift Risk:** Shift in borrower transaction patterns may skew scoring indices.
*   **Abuse Risk:** Risk of prompt-injection or unauthorized model querying.

---

## PART 19: Enterprise AI Assumptions
*   **Vertex AI SLA:** Assume Google Cloud AI platforms maintain stable services.
*   **Accuracy Baseline:** Assume model training datasets are representative.
*   **Staff Adoption:** Assume credit officers adopt and trust AI-generated recommendations.

---

## PART 20: Five-Year Enterprise AI Roadmap
*   **Phase 1 (2026-2027):** Automated document spreading, basic credit scoring, and AA integration.
*   **Phase 2 (2028-2029):** Real-time invoice financing (TReDS), dynamic limits calculation, and CRM AI tools.
*   **Phase 3 (2030-2031):** Multi-agent underwriting coordinates, and EWS alerts integrated.
*   **Phase 4 (2032-2033):** Financial digital twins, and embedded finance portals launched.
*   **Phase 5 (2034-2035):** Fully autonomous credit checks under human audit control.

---

## PART 21: Enterprise AI Reference Architecture

The reference model connects all AI components:

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                     AAROHAN AI REFERENCE MODEL                         │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 1. Ingestion: Consented GST/AA API records                              │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 2. Compute Runtime: Cloud Run microservices hosting ADK agents         │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 3. ML Engine: Vertex AI model registry, safety filters, prompt DB      │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 4. Output Layer: Grounded CAM dossiers, EWS alerts, RM suggestions      │
  └────────────────────────────────────────────────────────────────────────┘
```

*   **Registry Adapter:** Expose and route services using secure gateways.
*   **Analytics Layer:** Process transaction files using BigQuery and Looker dashboards.
*   **Security & Compliance:** Log all approvals and access histories in write-once audit stores.

---

## PART 22: Conclusion
*   **Purpose:** Conclude the Enterprise AI Architecture document.
*   **Business Objective:** Approve the target business AI classifications and lifecycles.
*   **Banking Objective:** Align MLOps data stewardship and quality audits under a single framework.
*   **Regulatory Considerations:** Prepares the platform for regulatory inspects.
*   **Deliverables:** Approved AI Reference Architecture.
*   **Owner:** Chief AI Officer (CAIO).
*   **Review Authority:** Board of Directors.
