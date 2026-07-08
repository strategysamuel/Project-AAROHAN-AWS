# Enterprise Application Architecture

**Document ID:** AAR-APA-008  
**Document Name:** Enterprise Application Architecture  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 (ERDA), AAR-EAV-002 (EAV), AAR-BAR-003 (Business Architecture), AAR-BKA-004 (Banking Architecture), AAR-INA-005 (Information Architecture), AAR-DTA-006 (Data Architecture), AAR-AIA-007 (AI Architecture)  
**Next Artifact:** AAR-IGA-009 (Enterprise Integration Architecture)  
**Target Audience:** IDBI Bank Board, MD & CEO, CIO, CTO, Chief Product Officer, Chief Credit Officer, and Enterprise Architecture Board  
**Document Owner:** Chief Application Architect / Chief Product Officer (CPO)  
**Approval Authority:** Enterprise Architecture Review Board (EARB)  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Application Architect | Initial Release of Enterprise Application Architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Document Metadata & Scope](#document-metadata--scope)
3. [PART 1: Enterprise Application Vision](#part-1-enterprise-application-vision)
4. [PART 2: Application Strategy](#part-2-application-strategy)
5. [PART 3: Enterprise Application Landscape](#part-3-enterprise-application-landscape)
6. [PART 4: Application Capability Mapping](#part-4-application-capability-mapping)
7. [PART 5: Application Collaboration Model](#part-5-application-collaboration-model)
8. [PART 6: Application Service Catalogue](#part-6-application-service-catalogue)
9. [PART 7: Enterprise User Experience Model](#part-7-enterprise-user-experience-model)
10. [PART 8: Application Workflow Architecture](#part-8-application-workflow-architecture)
11. [PART 9: Application Decision Support](#part-9-application-decision-support)
12. [PART 10: Application Security Responsibilities](#part-10-application-security-responsibilities)
13. [PART 11: Application Governance](#part-11-application-governance)
14. [PART 12: Application Portfolio Management](#part-12-application-portfolio-management)
15. [PART 13: Application KPIs](#part-13-application-kpis)
16. [PART 14: Application Risks](#part-14-application-risks)
17. [PART 15: Application Assumptions](#part-15-application-assumptions)
16. [PART 16: Five-Year Application Evolution](#part-16-five-year-application-evolution)
17. [PART 17: Enterprise Application Reference Model](#part-17-enterprise-application-reference-model)
18. [PART 18: Conclusion](#part-18-conclusion)

---

## Executive Summary
This document defines the Enterprise Application Architecture (AAR-APA-008) for Project AAROHAN. It maps the target landscape of front-end portals, underwriting engines, risk platforms, and reporting portals. The ERDA standards ensure that all applications use standardized business rules, reference data models, and decoupled APIs. This setup allows IDBI Bank to scale resources based on transaction volumes.

---

## Document Metadata & Scope
*   **Purpose:** Define the logical application architecture, portfolio classifications, and orchestration paths.
*   **Scope:** Governs all customer-facing applications, internal staff portals, and background processing systems.
*   **Audience:** Board members, MD & CEO, Chief Product Officer, CIO, CTO, and application architects.
*   **Application Vision Statement:** Transition commercial systems from isolated tools to a secure, cognitive application platform.

---

## PART 1: Enterprise Application Vision
*   **Purpose:** Align application development with the bank's strategic MSME business targets.
*   **Application Objective:** Provide a seamless, role-based application interface for customers and staff.
*   **Business Objective:** Drive credit volume growth in priority sector manufacturing and services.
*   **Business Owner:** Chief Product Officer (CPO).
*   **Inputs:** Strategic bank directions, user persona guidelines.
*   **Outputs:** Target state application portfolios.
*   **Dependencies:** Enterprise architecture review board sign-off.
*   **Deliverables:** Application Portfolio Vision Manifesto.
*   **Owner:** Chief Application Architect.
*   **Review Authority:** CIO.
*   **Success Criteria:** Application designs aligned with target operating model roles.

---

## PART 2: Application Strategy
*   **Purpose:** Outline how applications support AI-powered MSME relationship banking.
*   **Business Objective:** Lower operational transaction costs.
*   **Banking Objective:** Underwrite loans using alternate, transaction-level records.
*   **Regulatory Considerations:** Aligns with RBI digital lending guidelines on application interfaces.
*   **Inputs:** System telemetry, customer onboarding logs.
*   **Outputs:** UI design standards, API integrations.
*   **Dependencies:** Model registry connections.
*   **Deliverables:** Application UX & Integration Strategy.
*   **Owner:** Chief Digital Officer (CDO).
*   **Review Authority:** Chief Credit Officer (CCO).
*   **Success Criteria:** Customer onboarding drop-off rate reduced by 50%.

---

## PART 3: Enterprise Application Landscape

The platform maps its application ecosystem across 20 logical systems:

```
  ┌──────────────────────────────────────────────────────────┐
  │                 AAROHAN APPLICATION LANDSCAPE            │
  ├────────────────────────────┬─────────────────────────────┤
  │       User Portals         │    Core Processing Engines  │
  │  - MSME Customer Portal    │  - Credit Appraisal Engine  │
  │  - RM Sales Cockpit        │  - Financial Health Card App│
  ├────────────────────────────┼─────────────────────────────┤
  │     Risk & Monitoring      │    Security & Governance    │
  │  - EWS Alert Console       │  - Admin Control Panel      │
  │  - Portfolio Analytics App │  - Audit Trail Engine       │
  └────────────────────────────┴─────────────────────────────┘
```

*   **User Portals:** Borrower portal, Relationship Manager sales console.
*   **Processing Engines:** Credit scoring, automated document parsing.
*   **Risk & Analytics Portals:** EWS alert console, portfolio stress testing.
*   **Security & Audit Portals:** Admin panel, compliance logs.

---

## PART 4: Application Capability Mapping
*   **Business Capabilities:** Onboarding, Credit, Risk, and Payments.
*   **Banking Capabilities:** Interest calculations, credit limits, and collections.
*   **AI Capabilities:** Text summarization, risk alerts, and credit recommendations.
*   **Information Domains:** Customer profiles, credit files, and compliance records.
*   **Data Domains:** Golden master files, transaction histories, and vector databases.

---

## PART 5: Application Collaboration Model

Applications collaborate asynchronously using secure, event-driven interfaces:

```
  [ Customer Portal ] ──> (Onboarding Event) ──> [ Appraisal Engine ]
                                                        │
  [ Looker Portal ] <── (Report Query) <── [ BigQuery Database ] ◄──┘
```

*   **Customer Portal:** Triggers onboarding events when applications are submitted.
*   **Appraisal Engine:** Processes applications and exports results to databases.
*   **Looker Portal:** Queries analytics databases to generate steering reports.

---

## PART 6: Application Service Catalogue

For every logical system, we define the operational parameters:

### Application Example: Financial Health Platform
*   **Purpose:** Parse financial records to generate verified business health cards.
*   **Business Objective:** Speed up underwriting preparation times.
*   **Banking Objective:** Calculate cash flow coverage and debt service ratios.
*   **Primary Users:** Credit Officers, Underwriters.
*   **Business Owner:** Head of Underwriting.
*   **Major Capabilities:** Bank statements spreading, tax data normalization.
*   **Inputs:** Scanned PDF balance sheets, GSTIN tax logs, AA files.
*   **Outputs:** Business Health Cards, cash-flow coverage ratios.
*   **AI Opportunities:** Classification models and error detection.
*   **Dependencies:** DPI integration APIs.
*   **KPIs:** Analysis TAT, error rate.
*   **Risks:** Registry connection timeouts or data format changes.
*   **Success Criteria:** Calculations completed in < 5 minutes with zero errors.

---

## PART 7: Enterprise User Experience Model
*   **Customers:** Fast, mobile-first interface in regional languages.
*   **RMs:** Sales dashboard showing active client profiles and credit alerts.
*   **Credit Officers:** Pre-compiled credit memos and checklist interfaces.
*   **Executives:** Dashboard reports showing portfolio yields and NPA ratios.

---

## PART 8: Application Workflow Architecture
*   **Onboarding Flow:** Customer registers -> AA fetches statements -> Identity validated -> Limits calculated.
*   **Exception Flow:** System flags policy exception -> File routes to senior underwriter queue -> Underwriter reviews and signs off.

---

## PART 9: Application Decision Support
*   **Human-in-the-Loop (HITL):** Final lending approvals, policy adjustments, and risk parameters must remain under human control.
*   **AI-Assisted:** Systems compile credit memos and checklist summaries for reviewers.
*   **Fully Automated:** Auto-approval for low-risk micro loans where GST and bank statement records are verified.

---

## PART 10: Application Security Responsibilities
*   **User Authentication:** Enforce multi-factor verification and role-based access.
*   **API Security:** Restrict and monitor gateway access using OAuth tokens.
*   **Data Protection:** Mask customer PII across all user-facing frontends.

---

## PART 11: Application Governance
*   **Ownership:** Chief Product Officer owns all active applications and code repositories.
*   **Change Management:** All modifications must be submitted as ADR files.
*   **Release Rules:** Security scans and unit tests are required before release.

---

## PART 12: Application Portfolio Management
*   **Strategic:** Customer Portal, RM Workspace, Credit Appraisal Engine.
*   **Core:** Account management, payment clearing, interest engines.
*   **Supporting:** Support desk triage, notification dispatchers.
*   **Emerging:** Financial digital twins, agent-guided negotiations.

---

## PART 13: Application KPIs

AAROHAN monitors and reports KPIs across four application dimensions:

| Category | KPI | Target Baseline | Formula |
| :--- | :--- | :---: | :--- |
| **Availability** | System Uptime | > 99.99% | $\text{System Runtime} / \text{Total Schedule}$ |
| **Adoption** | Active User Ratio | > 85% | $\text{Daily Active Users} / \text{Registered Users}$ |
| **Productivity** | RM Processing Capacity | +50% | $\text{Accounts Per RM} - \text{Baseline Capacity}$ |
| **Efficiency** | STP Rate | > 80% | $\text{STP Approvals} / \text{Total Approvals}$ |

---

## PART 14: Application Risks
*   **Integration Timeout:** External registry connection timeouts may delay onboarding.
*   **User Friction:** Complexity in mobile interfaces may increase drop-off rates.
*   **Vulnerability Risk:** Software security flaws may lead to data exposure.

---

## PART 15: Application Assumptions
*   **API Gateway:** Assume Apigee gateways maintain stable connection services.
*   **System Replicas:** Assume database read-replicas handle analytics queries without lag.
*   **Staff Training:** Assume relationship managers adopt and use CRM portal features.

---

## PART 16: Five-Year Application Evolution
*   **Year 1-2 (Integrated Apps):** Complete alternate data pipeline integrations (GST, AA, EPFO).
*   **Year 3-4 (Intelligent Apps):** Deploy real-time risk scoring and conversational reporting engines.
*   **Year 5 (Autonomous Platform):** Self-learning credit scoring networks operating within human validation.

---

## PART 17: Enterprise Application Reference Model

The reference model connects all application components:

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   AAROHAN APPLICATION REFERENCE MODEL                  │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 1. Portals: Borrower portal, RM mobile CRM, Looker dashboards          │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 2. Processing Engines: Credit scorer, document parser, risk monitor    │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 3. Common Services: Workflow workflows, API proxies, payment gateways  │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 4. Infrastructure: Cloud Run containers, AlloyDB and BigQuery databases│
  └────────────────────────────────────────────────────────────────────────┘
```

*   **Portals:** Direct client and internal staff operating interfaces.
*   **Processing Engines:** Underwriting, risk, and analytics services.
*   **Common Services:** Shared components like payments and alerts.

---

## PART 18: Conclusion
*   **Purpose:** Conclude the Enterprise Application Architecture document.
*   **Business Objective:** Approve the target business application classifications and lifecycles.
*   **Banking Objective:** Align data stewardship and quality audits under a single framework.
*   **Regulatory Considerations:** Prepares the platform for regulatory inspects.
*   **Deliverables:** Approved Application Reference Architecture.
*   **Owner:** Chief Application Architect.
*   **Review Authority:** Board of Directors.
