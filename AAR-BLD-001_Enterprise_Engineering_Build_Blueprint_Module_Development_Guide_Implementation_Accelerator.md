# Enterprise Engineering Build Blueprint, Module Development Guide & Implementation Accelerator

**Document ID:** AAR-BLD-001  
**Document Name:** Enterprise Engineering Build Blueprint, Module Development Guide & Implementation Accelerator  
**Version:** 1.0  
**Status:** Approved for Engineering Execution  
**Dependencies:** Entire Enterprise Repository, Executive Compendium (AAR-EXEC-BOOK-001), Demo Storyboard (AAR-DEMO-001), UX Playbook (AAR-UX-PLAYBOOK-001), and Screen Blueprint (AAR-SCR-001)  
**Target Audience:** Engineering Managers, Technical Architects, Backend/Frontend Engineers, AI/Data/QA/DevSecOps Engineers, and Google Cloud Professional Services  
**Document Owner:** Chief Engineering Delivery Architect  
**Approval Authority:** Enterprise Architecture Review Board (EARB) / CTO Office

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Engineering Delivery Architect | Initial Release of Complete Engineering Build Blueprint. | CTO / EARB |

---

## Table of Contents
1. [Executive Summary & Engineering Governance](#executive-summary--engineering-governance)
2. [Logical Module Decomposition (20 Engineering Domains)](#logical-module-decomposition-20-engineering-domains)
3. [Engineering Delivery Framework](#engineering-delivery-framework)
4. [Google Cloud Conceptual Alignment Map](#google-cloud-conceptual-alignment-map)
5. [Implementation Accelerator & Sprint Planner](#implementation-accelerator--sprint-planner)
6. [Quality Gates, Testing Readiness & Release Principles](#quality-gates-testing-readiness--release-principles)

---

## Executive Summary & Engineering Governance

This document establishes the strategic delivery blueprint for Project AAROHAN, translating the target functional and solution architectures into executable, modular engineering work packages. It defines the decomposition, sequencing, ownership, environment routing, and quality parameters required for a Tier-1 banking release. 

### Core Delivery Directives:
*   **Security Baseline:** Zero-trust networks, mandatory Secret Manager token injection, and field-level masking.
*   **AI Integration:** Autonomous agent orchestration built via the Agent Development Kit (ADK) using the Model Context Protocol (MCP) for back-end system lookups.
*   **Scale Target:** Microservices isolated inside Cloud Run container instances, orchestrated via Cloud Workflows.

---

## Logical Module Decomposition (20 Engineering Domains)

### 1. Authentication & Identity
*   **Module ID:** AAR-MOD-ATH-001
*   **Business Purpose:** Ensure secure, centralized IAM and customer single sign-on (SSO).
*   **Scope:** Customer OTP auth, employee Active Directory/OIDC login, session validation.
*   **Business Capabilities:** Multi-Factor Authentication (MFA), Single Sign-On (SSO), OAuth2 Token Granting.
*   **Screens Supported:** All portal login canvases (Customer, RM, Branch, Committee, Admin).
*   **AI Features:** Adaptive risk-based step-up authentication.
*   **Google Cloud Services:** Identity Platform, Identity-Aware Proxy (IAP), Secret Manager.
*   **Dependencies:** Core Banking User Directory, SMS Gateway.
*   **Engineering Team:** CyberSecurity & Identity Team (CS-ID).
*   **Suggested Development Order / Parallelization:** Step 1 / High (foundation block).
*   **Testing Requirements:** Penetration testing, OAuth token validation, load testing under 10k concurrent requests/sec.
*   **Definition of Done:** 100% test coverage, OWASP Top-10 audit pass, zero secrets stored in code.
*   **Business Acceptance Criteria:** Seamless, secure login within 3 seconds; auto-lockout after 5 failed attempts.
*   **Risks & Mitigation:** Identity token theft. *Mitigation:* Short-lived JWTs (15 min) and OAuth 2.0 refresh token rotation.

---

### 2. User & Role Management
*   **Module ID:** AAR-MOD-URL-002
*   **Business Purpose:** Define and enforce role permissions and data access visibility levels.
*   **Scope:** Fine-grained role definition, row-level data security filters, employee assignment queues.
*   **Business Capabilities:** Role-Based Access Control (RBAC), Row-Level Security (RLS), Field-Level Masking.
*   **Screens Supported:** System Administration Portal (`AAR-SCR-SYS-001`).
*   **AI Features:** Dynamic permission anomaly flags.
*   **Google Cloud Services:** Cloud IAM, AlloyDB RLS Policies, Apigee (security proxy).
*   **Dependencies:** Authentication & Identity (`AAR-MOD-ATH-001`).
*   **Engineering Team:** Platform Services Group (PSG).
*   **Suggested Development Order / Parallelization:** Step 2 / Parallel with Auth module.
*   **Testing Requirements:** Verify role matrix permissions across all 14 personas.
*   **Definition of Done:** Row-level masking active for PII data in analytical stores.
*   **Business Acceptance Criteria:** Customer PII is fully masked for unauthorized bank staff.
*   **Risks & Mitigation:** Policy drift. *Mitigation:* GitOps-driven IAM policy sync.

---

### 3. MSME Onboarding
*   **Module ID:** AAR-MOD-MSM-003
*   **Business Purpose:** Provide frictionless registration and KYC verification for MSME clients.
*   **Scope:** Entity creation, registration wizard state tracking, document uploads.
*   **Business Capabilities:** Digital KYC validation, status logging.
*   **Screens Supported:** MSME Onboarding Canvas (`AAR-SCR-MSM-001`), RM Portal.
*   **AI Features:** Document extraction (ID cards, corporate licenses).
*   **Google Cloud Services:** Cloud Run, Cloud Storage, Document AI.
*   **Dependencies:** User & Role Management (`AAR-MOD-URL-002`), DPI Gateway.
*   **Engineering Team:** Digital Experience Squad (DXS).
*   **Suggested Development Order / Parallelization:** Step 3 / Parallel with Consent module.
*   **Testing Requirements:** Integration tests with Document AI OCR templates.
*   **Definition of Done:** Customer data forms auto-fill from scanned business documents.
*   **Business Acceptance Criteria:** Onboarding form completion under 10 minutes.
*   **Risks & Mitigation:** Poor image quality uploads. *Mitigation:* Client-side image validation.

---

### 4. Consent Management
*   **Module ID:** AAR-MOD-CON-004
*   **Business Purpose:** Capture and manage client permissions for financial data retrieval.
*   **Scope:** Account Aggregator consent workflows, permission logs.
*   **Business Capabilities:** Consent Artifact Signing, Event-driven consent tracking.
*   **Screens Supported:** Onboarding & Consent Center (`AAR-SCR-RM-002`).
*   **AI Features:** Conversational consent descriptions.
*   **Google Cloud Services:** Cloud Run, Pub/Sub, Firestore (consent registry).
*   **Dependencies:** Authentication & Identity (`AAR-MOD-ATH-001`).
*   **Engineering Team:** Platform Services Group (PSG).
*   **Suggested Development Order / Parallelization:** Step 4 / High parallelization potential.
*   **Testing Requirements:** Verification of digital signature workflows.
*   **Definition of Done:** Consent transactions logged securely in audit tables.
*   **Business Acceptance Criteria:** Customers can revoke financial access at any time.
*   **Risks & Mitigation:** Network timeouts during consent request triggers. *Mitigation:* Async polling and retry mechanisms.

---

### 5. Digital Public Infrastructure Integration
*   **Module ID:** AAR-MOD-DPI-005
*   **Business Purpose:** Connect to external national public registries (GSTN, India Stack, ULI).
*   **Scope:** API wrappers, data standard translation layers, mock server configurations.
*   **Business Capabilities:** Real-time business tax filing checks, property title lookups.
*   **Screens Supported:** RM Onboarding Canvas, Credit Analyst Portal.
*   **AI Features:** Tax history anomaly predictions.
*   **Google Cloud Services:** Apigee, Cloud Run, Cloud NAT.
*   **Dependencies:** Apigee Configuration, External Agency Gateways.
*   **Engineering Team:** Integration Squad (IS).
*   **Suggested Development Order / Parallelization:** Step 5 / Parallel with Onboarding.
*   **Testing Requirements:** Latency testing, third-party sandboxed load testing.
*   **Definition of Done:** 100% validation of incoming payloads against regional schemas.
*   **Business Acceptance Criteria:** External database calls complete within 2.5 seconds.
*   **Risks & Mitigation:** Third-party system downtime. *Mitigation:* Local caching of retrieved ratings and circuit breakers.

---

### 6. Financial Health Card Engine
*   **Module ID:** AAR-MOD-FHC-006
*   **Business Purpose:** Compile financial metrics, cash-flow trends, and debt service ratios.
*   **Scope:** Parsing bank statements, tax files, and generating score grids.
*   **Business Capabilities:** Real-time cash flow statement preparation, alternate credit scoring.
*   **Screens Supported:** Financial Health Card Screen (`AAR-SCR-CRE-001`).
*   **AI Features:** Pattern clustering for cash inflow trends.
*   **Google Cloud Services:** Cloud Run, BigQuery, AlloyDB.
*   **Dependencies:** DPI Integration (`AAR-MOD-DPI-005`), Consent Management (`AAR-MOD-CON-004`).
*   **Engineering Team:** Credit Engineering Team (CET).
*   **Suggested Development Order / Parallelization:** Step 6 / Sequential dependencies.
*   **Testing Requirements:** Precision matching verification against manually compiled spreadsheets.
*   **Definition of Done:** Automated calculation match rate of 100% on historical tests.
*   **Business Acceptance Criteria:** Spreading metrics calculated in less than 30 seconds.
*   **Risks & Mitigation:** Non-standard PDF file formats. *Mitigation:* Document parsing exception fallback queue.

---

### 7. AI Decision Intelligence
*   **Module ID:** AAR-MOD-AID-007
*   **Business Purpose:** Host and score AI models for risk classification and probability of default (PD).
*   **Scope:** Machine learning pipeline hosting, inference APIs, prediction logging.
*   **Business Capabilities:** AI-driven credit scoring, alternative default forecasting.
*   **Screens Supported:** Credit Analyst Spreading, Committee presentation.
*   **AI Features:** Machine Learning scorecards, transaction anomaly classification.
*   **Google Cloud Services:** Vertex AI, Gemini, BigQuery ML.
*   **Dependencies:** Financial Health Card Engine (`AAR-MOD-FHC-006`).
*   **Engineering Team:** Data & AI Squad (DAIS).
*   **Suggested Development Order / Parallelization:** Step 7 / Sequential dependency.
*   **Testing Requirements:** Back-testing predictions on historical data portfolios.
*   **Definition of Done:** Model latency under 200ms, audit-ready versioned logs.
*   **Business Acceptance Criteria:** Score accuracy meets minimum Gini coefficient threshold (>0.60).
*   **Risks & Mitigation:** Feature drift. *Mitigation:* Continuous model evaluation inside Vertex AI Model Registry.

---

### 8. Credit Assessment
*   **Module ID:** AAR-MOD-CAS-008
*   **Business Purpose:** Apply policy rules and decision trees to evaluate credit applications.
*   **Scope:** Credit policy matrix execution, risk tier categorization.
*   **Business Capabilities:** Policy compliance matching, exposure calculation.
*   **Screens Supported:** Credit Analyst Workspace (`AAR-SCR-CRE-001`).
*   **AI Features:** Predictive risk segment classification.
*   **Google Cloud Services:** Cloud Run, Cloud Workflows, AlloyDB.
*   **Dependencies:** AI Decision Intelligence (`AAR-MOD-AID-007`).
*   **Engineering Team:** Credit Engineering Team (CET).
*   **Suggested Development Order / Parallelization:** Step 8 / Core path dependency.
*   **Testing Requirements:** Unit testing of 200+ rule logic boundaries.
*   **Definition of Done:** Zero manual calculation overrides required for base policy parameters.
*   **Business Acceptance Criteria:** Automated eligibility check runs in less than 5 seconds.
*   **Risks & Mitigation:** Policy changes. *Mitigation:* Configurable rule criteria managed via GitOps dashboard.

---

### 9. CAM Generation
*   **Module ID:** AAR-MOD-CAM-009
*   **Business Purpose:** Draft and format the definitive Credit Assessment Memo (CAM).
*   **Scope:** PDF builder, template engine, text generation assembly.
*   **Business Capabilities:** Structured document packaging.
*   **ScreensSupported:** CAM Generation Console (`AAR-SCR-CRE-002`).
*   **AI Features:** Generative narrative summaries of financial strengths and weaknesses.
*   **Google Cloud Services:** Vertex AI (Gemini), Cloud Run, Cloud Storage.
*   **Dependencies:** Credit Assessment (`AAR-MOD-CAS-008`), Financial Health Engine (`AAR-MOD-FHC-006`).
*   **Engineering Team:** Credit Engineering Team (CET) & AI Squad.
*   **Suggested Development Order / Parallelization:** Step 9 / Parallel to workspace design.
*   **Testing Requirements:** PDF accessibility checks, formatting validation.
*   **Definition of Done:** Generated files conform to the standard banking structure and audit citations.
*   **Business Acceptance Criteria:** Automated drafting reduces manual preparation time by 60%.
*   **Risks & Mitigation:** Content inaccuracies (hallucinations). *Mitigation:* Citations linking summaries back to verified bank statements.

---

### 10. Workflow Engine
*   **Module ID:** AAR-MOD-WFE-010
*   **Business Purpose:** Manage states, locks, approvals, and transitions across the loan life cycle.
*   **Scope:** Workflow transitions, SLA trackers, task ownership management.
*   **Business Capabilities:** Lifecycle orchestration, state persistence.
*   **Screens Supported:** Queue Managers (RM, Credit Analyst, Committee).
*   **AI Features:** Predictive SLA routing.
*   **Google Cloud Services:** Cloud Workflows, Cloud Run, Firestore, Pub/Sub.
*   **Dependencies:** User & Role Management (`AAR-MOD-URL-002`).
*   **Engineering Team:** Platform Services Group (PSG).
*   **Suggested Development Order / Parallelization:** Step 3 (Base architecture engine).
*   **Testing Requirements:** Concurrency locking and race-condition validation.
*   **Definition of Done:** Safe state transitions verified with transactional commits.
*   **Business Acceptance Criteria:** Zero case locks stuck in pipeline states.
*   **Risks & Mitigation:** High concurrency contention on case files. *Mitigation:* Optimistic locking with automatic retries.

---

### 11. Notification Engine
*   **Module ID:** AAR-MOD-NOT-011
*   **Business Purpose:** Dispatch real-time alerts, SMS, push notifications, and emails.
*   **Scope:** Notification queue routing, templates, status logs.
*   **Business Capabilities:** Omni-channel notification alerts.
*   **Screens Supported:** Customer dashboard, RM Alerts Console.
*   **AI Features:** Best-time-to-send communications predictions.
*   **Google Cloud Services:** Pub/Sub, Cloud Run, Firebase Cloud Messaging.
*   **Dependencies:** Workflow Engine (`AAR-MOD-WFE-010`).
*   **Engineering Team:** Digital Experience Squad (DXS).
*   **Suggested Development Order / Parallelization:** Step 5 / Parallel implementation.
*   **Testing Requirements:** Delivery SLA checks, retry failures.
*   **Definition of Done:** Async messaging with guaranteed delivery logs.
*   **Business Acceptance Criteria:** Notifications delivered within 5 seconds of event triggers.
*   **Risks & Mitigation:** External gateway failures. *Mitigation:* Local dead-letter queues.

---

### 12. Relationship Manager Workspace
*   **Module ID:** AAR-MOD-RMW-012
*   **Business Purpose:** Provide sales staff with a mobile portal to register leads and track status.
*   **Scope:** Sales pipelines, meeting logs, task queues.
*   **Business Capabilities:** Onboard management, sales activity tracking.
*   **Screens Supported:** RM Dashboard & Pipeline (`AAR-SCR-RM-001`).
*   **AI Features:** Client email drafters.
*   **Google Cloud Services:** Cloud Run, Firestore, Looker (sales graphs).
*   **Dependencies:** Workflow Engine (`AAR-MOD-WFE-010`), Lead Engine.
*   **Engineering Team:** Digital Experience Squad (DXS).
*   **Suggested Development Order / Parallelization:** Step 10 / High parallelization.
*   **Testing Requirements:** Mobile web and browser validation tests.
*   **Definition of Done:** Mobile client loads fully within 2 seconds.
*   **Business Acceptance Criteria:** RMs can view lead progression updates instantly.
*   **Risks & Mitigation:** Slow cellular networks. *Mitigation:* Offline caching and compression.

---

### 13. Credit Committee Workspace
*   **Module ID:** AAR-MOD-CCW-013
*   **Business Purpose:** Facilitate review, voting, and pricing approvals on high-value files.
*   **Scope:** Agenda builder, casting votes, recording session decisions.
*   **Business Capabilities:** Multi-party voting.
*   **Screens Supported:** Committee Portal (`AAR-SCR-COM-001`).
*   **AI Features:** Meeting summarization.
*   **Google Cloud Services:** Cloud Run, AlloyDB, Pub/Sub.
*   **Dependencies:** Workflow Engine (`AAR-MOD-WFE-010`), CAM Generation (`AAR-MOD-CAM-009`).
*   **Engineering Team:** Credit Engineering Team (CET).
*   **Suggested Development Order / Parallelization:** Step 11 / Mid-level parallelization.
*   **Testing Requirements:** Secure consensus voting validations.
*   **Definition of Done:** All committee approvals require digital validation logs.
*   **Business Acceptance Criteria:** Voting status updates in real-time.
*   **Risks & Mitigation:** Uncommitted votes. *Mitigation:* Persistent stage audit logs.

---

### 14. Portfolio Intelligence
*   **Module ID:** AAR-MOD-PTI-014
*   **Business Purpose:** Aggregate and monitor post-disbursement loan profiles.
*   **Scope:** Amortization tracking, covenant verification.
*   **Business Capabilities:** Financial covenant tracking.
*   **Screens Supported:** Portfolio Monitoring (`AAR-SCR-PTM-001`).
*   **AI Features:** Covenant breach prediction models.
*   **Google Cloud Services:** BigQuery, Looker, Cloud Run.
*   **Dependencies:** Data Platform, Core Banking.
*   **Engineering Team:** Data & AI Squad (DAIS).
*   **Suggested Development Order / Parallelization:** Step 12 / Independent stream.
*   **Testing Requirements:** Large-scale query validation on BigQuery tables.
*   **Definition of Done:** Dashboards match general ledger account balances.
*   **Business Acceptance Criteria:** Portfolio dashboards refresh daily.
*   **Risks & Mitigation:** Large tables timeout. *Mitigation:* Partitioned tables.

---

### 15. Early Warning System
*   **Module ID:** AAR-MOD-EWS-015
*   **Business Purpose:** Flag high-risk accounts using transaction details.
*   **Scope:** Exception rule parsing, alert status queues.
*   **Business Capabilities:** Predictive account monitoring.
*   **Screens Supported:** EWS Alert Console (`AAR-SCR-RSK-001`).
*   **AI Features:** Cash flow trend predictions.
*   **Google Cloud Services:** BigQuery ML, Eventarc, Cloud Run, AlloyDB.
*   **Dependencies:** Portfolio Intelligence (`AAR-MOD-PTI-014`).
*   **Engineering Team:** Data & AI Squad (DAIS) / Credit Engineering.
*   **Suggested Development Order / Parallelization:** Step 13 / Independent.
*   **Testing Requirements:** Back-testing alerts on historical collections data.
*   **Definition of Done:** Real-time warnings generated for defined criteria.
*   **Business Acceptance Criteria:** Alerts appear within 24 hours of a critical trigger event.
*   **Risks & Mitigation:** High volume of false positive flags. *Mitigation:* Dynamic, AI-adjusted threshold adjustments.

---

### 16. Executive Dashboard
*   **Module ID:** AAR-MOD-EXD-016
*   **Business Purpose:** Present aggregate credit metrics and operational charts to executives.
*   **Scope:** KPI cards, geographical yields.
*   **Business Capabilities:** Executive performance reporting.
*   **Screens Supported:** Executive Cockpit (`AAR-SCR-EXE-001`, `AAR-SCR-EXE-002`).
*   **AI Features:** Summary briefings.
*   **Google Cloud Services:** Looker, BigQuery.
*   **Dependencies:** Portfolio Intelligence (`AAR-MOD-PTI-014`).
*   **Engineering Team:** Data & AI Squad (DAIS).
*   **Suggested Development Order / Parallelization:** Step 14 / Parallel to data ingestion.
*   **Testing Requirements:** Row-level data authorization test cases.
*   **Definition of Done:** Secure, aggregated dashboard reports.
*   **Business Acceptance Criteria:** Executive dashboards load in under 3 seconds.
*   **Risks & Mitigation:** High API costs. *Mitigation:* Looker caching layers.

---

### 17. AI Business Coach
*   **Module ID:** AAR-MOD-ABC-017
*   **Business Purpose:** Provide interactive financial advisory services to borrowers.
*   **Scope:** Advisor chat window, analysis narrative summaries.
*   **Business Capabilities:** Automated advisory support.
*   **Screens Supported:** MSME Portal.
*   **AI Features:** Conversational finance advisor.
*   **Google Cloud Services:** Vertex AI (Gemini), Agent Development Kit (ADK), Cloud Run.
*   **Dependencies:** AI Decision Intelligence (`AAR-MOD-AID-007`).
*   **Engineering Team:** Data & AI Squad (DAIS).
*   **Suggested Development Order / Parallelization:** Step 15 / High parallelization.
*   **Testing Requirements:** Prompt vulnerability assessments.
*   **Definition of Done:** Responses pass validation for accuracy and tone.
*   **Business Acceptance Criteria:** Customers receive clear, structured answers.
*   **Risks & Mitigation:** Inappropriate advice. *Mitigation:* Sandbox validation layers.

---

### 18. Reporting & Analytics
*   **Module ID:** AAR-MOD-RPT-018
*   **Business Purpose:** Generate statutory, regulatory, and credit reports.
*   **Scope:** Automated PDF generation, scheduler rules.
*   **Business Capabilities:** Compliance report building.
*   **Screens Supported:** Reports sections across portals.
*   **AI Features:** Automated description tagging.
*   **Google Cloud Services:** BigQuery, Looker, Cloud Run, Cloud Storage.
*   **Dependencies:** Data Platform.
*   **Engineering Team:** Platform Services Group (PSG).
*   **Suggested Development Order / Parallelization:** Step 8 / Independent.
*   **Testing Requirements:** Check format layout configurations.
*   **Definition of Done:** Reports compile without errors.
*   **Business Acceptance Criteria:** Batch reports execute within schedule limits.
*   **Risks & Mitigation:** Data exposure. *Mitigation:* Encryption key controls on export locations.

---

### 19. Administration
*   **Module ID:** AAR-MOD-ADM-019
*   **Business Purpose:** Manage platform settings, workflows, and loan pricing tiers.
*   **Scope:** Rule configurator, fee setup.
*   **Business Capabilities:** Dynamic policy configuration.
*   **Screens Supported:** Admin Configurator (`AAR-SCR-ADM-001`).
*   **AI Features:** Policy conflict warnings.
*   **Google Cloud Services:** Cloud Run, AlloyDB, Firestore.
*   **Dependencies:** User & Role Management (`AAR-MOD-URL-002`).
*   **Engineering Team:** PSG.
*   **Suggested Development Order / Parallelization:** Step 9 / Parallel.
*   **Testing Requirements:** Verification of access control parameters.
*   **Definition of Done:** Changes logged to audit trails.
*   **Business Acceptance Criteria:** Rules deploy instantly without code rebuilds.
*   **Risks & Mitigation:** System misconfiguration. *Mitigation:* Review workflow for config changes.

---

### 20. Platform Services
*   **Module ID:** AAR-MOD-PLS-020
*   **Business Purpose:** Shared utilities including PDF generation, caching, and document signing.
*   **Scope:** Reusable utility services.
*   **Business Capabilities:** Core framework services.
*   **Screens Supported:** N/A (Internal).
*   **AI Features:** Performance optimization recommendations.
*   **Google Cloud Services:** Cloud Run, Cloud Memorystore, Secret Manager.
*   **Dependencies:** None.
*   **Engineering Team:** Platform Services Group (PSG).
*   **Suggested Development Order / Parallelization:** Step 1 / Baseline framework.
*   **Testing Requirements:** Load testing of utility libraries.
*   **Definition of Done:** Shared packages published in internal registry.
*   **Business Acceptance Criteria:** 99.99% availability of basic shared services.
*   **Risks & Mitigation:** Component coupling. *Mitigation:* Modular interface designs.

---

## Engineering Delivery Framework

```
                       PROJECT MONOREPO
  ┌───────────────────────────┴───────────────────────────┐
  ├── apps/ (Deployment Applications)                     ├── packages/ (Shared Libraries)
  │   ├── customer-portal/                                │   ├── auth-lib/
  │   ├── employee-workspace/                             │   ├── dpi-schemas/
  │   └── admin-console/                                  │   └── api-client/
  └── infra/ (Terraform Code)                             └── services/ (Cloud Run Microservices)
      ├── landing-zones/                                      ├── spreading-engine/
      └── pipeline-definitions/                               └── report-generator/
```

### 1. Repository Structure
*   **Strategy:** Single Monorepo using `Turborepo` or `Nx` for build orchestration.
*   **Rationale:** Simpler dependency management across shared libraries, single CI pipeline execution, and shared type definitions.

### 2. Coding Standards & Review
*   **Frameworks:** TypeScript/Node.js for microservices, Python for data and AI workloads.
*   **Linter & Formatter:** ESLint/Prettier, Black (Python).
*   **Review Gates:** Mandatory approvals from two senior engineers, no warnings allowed, sonar-scan coverage > 85%.

### 3. Git Branching Strategy
*   **Model:** Trunk-Based Development.
*   **Short-lived branches:** `feature/AAR-*` or `fix/AAR-*` merged daily.
*   **Releases:** Tagged on main branch (`v1.0.0-rc1`), generating release branches only for hotfix situations.

### 4. Secrets & Configuration Management
*   **Secrets:** Managed via Google Cloud Secret Manager. Values are injected as environment variables in Cloud Run at runtime; no keys in version control.
*   **Config:** Environment-specific settings stored in JSON configs inside `infra/configs/`.

---

## Google Cloud Conceptual Alignment Map

```
┌────────────────────────────────────────────────────────────────────────┐
│                              APIGEE EDGE                               │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        CLOUD RUN CONTAINER GRID                        │
│   ┌────────────────────┐   ┌────────────────────┐   ┌────────────────┐ │
│   │  ONBOARDING (003)  │   │  SPREADING (006)   │   │ WORKFLOWS (010)│ │
│   └─────────┬──────────┘   └─────────┬──────────┘   └────────┬───────┘ │
└─────────────┼────────────────────────┼───────────────────────┼─────────┘
              ▼                        ▼                       ▼
┌─────────────┴────────────────────────┴───────────────────────┴─────────┐
│                          ALLOYDB / FIRESTORE                           │
└────────────────────────────────────────────────────────────────────────┘
```

*   **Vertex AI & Gemini:** Run alternate scoring models, write CAM texts, and power help interfaces.
*   **Agent Development Kit (ADK) & Model Context Protocol (MCP):** Connect AI interfaces to database structures.
*   **Cloud Run:** Host microservices in container environments.
*   **AlloyDB & Firestore:** Store transaction details, state properties, and session data.
*   **Apigee:** Central API gateway for security filtering and partner routing.
*   **Pub/Sub & Eventarc:** Manage asynchronous communication between services.
*   **Looker:** Render analytics dashboards for RMs and Executives.

---

## Implementation Accelerator & Sprint Planner

### 1. Sprint Roadmap (6 Sprints)

```
Sprint 1: Core Foundation  ──► Sprint 2: Data Ingestion ──► Sprint 3: Health Card & Rules
- Auth & Role Setup            - MSME Onboarding           - Spreading Engine
- DB/AlloyDB Deployment        - AA Consent APIs           - Policy Matrix Verification
                                                                   │
Sprint 6: Rollout          ◄── Sprint 5: Workspaces     ◄── Sprint 4: CAM & AI Analytics
- Sandbox Testing              - Committeevoting           - Gemini Narrative Generation
- Looker Dashboard Live        - RM CRM Dashboard          - Vertex Scorecard models
```

### 2. Engineering Work Package Catalogue

#### Package ID: AAR-WP-001 (Foundation)
*   *Scope:* Auth Setup, Cloud Run Landing Zone deployment.
*   *Owners:* PSG & CS-ID.
*   *Sprints:* Sprint 1.

#### Package ID: AAR-WP-002 (Inflow Data)
*   *Scope:* Account Aggregator, GSTN APIs.
*   *Owners:* Integration Squad.
*   *Sprints:* Sprint 2.

#### Package ID: AAR-WP-003 (Credit Scoring Engine)
*   *Scope:* Spreading rules, Alternative default scoring models.
*   *Owners:* Credit Engineering Team & Data/AI Squad.
*   *Sprints:* Sprints 3 & 4.

---

## Quality Gates, Testing Readiness & Release Principles

### 1. Platform Quality Gates

```
[ Git Push ] ──> [ Linter & Tests (100% Pass) ] ──> [ SonarQube (>85%) ] ──> [ Artifact Registry ]
                                                                                   │
[ Staging Deploy ] ◄── [ Integration Tests ] ◄── [ Vulnerability Scan ] ◄──────────┘
```

### 2. Environment Promotion Strategy
*   **Dev:** Triggered automatically on commit merges to `main`.
*   **Staging (UAT):** Triggered by releasing tagged candidates (`v*.*.*-rc*`). Requires manual approval in Google Cloud Deploy pipeline.
*   **Production:** Promoted from Staging after QA validation and approval.

---

**Approved & Signed By:**  
*Chief Engineering Delivery Architect, Project AAROHAN*  
*Professional Services Delivery Lead, Google Cloud*  
*Head, Digital Transformation Office (DTO), IDBI Bank*
