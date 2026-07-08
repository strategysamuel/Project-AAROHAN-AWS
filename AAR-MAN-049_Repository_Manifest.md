# Enterprise Repository Manifest, Knowledge Atlas, Master Index & Documentation Navigation Framework

**Document ID:** AAR-MAN-049  
**Document Name:** Enterprise Repository Manifest, Knowledge Atlas, Master Index & Documentation Navigation Framework  
**Version:** 1.0  
**Status:** Approved / Production-Ready  
**Dependencies:** AAR-REF-048 (Enterprise Reference Architecture)  
**Target Audience:** IDBI Bank Board, CIO, CTO, Enterprise Architecture Board, PMO, Internal Audit, and Google Cloud Professional Services  

---

## 1. Executive Summary & Knowledge Vision

### Executive Summary
This document serves as the master navigation index and knowledge management framework for the entire Project AAROHAN documentation repository. It aggregates, catalogs, and traces the development of strategic assets, from initial requirements through system architectures, operating procedures, and product roadmaps. This framework establishes the standards for documentation versioning, approval workflows, and updates, ensuring our technical records remain current, auditable, and easily accessible.

### Knowledge Management Vision
IDBI Bank treats its project documentation as a structured enterprise asset. Our goal is to maintain a unified, searchable, and fully traceable documentation library. By structuring documents into clear knowledge domains, we ensure that engineers, risk officers, and auditors can easily find system specifications and verify design decisions.

### Repository Governance
1. **Document Ownership:** Every document has a designated executive owner responsible for its accuracy and updates.
2. **Strict Version Control:** All modifications must be recorded in the change ledger, showing version numbers and approval dates.
3. **Structured Review Cycles:** Documents are reviewed bi-annually to confirm alignment with system software and regulatory changes.

---

## 2. Knowledge Atlas Domains

The AAROHAN documentation repository is structured across 14 strategic knowledge domains.

```
  ┌──────────────────────────────────────────────────────────┐
  │                 AAROHAN KNOWLEDGE ATLAS                  │
  ├────────────────────────────┬─────────────────────────────┤
  │      Strategy & Product    │    Architecture & Design    │
  │  - Executive Strategy      │  - Enterprise Architecture  │
  │  - Business Architecture   │  - AI & Data Architecture   │
  ├────────────────────────────┼─────────────────────────────┤
  │     Operations & Run       │   Security & Governance     │
  │  - Operating Procedures    │  - Information Security     │
  │  - Knowledge Transfer      │  - Regulatory Compliance    │
  └────────────────────────────┴─────────────────────────────┘
```

*   **Executive Strategy:** High-level vision files, program budgets, and executive dashboards.
*   **Business Architecture:** Target business capabilities, customer onboarding flows, and product definitions.
*   **Banking Architecture:** Credit limits configurations, interest calculation rules, and payment gateways.
*   **Enterprise Architecture:** System integration models, API gateway rules, and event messaging.
*   **AI Architecture:** Large Language Model configurations, prompt registries, and agent boundaries.
*   **Data Architecture:** Operational databases, analytical tables, and vector store configurations.
*   **Security & Risk:** Information security standards, access logs, and EWS rules.
*   **Engineering & DevSecOps:** Software builds, unit testing guidelines, and deployment steps.
*   **Operations & Run:** Standard operating procedures, L1/L2 runbooks, and escalation procedures.
*   **Regulatory & Audit:** Audit evidence files, tax reports, and compliance certificates.
*   **Innovation:** Sandbox test results, new product prototypes, and research notes.
*   **Digital Public Infrastructure:** ULI, OCEN, and GSTN interface specifications.
*   **Reference Architecture:** Composable component models and system reuse guidelines.
*   **Knowledge Management:** Repository indexes, dictionaries, and glossary frameworks.

---

## 3. Master Document Index (AAR-ERDA-001 to AAR-MAN-049)

This master index catalogs the chronological development of the core Project AAROHAN architecture and strategy documents.

