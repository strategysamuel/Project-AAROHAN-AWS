# AAR-ESE-002: Project AAROHAN Enterprise Simulation Engine (ESE) Product Backlog

**Document Classification**: Enterprise Product Management  
**Version**: 1.0  
**Status**: 🟢 APPROVED FOR SPRINT PLANNING  
**Date**: 2026-07-08  
**Platform**: Project AAROHAN — ESE Companion Platform  
**Confidentiality**: IDBI Bank Internal

---

## 1. Executive Summary

This document defines the complete **Enterprise Simulation Engine (ESE) Product Backlog** — the authoritative catalog of all capabilities required to transform Project AAROHAN into a fully self-contained, demo-ready, training-ready, and hackathon-ready Digital Public Infrastructure (DPI) banking simulation platform.

The backlog is organized across three releases (ESE v1.0, v1.1, v2.0), 16 epics, 48 features, and 62 user stories. The ESE MVP (v1.0) delivers the minimum capability set required for Hackathon demonstrations, Board presentations, customer showcases, and Credit Officer training within approximately 4.5 Agile sprints.

---

## 2. Vision

> *"Any IDBI Bank stakeholder, partner, or hackathon participant should be able to experience the complete AI-powered MSME credit lifecycle — from customer registration to loan disbursement — in a safe, realistic, fully offline simulation environment, with no external API dependencies and no real customer data."*

---

## 3. Product Objectives

| Objective | Measure of Success |
| :--- | :--- |
| Zero external API dependency in simulation mode | 100% offline demo capability |
| Production business logic preserved exactly | Zero changes to v1.1.0 core service code |
| Realistic MSME personas and datasets | ≥ 13 named scenarios with stateful data |
| One-click demo journeys | ≤ 30 seconds to launch any journey |
| Multi-team hackathon support | ≥ 20 concurrent isolated namespaces |
| AI-generated narratives in Demo Mode | Live Vertex AI Gemini on synthetic data |
| Rapid dataset reset | Full reset in ≤ 60 seconds |
| Training scenario coverage | ≥ 10 MSME borrower typologies |

---

## 4. Success Criteria

| Scenario | Success Criterion |
| :--- | :--- |
| **Hackathon Demo** | All 10 demo journeys complete end-to-end without errors; fraud scenario auto-rejects in < 5 seconds |
| **Board Presentation** | "Perfect Borrower" journey completes in < 5 minutes with live Gemini narrative |
| **Customer Demo** | 3 contrasting scenarios (approved, rejected, manual review) executable within a 15-minute slot |
| **Credit Officer Training** | Trainee completes 5 distinct borrower scenarios; trainer reviews interaction logs |
| **Hackathon Sandbox** | 20 teams operate simultaneously with zero cross-namespace data leakage |

---

## 5. Product Roadmap

### ESE v1.0 — Hackathon & Demo MVP
**Target**: ~4.5 Sprints  
**Goal**: Deliver a complete, demo-ready simulation platform for hackathon presentations and board-level showcases.  
**Scope**: Core simulation adapters, 50-customer synthetic dataset, 13 scenarios, 10 demo journeys, Admin Console v1, Vertex AI Demo Mode.

### ESE v1.1 — Training & Sandbox Enhancement
**Target**: ~2 Sprints post-v1.0  
**Goal**: Extend the platform for credit officer training programs and external partner integration testing.  
**Scope**: Training Mode slow-response simulation, namespace isolation for hackathon teams, 100-customer dataset expansion, reporting and audit export.

### ESE v2.0 — Generative Simulation Platform
**Target**: ~3 Sprints post-v1.1  
**Goal**: Enable AI-generated new personas and multi-language demo journeys.  
**Scope**: Gemini-powered persona generator, multi-language UI (Hindi, Tamil, Telugu), regulator-facing demo mode, repayment lifecycle simulation.

---

## 6. Epic Catalog

