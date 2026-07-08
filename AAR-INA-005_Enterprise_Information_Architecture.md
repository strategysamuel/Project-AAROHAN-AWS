# Enterprise Information Architecture

**Document ID:** AAR-INA-005  
**Document Name:** Enterprise Information Architecture  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 (ERDA), AAR-EAV-002 (EAV), AAR-BAR-003 (Business Architecture), AAR-BKA-004 (Banking Architecture)  
**Next Artifact:** AAR-DTA-006 (Enterprise Data Architecture)  
**Target Audience:** IDBI Bank Board, MD & CEO, Chief Data Officer, CIO, CTO, Chief Credit Officer, and Chief Risk Officer  
**Document Owner:** Chief Information Architect (CIA) / Chief Data Officer (CDO)  
**Approval Authority:** Enterprise Data Governance Committee (EDGC)  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Information Architect | Initial Release of Enterprise Information Architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Document Metadata & Scope](#document-metadata--scope)
3. [PART 1: Enterprise Information Vision](#part-1-enterprise-information-vision)
4. [PART 2: Role of Information in AI-Powered MSME Banking](#part-2-role-of-information-in-ai-powered-msme-banking)
5. [PART 3: Information Architecture Principles](#part-3-information-architecture-principles)
6. [PART 4: Enterprise Information Domains](#part-4-enterprise-information-domains)
7. [PART 5: Business Information Model](#part-5-business-information-model)
8. [PART 6: Enterprise Information Lifecycle](#part-6-enterprise-information-lifecycle)
9. [PART 7: Information Ownership Model](#part-7-information-ownership-model)
10. [PART 8: Information Classification Framework](#part-8-information-classification-framework)
11. [PART 9: Enterprise Metadata Architecture](#part-9-enterprise-metadata-architecture)
12. [PART 10: Master Information Catalogue](#part-10-master-information-catalogue)
13. [PART 11: Alternate Information Framework](#part-11-alternate-information-framework)
14. [PART 12: Enterprise Information Flows](#part-12-enterprise-information-flows)
15. [PART 13: Information Quality Framework](#part-13-information-quality-framework)
16. [PART 14: Information Governance Framework](#part-14-information-governance-framework)
17. [PART 15: Information Security Classification](#part-15-information-security-classification)
18. [PART 16: Information Lineage](#part-16-information-lineage)
19. [PART 17: Enterprise Reporting Information Model](#part-17-enterprise-reporting-information-model)
20. [PART 18: Enterprise KPI Information Model](#part-18-enterprise-kpi-information-model)
21. [PART 19: Information Risks](#part-19-information-risks)
22. [PART 20: Information Assumptions](#part-20-information-assumptions)
23. [PART 21: Future Information Strategy](#part-21-future-information-strategy)
24. [PART 22: Enterprise Information Reference Model](#part-22-enterprise-information-reference-model)
25. [PART 23: Conclusion](#part-23-conclusion)

---

## Executive Summary
This document defines the Enterprise Information Architecture (AAR-INA-005) for Project AAROHAN. It establishes the conceptual definition, business metadata, lifecycle standards, ownership structures, and regulatory mapping for all information objects used across the MSME credit ecosystem. The ERDA guidelines ensure that information remains high-quality, traceable, compliant, and ready to feed the platform's AI decision engine.

---

## Document Metadata & Scope
*   **Purpose:** Define the conceptual information domains, taxonomy rules, metadata schemes, and ownership grids.
*   **Scope:** Governs all business information objects supporting lead, onboarding, underwriting, monitoring, and audit operations.
*   **Audience:** Board members, MD & CEO, Chief Data Officer, CIO, CTO, compliance managers, and database administrators.
*   **Information Vision:** Transition operations from static document files to dynamic, integrated financial records.

---

## PART 1: Enterprise Information Vision
*   **Purpose:** Align information assets with the bank's strategic MSME growth targets.
*   **Business Objective:** Protect borrower data privacy while utilizing transaction-level records.
*   **Banking Objective:** Move to self-optimizing risk underwriting engines.
*   **Regulatory Considerations:** Aligns with national data protection laws (DPDP) and RBI guidelines.
*   **Inputs:** Strategic bank directions, regulatory mandates.
*   **Outputs:** Target state information strategies.
*   **Dependencies:** Data governance committee sponsorship.
*   **Deliverables:** Information Strategy Manifesto.
*   **Owner:** Chief Data Officer (CDO).
*   **Review Authority:** Board of Directors.
*   **Success Criteria:** Platform target models aligned with data sovereignty laws.

---

## PART 2: Role of Information in AI-Powered MSME Banking
*   **Purpose:** Outline how information assets support automated credit operations.
*   **Business Objective:** Lower operational transaction costs.
*   **Banking Objective:** Underwrite loans using alternate, transaction-level records.
*   **Regulatory Considerations:** Aligns with RBI digital lending guidelines on data usage.
*   **Inputs:** Competitor product terms, credit bureau market reports.
*   **Outputs:** AI Grounding configurations.
*   **Dependencies:** Model registry connections.
*   **Deliverables:** AI Grounding Strategy.
*   **Owner:** Chief AI Officer (CAIO).
*   **Review Authority:** AI Governance Committee.
*   **Success Criteria:** Recommendation accuracy > 98% with zero hallucinations.

---

## PART 3: Information Architecture Principles
1.  **Information Ownership:** Every information object has an assigned business owner accountable for its quality and classification.
2.  **Metadata Grounding:** AI recommendations must reference verified business metadata entries.
3.  **Consent-based Ingestion:** Information from external registries may only be pulled with valid, active consent tokens.
4.  **Zero PII Leakage:** Personally Identifiable Information (PII) must be masked or encrypted across all analytics databases.

---

## PART 4: Enterprise Information Domains

We partition the platform's information universe across 19 strategic domains:

```
  ┌──────────────────────────────────────────────────────────┐
  │                 AAROHAN INFORMATION DOMAINS              │
  ├────────────────────────────┬─────────────────────────────┤
  │      Profile & Identity    │      Credit & Risk          │
  │  - Customer Profile        │  - Alternate Scorecards     │
  │  - DPI consent records     │  - Credit Memos (CAM)       │
  ├────────────────────────────┼─────────────────────────────┤
  │      Operational Run       │    Security & Compliance    │
  │  - Workflow state logs     │  - Auditable transaction logs│
  │  - Notification templates  │  - DPDP Consent Tokens      │
  └────────────────────────────┴─────────────────────────────┘
```

*   **Customer:** Borrower identifiers, contact details, business registries.
*   **Credit:** Alt-DSCR calculations, scoring ratings, limit history.
*   **Compliance:** DPDP consent profiles, RBI priority sector categories, audit histories.
*   **AI:** Prompt templates, safety filter configurations, grounding logs.

---

## PART 5: Business Information Model

For every strategic domain, we define the conceptual data parameters:

### Information Domain Example: Alternate Data
*   **Purpose:** Store validated transaction and tax logs retrieved from external registries.
*   **Business Meaning:** Real-time business activity logs replacing historical audited balance sheets.
*   **Business Owner:** Head of Underwriting.
*   **Information Producer:** Account Aggregator, GSTN APIs, EPFO gateways.
*   **Information Consumer:** Vertex AI, Underwriters, Risk analysts.
*   **Information Quality Requirements:** Schema consistency, timeliness (less than 24 hours lag).
*   **Security Classification:** Restricted.
*   **Regulatory Mapping:** RBI Digital Lending Guidelines.
*   **AI Usage:** Cash-flow analysis and anomaly detection.
*   **Reporting Usage:** Credit Memos (CAM) and Early Warning Signal dashboards.
*   **Retention Requirement:** Active loan lifecycle plus 10 years in encrypted archives.
*   **Risks:** External registry connection timeouts or data format changes.
*   **Success Criteria:** Retrieval latency < 10 seconds.

---

## PART 6: Enterprise Information Lifecycle

Information moves through a controlled lifecycle managed by automated checks:

$$\text{Information Creation} \rightarrow \text{Data Validation} \rightarrow \text{Context Enrichment} \rightarrow \text{System Consumption} \rightarrow \text{Secure Sharing} \rightarrow \text{Encrypted Archival} \rightarrow \text{Data Disposal}$$

*   **Data Validation:** Verify schema rules and check signature authenticity.
*   **Secure Sharing:** Restrict data transmission to authorized, TLS-encrypted API gateways.
*   **Data Disposal:** Delete files automatically after the retention period using secure erasure.

---

## PART 7: Information Ownership Model
*   **Business Owners:** Executive heads (e.g., Head of Credit owns Credit Domain) accountable for policy rules and classifications.
*   **Data Stewards:** Data analysts responsible for metadata descriptions and data quality audits.
*   **Data Custodians:** Database administrators responsible for backups, encryption, and performance optimization.

---

## PART 8: Information Classification Framework

The bank classifies information into five strategic security tiers:

1.  **Public:** Marketing copy, general products terms, public APIs.
2.  **Internal:** Branch operating manuals, project dashboards.
3.  **Confidential:** RM sales logs, non-credit customer profiles.
4.  **Restricted:** Underwriting risk score parameters, early warning signal rules.
5.  **Highly Confidential:** Customer PII, password credentials, system encryption keys.

---

## PART 9: Enterprise Metadata Architecture
*   **Business Metadata:** Column descriptions, business glossary terms, mapping codes.
*   **Technical Metadata:** Database table names, column formats, replication lags.
*   **Operational Metadata:** Processing timestamps, batch execution logs, API traffic limits.
*   **AI Metadata:** Model version markers, training dates, safety filter metrics.

---

## PART 10: Master Information Catalogue

AAROHAN maintains a master registry of 22 core business information objects:

*   **Customer & Entity Profiles:** Consolidated customer identifiers (PAN, Udyam, CIN).
*   **Financial Health Cards:** Aggregated tax and cash flow metrics.
*   **Credit Proposals (CAM):** Pre-compiled credit memorandum templates.
*   **Consent Records:** Consent status tokens and validation timestamps.
*   **Risk Alerts (EWS):** Transaction indicators and default warnings.

---

## PART 11: Alternate Information Framework
*   **GSTN & AA Records:** Transaction logs and tax filing dates.
*   **EPFO & ESIC Logs:** Employee count and payroll stability metrics.
*   **TReDS & GeM Data:** Verified invoice records and procurement orders.
*   **FASTag & Utilities (Future-ready):** Freight logs and water/electricity usage patterns.

---

## PART 12: Enterprise Information Flows

```
[ DPI Registry Fetch ] ──> [ Schema Normalization ] ──> [ Data Quality Check ] ──> [ Vector Storage ]
                                                                                         │
[ Executive Report ] <── [ Looker Dashboards ] <── [ BigQuery Warehouse ] <──────────────┘
```

1.  **Ingestion:** API gateways fetch consented registry files.
2.  **Normalization:** Schema converters structure data into uniform database formats.
3.  **Storage:** Systems route transactional records to AlloyDB and analytics files to BigQuery.
4.  **Reporting:** BigQuery views generate the Looker dashboards for steering committees.

---

## PART 13: Information Quality Framework
*   **Accuracy:** Cross-check transaction inputs against verified bank statement logs.
*   **Completeness:** Flag applications with missing tax or registration records.
*   **Consistency:** Normalizes data parameters across different registry types.
*   **Timeliness:** Query logs daily to keep credit limits aligned with current profiles.

---

## PART 14: Information Governance Framework
*   **Data Governance Committee (DGC):** Meets monthly to review quality audits and data access logs.
*   **Compliance Verification:** Automated verification of data classifications before release.
*   **Escalation Logic:** Data discrepancies escalated from Stewards to Owners within 24 hours.

---

## PART 15: Information Security Classification

Each information domain is mapped to standard security profiles:

| Information Domain | Confidentiality | Integrity | Availability | Privacy | Encryption | Auditability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Customer Profile** | Confidential | High | High | High | TLS & AES-256| Full Trail |
| **Credit Scoring** | Restricted | High | High | Medium | AES-256 | Full Trail |
| **Alternate Data** | Restricted | High | Medium | High | AES-256 | Full Trail |
| **AI Prompts** | Restricted | High | High | Low | TLS | Versioned |

---

## PART 16: Information Lineage

All critical information objects are tracked from source to storage:

$$\text{Source (NSDL API)} \rightarrow \text{Validation (Apigee WAF)} \rightarrow \text{Ingestion (Cloud Run)} \rightarrow \text{Encryption (Cloud KMS)} \rightarrow \text{Active DB (AlloyDB)} \rightarrow \text{Warehouse (BigQuery)} \rightarrow \text{Dashboard (Looker)}$$

This ensures auditors can trace any calculated credit score back to its raw registry source.

---

## PART 17: Enterprise Reporting Information Model
*   **Board & CEO Report:** Financial portfolios, NIM growth, Gross NPA, and Priority sector lending metrics.
*   **Credit & Risk Report:** Queue logs, average decision TAT, and early warning signal alerts frequency.
*   **Regulators Report:** Priority sector categories, credit guarantee claims, and DPDP compliance audits.

---

## PART 18: Enterprise KPI Information Model
*   **Portfolio Yield:** requires active interest schedules and outstanding loan balances.
*   **Decision TAT:** requires application submit and approval timestamps.
*   **NPA Ratio:** requires credit classification flags and outstanding ledger balances.

---

## PART 19: Information Risks
*   **Registry Format Risk:** External registry schema modifications may break ingestion pipelines.
*   **Data Leak Risk:** Risk of unauthorized customer data exposure on public frontends.
*   **Stale Data Risk:** Outdated transaction files may lead to incorrect credit limits.

---

## PART 20: Information Assumptions
*   **API Stability:** Assume national DPI gateways maintain stable API services.
*   **Data Accuracy:** Assume data fetched from central government registries is accurate.
*   **Storage Performance:** Assume database clusters handle the required read/write latencies.

---

## PART 21: Future Information Strategy
*   **Year 1-2 (Integrated Data):** Complete alternate data pipeline integrations (GST, AA, EPFO).
*   **Year 3-4 (Intelligent Data):** Deploy real-time risk scoring and conversational reporting engines.
*   **Year 5 (Autonomous Data):** Self-learning credit scoring networks operating within human validation.

---

## PART 22: Enterprise Information Reference Model

The reference model connects all information domains:

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   AAROHAN INFORMATION REFERENCE MODEL                  │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 1. alternate Data: GSTN transaction logs, EPFO counts, AA balances     │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 2. Core Entities: Customer profile, Credit proposal, Loan Account      │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 3. Metadata Engine: Technical formats, AI prompts, compliance logs     │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 4. Governance Layer: DGC guidelines, RBAC roles, encryption keys       │
  └────────────────────────────────────────────────────────────────────────┘
```

*   **Ingestion Gateway:** Expose and route services using secure gateways.
*   **Analytics Layer:** Process transaction files using BigQuery and Looker dashboards.
*   **Security & Compliance:** Log all approvals and access histories in write-once audit stores.

---

## PART 23: Conclusion
*   **Purpose:** Conclude the Enterprise Information Architecture document.
*   **Business Objective:** Approve the target business information classifications and lifecycles.
*   **Banking Objective:** Align data stewardship and quality audits under a single framework.
*   **Regulatory Considerations:** Prepares the platform for regulatory inspects.
*   **Deliverables:** Approved Information Reference Architecture.
*   **Owner:** Chief Information Architect (CIA).
*   **Review Authority:** Board of Directors.