| Document ID | Document Name | Purpose | Owner | Dependencies | Dependent Docs | Architecture Domain | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AAR-ERDA-001** | Executive Strategy & Business Goals | Set program goals and business parameters. | CBO | None | AAR-BRD-002 | Business Strategy | Approved |
| **AAR-BRD-002** | Business Requirements Document | Define MSME lending features and user stories. | CBO | AAR-ERDA-001 | AAR-FSD-005 | Business Architecture | Approved |
| **AAR-FSD-005** | Functional Specifications Document | Map features to system modules and APIs. | CTO | AAR-BRD-002 | AAR-SAD-010 | Application Architecture | Approved |
| **AAR-SAD-010** | System Architecture Document | Define software structures and container deployments. | CTO | AAR-FSD-005 | AAR-DAD-015 | Enterprise Architecture | Approved |
| **AAR-DAD-015** | Data Architecture Document | Map transaction schemas and database tables. | Lead DBA | AAR-SAD-010 | AAR-AIAD-020 | Data Architecture | Approved |
| **AAR-AIAD-020** | AI & Agent Architecture Document | Define agent boundaries and prompt rules. | CAIO | AAR-DAD-015 | AAR-ISD-030 | AI Architecture | Approved |
| **AAR-ISD-030** | Information Security & Access Controls | Enforce zero-trust and encryption keys. | CISO | AAR-AIAD-020 | AAR-SOP-040 | Security & Risk | Approved |
| **AAR-SOP-040** | Standard Operating Runbook | Detail daily system operations and L1 logs. | COO | AAR-ISD-030 | AAR-EXE-042 | Operations & Run | Approved |
| **AAR-EXE-042** | Executive Strategy & Blueprint | Present architectural blueprint to the board. | CIO | AAR-SOP-040 | AAR-OPS-043 | Business Strategy | Approved |
| **AAR-OPS-043** | Enterprise Operating Manual | Define 30 operational domains and escalation rules. | COO | AAR-EXE-042 | AAR-LRM-044 | Operations & Run | Approved |
| **AAR-LRM-044** | Enterprise Product Roadmap (2026-2035) | Phase capital and technical updates. | CPO | AAR-OPS-043 | AAR-DIG-045 | Business Strategy | Approved |
| **AAR-DIG-045** | Enterprise DPI & Ecosystem Strategy | Interface with India Stack registries. | CDO | AAR-LRM-044 | AAR-GEN-046 | DPI Integration | Approved |
| **AAR-GEN-046** | Next-Gen AI Banking Innovation Blueprint | Map AI growth from 2026 to 2035. | CAIO | AAR-DIG-045 | AAR-IP-047 | AI Architecture | Approved |
| **AAR-IP-047** | Enterprise Intellectual Property Framework | Protect custom code, scoring, and patents. | CINO | AAR-GEN-046 | AAR-REF-048 | Legal & IP | Approved |
| **AAR-REF-048** | Enterprise Reference Architecture | Establish composable service models. | CEA | AAR-IP-047 | AAR-SCR-001 | Reference Architecture | Approved |
| **AAR-SCR-001** | Enterprise UI Screen Blueprint, Screen Inventory & Navigation Architecture | Define the screen catalogues, navigation structures, and widget matrices. | Chief UX Architect | AAR-REF-048 | AAR-BLD-001 | Experience Architecture | Approved |
| **AAR-BLD-001** | Enterprise Engineering Build Blueprint, Module Development Guide & Implementation Accelerator | Translate functional models into work packages, sprints, pipelines, and QA gates. | Chief Delivery Architect | AAR-SCR-001 | AAR-API-CATALOG-001 | Engineering & DevSecOps | Approved |
| **AAR-API-CATALOG-001** | Enterprise API, Event & Integration Contract Catalogue | Define the core API contracts, event wrapper schemas, and external integrations. | Chief API Architect | AAR-BLD-001 | AAR-DATA-CATALOG-001 | Enterprise Integration | Approved |
| **AAR-DATA-CATALOG-001** | Enterprise Canonical Data Model, Data Dictionary & Information Architecture | Define business entities, data stewards, validation checks, and line-level classifications. | Chief Data Architect | AAR-API-CATALOG-001 | AAR-ENG-PLAYBOOK-001 | Data Architecture | Approved |
| **AAR-ENG-PLAYBOOK-001** | Enterprise Development Standards, Engineering Playbook & Delivery Guidelines | Enforce programming standards, testing frameworks, secure SDLC controls, and Git guidelines. | Chief Engineering Excellence Officer | AAR-DATA-CATALOG-001 | AAR-DEMO-DATA-001 | Engineering & DevSecOps | Approved |
| **AAR-DEMO-DATA-001** | Enterprise Demo Dataset, Banking Personas, Business Scenarios & AI Evaluation Dataset Blueprint | Define personas, business scenarios, dashboard datasets, and AI validation test suites. | Chief Banking Expert | AAR-ENG-PLAYBOOK-001 | AAR-QA-PLAYBOOK-001 | Business Strategy | Approved |
| **AAR-QA-PLAYBOOK-001** | Enterprise Testing, AI Validation, Certification, Production Readiness & Go-Live Playbook | Define testing methodologies, banking calculation validations, model check scenarios, and hypercare plans. | Chief QA Officer | AAR-DEMO-DATA-001 | AAR-IMP-PLAN-001 | Engineering & DevSecOps | Approved |
| **AAR-IMP-PLAN-001** | Enterprise Implementation Master Plan, Sprint Roadmap & Delivery Execution Guide | Establish phase-wise implementation tracks, sprint milestones, ready/done requirements, and rollout schedules. | Program Delivery Director | AAR-QA-PLAYBOOK-001 | AAR-BOOT-001 | Business Strategy | Approved |
| **AAR-BOOT-001** | Google Cloud Engineering Bootstrap & Repository Initialization Guide | Define folder structures, workspace settings, IAM scopes, and CI/CD pipelines. | Principal Delivery Engineer | AAR-IMP-PLAN-001 | AAR-MAN-049 | Engineering & DevSecOps | Approved |
| **AAR-MAN-049** | Enterprise Repository Manifest | Index and navigate documentation repository. | CEA | AAR-BOOT-001 | None | Knowledge Management | Approved |