| Epic ID | Epic Name | Description | Release |
| :--- | :--- | :--- | :---: |
| EP-ESE-001 | Simulation Core | Adapter interface and mode-switching infrastructure | v1.0 |
| EP-ESE-002 | Demo Dataset Engine | Synthetic dataset seeder and management | v1.0 |
| EP-ESE-003 | Banking Personas | 13 named MSME borrower scenario definitions | v1.0 |
| EP-ESE-004 | CKYC Simulator | CKYC simulation adapter and KYC status scenarios | v1.0 |
| EP-ESE-005 | GSTN Simulator | GST filing history simulation adapter | v1.0 |
| EP-ESE-006 | Account Aggregator Simulator | Bank statement simulation adapter | v1.0 |
| EP-ESE-007 | EPFO Simulator | Employee and provident fund simulation adapter | v1.0 |
| EP-ESE-008 | MCA Simulator | Corporate registry simulation adapter | v1.0 |
| EP-ESE-009 | RBI Fraud Registry Simulator | Blacklist validation simulation adapter | v1.0 |
| EP-ESE-010 | OCEN/ULI Marketplace Simulator | Loan offer and disbursement simulation adapter | v1.0 |
| EP-ESE-011 | AI Simulation Engine | Gemini Demo Mode + pre-generated narrative library | v1.0 |
| EP-ESE-012 | Demo Console | Admin Console for scenario, dataset, and mode management | v1.0 |
| EP-ESE-013 | Executive Dashboard Simulator | Portfolio KPI aggregation simulation | v1.0 |
| EP-ESE-014 | Scenario Generator | AI-powered persona generation engine | v2.0 |
| EP-ESE-015 | Reporting Engine | Demo session reports and audit export | v1.1 |
| EP-ESE-016 | Analytics Engine | Demo usage analytics and session tracking | v1.1 |

---

## 7. Feature Catalog

### EP-ESE-001: Simulation Core

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-001-01 | Adapter Interface Design | Enables zero-code-change simulation layer | Critical | Medium | None |
| F-ESE-001-02 | ESE_MODE Environment Variable | Controls adapter selection per deployment | Critical | Low | F-ESE-001-01 |
| F-ESE-001-03 | Adapter Factory Pattern | Dependency-injection-based adapter loading | Critical | Medium | F-ESE-001-01 |
| F-ESE-001-04 | Adapter Health Check | Validates all adapters on startup | High | Low | F-ESE-001-03 |

### EP-ESE-002: Demo Dataset Engine

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-002-01 | Dataset Seeder Script | One-command 50-customer dataset initialization | Critical | Medium | EP-ESE-003 |
| F-ESE-002-02 | Dataset Reset API | Wipes and re-seeds dataset in < 60 seconds | Critical | Low | F-ESE-002-01 |
| F-ESE-002-03 | Namespace Management | Isolated dataset namespaces per team | High | Medium | F-ESE-002-01 |
| F-ESE-002-04 | Synthetic Transaction Generator | 60,000 realistic bank transactions | High | High | None |
| F-ESE-002-05 | GST Return Generator | 1,800 synthetic GST filing records | High | Medium | None |

### EP-ESE-003: Banking Personas

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-003-01 | Persona Schema Definition | Structured JSON schema for all 13 scenarios | Critical | Low | None |
| F-ESE-003-02 | Approved Persona Pack | 7 approvable MSME personas | Critical | Medium | F-ESE-003-01 |
| F-ESE-003-03 | Rejected Persona Pack | 3 rejection scenarios (fraud, GST, EPFO) | Critical | Medium | F-ESE-003-01 |
| F-ESE-003-04 | Manual Review Persona Pack | 3 borderline scenarios | High | Medium | F-ESE-003-01 |
| F-ESE-003-05 | Synthetic PAN Format | `SIMxxNNNNS` format to prevent production confusion | Critical | Low | F-ESE-003-01 |

### EP-ESE-004: CKYC Simulator

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-004-01 | SimulationCKYCAdapter | Replaces live CKYC API with synthetic records | Critical | Medium | F-ESE-001-01 |
| F-ESE-004-02 | KYC Status Scenarios | CLEAN, EXPIRED_KYC, INCOMPLETE_KYC outcomes | High | Low | F-ESE-004-01 |

### EP-ESE-005: GSTN Simulator

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-005-01 | SimulationGSTNAdapter | Synthetic GSTIN filing history responses | Critical | Medium | F-ESE-001-01 |
| F-ESE-005-02 | GST Growth Scenarios | HIGH_GROWTH, STABLE, SEASONAL, NON_COMPLIANT | High | Medium | F-ESE-005-01 |
| F-ESE-005-03 | GST Revenue Consistency | Revenue consistent with AA cash flow (±15%) | Medium | High | F-ESE-002-04 |

### EP-ESE-006: Account Aggregator Simulator

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-006-01 | SimulationAAAdapter | 24-month synthetic bank statement responses | Critical | High | F-ESE-001-01 |
| F-ESE-006-02 | Cash Flow Scenario Packs | STRONG, SEASONAL, STRESSED, NEW_ACCOUNT | High | Medium | F-ESE-006-01 |
| F-ESE-006-03 | Realistic Transaction Patterns | Salary, GST payments, EMIs, seasonal spikes | High | High | F-ESE-002-04 |

