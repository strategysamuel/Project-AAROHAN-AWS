# Enterprise API, Apigee & Digital Contract Architecture

**Document ID:** AAR-APS-026  
**Document Name:** Enterprise API, Apigee & Digital Contract Architecture  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 through AAR-AIS-025 (All Previous Reference Architecture & AI Platform Volumes)  
**Next Artifact:** AAR-EDA-027 (Enterprise Event-Driven Banking Architecture)  
**Target Audience:** IDBI Bank Board, CIO, CTO, API Design Teams, Google Cloud Principal API Architects, and Partner Integrators  
**Document Owner:** Chief API Architect / Apigee Architect  
**Approval Authority:** API Governance Board (AGB) / EARB  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Google Cloud Professional Services | Initial Release of Enterprise API & Apigee Architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [API Vision & Principles](#api-vision--principles)
3. [API Domains Reference Catalogue (36 Domains)](#api-domains-reference-catalogue-36-domains)
4. [Digital Contract Model](#digital-contract-model)
5. [API Governance Framework](#api-governance-framework)
6. [Banking Ecosystem API Integration](#banking-ecosystem-api-integration)
7. [Google Cloud Conceptual Mapping](#google-cloud-conceptual-mapping)
8. [API Traceability Matrix](#api-traceability-matrix)
9. [Conclusion](#conclusion)

---

## Executive Summary
This document defines the Enterprise API, Apigee & Digital Contract Architecture (AAR-APS-026) for Project AAROHAN. It maps the gateway configurations, rate-limiting rules, OAuth credential directories, digital API contracts, and integration pathways needed to run a secure, serverless, and API-first banking system. The ERDA guidelines ensure that all Apigee proxies, tool-calling APIs, and partner interfaces conform to zero-trust principles.

---

## API Vision & Principles
*   **Vision:** Establish a secure, governed, and highly reusable API layer that acts as the primary communication bus connecting customers, RMs, underwriters, risk monitors, AI agents, and national DPI registries.
*   **API Principles:** API-First Design, Loose Coupling, Strict Schema Versioning, Zero PII Exposure, and Consent Validation Checkpoints.

---

## API Domains Reference Catalogue (36 Domains)

Below are the detailed specifications for key API domains:

### API Domain 31: GST Integration APIs
*   **API Domain ID:** API-031
*   **Purpose:** Fetch and normalise invoice turnovers from tax registries.
*   **Business Capability:** Financial Health Assessment.
*   **Consumers:** Credit Analyst Agent, Underwriters, Risk engines.
*   **Providers:** GSTN registry, API gateway.
*   **Security Classification:** Restricted.
*   **Authentication:** Mutual TLS (mTLS).
*   **Authorization:** Verified against active customer consent tokens.
*   **Rate Limiting:** 100 requests per minute per borrower file.
*   **Versioning:** Semantic versioning (v1, v2).
*   **Error Handling:** API timeout (504 gateway timeout) triggers automatic retry queues.
*   **Audit Requirements:** Log client PAN, timestamp, and payload size.
*   **SLA:** Response latency < 3 seconds.
*   **KPIs:** API connection latency, payload size.
*   **Future Google Cloud Service Mapping:** Apigee, Cloud Run, Cloud KMS.

---

### API Domain 36: Core Banking CBS APIs
*   **API Domain ID:** API-036
*   **Purpose:** Route verified loan disbursement and repayment records to core ledgers.
*   **Business Capability:** Loan Disbursement.
*   **Consumers:** Disbursement Service, Workflow Engine.
*   **Providers:** Core Finacle database.
*   **Security Classification:** Highly Confidential.
*   **Authentication:** Client certificates and token verification.
*   **Authorization:** Restricted to Authorized Operations engines.
*   **Rate Limiting:** 1,000 requests per minute.
*   **Versioning:** Major revisions only (v1.0).
*   **Error Handling:** Database lock errors trigger transaction rollback alerts.
*   **Audit Requirements:** Log all transaction balances and account numbers.
*   **SLA:** Response latency < 50ms.
*   **KPIs:** Connection availability rate, sync latency.
*   **Future Google Cloud Service Mapping:** Apigee, Secret Manager, Cloud KMS.

---

*Note: All other 34 API domains (Customer, Authentication, Consent, MSME Profile, Financial Health, Credit, CAM, Risk, Pricing, Collateral, Document, AI Decision, Agent, MCP Tool, Knowledge, RAG, Knowledge Graph, Portfolio, Analytics, Dashboard, Notification, Workflow, Audit, Administration, Configuration, Regulatory, Partner, OCEN, ULI, Account Aggregator, EPFO, TReDS, CGTMSE, and Credit Bureau APIs) follow the same structured design specification, conceptually mapped to their respective native Google Cloud services.*

---

## Digital Contract Model
*   **Service Contracts:** REST schemas define request/response formats.
*   **Data Contracts:** Enforce data validation rules and mask PII fields.
*   **AI & MCP Contracts:** JSON-RPC tool schemas define inputs and parameters for Gemini models.
*   **Compatibility:** All API modifications must maintain backward compatibility within minor versions.

---

## API Governance Framework
*   **API Review Board (ARB):** Reviews and approves all new API contracts and changes.
*   **Onboarding:** Partners register and acquire credentials via developer portals.
*   **Deprecation Policy:** Deprecated endpoints are supported for 90 days before deactivation.

---

## Banking Ecosystem API Integration
*   **Finacle CBS Integration:** Secured using Apigee proxies and private networking links.
*   **DPI Registries:** Direct API connections to Account Aggregator (AA), Unified Lending Interface (ULI), and GSTN.
*   **Supply Chain Networks:** API interfaces for TReDS exchanges and ONDC.

---

## Google Cloud Conceptual Mapping
*   **Gateway & Security:** Apigee, API Gateway, Cloud Armor, IAM.
*   **Compute & Integration:** Cloud Run, Cloud Workflows, Pub/Sub.
*   **Data & Registry:** AlloyDB, Secret Manager.

---

## API Traceability Matrix

This matrix traces API capabilities to business and functional requirements:

| API Domain ID | Business Capability | Functional Module | Workflow ID | Requirement ID | GCP Target Service |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API-031** | Financial Health | Module 5 | WF-002 | FR-002 | Apigee, Cloud Run |
| **API-036** | Loan Disbursement | Module 36 | WF-001 | FR-001 | Apigee, KMS |
| **API-003** | Consent management | Module 4 | WF-001 | FR-001 | Apigee, AlloyDB |
| **API-013** | AI RM Copilot | Module 17 | WF-003 | FR-003 | Gemini, ADK |

---

## Conclusion
*   **Purpose:** Conclude the API & Apigee Architecture document.
*   **Business Objective:** Approve the target business integration and API lifecycles.
*   **Banking Objective:** Baselines all credit and risk designs under a single framework.
*   **Regulatory Considerations:** Prepares the platform for API security inspections.
*   **Deliverables:** Approved API Reference Architecture.
*   **Owner:** Chief API Architect.
*   **Review Authority:** Board of Directors.