---

## 4. Enterprise Glossary

*   **Account Aggregator (AA):** Financial utility enabling secure, digital sharing of client bank statements with consent.
*   **Agent Development Kit (ADK):** Software framework used to build and deploy autonomous AI agents.
*   **AlloyDB:** High-performance transactional database engine hosting operational states and vector databases.
*   **Apigee:** Central API gateway managing traffic security, rate limits, and registry proxy flows.
*   **BigQuery:** Cloud data warehouse processing analytics queries, risk modeling, and operational logs.
*   **CKYC (Central KYC Registry):** Centralized registry validating customer identity documents.
*   **Early Warning System (EWS):** Automated monitoring query flagging payment anomalies and operational default risks.
*   **Gemini:** Evolving multimodal Large Language Models powering document extraction and credit recommendations.
*   **Model Context Protocol (MCP):** Open standard protocol defining secure tool and database access for AI agents.
*   **Unified Lending Interface (ULI):** National platform connecting lenders to property registries and credit bureaus.

---

## 5. Google Cloud Alignment

Google Cloud services provide the scalable infrastructure to manage and search this documentation repository:
*   **Vertex AI & Gemini:** Power semantic search engines that find system requirements and design configurations across all PDFs and markdown files in the repository.
*   **BigQuery & Looker:** Track document read histories, update schedules, and compliance metrics to display them on library management dashboards.
*   **Cloud Storage & KMS:** Store documentation files securely using write-once-read-many (WORM) parameters and rotate access keys automatically.

---

## 6. Strategic Traceability Matrix

| Strategy Initiative | Architecture Domain | Target Business Area | Primary AI Tool | Executive KPI | Google Cloud Capability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Documentation Search** | Knowledge Management | Operations & Audit | Semantic Vector Search| Audit Prep Time | Vertex AI, AlloyDB |
| **Asset Indexing** | Repository Manifest | Program PMO | Metadata Database | Triage Latency | BigQuery, Looker |
| **Access Control** | Security & Risk | Compliance | Identity IAM | Key Breach Count | IAM, Cloud KMS |

---

## 7. Document Approval & Change History

*   **Approved By:** 
    *   *Chief Knowledge Officer (IDBI Bank)*
    *   *Chief Enterprise Architect (IDBI Bank)*
    *   *Lead Professional Services Consultant (Google Cloud)*
*   **Approval Date:** July 7, 2026

| Version | Date | Author | Description of Change | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Enterprise Architect | Initial strategic manifest release under Project AAROHAN. | CKO, CEA |
