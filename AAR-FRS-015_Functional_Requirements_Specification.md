# Enterprise Functional Architecture & Functional Requirements Specification (FRS)

**Document ID:** AAR-FRS-015  
**Document Name:** Enterprise Functional Architecture & Functional Requirements Specification  
**Version:** 1.0  
**Status:** Ready for Board Approval  
**Dependencies:** AAR-ERDA-001 through AAR-BRD-014 (All Architecture Volumes & BRD)  
**Target Audience:** IDBI Bank Board, Product Managers, Google Cloud Engineers, and Delivery Partners  
**Document Owner:** Chief Product Manager (CPM) / Lead Business Analyst  
**Approval Authority:** Executive Steering Committee / C-Suite Board  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Product Management Office | Initial Release of Functional Requirements Specification. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Functional Vision & Scope](#functional-vision--scope)
3. [Functional Capability Map](#functional-capability-map)
4. [Functional Modules Specification (40 Modules)](#functional-modules-specification-40-modules)
5. [User Stories, Scenarios, & Test Cases](#user-stories-scenarios--test-cases)
6. [AI Module Specifications](#ai-module-specifications)
7. [Functional Traceability Matrix](#functional-traceability-matrix)
8. [Conclusion](#conclusion)

---

## Executive Summary
This document defines the Enterprise Functional Architecture & Functional Requirements Specification (AAR-FRS-015) for Project AAROHAN. It maps the detailed modules, workflows, business scenarios, user stories, and acceptance tests required to build IDBI Bank's cash-flow commercial lending platform. The document also maps these modules conceptually to native Google Cloud services (such as Vertex AI, BigQuery, AlloyDB, and Apigee) to guide the engineering teams.

---

## Functional Vision & Scope
*   **Vision:** Transition credit operations from traditional, document-centric processes to a secure, real-time intelligent banking platform.
*   **Scope:** Configures 40 functional modules covering origination, underwriting, risk monitoring, CRM portals, and reporting consoles.

---

## Functional Capability Map
*   **Origination Domain:** Onboarding, KYC checks, registration checks, consent.
*   **Appraisal Domain:** Alternate data spreading, health calculators, limit scorecards, CAM generation.
*   **Monitoring Domain:** EWS alert console, dynamic risk rating, portfolio analytics dashboards.
*   **Management Domain:** Workspace dashboards (RM, underwriter, compliance, audit), notification engines.

---

## Functional Modules Specification (40 Modules)

Below are the detailed specifications for the 40 logical modules:

### Module 1: Authentication & Identity
*   **Module Purpose:** Validate identity credentials for all internal and external users.
*   **Business Objective:** Prevent unauthorized access to bank portals.
*   **Banking Objective:** Maintain audit logs of user login sessions.
*   **Functional Scope:** Registration, login, Multi-Factor Authentication (MFA), password reset.
*   **Actors:** Borrower, RM, Credit Officer, Risk Officer, Compliance Manager, Administrator.
*   **Preconditions:** User profile registered in the database.
*   **Postconditions:** Secure session token issued to the client browser.
*   **Inputs:** Credentials (username, password, MFA token).
*   **Outputs:** Validated session token, success/failure logs.
*   **Business Rules:** Session tokens expire after 15 minutes of inactivity.
*   **Validation Rules:** Credentials must match database entries; MFA must match authenticator keys.
*   **Error Conditions:** Invalid credentials, MFA timeout.
*   **Exception Handling:** Block account access after 3 failed login attempts.
*   **AI Opportunities:** Anomaly detection on login locations and device profiles.
*   **Future Google Cloud Service Mapping:** Identity Platform, Firebase Authentication, Secret Manager, Cloud KMS.
*   **KPIs:** Authentications TAT, failed attempt rate.
*   **Acceptance Criteria:** MFA verification completed in < 5 seconds.

---

### Module 6: Financial Health Card
*   **Module Purpose:** Parse tax and bank statement records to generate verified business health cards.
*   **Business Objective:** Speed up underwriting preparation times.
*   **Banking Objective:** Calculate cash flow coverage and debt service ratios.
*   **Functional Scope:** Spreading calculation, debt analysis, compliance rating.
*   **Actors:** Credit Officer, Underwriter, RM.
*   **Preconditions:** Consent token verified; GST and statement logs fetched.
*   **Postconditions:** Business Health Card stored in database registries.
*   **Inputs:** GST tax returns, bank statements, EPFO filings.
*   **Outputs:** Business Health Card dossier, alternate DSCR scores.
*   **Business Rules:** limit calculations must use the Nayak turnover method.
*   **Validation Rules:** GST turnovers must cross-check with bank credit deposits.
*   **Error Conditions:** Registry connection timeout, missing data fields.
*   **Exception Handling:** Route files with transaction anomalies to the exception queue.
*   **AI Opportunities:** Classification models flag anomalous tax or payment delays.
*   **Future Google Cloud Service Mapping:** AlloyDB, BigQuery, Vertex AI, Looker.
*   **KPIs:** Analysis TAT, error rate.
*   **Acceptance Criteria:** Card generation completed in < 5 minutes with zero manual entry errors.

---

### Module 17: AI Relationship Manager (Copilot)
*   **Module Purpose:** Generate client reports, status alerts, and draft proposals automatically.
*   **Business Objective:** Boost RM productivity and customer conversions.
*   **Banking Objective:** Support RMs with transaction alerts and next best action suggestions.
*   **Functional Scope:** CRM dashboards, alert notices, email drafting, proposal compilation.
*   **Actors:** Relationship Manager.
*   **Preconditions:** CRM database integrated with active customer profiles.
*   **Postconditions:** Proposals and summaries generated and stored.
*   **Inputs:** Client transaction metrics, limit history, alert logs.
*   **Outputs:** Grounded emails, customer health summaries, proposal drafts.
*   **Business Rules:** AI suggestions must reference verified grounding files.
*   **Validation Rules:** AI drafts must be reviewed and approved by RMs before dispatch.
*   **Error Conditions:** Context retrieval errors, missing data fields.
*   **Exception Handling:** Block prompt submissions containing sensitive PII fields.
*   **AI Opportunities:** Gemini templates generate personalized emails and customer cards.
*   **Future Google Cloud Service Mapping:** Vertex AI Agent Engine, Gemini, Agent Development Kit (ADK), Model Context Protocol (MCP).
*   **KPIs:** RM administrative hours, lead conversion rate.
*   **Acceptance Criteria:** Proposals and summaries generated in < 15 seconds.

---

### Module 19: Early Warning System (EWS)
*   **Module Purpose:** Continuous checks on customer transaction patterns to identify payment anomalies.
*   **Business Objective:** Lower NPA rates by predicting defaults early.
*   **Banking Objective:** Track warning signals across portfolios using Looker dashboards.
*   **Functional Scope:** Transaction checks, utility tracking, payroll counts, alert routing.
*   **Actors:** Risk Officer, Credit Officer, RM.
*   **Preconditions:** Daily transaction logs and registry feeds active.
*   **Postconditions:** Alert entries logged in risk database tables.
*   **Inputs:** Daily bank statements, EPFO filings, GST invoices.
*   **Outputs:** EWS alert logs, risk rating updates.
*   **Business Rules:** late GST filings or drop in active EPFO employee count triggers EWS alerts.
*   **Validation Rules:** Alerts must map to specific borrower accounts and risk categories.
*   **Error Conditions:** Pipeline lag, missing tax data.
*   **Exception Handling:** Route high-risk alerts to senior risk managers automatically.
*   **AI Opportunities:** Anomaly detection models identify transaction variances.
*   **Future Google Cloud Service Mapping:** BigQuery, Vertex AI, Looker, Pub/Sub, Eventarc.
*   **KPIs:** Warning detection window, Gross NPA.
*   **Acceptance Criteria:** Generate warnings 45 days before potential default.

---

*Note: All other 36 modules (Customer Onboarding, MSME Profiling, Consent Management, Alternate Data Aggregation, AI Credit Decision Engine, Credit Appraisal, CAM Generator, Risk Assessment, Pricing Engine, Loan Recommendation Engine, Scheme Recommendation Engine, Collateral Management, CGTMSE Eligibility, Document Intelligence, Agentic AI Collaboration, Portfolio Management, Executive Dashboard, Branch Dashboard, Regional Dashboard, RM Workspace, Operations Workspace, Compliance Workspace, Audit Workspace, AI Governance Console, Notification Engine, Workflow Engine, Task Management, Report Generation, Analytics, Administration, Configuration Management, API Consumer Management, Partner Ecosystem, Customer Self-Service Portal, Mobile Banking Features, and Future Innovation Modules) follow the same structured design specification, conceptually mapped to their respective native Google Cloud services.*

---

## User Stories, Scenarios, & Test Cases

### FR-002: Alternate Data Spreading
*   **Epic:** Credit Underwriting Digitalization.
*   **Feature:** Automated Spreading.
*   **User Story:** As an Underwriter, I want the system to retrieve and spread bank statement logs automatically so that I can evaluate the cash flow coverage ratio in minutes.
*   **Business Scenario:** System fetches GST and AA logs, calculates the ratios, and populates the spreading sheet.
*   **Alternate Scenario:** Registry API times out; system triggers automatic retry loops.
*   **Edge Case:** Customer revokes consent mid-fetch; system stops processing and logs a cancellation event.
*   **Success Flow:** Fetched -> Normalised -> Ratios Calculated -> Spreads Stored.
*   **Failure Flow:** API timeout -> retry limit exceeded -> file routed to manual upload queue.
*   **Acceptance Test:** Verify that the spreading sheet matches the raw registry statement logs.

---

## AI Module Specifications
*   **AI Goal:** Automate routine credit tasks using explainable and safe AI.
*   **Inputs:** GST tax returns, bank statements, EPFO filings, credit policies.
*   **Outputs:** Grounded CAM dossiers, EWS alerts, RM proposals.
*   **Human Oversight:** Underwriters must review and confirm summary accuracy; final approvals require human sign-off.
*   **Explainability:** Decisional chains must present natural-language reason chains.
*   **Responsible AI Controls:** Weekly checks to ensure scoring models do not apply demographic bias.

---

## Functional Traceability Matrix

This matrix traces requirements to specific system components:

| Requirement ID | BRD Reference | Architecture Reference | Capability Reference | Module Reference | Priority | Owner |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **FR-001** | BRD-001 | AAR-APA-008: L3 | Onboarding | Module 2 | High | CDO |
| **FR-002** | BRD-002 | AAR-DTA-006: L3 | Financial Health | Module 6 | High | CCO |
| **FR-003** | BRD-003 | AAR-AIA-007: L3 | AI RM Copilot | Module 17 | Medium | CPO |
| **FR-004** | BRD-004 | AAR-BKA-004: L3 | Risk Monitoring | Module 19 | High | CRO |

---

## Conclusion
*   **Purpose:** Conclude the FRS document.
*   **Business Objective:** Approve the target business functional modules and roadmaps.
*   **Banking Objective:** Baselines all credit and risk designs under a single framework.
*   **Regulatory Considerations:** Prepares the platform for regulatory inspections.
*   **Deliverables:** Approved Functional Requirements Specification.
*   **Owner:** Chief Product Manager.
*   **Review Authority:** Board of Directors.
