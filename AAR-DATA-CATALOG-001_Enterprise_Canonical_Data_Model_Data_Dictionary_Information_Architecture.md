# Enterprise Canonical Data Model, Data Dictionary & Information Architecture

**Document ID:** AAR-DATA-CATALOG-001  
**Document Name:** Enterprise Canonical Data Model, Data Dictionary & Information Architecture  
**Version:** 1.0  
**Status:** Approved for Data Platform & Analytics Engineering  
**Dependencies:** Entire Enterprise Repository, Engineering Build Blueprint (AAR-BLD-001), API Catalogue (AAR-API-CATALOG-001), and Screen Blueprint (AAR-SCR-001)  
**Target Audience:** Data Engineers, Backend Engineers, AI Engineers, Business Analysts, Enterprise Architects, Reporting Teams, and Data Governance Teams  
**Document Owner:** Chief Data Architect  
**Approval Authority:** Enterprise Architecture Review Board (EARB) / Data Governance Committee

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Data Architect | Initial strategic release of the Enterprise Canonical Information Model. | EARB Approved |

---

## Table of Contents
1. [Executive Summary & Information Architecture Standards](#executive-summary--information-architecture-standards)
2. [Canonical Entity Catalogue (Core Domains)](#canonical-entity-catalogue-core-domains)
3. [Master Data & Reference Data Governance](#master-data--reference-data-governance)
4. [Enterprise Data Governance Framework](#enterprise-data-governance-framework)
5. [AI Data Conceptual Models](#ai-data-conceptual-models)
6. [Google Cloud Conceptual Data Platform Mapping](#google-cloud-conceptual-data-platform-mapping)

---

## Executive Summary & Information Architecture Standards

This document establishes the Enterprise Canonical Data Model, Data Dictionary & Information Architecture (AAR-DATA-CATALOG-001) for Project AAROHAN. It acts as the single source of truth for IDBI Bank’s digital MSME lending entities. Conceptualized to bridge transactional operations (managed via AlloyDB) and big-data analytics (managed via BigQuery), it outlines the structural rules, data dictionary details, AI feature structures, and governance definitions without prescribing physical schemas, DDL, or database code.

### Core Data Modeling Standards:
*   **Logical Normalization:** Concepts follow logical 3NF constructs.
*   **Entity Identity Rules:** Every canonical entity must possess a unique, system-wide identifier formatted as `ENT-{DOMAIN}-{UUID}`.
*   **Privacy Guardrails:** Attributes classified under High/Critical privacy levels must enforce masking patterns at the query gateway.

---

## Canonical Entity Catalogue (Core Domains)

### 1. Customer
*   **Entity ID:** AAR-ENT-CST-001
*   **Business Definition:** Any individual or registered corporate entity requesting credit services from IDBI Bank.
*   **Business Purpose:** Master client profile, relationship tracking.
*   **Primary Owner:** Chief Business Officer (CBO).
*   **Data Steward:** Customer Experience Lead.
*   **Source Systems:** Core Banking System (CBS), CKYC registry, Customer self-service portal.
*   **Consumers:** RM Workspace, Credit Analyst Portal, Risk Management.
*   **Business Attributes:** Customer ID, Registered Name, PAN Code, Email Address, Phone Number, Customer Segment, Date of Incorporation.
*   **Mandatory Fields:** Customer ID, Registered Name, PAN Code, Phone Number.
*   **Optional Fields:** Secondary Email, Alternate Phone, Website URL.
*   **Reference Data:** Customer Segment codes.
*   **Validation Rules:** PAN Code must conform to 10-character alpha-numeric formats; Phone must contain exactly 10 numeric digits.
*   **Business Rules:** A customer cannot hold duplicate active profile records.
*   **Lifecycle:** Prospect -> Onboarding -> Active -> Dormant -> Suspended.
*   **Privacy Classification:** Critical PII (Full encryption at rest, field-level masking).
*   **Retention Policy:** 10 years past account closure.
*   **Data Quality Rules:** Phone number completeness = 100%; PAN validation match = 100%.
*   **Relationships:** One-to-many relationship with Loan Applications, one-to-many relationship with Loan Accounts.
*   **KPIs Supported:** Active Customer Growth YoY, Customer Dropout Rate.
*   **AI Usage:** Propensity to default, cross-sell targeting.
*   **Reporting Usage:** Monthly active client count.

---

### 2. MSME Enterprise
*   **Entity ID:** AAR-ENT-ENT-002
*   **Business Definition:** The corporate legal entity conducting the MSME business, verified via GSTN and Udyam registries.
*   **Business Purpose:** Enterprise profile validation, business classification mapping.
*   **Primary Owner:** Head of MSME Lending.
*   **Data Steward:** Business Onboarding Steward.
*   **Source Systems:** GSTN Registry, Udyam Registry, MCA database.
*   **Consumers:** Credit Assessment Engine, Underwriting Workspace.
*   **Business Attributes:** Enterprise ID, Legal Entity Name, GSTIN, Udyam Registration Number, Constitution Type (Proprietorship, Partnership, Private Limited), Annual Turnover, Industry Sector.
*   **Mandatory Fields:** Enterprise ID, GSTIN, Legal Entity Name, Constitution Type.
*   **Optional Fields:** Udyam Number, Annual Export Turnovers.
*   **Validation Rules:** GSTIN must follow the 15-character standard format.
*   **Lifecycle:** Registered -> Active -> Audited -> Default.
*   **Privacy Classification:** High (Tax and business financials protected).
*   **Relationships:** Many-to-one relationship with Customer ID.
*   **KPIs Supported:** MSME segment market share.

---

### 3. Proprietor / Directors
*   **Entity ID:** AAR-ENT-DIR-003
*   **Business Purpose:** Master record of individuals controlling the MSME legal entity.
*   **Scope:** KYC validation, credit history lookup.
*   **Source Systems:** MCA Database, DigiLocker.
*   **Business Attributes:** Director ID, DIN (Director Identification Number), PAN, Full Name, Net Worth.
*   **Privacy Classification:** Critical PII.

---

### 4. Branch
*   **Entity ID:** AAR-ENT-BRH-004
*   **Business Purpose:** Physical branch structure coordinating regional loans.
*   **Scope:** Operations routing, regional compliance.
*   **Source Systems:** CBS Master.
*   **Business Attributes:** Branch Code, Name, Region, State, Officer Code.
*   **Privacy Classification:** Low.

---

### 5. Relationship Manager
*   **Entity ID:** AAR-ENT-RMG-005
*   **Business Purpose:** RM employee profile managing pipeline leads.
*   **Scope:** Resource assignment, performance metrics.
*   **Source Systems:** HRMS.
*   **Business Attributes:** RM ID, Full Name, Assigned Branch Code, Sales Targets.
*   **Privacy Classification:** Medium.

---

### 6. Loan Application
*   **Entity ID:** AAR-ENT-APP-006
*   **Business Purpose:** The credit application file traversing the approval workflow lifecycle.
*   **Scope:** Lifecycle tracking, credit terms, pricing metadata.
*   **Source Systems:** Loan Origination Engine.
*   **Business Attributes:** Application ID, Customer ID, Requested Amount, Interest Rate Proposed, Workflow State, Last Action Timestamp.
*   **Privacy Classification:** Medium.

---

### 7. Financial Health Card
*   **Entity ID:** AAR-ENT-FHC-007
*   **Business Purpose:** Summarized cash flow metrics and ratio calculations.
*   **Scope:** Lending risk analysis, cash-flow check inputs.
*   **Source Systems:** Spreading Engine.
*   **Business Attributes:** Health Card ID, DSCR, Alt-DSCR, Average Balance, GST Turnover Verification Ratio.
*   **Privacy Classification:** High.

---

### 8. Credit Assessment
*   **Entity ID:** AAR-ENT-CAS-008
*   **Business Purpose:** Policy decision results and risk scoring outcomes.
*   **Scope:** Underwriter decision support.
*   **Source Systems:** Credit Engine.
*   **Business Attributes:** Assessment ID, Risk Score, Rating Category, Policy Met Indicators, Approved Limit.
*   **Privacy Classification:** High.

---

### 9. CAM
*   **Entity ID:** AAR-ENT-CAM-009
*   **Business Purpose:** Narrative and financial summaries compiled in the Credit Assessment Memo.
*   **Scope:** Committee presentation documentation.
*   **Source Systems:** CAM Generator, Gemini narrative models.
*   **Business Attributes:** CAM ID, Application ID, Qualitative Summary text, Generated References, Auditor Sign-off parameters.
*   **Privacy Classification:** High.

---

### 10. Loan Account
*   **Entity ID:** AAR-ENT-ACC-010
*   **Business Purpose:** Post-disbursement credit account tracking balances and repayment schedules.
*   **Scope:** Repayment monitoring, portfolio finance analytics.
*   **Source Systems:** Core Banking System (CBS).
*   **Business Attributes:** Account Number, Disbursed Value, Principal Outstanding, Interest Accrued, Overdue Days count.
*   **Privacy Classification:** High.

---

### 11. Collateral
*   **Entity ID:** AAR-ENT-COL-011
*   **Business Purpose:** Asset details pledged to back the credit facility.
*   **Scope:** Collateral valuation audits, risk reduction.
*   **Source Systems:** Collateral Management System.
*   **Business Attributes:** Collateral ID, Type, Valuation Value, Last Assessment Date, Legal Title verification parameters.
*   **Privacy Classification:** Medium.

---

### 12. Guarantor
*   **Entity ID:** AAR-ENT-GUR-012
*   **Business Purpose:** Identity and credit profile of third parties backing the loan.
*   **Scope:** KYC validation, bureau assessment.
*   **Source Systems:** Bureau Interface, CKYC.
*   **Business Attributes:** Guarantor ID, PAN, Name, CIBIL Score, Net Worth.
*   **Privacy Classification:** Critical PII.

---

### 13. Consent
*   **Entity ID:** AAR-ENT-CON-013
*   **Business Purpose:** Digital authorization metadata permitting third-party data retrieval.
*   **Scope:** Audit compliance, AA data routing.
*   **Source Systems:** Consent Manager.
*   **Business Attributes:** Consent ID, Customer ID, Expiry Date, Scope Indicators, Signature Hash.
*   **Privacy Classification:** High.

---

### 14. Account Aggregator Data
*   **Entity ID:** AAR-ENT-AAD-014
*   **Business Purpose:** Raw transactional banking history pulled from source banks.
*   **Scope:** Cash flow spreading calculations.
*   **Source Systems:** AA Gateways.
*   **Business Attributes:** AA Data ID, Bank Identifier, Account Class, Transaction Ledger JSON string.
*   **Privacy Classification:** Critical PII.

---

### 15. GST Data
*   **Entity ID:** AAR-ENT-GST-015
*   **Business Purpose:** Tax filing history records used to verify turnover metrics.
*   **Scope:** Financial health evaluation.
*   **Source Systems:** GSTN Registry.
*   **Business Attributes:** GST Data ID, GSTIN, Monthly Filing Dates, Total Inward Supplies, Total Outward Supplies.
*   **Privacy Classification:** High.

---

### 16. UPI Data
*   **Entity ID:** AAR-ENT-UPI-016
*   **Business Purpose:** Real-time collection payment statuses.
*   **Scope:** Payment clearing, collections settlement.
*   **Source Systems:** UPI Switch.
*   **Business Attributes:** UPI Txn ID, VPA, Target ID, Status (Success/Failure).
*   **Privacy Classification:** Medium.

---

### 17. Bank Statement
*   **Entity ID:** AAR-ENT-BST-017
*   **Business Purpose:** PDF statement files uploaded manually by users.
*   **Scope:** Document parsing fallbacks.
*   **Source Systems:** Document Storage, Customer Uploads.
*   **Business Attributes:** Document ID, File Path reference, Parse status, Document AI confidence scores.
*   **Privacy Classification:** High.

---

### 18. EPFO
*   **Entity ID:** AAR-ENT-EPF-018
*   **Business Purpose:** Verified social security filings showing employer payroll details.
*   **Scope:** Checking employee size stability.
*   **Source Systems:** EPFO Portal.
*   **Business Attributes:** EPFO Record ID, Employee count, Total wages paid, Date of last return.
*   **Privacy Classification:** High.

---

### 19. TReDS
*   **Entity ID:** AAR-ENT-TRD-019
*   **Business Purpose:** Trade invoice status details pulled from financing exchanges.
*   **Scope:** Working capital assessment.
*   **Source Systems:** RXIL, M1Xchange, Invoicemart.
*   **Business Attributes:** Invoice ID, Seller PAN, Buyer PAN, Due Date, Status (Financed/Unfinanced).
*   **Privacy Classification:** Medium.

---

### 20. MCA
*   **Entity ID:** AAR-ENT-MCA-020
*   **Business Purpose:** Corporate filing registration details.
*   **Scope:** Legal existence validation.
*   **Source Systems:** MCA Gateway.
*   **Business Attributes:** Corporate ID (CIN), Share Capital, Active Status, Charge Details summary.
*   **Privacy Classification:** Medium.

---

### 21. CKYC
*   **Entity ID:** AAR-ENT-CKY-021
*   **Business Purpose:** Government KYC profile matches.
*   **Scope:** Checking customer identity records.
*   **Source Systems:** CERSAI CKYC.
*   **Business Attributes:** CKYC Number, Full Name, PAN Linkage, Photo Reference.
*   **Privacy Classification:** Critical PII.

---

### 22. DigiLocker
*   **Entity ID:** AAR-ENT-DGL-022
*   **Business Purpose:** Customer document URLs retrieved from digital vaults.
*   **Scope:** Secure document collection.
*   **Source Systems:** National DigiLocker API.
*   **Business Attributes:** Lock ID, Document Type, Reference URI.
*   **Privacy Classification:** High.

---

### 23. Risk Assessment
*   **Entity ID:** AAR-ENT-RSK-023
*   **Business Purpose:** Computed default probabilities and structural risk ratings.
*   **Scope:** Risk management monitoring.
*   **Source Systems:** Vertex AI risk engines.
*   **Business Attributes:** Risk ID, Current Rating, Probability of Default (PD) value, Date of assessment.
*   **Privacy Classification:** High.

---

### 24. Early Warning Signal
*   **Entity ID:** AAR-ENT-EWS-024
*   **Business Purpose:** Warning indicators triggered on accounts showing transaction anomalies.
*   **Scope:** Portfolio monitoring, RM task allocation.
*   **Source Systems:** EWS rule engine.
*   **Business Attributes:** Alert ID, Account ID, Trigger Code, Severity (Red, Amber, Green).
*   **Privacy Classification:** High.

---

### 25. Portfolio
*   **Entity ID:** AAR-ENT-PTF-025
*   **Business Purpose:** Consolidated portfolio yield statistics and metrics.
*   **Scope:** Executive and risk dashboard analysis.
*   **Source Systems:** Analytics Warehouse (BigQuery).
*   **Business Attributes:** Portfolio ID, Total Exposure, Weighted Risk rating, Gross NPA ratio (%).
*   **Privacy Classification:** Medium.

---

### 26. AI Recommendation
*   **Entity ID:** AAR-ENT-REC-026
*   **Business Purpose:** Automated advice outputs (e.g., credit extensions, payment plans).
*   **Scope:** RM Workspace, MSME portal.
*   **Source Systems:** Gemini model pipelines.
*   **Business Attributes:** Rec ID, Trigger Category, Suggested Actions details, Confidence Score.
*   **Privacy Classification:** High.

---

### 27. AI Explanation
*   **Entity ID:** AAR-ENT-EXP-027
*   **Business Purpose:** Explainability traces justifying credit or risk classifications.
*   **Scope:** Audit validation.
*   **Source Systems:** Vertex AI Explainable models.
*   **Business Attributes:** Explanation ID, Recommendation ID, Citation References list, Feature Weights vector.
*   **Privacy Classification:** High.

---

### 28. Workflow
*   **Entity ID:** AAR-ENT-WKF-028
*   **Business Purpose:** Step-by-step records showing transaction path stages and actions.
*   **Scope:** Process optimization, SLA logs.
*   **Source Systems:** Cloud Workflows.
*   **Business Attributes:** Workflow ID, Application ID, Assigned Group ID, Action Actor ID, Step Status.
*   **Privacy Classification:** Medium.

---

### 29. Audit Trail
*   **Entity ID:** AAR-ENT-AUD-029
*   **Business Purpose:** Immutable logs recording database changes and actions.
*   **Scope:** Forensic auditing, compliance reviews.
*   **Source Systems:** System Security Loggers.
*   **Business Attributes:** Audit ID, Timestamp, Actor ID, Event Category, Payload Hash.
*   **Privacy Classification:** High.

---

### 30. Notification
*   **Entity ID:** AAR-ENT-NTF-030
*   **Business Purpose:** Records of dispatched communications.
*   **Scope:** Client contact records.
*   **Source Systems:** Notification Engine.
*   **Business Attributes:** Notification ID, Customer ID, Delivery channel, Status (Sent/Failed).
*   **Privacy Classification:** Medium.

---

### 31. User
*   **Entity ID:** AAR-ENT-USR-031
*   **Business Purpose:** Internal and external user registry profiles.
*   **Scope:** System access governance.
*   **Source Systems:** Identity Registry.
*   **Business Attributes:** User ID, Name, Email, Role Profile ID.
*   **Privacy Classification:** Critical PII.

---

### 32. Role
*   **Entity ID:** AAR-ENT-ROL-032
*   **Business Purpose:** Logical roles matching access profiles.
*   **Scope:** Permissions management.
*   **Source Systems:** Admin Console.
*   **Business Attributes:** Role ID, Name, Description.
*   **Privacy Classification:** Low.

---

### 33. Permissions
*   **Entity ID:** AAR-ENT-PRM-033
*   **Business Purpose:** System endpoint and view action flags assigned to roles.
*   **Scope:** Access controls validation.
*   **Source Systems:** IAM definitions.
*   **Business Attributes:** Permission ID, Action Target Code.
*   **Privacy Classification:** Low.

---

## Master Data & Reference Data Governance

Master and Reference data values are stored in managed caches and verified via continuous synchronization checks.

### 1. Master Data Domains
*   **Branch/Region Master:** Governs branch hierarchies (Branch -> District -> State -> Region).
*   **Industry Classification Master:** Aligns borrowers with NIC (National Industrial Classification) codes to monitor exposure limits.
*   **Risk Grade Master:** Standardizes risk ratings across internal scorecard profiles.
*   **MSME Classification Master:** Classifies enterprises based on investment and turnover thresholds (Micro, Small, Medium).

### 2. Reference Data Code Sets
*   **Workflow States:** `DRAFT`, `CONSENT_PENDING`, `SPREADING`, `RISK_EVALUATION`, `UNDERWRITING`, `APPROVED`, `DISBURSED`, `REJECTED`.
*   **EWS Alert Severity:** `CRITICAL_RED`, `WARNING_AMBER`, `MONITOR_GREEN`.
*   **Consent Status:** `REQUESTED`, `APPROVED`, `REVOKED`, `EXPIRED`.

---

## Enterprise Data Governance Framework

```
   ┌────────────────────────────────────────────────────────┐
   │                  DATAPLEX DATA GOVERNANCE              │
   ├────────────────────────────┬───────────────────────────┤
   │      Data Lineage          │     Metadata Cataloguing  │
   │  - Auto-track data flows   │  - Dataplex Data Catalog  │
   ├────────────────────────────┼───────────────────────────┤
   │      Quality Engine        │     Security Guardrails   │
   │  - Validation Rules        │  - Dynamic Column Masking │
   └────────────────────────────┴───────────────────────────┘
```

*   **Lineage Tracking:** Automatically captured as data moves from AlloyDB to BigQuery.
*   **Metadata Standards:** Fields in the Data Catalog must include description, owner, steward, and classification tags.
*   **Data Quality Rules:** Monitored via Dataplex rules to detect schema changes or anomalies.

---

## AI Data Conceptual Models

Conceptual specifications mapping variables used by the AI engine.

### 1. Feature Store Model
*   **Domain:** Vertex AI Feature Store.
*   **Entities:**
    *   *MSME_Fin_Features:* Aggregates variables like 12-month average cash balance, debt service ratios, and GST file delays.
    *   *MSME_Trend_Features:* Tracks 3-month month-on-month trend directions (sales change %, balance change %).

### 2. Prompt & Explainability Context
*   **Domain:** BigQuery Analytical structures.
*   **Entities:**
    *   *Prompt_Context:* Tracks templates used, context values injected, and output results.
    *   *Explainability_Metadata:* Logs SHAP/IG feature weight scores mapping how attributes impacted model decisions.

---

## Google Cloud Conceptual Data Platform Mapping

```
┌────────────────────────────────────────┐
│               DATAPLEX                 │
└──────────────────┬─────────────────────┘
                   ▼
┌────────────────────────────────────────┐
│          ALLOYDB (OLTP Core)           │
└──────────────────┬─────────────────────┘
                   │  (Datastream CDC)
                   ▼
┌────────────────────────────────────────┐
│         BIGQUERY (OLAP Warehouse)      │
│   ┌────────────────────────────────┐   │
│   │  Dataplex Data Catalog         │   │
│   ├────────────────────────────────┤   │
│   │  Vertex AI Feature Store       │   │
│   └────────────────────────────────┘   │
└────────────────────────────────────────┘
```

1. **AlloyDB:** Handles transactional processing, state checks, and operational database logs.
2. **Datastream:** Replicates transactional mutations from AlloyDB to BigQuery in near-real-time via CDC.
3. **BigQuery:** Central analytical repository hosting data models, feature tables, and ML training sets.
4. **Dataplex & Data Catalog:** Enforces data quality rules, logs data lineage, and manages data classification tagging.

---

**Approved & Signed By:**  
*Chief Data Architect, Project AAROHAN*  
*Director, Google Cloud Professional Services*  
*Head, Digital Transformation Office (DTO), IDBI Bank*