### EP-ESE-007: EPFO Simulator

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-007-01 | SimulationEPFOAdapter | Workforce and PF contribution simulation | High | Medium | F-ESE-001-01 |
| F-ESE-007-02 | EPFO Compliance Scenarios | GROWING, STABLE, DECLINING, NON_COMPLIANT | High | Low | F-ESE-007-01 |

### EP-ESE-008: MCA Simulator

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-008-01 | SimulationMCAAdapter | Corporate registry synthetic responses | High | Medium | F-ESE-001-01 |
| F-ESE-008-02 | MCA Compliance Scenarios | ACTIVE_COMPLIANT, PENDING_FILING, DORMANT | Medium | Low | F-ESE-008-01 |

### EP-ESE-009: RBI Fraud Registry Simulator

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-009-01 | SimulationFraudAdapter | Blacklist lookup simulation | Critical | Low | F-ESE-001-01 |
| F-ESE-009-02 | Fraud Blacklist Dataset | 5 synthetic blacklisted PANs seeded in dataset | Critical | Low | F-ESE-009-01 |
| F-ESE-009-03 | Auto-Rejection Flow | Preserves production rejection + audit log behavior | Critical | Low | F-ESE-009-01 |

### EP-ESE-010: OCEN/ULI Marketplace Simulator

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-010-01 | SimulationOCENAdapter | 5 simulated lender pool with offer generation | High | High | F-ESE-001-01 |
| F-ESE-010-02 | Lender Offer Scenarios | OFFER_AVAILABLE, PENDING, DISBURSED, DECLINED | High | Medium | F-ESE-010-01 |
| F-ESE-010-03 | Disbursement Simulation | Full disbursement lifecycle tracking | High | Medium | F-ESE-010-01 |

### EP-ESE-011: AI Simulation Engine

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-011-01 | SimulationGeminiAdapter | Pre-generated narrative library for Training/Testing | Critical | Medium | F-ESE-001-01 |
| F-ESE-011-02 | Live Gemini Demo Mode | Routes to Vertex AI Gemini in Demo Mode | Critical | Medium | F-ESE-011-01 |
| F-ESE-011-03 | Narrative Library | 13 scenario-specific pre-generated credit narratives | High | High | EP-ESE-003 |
| F-ESE-011-04 | Explainability Tag Mapping | Tag-to-human-language explanation dictionary | High | Low | None |
| F-ESE-011-05 | CAM Simulation Adapter | Pre-structured CAM template + Gemini narrative | High | Medium | F-ESE-011-01 |

### EP-ESE-012: Demo Console

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :---: | :---: | :---: | :--- |
| F-ESE-012-01 | Admin Console Backend | FastAPI service for all admin operations | Critical | High | EP-ESE-002 |
| F-ESE-012-02 | Mode Switcher | UI + API to toggle ESE_MODE at runtime | Critical | Medium | F-ESE-001-02 |
| F-ESE-012-03 | Scenario Loader | One-click activation of named MSME scenarios | Critical | Medium | EP-ESE-003 |
| F-ESE-012-04 | Dataset Reset | Full synthetic dataset wipe-and-reseed UI | Critical | Low | F-ESE-002-02 |
| F-ESE-012-05 | Fraud Injector | Mark any PAN as fraud-blacklisted | High | Low | F-ESE-009-01 |
| F-ESE-012-06 | Audit Log Viewer | Browse all AI credit decision audit entries | High | Medium | None |
| F-ESE-012-07 | Customer Generator | Seed new synthetic MSME customer on demand | High | Medium | F-ESE-002-01 |
| F-ESE-012-08 | Journey Library UI | One-click launch for all 10 demo journeys | Critical | High | EP-ESE-014 (v1.0) |
| F-ESE-012-09 | Access Control | Role-based console access (Admin/Demo/Trainer) | High | Medium | None |

### EP-ESE-013: Executive Dashboard Simulator

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-013-01 | Portfolio KPI Aggregation | Dynamic KPIs updated as journeys complete | High | Medium | EP-ESE-002 |
| F-ESE-013-02 | Fraud Match Dashboard | Real-time view of fraud events in session | High | Low | F-ESE-009-01 |

### EP-ESE-014: Demo Journey Library (v1.0 scope)

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-014-01 | Journey Controller | Step-sequenced orchestrator for demo flows | Critical | High | All adapters |
| F-ESE-014-02 | Perfect Borrower Journey | SCN-001 end-to-end approval journey | Critical | Medium | F-ESE-014-01 |
| F-ESE-014-03 | Fraud Registry Journey | SCN-008 fraud auto-reject journey | Critical | Low | F-ESE-014-01 |
| F-ESE-014-04 | New-to-Credit Journey | SCN-002 manual review workflow | High | Medium | F-ESE-014-01 |
| F-ESE-014-05 | Women Entrepreneur Journey | SCN-012 MUDRA showcase | High | Medium | F-ESE-014-01 |
| F-ESE-014-06 | Full MSME Lifecycle Journey | Registration to EWS monitoring | High | High | F-ESE-014-01 |

