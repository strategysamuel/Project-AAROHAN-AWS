# Enterprise Business Requirements Document (BRD)

**Document ID:** AAR-BRD-014  
**Document Name:** Enterprise Business Requirements Document  
**Version:** 1.0  
**Status:** Ready for Board Approval  
**Dependencies:** AAR-ERDA-001 through AAR-EARB-013 (All Architecture Volumes)  
**Target Audience:** IDBI Bank Board, Business Heads, Google Cloud Architects, and Delivery Teams  
**Document Owner:** Chief Product Officer (CPO)  
**Approval Authority:** Executive Committee / C-Suite Board  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Product Management Office | Initial Release of Business Requirements Document. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Business Objectives & Drivers](#business-objectives--drivers)
3. [Scope and Business Personas](#scope-and-business-personas)
4. [Business Capabilities & Functions](#business-capabilities--functions)
5. [Functional Requirements & GCP Service Mapping](#functional-requirements--gcp-service-mapping)
6. [Non-Functional Requirements (Business View)](#non-functional-requirements-business-view)
7. [Reporting, Analytics & AI Requirements](#reporting-analytics--ai-requirements)
8. [Digital Public Infrastructure & Alternate Data Requirements](#digital-public-infrastructure--alternate-data-requirements)
9. [Product Module Business Requirements](#product-module-business-requirements)
10. [Governance, Risk & Compliance Requirements](#governance-risk--compliance-requirements)
11. [Acceptance Criteria & Success Metrics](#acceptance-criteria--success-metrics)
12. [Business Traceability Matrix](#business-traceability-matrix)
13. [Glossary & Appendices](#glossary--appendices)

---

## Executive Summary
This document defines the Enterprise Business Requirements Document (AAR-BRD-014) for Project AAROHAN. It translates approved enterprise architectures into functional specifications for IDBI Bank's cash-flow commercial lending platform. The document also maps these requirements to native Google Cloud services (such as Vertex AI, BigQuery, AlloyDB, and Apigee) to guide the implementation teams.

---

## Business Objectives & Drivers
*   **Turnaround Time (TAT) Reduction:** Reduce credit underwriting decisions from several days to under 30 minutes.
*   **Priority Sector Lending (PSL):** Expand lending volumes to micro and small enterprises (manufacturing and services) using alternate data.
*   **Risk Minimization:** Establish early warning indicators to keep overall portfolio NPA ratios below 2.0%.

---

## Scope and Business Personas
*   **In Scope:** Onboarding, alternate data spreading (GST/AA), credit checks, automated credit memo compilation, early warning dashboards, and consent management.
*   **Out of Scope:** Core database migrations, physical server provisioning, and non-MSME retail banking portals.
*   **Personas:** Borrower, Relationship Manager, Underwriter, Risk Officer, Compliance Manager, Executive, and Audit Lead.

---

## Business Capabilities & Functions
*   **Origination:** Verification of customer registrations (UIDAI, CKYC, PAN, Udyam) and consent capture.
*   **Underwriting:** Cash flow spread sheet compilation, scoring calculators, and policy verification checklists.
*   **Portfolio Management:** Early warning alert routing, concentration monitoring, and regulatory reporting.

---

## Functional Requirements & GCP Service Mapping

### FR-001: Digital Customer Onboarding
*   **Requirement ID:** FR-001
*   **Priority:** High
*   **Business Value:** Lowers customer acquisition cost and limits lead drop-offs.
*   **Business Owner:** Head of Digital Banking.
*   **Description:** Allow borrowers to register and verify identity credentials digitally using national registries.
*   **Acceptance Criteria:** KYC and registration validations completed in < 2 minutes.
*   **Dependencies:** Apigee integration availability.
*   **AI Opportunity:** Document AI structures scanned certificates.
*   **Future Google Cloud Service Mapping:** Apigee, Firebase Authentication, Identity Platform, Document AI.
*   **KPIs:** Onboarding completion rate, verification TAT.

---

### FR-002: Alternate Data Spreading
*   **Requirement ID:** FR-002
*   **Priority:** High
*   **Business Value:** Eliminates manual data entry errors and accelerates credit scoring.
*   **Business Owner:** Head of Underwriting.
*   **Description:** Automatically retrieve and normalize bank statements and tax logs (GSTN, AA).
*   **Acceptance Criteria:** Compile 12-month cash-flow spreads in < 3 minutes.
*   **Dependencies:** Customer consent validation.
*   **AI Opportunity:** Anomaly detection models identify transaction variances.
*   **Future Google Cloud Service Mapping:** AlloyDB, BigQuery, Vertex AI, Cloud Workflows.
*   **KPIs:** Spreading TAT, calculation accuracy.

---

### FR-003: Relationship Manager Copilot
*   **Requirement ID:** FR-003
*   **Priority:** Medium
*   **Business Value:** Boosts RM productivity and conversion rates.
*   **Business Owner:** Head of Relationship Banking.
*   **Description:** An AI co-pilot that assists RMs by highlighting customer profiles, generating alert notices, and drafting proposals.
*   **Acceptance Criteria:** Proposals and summaries generated in < 15 seconds.
*   **Dependencies:** CRM database integrations.
*   **AI Opportunity:** Gemini templates generate personalized emails and customer cards.
*   **Future Google Cloud Service Mapping:** Vertex AI Agent Engine, Gemini, Agent Development Kit (ADK), Model Context Protocol (MCP).
*   **KPIs:** Lead conversion rate, RM admin hours.

---

### FR-004: Early Warning System (EWS)
*   **Requirement ID:** FR-004
*   **Priority:** High
*   **Business Value:** Lowers NPA rates by predicting defaults early.
*   **Business Owner:** Chief Risk Officer (CRO).
*   **Description:** Continuous checks on customer transaction patterns to identify payment anomalies.
*   **Acceptance Criteria:** Generate warnings 45 days before potential default.
*   **Dependencies:** Analytics pipeline availability.
*   **AI Opportunity:** Classification models flag anomalous tax or payment delays.
*   **Future Google Cloud Service Mapping:** Vertex AI, BigQuery, Looker, Pub/Sub.
*   **KPIs:** Warning detection window, Gross NPA.

---

## Non-Functional Requirements (Business View)
*   **Uptime Availability:** Target system availability > 99.99% during business hours.
*   **Performance Latency:** User dashboard load times kept under 2 seconds.
*   **Accessibility:** Multilingual support across mobile and web portals.

---

## Reporting, Analytics & AI Requirements
*   **Executive Dashboards:** Unified Looker dashboards tracking NIM growth, credit metrics, and PSL targets.
*   **AI Explainability:** Underwriting recommendations must generate a natural-language reason chain mapping back to verified policy files.

---

## Digital Public Infrastructure & Alternate Data Requirements
*   **Consent Gateways:** Integrations with Account Aggregator and ULI registries.
*   **Tax Integrations:** GSTN database connectors to verify customer sales invoices.

---

## Product Module Business Requirements
*   **Working Capital Lines:** Limits calculated using the Nayak turnover method (fixed 25% of projected sales).
*   **Trade Finance:** Real-time financing of GSTR invoice receivables through TReDS integration.

---

## Governance, Risk & Compliance Requirements
*   **Consent Management:** Maintain active customer authorization profiles in secure database tables.
*   **DPDP Compliance:** Automated erasure of active query tokens upon customer request.

---

## Acceptance Criteria & Success Metrics
*   **Underwriting TAT:** Credit memos prepared in < 30 minutes.
*   **STP Rate:** Straight-Through-Processing rate > 80% for micro loans.
*   **Gross NPA:** NPA ratio kept under 2.0%.

---

## Business Traceability Matrix

This matrix traces requirements to strategic business goals:

| Requirement ID | Strategic Goal | Functional Module | GCP Target Service |
| :--- | :--- | :--- | :--- |
| **FR-001** | Onboarding TAT < 15 mins | Customer Registration | Apigee, Firebase |
| **FR-002** | Underwriting TAT < 30 mins | Credit Appraisal Engine | AlloyDB, BigQuery |
| **FR-003** | Lead Conversion +25% | RM CRM Dashboard | Gemini, ADK |
| **FR-004** | Portfolio NPA < 2.0% | EWS Alert Console | BigQuery, Looker |

---

## Glossary & Appendices
*   **AA:** Account Aggregator Framework.
*   **ULI:** Unified Lending Interface.
*   **GSTN:** GST Network.
*   **NTC:** New to Credit.
*   **CAM:** Credit Assessment Memorandum.
