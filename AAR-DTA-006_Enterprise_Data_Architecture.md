# Enterprise Data Architecture

**Document ID:** AAR-DTA-006  
**Document Name:** Enterprise Data Architecture  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 (ERDA), AAR-EAV-002 (EAV), AAR-BAR-003 (Business Architecture), AAR-BKA-004 (Banking Architecture), AAR-INA-005 (Information Architecture)  
**Next Artifact:** AAR-AIA-007 (Enterprise AI Architecture)  
**Target Audience:** IDBI Bank Board, MD & CEO, CIO, CDO, CTO, Chief Credit Officer, Chief Risk Officer, and Data Governance Council  
**Document Owner:** Chief Data Architect (CDA) / Chief Data Officer (CDO)  
**Approval Authority:** Data Governance Council (DGC)  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Data Architect | Initial Release of Enterprise Data Architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Document Metadata & Scope](#document-metadata--scope)
3. [PART 1: Enterprise Data Vision](#part-1-enterprise-data-vision)
4. [PART 2: Role of Data in AI-Powered MSME Banking](#part-2-role-of-data-in-ai-powered-msme-banking)
5. [PART 3: Enterprise Data Principles](#part-3-enterprise-data-principles)
6. [PART 4: Enterprise Data Domains](#part-4-enterprise-data-domains)
7. [PART 5: Canonical Enterprise Data Model](#part-5-canonical-enterprise-data-model)
8. [PART 6: Master Data Management (MDM)](#part-6-master-data-management-mdm)
9. [PART 7: Reference Data Architecture](#part-7-reference-data-architecture)
10. [PART 8: Metadata Architecture](#part-8-metadata-architecture)
11. [PART 9: Enterprise Data Quality Framework](#part-9-enterprise-data-quality-framework)
12. [PART 10: Enterprise Data Governance](#part-10-enterprise-data-governance)
13. [PART 11: Enterprise Data Lifecycle](#part-11-enterprise-data-lifecycle)
14. [PART 12: Alternate Data Architecture](#part-12-alternate-data-architecture)
13. [PART 13: Enterprise Data Lineage](#part-13-enterprise-data-lineage)
14. [PART 14: Enterprise Data Security](#part-14-enterprise-data-security)
15. [PART 15: Enterprise Data Sharing Architecture](#part-15-enterprise-data-sharing-architecture)
16. [PART 16: Enterprise Data Products](#part-16-enterprise-data-products)
17. [PART 17: Enterprise Data KPIs](#part-17-enterprise-data-kpis)
18. [PART 18: Data Risks](#part-18-data-risks)
19. [PART 19: Data Assumptions](#part-19-data-assumptions)
20. [PART 20: Five-Year Enterprise Data Strategy](#part-20-five-year-enterprise-data-strategy)
21. [PART 21: Enterprise Data Reference Model](#part-21-enterprise-data-reference-model)
22. [PART 22: Conclusion](#part-22-conclusion)

---

## Executive Summary
This document establishes the Enterprise Data Architecture (AAR-DTA-006) for Project AAROHAN. It defines the logical data organization, master data registries (MDM), reference datasets, validation rules, security classifications, and lifecycle frameworks necessary to operate a transaction-based, cash-flow lending system. This architecture ensures that data remains structured, secure, and formatted to feed the platform's machine learning engines.

---

## Document Metadata & Scope
*   **Purpose:** Establish the logical data structures, governance models, and data products supporting credit and risk.
*   **Scope:** Governs all database schemas, analytical warehouses, registry adapters, and data pipelines.
*   **Audience:** Board members, MD & CEO, Chief Data Officer, CIO, CTO, database leads, and compliance auditors.
*   **Data Strategy:** Transform isolated data structures into a unified, secure, real-time intelligent data ecosystem.

---

## PART 1: Enterprise Data Vision
*   **Purpose:** Outline the target state of the data platform.
*   **Data Objective:** Provide unified, secure profiles of MSME customer transactions.
*   **Business Objective:** Drive credit volume growth in priority sector manufacturing and services.
*   **Business Owner:** Chief Data Officer (CDO).
*   **Inputs:** Bank strategic plans, technology guidelines.
*   **Outputs:** Target state data models.
*   **Dependencies:** Data governance committee sponsorship.
*   **Deliverables:** Data Platform Vision Manifesto.
*   **Owner:** Chief Data Architect (CDA).
*   **Review Authority:** Data Governance Council (DGC).
*   **Success Criteria:** Platform target models aligned with data sovereignty laws.

---

## PART 2: Role of Data in AI-Powered MSME Banking
*   **Purpose:** Outline how data assets support automated credit and scoring engines.
*   **Business Objective:** Lower operational transaction costs.
*   **Banking Objective:** Underwrite loans using alternate, transaction-level records.
*   **Regulatory Considerations:** Aligns with RBI digital lending guidelines on data usage.
*   **Inputs:** Competitor product terms, credit bureau market reports.
*   **Outputs:** AI Grounding configurations.
*   **Dependencies:** Model registry connections.
*   **Deliverables:** AI Grounding Data Strategy.
*   **Owner:** Chief AI Officer (CAIO).
*   **Review Authority:** AI Governance Committee.
*   **Success Criteria:** Recommendation accuracy > 98% with zero hallucinations.

---

## PART 3: Enterprise Data Principles
1.  **Data as a Shared Asset:** Manage data centrally to ensure it is accessible to all authorized applications.
2.  **Strict Consent Validation:** Only fetch data from registries when authorized by active customer consent tokens.
3.  **Data Minimization:** Only pull the data required to calculate credit scores and verify identity, avoiding unnecessary storage of customer PII.
4.  **Zero-Trust Security:** Encrypt all data tables and restrict access based on role-based permission profiles.

---

## PART 4: Enterprise Data Domains

We partition the platform's data universe across 18 key domains:

```
  ┌──────────────────────────────────────────────────────────┐
  │                 AAROHAN DATA DOMAINS                     │
  ├────────────────────────────┬─────────────────────────────┤
  │       Master & Profile     │        Transaction          │
  │  - Golden customer record  │  - Live invoice streams     │
  │  - Reference code tables   │  - Payment clearing logs    │
  ├────────────────────────────┼─────────────────────────────┤
  │      Compliance & Risk     │         AI & Metrics        │
  │  - Consent status history  │  - Safety filters logs      │
  │  - EWS alert profiles      │  - Grounding vectors        │
  └────────────────────────────┴─────────────────────────────┘
```

*   **Customer & Master Data:** Unified borrower profiles, registry codes.
*   **Transaction & Alternate Data:** GST filings, bank statements.
*   **Compliance & Audit Data:** Consent records, operational logs.
*   **AI Data:** Prompt databases, model weights.

---

## PART 5: Canonical Enterprise Data Model

The canonical model defines relationships between business entities:

```
  [ Customer Entity ] 1 ── * [ Loan Account ]
           1                       1
           │                       │
           ▼ *                     ▼ *
  [ GST Profile ]         [ Transaction Record ]
```

*   **Customer Entity:** Stores primary identity keys (PAN, Udyam, CIN).
*   **Loan Account:** Stores active credit limits, interest settings, and payment status.
*   **GST Profile:** Tracks verified sales, invoices, and purchase records.
*   **Transaction Record:** Logs daily cash flows, credits, and debits.

---

## PART 6: Master Data Management (MDM)
*   **Golden Record:** The single, validated profile of a customer, compiled by matching records from NSDL, CKYC, and Udyam.
*   **Stewardship:** Data stewards audit master records weekly to identify and resolve duplicates.
*   **Synchronization:** Updates to core customer profiles are synchronized across all business databases.

---

## PART 7: Reference Data Architecture
*   **Standard Code Sets:** ISO currency codes, National Industrial Classification (NIC) codes, state/district geography codes.
*   **Product Hierarchies:** Standard product classifications (Cash Credit, term loans, invoice financing) mapped to ledger codes.

---

## PART 8: Metadata Architecture
*   **Business Metadata:** Data definitions, business glossary terms, mapping codes.
*   **Technical Metadata:** Database table names, column formats, replication lags.
*   **Operational Metadata:** Processing timestamps, batch execution logs, API traffic limits.
*   **AI Metadata:** Model version markers, training dates, safety filter metrics.

---

## PART 9: Enterprise Data Quality Framework
*   **Accuracy:** Cross-check transaction inputs against verified bank statement logs.
*   **Completeness:** Flag applications with missing tax or registration records.
*   **Consistency:** Normalizes data parameters across different registry types.
*   **Timeliness:** Query logs daily to keep credit limits aligned with current profiles.

---

## PART 10: Enterprise Data Governance
*   **Governance Committees:** The Data Governance Council meets monthly to review quality audits and access logs.
*   **Stewardship:** Data Stewards monitor data quality metrics and correct data errors.
*   **Policies:** Standard procedures for data classification, retention, and disposal.

---

## PART 11: Enterprise Data Lifecycle

Data moves through a controlled lifecycle managed by automated checks:

$$\text{Data Acquisition} \rightarrow \text{Data Validation} \rightarrow \text{Context Enrichment} \rightarrow \text{System Consumption} \rightarrow \text{Secure Sharing} \rightarrow \text{Encrypted Archival} \rightarrow \text{Data Disposal}$$

*   **Data Validation:** Verify schema rules and check signature authenticity.
*   **Secure Sharing:** Restrict data transmission to authorized, TLS-encrypted API gateways.
*   **Data Disposal:** Delete files automatically after the retention period using secure erasure.

---

## PART 12: Alternate Data Architecture
*   **GSTN & AA Records:** Transaction logs and tax filing dates.
*   **EPFO & ESIC Logs:** Employee count and payroll stability metrics.
*   **TReDS & GeM Data:** Verified invoice records and procurement orders.
*   **FASTag & Utilities (Future-ready):** Freight logs and water/electricity usage patterns.

---

## PART 13: Enterprise Data Lineage

All critical data objects are tracked from source to storage:

$$\text{Source (NSDL API)} \rightarrow \text{Validation (Apigee WAF)} \rightarrow \text{Ingestion (Cloud Run)} \rightarrow \text{Encryption (Cloud KMS)} \rightarrow \text{Active DB (AlloyDB)} \rightarrow \text{Warehouse (BigQuery)} \rightarrow \text{Dashboard (Looker)}$$

This ensures auditors can trace any calculated credit score back to its raw registry source.

---

## PART 14: Enterprise Data Security

Each information domain is mapped to standard security profiles:

| Information Domain | Confidentiality | Integrity | Availability | Privacy | Encryption | Auditability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Customer Profile** | Confidential | High | High | High | TLS & AES-256| Full Trail |
| **Credit Scoring** | Restricted | High | High | Medium | AES-256 | Full Trail |
| **Alternate Data** | Restricted | High | Medium | High | AES-256 | Full Trail |
| **AI Prompts** | Restricted | High | High | Low | TLS | Versioned |

---

## PART 15: Enterprise Data Sharing Architecture
*   **Internal Sharing:** Microservices communicate using REST APIs protected by oauth.
*   **External Sharing:** Expose secure APIs via Apigee for partner NBFCs and co-lenders.
*   **Regulatory Sharing:** Automated file transfers (SFTP) route tax and PSL reports to central banks.

---

## PART 16: Enterprise Data Products

The platform packages data into reusable data products:

*   **Financial Health Card:** Provides aggregated tax and cash flow metrics.
*   **Credit Proposal Dossier:** Contains pre-compiled credit memorandum templates.
*   **Portfolio Risk Dashboard:** Monitors sector exposure and early warning alert frequency.

---

## PART 17: Enterprise Data KPIs

AAROHAN defines and monitors KPIs across six strategic dimensions:

| Category | Key Performance Indicator (KPI) | Target Baseline | Formula | Owner |
| :--- | :--- | :---: | :--- | :--- |
| **Data Quality** | Accuracy Score | > 99.5% | $\text{Correct Records} / \text{Total Records}$ | CDO |
| **Governance** | Audit Coverage | 100% | $\text{Audited Tables} / \text{Total Tables}$ | CISO |
| **Operations** | Data Sync Latency | < 5 seconds | $\text{Sync Time} - \text{Commit Time}$ | CTO |
| **AI Readiness**| Prompt Accuracy | > 98% | $\text{Correct Prompts} / \text{Total Prompts}$ | CAIO |
| **Compliance** | Consent Validation Rate | 100% | $\text{Validated Consents} / \text{Total Queries}$| CBO |

---

## PART 18: Data Risks
*   **Registry Format Risk:** External registry schema modifications may break ingestion pipelines.
*   **Data Leak Risk:** Risk of unauthorized customer data exposure on public frontends.
*   **Stale Data Risk:** Outdated transaction files may lead to incorrect credit limits.

---

## PART 19: Data Assumptions
*   **API Stability:** Assume national DPI gateways maintain stable API services.
*   **Data Accuracy:** Assume data fetched from central government registries is accurate.
*   **Storage Performance:** Assume database clusters handle the required read/write latencies.

---

## PART 20: Five-Year Enterprise Data Strategy
*   **Year 1-2 (Integrated Data):** Complete alternate data pipeline integrations (GST, AA, EPFO).
*   **Year 3-4 (Intelligent Data):** Deploy real-time risk scoring and conversational reporting engines.
*   **Year 5 (Autonomous Data):** Self-learning credit scoring networks operating within human validation.

---

## PART 21: Enterprise Data Reference Model

The reference model connects all data components into a single framework:

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                     AAROHAN DATA REFERENCE MODEL                       │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 1. Ingestion Layer: API gateway connectors, consent check filters      │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 2. Storage Layer: AlloyDB transactions, BigQuery analytics warehouses  │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 3. Services Layer: MDM golden records, reference tables, metadata      │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 4. Consumers: Underwriting agents, Risk dashboards, Audit logs         │
  └────────────────────────────────────────────────────────────────────────┘
```

*   **Ingestion Gateway:** Expose and route services using secure gateways.
*   **Analytics Layer:** Process transaction files using BigQuery and Looker dashboards.
*   **Security & Compliance:** Log all approvals and access histories in write-once audit stores.

---

## PART 22: Conclusion
*   **Purpose:** Conclude the Enterprise Data Architecture document.
*   **Business Objective:** Approve the target business data classifications and lifecycles.
*   **Banking Objective:** Align data stewardship and quality audits under a single framework.
*   **Regulatory Considerations:** Prepares the platform for regulatory inspects.
*   **Deliverables:** Approved Data Reference Architecture.
*   **Owner:** Chief Data Architect (CDA).
*   **Review Authority:** Board of Directors.