### EP-ESE-015: Reporting Engine (v1.1)

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :--- | :---: | :---: | :--- |
| F-ESE-015-01 | Session Summary Report | PDF export of completed demo journey | Medium | Medium | F-ESE-014-01 |
| F-ESE-015-02 | Training Interaction Log | Trainee action history for trainer review | Medium | Medium | EP-ESE-012 |
| F-ESE-015-03 | Audit Log Export | BigQuery export of all simulation audit events | Medium | Low | None |

### EP-ESE-016: Analytics Engine (v1.1)

| Feature ID | Feature Name | Business Value | Priority | Complexity | Dependencies |
| :--- | :--- | :---: | :---: | :---: | :--- |
| F-ESE-016-01 | Demo Session Tracker | Count and duration of demo journeys run | Medium | Medium | F-ESE-014-01 |
| F-ESE-016-02 | Scenario Popularity Analytics | Which scenarios are used most | Low | Low | F-ESE-016-01 |

---

## 8. User Story Catalog

### EP-ESE-001: Simulation Core

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-001 | DevOps Engineer | As a DevOps Engineer, I want to set `ESE_MODE=SIMULATION` and have all external integrations automatically use simulation adapters, so that I can deploy a fully offline demo environment without modifying any service code. | 1. Setting `ESE_MODE=SIMULATION` at container startup loads all simulation adapters. 2. Setting `ESE_MODE=PRODUCTION` loads all production adapters. 3. No business logic code is modified. 4. Health check endpoint confirms adapter mode. | 3 | Critical |
| US-ESE-002 | Enterprise Architect | As an Enterprise Architect, I want every external integration to implement a common adapter interface, so that simulation and production adapters are interchangeable without refactoring service code. | 1. `ExternalIntegrationAdapter` abstract base class defined. 2. All 10 adapters implement the interface. 3. Adapter swap requires only environment variable change. | 2 | Critical |

### EP-ESE-002: Demo Dataset Engine

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-003 | Demo Administrator | As a Demo Administrator, I want to run a single seeder command that populates all 50 MSME customer personas and their associated data, so that the platform is demo-ready in under 5 minutes. | 1. `python seed_demo_data.py` completes in < 5 minutes. 2. 50 customers, 75 loan apps, 1,800 GST records, 60,000 transactions seeded. 3. All 13 named scenario personas present and correct. | 5 | Critical |
| US-ESE-004 | Demo Administrator | As a Demo Administrator, I want to reset the entire synthetic dataset in under 60 seconds via the Admin Console, so that I can prepare for back-to-back demos. | 1. Admin Console "Reset Dataset" completes in < 60 seconds. 2. All customer, transaction, and decision records wiped. 3. Seeded dataset is restored immediately post-wipe. 4. Active demo session shows clean state. | 2 | Critical |
| US-ESE-005 | Hackathon Organizer | As a Hackathon Organizer, I want to create isolated dataset namespaces for each team, so that 20 teams can run simultaneously without seeing each other's data. | 1. Admin Console allows creation of named namespaces (e.g., `TEAM_A`). 2. All API calls within a namespace are scoped to that namespace's dataset. 3. Cross-namespace data access returns 403. 4. Namespace reset does not affect other namespaces. | 3 | High |

### EP-ESE-003: Banking Personas

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-006 | Product Manager | As a Product Manager, I want 13 predefined MSME borrower personas with distinct financial profiles and deterministic credit outcomes, so that every demo reliably showcases the full spectrum of lending scenarios. | 1. 13 persona JSON configs exist in `scenarios/`. 2. Each persona has: customer data, GST profile, AA cash flow profile, FHC score, expected credit decision. 3. Loading a persona always produces the defined credit outcome. 4. Synthetic PAN follows `SIMxxNNNNS` format. | 5 | Critical |
| US-ESE-007 | Trainer | As a Credit Officer Trainer, I want persona profiles to include edge cases (seasonal, GST non-compliant, fraud), so that trainees experience realistic challenging scenarios during training. | 1. At least 1 seasonal persona, 1 GST non-compliant persona, 1 fraud persona. 2. Seasonal persona shows visible revenue spikes in AA data. 3. Non-compliant persona has GST filing gaps. 4. Fraud persona triggers auto-rejection. | 3 | High |

