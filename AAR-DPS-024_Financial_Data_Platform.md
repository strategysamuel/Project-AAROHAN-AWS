# Enterprise Financial Data Intelligence Platform (FDIP)

**Document ID:** AAR-DPS-024  
**Document Name:** Enterprise Financial Data Intelligence Platform (FDIP)  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 through AAR-KG-023 (All Previous Reference Architecture & Knowledge Graph Volumes)  
**Next Artifact:** AAR-AIS-025 (Vertex AI, Gemini & AI Model Lifecycle Architecture)  
**Target Audience:** IDBI Bank Board, Chief Data Officer, CIO, CTO, Data Engineers, and Analytics Teams  
**Document Owner:** Chief Data Architect (CDA) / BigQuery Architect  
**Approval Authority:** Data Governance Council (DGC) / EARB  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Google Cloud Professional Services | Initial Release of Enterprise FDIP. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Enterprise Data Platform Vision](#enterprise-data-platform-vision)
3. [Data Domains & Metadata Registry (30 Domains)](#data-domains--metadata-registry-30-domains)
4. [Data Ingestion Patterns](#data-ingestion-patterns)
5. [Enterprise Data Products Strategy](#enterprise-data-products-strategy)
6. [AI Feature Platform Architecture](#ai-feature-platform-architecture)
7. [Enterprise Analytics & BI Platform](#enterprise-analytics--bi-platform)
8. [Data Governance & Dataplex Framework](#data-governance--dataplex-framework)
9. [Financial Health Engine Data Model](#financial-health-engine-data-model)
10. [Google Cloud Conceptual Mapping](#google-cloud-conceptual-mapping)
11. [FDIP Traceability Matrix](#fdip-traceability-matrix)
12. [Conclusion](#conclusion)

---

## Executive Summary
This document defines the Enterprise Financial Data Intelligence Platform (AAR-DPS-024) for Project AAROHAN. It maps the storage structures, feature platforms, analytical tables, metadata tags, governance frameworks, and ingestion tracks needed to run a secure, serverless commercial lending database. The ERDA guidelines ensure that all components are configured according to Google Cloud Well-Architected and Dataplex principles.

---

## Enterprise Data Platform Vision
*   **Vision:** Transition from traditional, siloed transactional databases to an integrated Financial Data Intelligence Platform (FDIP) that acts as a single, secure foundation for operational reporting, predictive features, and AI agent grounding.
*   **Data Principles:** Domain Ownership, Data as a Product, Federated Governance, and Self-Service Access.

---

## Data Domains & Metadata Registry (30 Domains)

Below are the detailed specifications for key data domains:

### Data Domain 7: Financial Health Data
*   **Domain ID:** DOM-007
*   **Purpose:** Store parsed and validated transaction indices and health indicators.
*   **Business Owner:** Head of Underwriting.
*   **Data Steward:** Credit Data Analyst.
*   **Primary Sources:** GSTN, bank statements (via AA), EPFO.
*   **Consumers:** Credit Analyst Agent, Underwriters, Risk analysts.
*   **Critical Data Elements:** Alt-DSCR, interest coverage, invoice values, late tax dates.
*   **Quality Rules:** Turnover figures must match bank credits with less than 2% variance.
*   **Retention:** Active use plus 10 years in encrypted archives.
*   **Sensitivity Classification:** Restricted.
*   **Regulatory Considerations:** RBI digital lending guidelines and consent frameworks.
*   **AI Usage:** Vertex AI prompt grounding and scoring calculations.
*   **KPIs:** Data retrieval latency, data completeness score.
*   **Future GCP Service Mapping:** AlloyDB, BigQuery, Dataplex.

---

### Data Domain 8: Alternate Data
*   **Domain ID:** DOM-008
*   **Purpose:** Ingest raw tax and statement registries data payloads.
*   **Business Owner:** Chief API Architect.
*   **Data Steward:** Integration Engineer.
*   **Primary Sources:** GSTN API, AA API, EPFO gateway.
*   **Consumers:** Credit scoring engines, EWS consoles.
*   **Critical Data Elements:** Tax file dates, employee counts, statement credits.
*   **Quality Rules:** Consent token signatures must be valid.
*   **Retention:** Ingest cache (30 days) -> Encrypted archive.
*   **Sensitivity Classification:** Restricted.
*   **Regulatory Considerations:** Consent verification and DPDP compliance.
*   **AI Usage:** Pre-spreading normalizations.
*   **KPIs:** Payload validation rate, ingestion TAT.
*   **Future GCP Service Mapping:** BigLake, Cloud Storage, Apigee.

---

*Note: All other 28 domains (Customer, MSME, Credit, Loans, Collateral, Risk, UPI, Account Aggregator, EPFO, Income Tax, TReDS, CGTMSE, Government Schemes, Supply Chain, CRM, Relationship Banking, Portfolio, Collections, Recovery, Fraud, Compliance, Audit, Knowledge, AI, Agent Telemetry, Operational Metrics, Executive KPIs, and Metadata) follow the same structured design specification, conceptually mapped to their respective native Google Cloud services.*

---

## Data Ingestion Patterns
*   **API-based Ingestion:** Eventarc and Pub/Sub route real-time registry payload requests to secure processors.
*   **Batch Ingestion:** Dataflow coordinates nightly transactions replication from core Finacle ledgers to BigQuery.
*   **Document Ingestion:** Cloud Storage triggers Document AI pipelines to extract tables from scanned balance sheets.

---

## Enterprise Data Products Strategy
*   **Financial Health Product:** Exposes Alt-DSCR and compliance indicators.
*   **Risk Intelligence Product:** Exposes warning indicators and defaults metrics.
*   **AI Feature Product:** Standardizes features for Vertex AI model grounding.

---

## AI Feature Platform Architecture
*   **Feature Engineering:** Automate calculations of invoice turnover averages and EMI checks.
*   **Feature Governance:** Dataplex catalogues all approved features to ensure reuse.
*   **Feature Lineage:** Traces feature values from raw database transactions to Looker dashboard visualizations.

---

## Enterprise Analytics & BI Platform
*   **Operational Analytics:** Looker dashboards display file queues, TAT, and exception rates.
*   **Executive Dashboards:** High-level metrics tracking Gross NPA, NIM, and Priority sector lending sub-targets.
*   **Self-Service BI:** BigQuery sandbox zones allow risk analysts to run custom SQL queries.

---

## Data Governance & Dataplex Framework
*   **Dataplex:** Automatically catalogs metadata, runs data quality checks, and monitors database security parameters.
*   **Metadata Registry:** Stores business descriptions, column formats, and lineage traces.

---

## Financial Health Engine Data Model
The engine calculates scores across eight core segments:
*   *Financial Score:* debt coverage ratios.
*   *Behavioral Score:* account balances variations.
*   *Compliance Score:* GST tax filing delays.
*   *Growth Score:* monthly invoice value trends.

---

## Google Cloud Conceptual Mapping
*   **Data Lakehouse:** BigQuery, BigLake, Dataplex.
*   **Transactional Store:** AlloyDB.
*   **Pipeline & Queue:** Dataflow, Pub/Sub, Eventarc.
*   **AI Feature Store:** Vertex AI Feature Store.
*   **BI & Dashboards:** Looker, Looker Studio.

---

## FDIP Traceability Matrix

This matrix traces data capabilities to business and functional requirements:

| Capability ID | Business Capability | Functional Module | Target GCP Service | Quality Metric |
| :--- | :--- | :--- | :--- | :--- |
| **FDIP-001** | Financial Health Assessment | Module 6 | BigQuery, AlloyDB | Retrieval Latency |
| **FDIP-002** | Risk Monitoring | Module 10 | BigQuery, Looker | Analysis Timeliness |
| **FDIP-003** | Credit scoring | Module 8 | Vertex AI Store | Feature Accuracy |
| **FDIP-004** | Onboarding KYC | Module 2 | Apigee, BigQuery | Validation Rate |

---

## Conclusion
*   **Purpose:** Conclude the FDIP Architecture document.
*   **Business Objective:** Approve the target business data products and registries.
*   **Banking Objective:** Baselines all credit and risk designs under a single framework.
*   **Regulatory Considerations:** Prepares the platform for data privacy audits.
*   **Deliverables:** Approved Data Platform Architecture.
*   **Owner:** Chief Data Officer (CDO).
*   **Review Authority:** Board of Directors.