### EP-ESE-004 through EP-ESE-010: Simulator Adapters

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-008 | Demo Administrator | As a Demo Administrator, I want the CKYC simulation adapter to return realistic KYC records for all 50 personas, so that the onboarding flow completes without external API dependency. | 1. `SimulationCKYCAdapter.fetch()` returns valid CKYC record for any seeded PAN. 2. KYC status respects persona configuration (CLEAN / EXPIRED / INCOMPLETE). 3. Response latency simulated at 200–400ms in Demo Mode. | 2 | Critical |
| US-ESE-009 | Credit Analyst (Trainee) | As a Credit Analyst Trainee, I want the GSTN simulation adapter to return 36 months of realistic GST filing history, so that I can learn to interpret revenue trends during training. | 1. 36 monthly GSTN records returned for each persona. 2. Revenue trend matches persona profile (growth / stable / declining). 3. Non-compliant persona has ≥ 3 missing filing months. | 3 | Critical |
| US-ESE-010 | Demo Administrator | As a Demo Administrator, I want the Account Aggregator simulation adapter to return 24 months of realistic bank transactions, so that the FHC engine can compute authentic DSCR values from synthetic data. | 1. 24 months × 4 accounts return consistent transactions. 2. DSCR computed from synthetic data falls within ±5% of persona-defined target. 3. Seasonal personas show revenue peaks in harvest/festival months. | 5 | Critical |
| US-ESE-011 | Credit Officer | As a Credit Officer, I want the EPFO simulation adapter to return realistic workforce data, so that the FHC score reflects employee strength as a creditworthiness signal. | 1. EPFO adapter returns employee count and PF compliance for each persona. 2. Non-compliant persona shows ≥ 3 months of missed PF contributions. | 2 | High |
| US-ESE-012 | Enterprise Architect | As an Enterprise Architect, I want the MCA simulation adapter to return valid corporate registry data, so that the director verification step completes without live API access. | 1. MCA adapter returns CIN, directors list, and incorporation date per persona. 2. Dormant company persona returns DORMANT status. | 2 | High |
| US-ESE-013 | Banking Executive | As a Banking Executive Demo Presenter, I want the RBI Fraud Registry simulation adapter to automatically reject blacklisted PAN personas with an immutable audit trail, so that I can demonstrate fraud prevention to regulators. | 1. 5 synthetic blacklisted PANs seeded. 2. Fraud persona receives BLACKLISTED status + CRITICAL SECURITY ALERT audit log. 3. Behavior is identical to production fraud rejection flow. 4. Non-fraud persona receives CLEAN status. | 2 | Critical |
| US-ESE-014 | Product Manager | As a Product Manager, I want the OCEN/ULI simulation adapter to generate 5 simulated lender offers for approved personas, so that I can demonstrate the full disbursement marketplace in demos. | 1. 5 lender offers generated for APPROVED personas. 2. Lender names, rates, and tenures are realistic and varied. 3. Disbursement status tracks through OFFERED → ACCEPTED → DISBURSED lifecycle. | 3 | High |

### EP-ESE-011: AI Simulation Engine

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-015 | Banking Executive Demo Presenter | As a Banking Executive, I want the credit engine to generate a live Vertex AI Gemini narrative using synthetic customer data in Demo Mode, so that every demonstration presents a fresh, impressive AI output. | 1. In `ESE_MODE=DEMO`, credit evaluation calls Vertex AI Gemini with synthetic financial data. 2. Narrative is generated fresh for each evaluation. 3. No real customer PAN or Aadhaar is included in the Gemini prompt. 4. Response includes live explainability tags. | 3 | Critical |
| US-ESE-016 | Credit Officer Trainer | As a Credit Officer Trainer, I want Training Mode to return pre-generated AI narratives from a library, so that training sessions do not depend on Vertex AI availability or quota. | 1. In `ESE_MODE=TRAINING`, Gemini adapter returns pre-generated narrative from library. 2. Library contains 13 narratives — one per scenario. 3. Narratives are grammatically correct and contextually accurate. | 2 | Critical |
| US-ESE-017 | Credit Officer (Trainee) | As a Credit Officer Trainee, I want to see plain-English explanations of AI explainability tags, so that I understand why a loan was approved or rejected without needing technical knowledge. | 1. Admin Console and RM Workspace display tag-to-explanation mapping. 2. All 8 tags have human-readable explanations. 3. Fraud tags display a distinct visual warning style. | 2 | High |

### EP-ESE-012: Demo Console

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-018 | Demo Administrator | As a Demo Administrator, I want an Admin Console web UI where I can load a named scenario, reset the dataset, and switch ESE mode — all without touching the terminal. | 1. Admin Console accessible at `/admin` on the ESE deployment. 2. Scenario list shows all 13 personas with one-click activation. 3. Mode switcher reflects active mode immediately. 4. Dataset reset button triggers wipe-and-reseed. | 5 | Critical |
| US-ESE-019 | DevSecOps Lead | As a DevSecOps Lead, I want the Admin Console to require authenticated login before any dataset modification, so that unauthorized participants cannot reset demo data during live sessions. | 1. Admin Console requires IDBI SSO or API key authentication. 2. Unauthenticated requests return 401. 3. Read-only role can view audit logs but cannot reset or modify. | 3 | High |
| US-ESE-020 | Demo Administrator | As a Demo Administrator, I want to inject a fraud case for any customer by clicking a button, so that I can demonstrate the RBI Fraud Registry rejection flow on demand during a presentation. | 1. "Inject Fraud" marks the selected customer's PAN as blacklisted. 2. Next credit evaluation for that customer triggers auto-rejection + audit log. 3. Fraud injection is reversible via Admin Console. | 2 | High |
| US-ESE-021 | Hackathon Organizer | As a Hackathon Organizer, I want to manage team namespaces from the Admin Console — creating, resetting, and deleting namespaces — so that I can onboard and support 20 teams efficiently. | 1. Admin Console lists all active namespaces. 2. "Create Namespace" generates a new isolated dataset for a team. 3. "Reset Namespace" wipes only that team's data. 4. "Delete Namespace" removes the namespace and all its data. | 3 | High |

### EP-ESE-013: Executive Dashboard Simulator

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-022 | IDBI Bank MD | As an IDBI Bank Managing Director, I want the Executive Dashboard to show live portfolio KPIs that update as demo journeys complete, so that I can see AI-driven lending at portfolio scale during the Board presentation. | 1. Dashboard shows: total applications, approvals, rejections, fraud matches, avg FHC score, total disbursed. 2. KPIs update within 5 seconds of journey completion. 3. Fraud match count increments when fraud injection occurs. | 3 | High |

### EP-ESE-014: Demo Journey Library

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-023 | Demo Administrator | As a Demo Administrator, I want to launch the "Perfect Borrower" journey with a single click and guide an executive audience through the complete credit lifecycle in under 5 minutes. | 1. Journey launches SCN-001 (Priya Textiles) on click. 2. Steps: Register → CKYC → GST → AA → FHC → AI Credit Eval → CAM → OCEN Offer → Disburse. 3. Journey completes in ≤ 5 minutes including Gemini narrative. | 5 | Critical |
| US-ESE-024 | Demo Administrator | As a Demo Administrator, I want to launch the "Fraud Registry in Action" journey to demonstrate real-time fraud prevention to regulators or auditors. | 1. Journey launches SCN-008 (Raja Motors). 2. Fraud PAN triggers auto-rejection within 3 seconds. 3. CRITICAL SECURITY ALERT visible in audit log. | 2 | Critical |
| US-ESE-025 | Credit Officer Trainer | As a Credit Officer Trainer, I want trainees to navigate the "New-to-Credit MSME" journey, including the manual review workflow, so that they experience the human-in-the-loop approval process. | 1. Journey launches SCN-002 (Ramesh Kirana). 2. Journey reaches PENDING_HUMAN_REVIEW status. 3. Trainee must approve or reject to proceed. 4. Journey records trainee action in interaction log. | 3 | High |

### EP-ESE-015 & EP-ESE-016: Reporting & Analytics (v1.1)

| Story ID | Persona | Description | Acceptance Criteria | SP | Priority |
| :--- | :--- | :--- | :--- | :---: | :---: |
| US-ESE-026 | Banking Executive | As a Banking Executive, I want to export a PDF summary of a completed demo journey to share with stakeholders who were not present, so that the demonstration has lasting impact. | 1. "Export Demo Report" button available after any completed journey. 2. PDF includes: journey name, personas used, credit outcomes, AI narrative excerpt, explainability tags. 3. PDF generated in < 10 seconds. | 3 | Medium |
| US-ESE-027 | IDBI Training Manager | As a Training Manager, I want to view a log of all trainee interactions for a session, so that I can assess trainee competency and provide coaching. | 1. Trainer portal shows all trainee actions: endpoints called, decisions made, time per step. 2. Log exportable to CSV. | 2 | Medium |

---

## 9. Release Mapping

### ESE v1.0 — Hackathon & Demo MVP

| Epic | Features | User Stories | Story Points |
| :--- | :--- | :---: | :---: |
| EP-ESE-001 Simulation Core | F-001-01 to 04 | US-ESE-001 to 002 | 5 SP |
| EP-ESE-002 Dataset Engine | F-002-01 to 05 | US-ESE-003 to 005 | 10 SP |
| EP-ESE-003 Banking Personas | F-003-01 to 05 | US-ESE-006 to 007 | 8 SP |
| EP-ESE-004 CKYC Simulator | F-004-01 to 02 | US-ESE-008 | 2 SP |
| EP-ESE-005 GSTN Simulator | F-005-01 to 03 | US-ESE-009 | 3 SP |
| EP-ESE-006 AA Simulator | F-006-01 to 03 | US-ESE-010 | 5 SP |
| EP-ESE-007 EPFO Simulator | F-007-01 to 02 | US-ESE-011 | 2 SP |
| EP-ESE-008 MCA Simulator | F-008-01 to 02 | US-ESE-012 | 2 SP |
| EP-ESE-009 RBI Fraud Simulator | F-009-01 to 03 | US-ESE-013 | 2 SP |
| EP-ESE-010 OCEN Simulator | F-010-01 to 03 | US-ESE-014 | 3 SP |
| EP-ESE-011 AI Simulation | F-011-01 to 05 | US-ESE-015 to 017 | 7 SP |
| EP-ESE-012 Demo Console | F-012-01 to 09 | US-ESE-018 to 021 | 13 SP |
| EP-ESE-013 Exec Dashboard | F-013-01 to 02 | US-ESE-022 | 3 SP |
| EP-ESE-014 Demo Journeys | F-014-01 to 06 | US-ESE-023 to 025 | 10 SP |
| **ESE v1.0 Total** | **48 Features** | **25 Stories** | **75 SP** |

### ESE v1.1 — Training & Sandbox Enhancement
**Added Scope**: Training Mode latency simulation, 100-customer dataset, reporting engine, analytics, namespace isolation hardening.  
**Estimated**: ~20 SP across 2 sprints.

### ESE v2.0 — Generative Simulation Platform
**Added Scope**: Gemini persona generator, multi-language UI (Hindi/Tamil/Telugu), regulator showcase mode, repayment lifecycle.  
**Estimated**: ~30 SP across 3 sprints.

---

## 10. MVP Scope

### Hackathon Demo MVP

| Requirement | Feature | Status |
| :--- | :--- | :---: |
| Offline operation (no live APIs) | EP-ESE-001 Adapter Core | v1.0 |
| 13 named scenarios loadable | EP-ESE-003 Personas | v1.0 |
| Dataset reset in < 60 seconds | F-ESE-002-02 | v1.0 |
| Perfect Borrower journey < 5 min | US-ESE-023 | v1.0 |
| Fraud Registry journey < 2 min | US-ESE-024 | v1.0 |
| Namespace isolation per team | US-ESE-005 | v1.0 |

### Board Presentation MVP

| Requirement | Feature | Status |
| :--- | :--- | :---: |
| Live Gemini AI narrative | F-ESE-011-02 | v1.0 |
| Executive Dashboard KPIs | EP-ESE-013 | v1.0 |
| Fraud prevention demonstration | US-ESE-024 | v1.0 |
| End-to-end lifecycle journey | US-ESE-025 | v1.0 |

### Customer Demo MVP

| Requirement | Feature | Status |
| :--- | :--- | :---: |
| ≥ 3 contrasting scenarios | EP-ESE-003 | v1.0 |
| AI explainability tags | F-ESE-011-04 | v1.0 |
| CAM generation | F-ESE-011-05 | v1.0 |
| OCEN loan offer display | EP-ESE-010 | v1.0 |

### Training MVP

| Requirement | Feature | Status |
| :--- | :--- | :---: |
| Pre-generated narratives | F-ESE-011-01 | v1.0 |
| Manual review workflow | US-ESE-025 | v1.0 |
| Trainee interaction log | US-ESE-027 | v1.1 |
| Edge case personas (GST, fraud) | US-ESE-007 | v1.0 |

---

## 11. Non-Functional Requirements

### Performance
* Dataset seed: ≤ 5 minutes
* Dataset reset: ≤ 60 seconds
* Demo journey launch: ≤ 30 seconds
* API response (simulation): ≤ 500ms P95 (Demo Mode); ≤ 50ms P95 (Testing Mode)
* AI narrative (Gemini, Demo Mode): ≤ 4 seconds P95
* Executive Dashboard refresh: ≤ 5 seconds

### Security
* No real PAN, Aadhaar, or bank account data in the ESE
* Synthetic PANs use `SIMxxNNNNS` format only
* Admin Console requires authentication; all actions audit-logged
* ESE deployed in isolated GCP project (`aarohan-ese`)
* No network routing between ESE and production GCP project

### Scalability
* Support ≥ 20 concurrent hackathon team namespaces
* Support ≥ 50 concurrent API requests across all services
* Cloud Run autoscaling 1–10 instances per service (same as production)

### Maintainability
* Zero diffs to production service business logic code
* Adapter interface is the only contract between simulation and production
* Synthetic dataset regenerable from schema definitions at any time

### Demo Reliability
* ESE must be deployable and functional entirely offline (no external API dependency in SIMULATION mode)
* All 10 demo journeys must pass end-to-end in a pre-demo smoke test script
* Dataset seed script is idempotent — safe to run multiple times

---

## 12. Risks

| Risk ID | Description | Likelihood | Impact | Mitigation |
| :--- | :--- | :---: | :---: | :--- |
| R-001 | Vertex AI Gemini unavailable during live hackathon demo | Low | High | Fallback to pre-generated narrative library automatically |
| R-002 | Synthetic data insufficient realism for regulator demo | Medium | Medium | Engage Banking Domain Expert to validate GST and AA data patterns |
| R-003 | Production code divergence from ESE adapter interface | Low | High | Adapter interface tests run as part of production CI/CD pipeline |
| R-004 | Namespace isolation failure under high concurrency | Low | High | Database-level namespace scoping + stress test before hackathon |
| R-005 | Persona credit outcomes drift from scenario config | Low | Medium | Outcome assertion tests seeded with each scenario load |

---

## 13. Assumptions

* The ESE reuses all v1.1.0 production microservice code without modification.
* ESE is deployed in a separate GCP project (`aarohan-ese`) with no network access to `aarohan-prod`.
* Vertex AI Gemini API is accessible from the ESE GCP project in Demo Mode.
* Synthetic data volumes (50 customers, 60,000 transactions) are sufficient for all v1.0 use cases.
* The Admin Console will be a new FastAPI microservice added only to the ESE platform.
* All demo journeys will be delivered as configurable JSON step-sequences, not hardcoded.

---

## 14. Future Enhancements

| Initiative | Release | Description |
| :--- | :---: | :--- |
| AI Persona Generator | ESE v2.0 | Gemini-powered creation of new MSME personas from demographic parameters |
| Multi-language Demo Mode | ESE v2.0 | Hindi, Tamil, Telugu UI translations of all demo journeys |
| Regulator Demo Mode | ESE v2.1 | RBI-facing showcase with audit trail export and regulatory commentary |
| Loan Repayment Lifecycle | ESE v1.1 | Simulate EMI repayments and portfolio aging for EWS demonstrations |
| Voice-Driven Demo Mode | ESE v2.0 | Presenter can narrate journeys via voice; AI advances the steps |
| ESE Mobile App | ESE v3.0 | Tablet-optimized demo experience for relationship manager field visits |

---

## 15. Executive Approval

| Role | Decision | Date |
| :--- | :---: | :---: |
| **Chief Product Officer** | ✅ APPROVED | 2026-07-08 |
| **Product Manager** | ✅ APPROVED | 2026-07-08 |
| **Enterprise Architect** | ✅ APPROVED | 2026-07-08 |
| **Banking Domain Expert** | ✅ APPROVED | 2026-07-08 |
| **AI Product Manager** | ✅ APPROVED | 2026-07-08 |
| **Google Cloud Principal Solutions Architect** | ✅ APPROVED | 2026-07-08 |
| **Technical Program Manager** | ✅ APPROVED | 2026-07-08 |

**ESE Product Backlog is approved. Sprint Planning for ESE v1.0 may commence.**

---

## 16. Appendix

### A. Story Point Summary

| Release | Story Points | Sprints (estimated) |
| :---: | :---: | :---: |
| ESE v1.0 | 75 SP | ~4.5 sprints |
| ESE v1.1 | ~20 SP | ~2 sprints |
| ESE v2.0 | ~30 SP | ~3 sprints |

### B. User Story Count by Epic

| Epic | Stories | SP |
| :--- | :---: | :---: |
| Simulation Core | 2 | 5 |
| Dataset Engine | 3 | 10 |
| Banking Personas | 2 | 8 |
| CKYC / GSTN / AA / EPFO / MCA Simulators | 5 | 14 |
| RBI Fraud / OCEN Simulators | 2 | 5 |
| AI Simulation Engine | 3 | 7 |
| Demo Console | 4 | 13 |
| Executive Dashboard | 1 | 3 |
| Demo Journey Library | 3 | 10 |
| Reporting & Analytics (v1.1) | 2 | 5 |
| **Total** | **27** | **80** |
