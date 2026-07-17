# AAR-ESE-003: Project AAROHAN Enterprise Simulation Engine — Sprint 1 Planning

**Document Classification**: Agile Sprint Planning  
**Sprint**: ESE Sprint 1 of 5  
**Version**: 1.0  
**Status**: 🟢 SPRINT PLANNING APPROVED  
**Date**: 2026-07-08  
**Sprint Duration**: 2 weeks (2026-07-08 to 2026-07-21)  
**Platform**: Enterprise Simulation Engine (ESE) v1.0

---

## 1. Executive Summary

This document defines the Sprint 1 plan for the **Project AAROHAN Enterprise Simulation Engine (ESE)**. Sprint 1 establishes the foundational simulation infrastructure — the adapter framework, environment switching, synthetic dataset, and banking persona definitions — upon which all subsequent simulation capabilities will be built.

Sprint 1 is the most technically foundational sprint of the ESE delivery. Its output enables every other sprint to build simulation adapters and demo journeys without revisiting infrastructure concerns. Sprint 1 delivers no user-facing demo journey — it delivers the engine that makes all demo journeys possible.

**Capacity**: 5 developers × 8 story points per sprint = **40 SP capacity**  
**Committed**: **38 SP**  
**Sprint Goal**: Build the Enterprise Simulation Foundation

---

## 2. Sprint Goal

> *"Establish the complete simulation infrastructure — adapter interfaces, environment switching, core dataset repository, seed loader, and six banking persona definitions — so that any simulation adapter in Sprint 2 can be implemented immediately without revisiting foundational architecture."*

### Sprint Goal Acceptance Test

The Sprint Goal is achieved when:
1. `ESE_MODE=SIMULATION` starts all services with simulation adapters loaded and health checks passing.
2. `ESE_MODE=PRODUCTION` starts all services with production adapters loaded and health checks passing.
3. The dataset seeder seeds all 6 Sprint 1 personas to the SQLite repository in < 2 minutes.
4. All 10 adapter interface contracts are defined, and the CKYC simulation adapter is implemented as the reference implementation.
5. All 6 persona JSON definitions are complete, validated, and deterministically bound to credit outcomes.

---

## 3. Sprint Scope

### In Scope

| Area | Deliverables |
| :--- | :--- |
| Simulation Configuration | `ESE_MODE` environment variable; adapter factory; mode health check |
| Adapter Interface Framework | Abstract base class for all 10 external integrations |
| CKYC Simulation Adapter | Reference implementation of the simulation adapter pattern |
| Dataset Repository | JSON schema; SQLite database design; seed loader script |
| Dataset Versioning | Version file (`ese_dataset_version.json`) tracking seed schema |
| Banking Personas (6) | Manufacturing MSME, Retail MSME, Startup, Exporter, Women Entrepreneur, Agri Enterprise |
| Synthetic Data Generator | Generation rules for GST filings, bank transactions, and EPFO records |
| Demo Configuration | `docker-compose.ese.yml` with `ESE_MODE=DEMO` pre-configured |

### Out of Scope (Deferred to Sprint 2+)

* GSTN, AA, EPFO, MCA, RBI Fraud, OCEN, Vertex AI adapters (Sprint 2)
* Admin Console (Sprint 3)
* Demo Journey Library (Sprint 4)
* Hackathon namespace isolation (Sprint 4)

---

## 4. Selected Epics

| Epic ID | Epic Name | Sprint 1 Contribution |
| :--- | :--- | :--- |
| **EP-ESE-001** | Simulation Core | Full delivery — adapter interface and mode switching |
| **EP-ESE-002** | Demo Dataset Engine | Partial delivery — schema, seeder, versioning (data volume Sprint 2) |
| **EP-ESE-003** | Banking Personas | Partial delivery — 6 of 13 personas |
| **EP-ESE-004** | CKYC Simulator | Reference implementation only |

---

## 5. Selected Features

| Feature ID | Feature Name | Sprint | Notes |
| :--- | :--- | :---: | :--- |
| F-ESE-001-01 | Adapter Interface Design | ✅ Sprint 1 | Full delivery |
| F-ESE-001-02 | ESE_MODE Environment Variable | ✅ Sprint 1 | Full delivery |
| F-ESE-001-03 | Adapter Factory Pattern | ✅ Sprint 1 | Full delivery |
| F-ESE-001-04 | Adapter Health Check | ✅ Sprint 1 | Full delivery |
| F-ESE-002-01 | Dataset Seeder Script | ✅ Sprint 1 | 6 personas seeded |
| F-ESE-002-02 | Dataset Reset API | ✅ Sprint 1 | Full delivery |
| F-ESE-003-01 | Persona Schema Definition | ✅ Sprint 1 | Full delivery |
| F-ESE-003-02 | Approved Persona Pack | 🔄 Partial | 3 of 7 approved personas |
| F-ESE-003-03 | Rejected Persona Pack | 🔄 Partial | 1 of 3 (fraud deferred to Sprint 2) |
| F-ESE-003-05 | Synthetic PAN Format | ✅ Sprint 1 | `SIMxxNNNNS` enforced |
| F-ESE-004-01 | SimulationCKYCAdapter | ✅ Sprint 1 | Reference implementation |

---

## 6. User Stories

### US-ESE-S1-001 — Simulation Mode Switching via Environment Variable
**Epic**: EP-ESE-001 Simulation Core  
**Persona**: DevOps Engineer  
**Story Points**: 3  
**Priority**: Critical

**User Story**:  
As a DevOps Engineer, I want to control the entire adapter layer by setting a single `ESE_MODE` environment variable at service startup, so that I can switch between simulation and production without touching any service code.

**Acceptance Criteria**:
1. Setting `ESE_MODE=SIMULATION` causes the adapter factory to load all simulation adapters at startup.
2. Setting `ESE_MODE=PRODUCTION` causes the adapter factory to load all production adapters.
3. Setting `ESE_MODE=DEMO` loads simulation adapters with Vertex AI enabled for the credit engine.
4. Setting `ESE_MODE=TRAINING` loads simulation adapters with artificial response latency enabled.
5. An invalid or missing `ESE_MODE` defaults to `SIMULATION` with a startup warning logged.
6. No service business logic code is aware of which adapter is loaded.
7. `GET /health` response includes `{"ese_mode": "SIMULATION", "adapters_loaded": 10}`.

**Technical Notes**:
* Implement in a new module: `services/ese-core/adapter_factory.py`
* `ESE_MODE` is read once at application startup via `os.getenv("ESE_MODE", "SIMULATION")`
* Adapter factory uses a registry pattern; new adapters register themselves

---

### US-ESE-S1-002 — Adapter Interface Abstract Base Class
**Epic**: EP-ESE-001 Simulation Core  
**Persona**: Enterprise Architect  
**Story Points**: 2  
**Priority**: Critical

**User Story**:  
As an Enterprise Architect, I want a formally defined abstract base class that every external integration adapter must implement, so that simulation and production adapters are interchangeable by design.

**Acceptance Criteria**:
1. `ExternalIntegrationAdapter` abstract base class defined with `fetch()` and `health_check()` abstract methods.
2. `AdapterRequest` and `AdapterResponse` data classes defined for type-safe interface communication.
3. Concrete adapter classes that do not implement all abstract methods raise `TypeError` at import.
4. Reference implementation (`SimulationCKYCAdapter`) inherits from the base class correctly.
5. Unit tests confirm the interface contract is enforced.
6. Docstrings on all abstract methods describe the expected input/output contract.

**Technical Notes**:
* Location: `services/ese-core/adapters/base.py`
* Use Python `abc.ABC` and `@abstractmethod`
* `AdapterRequest` contains: `integration_name`, `customer_id`, `scenario_id`, `params: dict`
* `AdapterResponse` contains: `data: dict`, `status_code: int`, `simulated: bool`, `latency_ms: float`

---

### US-ESE-S1-003 — Adapter Factory with Registry Pattern
**Epic**: EP-ESE-001 Simulation Core  
**Persona**: Technical Lead  
**Story Points**: 3  
**Priority**: Critical

**User Story**:  
As a Technical Lead, I want an adapter factory that resolves the correct adapter class for each integration based on the active `ESE_MODE`, so that adding a new adapter requires only registering it — not modifying factory logic.

**Acceptance Criteria**:
1. `AdapterFactory` class resolves adapter by `(integration_name, ese_mode)` key.
2. New adapters self-register using a `@register_adapter(integration, mode)` decorator.
3. Requesting an unregistered `(integration, mode)` combination raises `AdapterNotRegisteredError`.
4. Factory unit tests cover: valid simulation resolution, valid production resolution, unregistered error.
5. All 10 integration names are defined as constants in `adapter_registry.py`.

**Integration Name Constants**:
`CKYC, GSTN, AA, EPFO, MCA, RBI_FRAUD, OCEN, VERTEX_AI, CAM, FHC`

---

### US-ESE-S1-004 — Adapter Health Check Endpoint
**Epic**: EP-ESE-001 Simulation Core  
**Persona**: SRE Lead  
**Story Points**: 2  
**Priority**: High

**User Story**:  
As an SRE Lead, I want a health check endpoint that confirms all registered adapters are loaded and responsive, so that I can detect adapter misconfiguration before a demo starts.

**Acceptance Criteria**:
1. `GET /health/adapters` returns the health status of all registered adapters.
2. Response includes: adapter name, mode (SIMULATION/PRODUCTION), `is_healthy: bool`.
3. Any unhealthy adapter causes the overall health status to return HTTP 503.
4. Health check completes in < 500ms.
5. Endpoint is accessible without authentication in all ESE modes.

**Example Response**:
```json
{
  "ese_mode": "SIMULATION",
  "overall_status": "healthy",
  "adapters": [
    {"name": "CKYC", "mode": "SIMULATION", "is_healthy": true},
    {"name": "GSTN", "mode": "SIMULATION", "is_healthy": true}
  ]
}
```

---

### US-ESE-S1-005 — Dataset Repository Schema and SQLite Design
**Epic**: EP-ESE-002 Demo Dataset Engine  
**Persona**: Technical Lead  
**Story Points**: 5  
**Priority**: Critical

**User Story**:  
As a Technical Lead, I want the ESE dataset repository to use a well-defined JSON schema for persona definitions and a SQLite database for runtime simulation data, so that the dataset is portable, versioned, and independently resettable without affecting production databases.

**Acceptance Criteria**:
1. `personas/` directory contains one JSON file per persona following the canonical schema.
2. Persona JSON schema is documented in `personas/schema.json` with JSON Schema validation.
3. SQLite database `ese_dataset.db` is separate from all production service databases.
4. Database tables: `ese_customers`, `ese_businesses`, `ese_gst_records`, `ese_transactions`, `ese_ckyc_records`, `ese_epfo_records`, `ese_mca_records`, `ese_loan_applications`.
5. All ESE tables are prefixed `ese_` to prevent naming collisions with production tables.
6. `ese_dataset_version.json` records: schema version, seed timestamp, persona count.

**Persona JSON Schema (Canonical)**:
```json
{
  "scenario_id": "SCN-001",
  "persona_name": "Priya Textile Works",
  "pan": "SIMPT0001K",
  "gstin": "27SIMPT0001K1Z5",
  "business_type": "Manufacturing",
  "expected_credit_outcome": "APPROVED",
  "fhc_score_target": 92,
  "ckyc_status": "CLEAN",
  "gst_profile": "HIGH_GROWTH",
  "aa_cash_flow_profile": "STRONG_CASHFLOW",
  "epfo_status": "GROWING_WORKFORCE",
  "mca_status": "ACTIVE_COMPLIANT",
  "rbi_fraud_status": "CLEAN",
  "explainability_tags": ["DSCR_OK", "GST_GROWTH_STRONG", "FHC_STRONG"]
}
```

---

### US-ESE-S1-006 — Dataset Seed Loader Script
**Epic**: EP-ESE-002 Demo Dataset Engine  
**Persona**: Demo Administrator  
**Story Points**: 5  
**Priority**: Critical

**User Story**:  
As a Demo Administrator, I want a single command (`python seed_demo_data.py`) that reads all persona JSON files and populates the ESE SQLite database, so that the platform is demo-ready in under 5 minutes.

**Acceptance Criteria**:
1. `python seed_demo_data.py` completes successfully in < 5 minutes from a clean state.
2. Seeds all 6 Sprint 1 personas (13 in final release).
3. Generates associated records: 1 CKYC record, 12 GST filing records (12 months), 50 bank transactions, 1 EPFO record, 1 MCA record per persona.
4. Script is idempotent — running twice does not create duplicate records.
5. Seed completion log: `[SEED COMPLETE] 6 personas, 72 GST records, 300 transactions seeded in 42.3s`.
6. `ese_dataset_version.json` updated with seed timestamp and record counts.

**Seed Data Rules**:
* GST filing amounts consistent with AA cash flow profile (variance ≤ 15%)
* Transaction amounts scaled to persona business size (INR 5L–50L monthly)
* EPFO employee count proportional to revenue tier
* All dates relative to seed date (no hardcoded year references)

---

### US-ESE-S1-007 — Dataset Reset API
**Epic**: EP-ESE-002 Demo Dataset Engine  
**Persona**: Demo Administrator  
**Story Points**: 2  
**Priority**: Critical

**User Story**:  
As a Demo Administrator, I want a `POST /ese/admin/dataset/reset` endpoint that wipes and re-seeds the entire ESE dataset in under 60 seconds, so that I can prepare for back-to-back demonstrations without terminal access.

**Acceptance Criteria**:
1. `POST /ese/admin/dataset/reset` triggers wipe-and-reseed within 60 seconds.
2. Response includes: `{"status": "complete", "personas_seeded": 6, "duration_seconds": 34.2}`.
3. In-flight demo requests are not interrupted — reset queues until request completion.
4. Endpoint requires Admin authentication (API key in Sprint 1; SSO in Sprint 3).
5. Reset events are logged to the ESE audit log with timestamp and requesting user ID.

---

### US-ESE-S1-008 — Persona Schema Definition and Validation
**Epic**: EP-ESE-003 Banking Personas  
**Persona**: Product Owner  
**Story Points**: 3  
**Priority**: Critical

**User Story**:  
As a Product Owner, I want all 6 Sprint 1 personas defined in validated JSON files following the canonical schema, so that adapter responses are consistent, scenario outcomes are deterministic, and the team can develop adapters against stable persona profiles.

**Acceptance Criteria**:
1. 6 persona JSON files exist in `ese/personas/`:
   * `SCN-001_priya_textile_works.json` (Manufacturing MSME — APPROVED)
   * `SCN-002_ramesh_kirana_store.json` (Retail — MANUAL_REVIEW)
   * `SCN-005_techboost_solutions.json` (Startup — APPROVED)
   * `SCN-004_kavitha_exports.json` (Exporter — APPROVED)
   * `SCN-012_deepa_handicrafts.json` (Women Entrepreneur — APPROVED)
   * `SCN-013_green_valley_farms.json` (Agri Enterprise — APPROVED)
2. All 6 files pass JSON Schema validation against `personas/schema.json`.
3. Each file includes all required fields: `scenario_id`, `pan`, `gstin`, `expected_credit_outcome`, `explainability_tags`, all profile fields.
4. Synthetic PANs follow `SIMxxNNNNS` format.
5. Synthetic GSTINs follow `NN SIMxx NNNNS NZN` format.

---

### US-ESE-S1-009 — Manufacturing MSME Persona (SCN-001: Priya Textile Works)
**Epic**: EP-ESE-003 Banking Personas  
**Persona**: Banking Domain Expert  
**Story Points**: 2  
**Priority**: Critical

**User Story**:  
As a Banking Domain Expert, I want the Manufacturing MSME persona to represent a strong, bankable MSME with consistent GST compliance, healthy cash flows, and a growing workforce, so that it serves as the showcase "Perfect Borrower" in board presentations.

**Acceptance Criteria**:
1. `fhc_score_target: 92`, `gst_profile: HIGH_GROWTH`, `aa_cash_flow_profile: STRONG_CASHFLOW`.
2. 36 months of GST returns — 100% filing compliance, revenue growing at ≥ 15% YoY.
3. AA bank statement shows consistent positive EOD balance; DSCR ≥ 1.8.
4. EPFO employee count: 45 employees; 100% PF compliance.
5. `expected_credit_outcome: APPROVED`; `explainability_tags: ["DSCR_OK", "GST_GROWTH_STRONG", "FHC_STRONG"]`.
6. Credit amount eligibility: INR 50 Lakhs.

---

### US-ESE-S1-010 — Retail MSME Persona (SCN-002: Ramesh Kirana Store)
**Epic**: EP-ESE-003 Banking Personas  
**Persona**: Banking Domain Expert  
**Story Points**: 2  
**Priority**: Critical

**User Story**:  
As a Banking Domain Expert, I want the Retail MSME persona to represent a new-to-credit small retailer with limited formal financial history, so that trainees can experience the manual review and human-in-the-loop workflow.

**Acceptance Criteria**:
1. `fhc_score_target: 58`, `gst_profile: STABLE`, `aa_cash_flow_profile: STRONG_CASHFLOW`.
2. GST history: 18 months (recently registered); no prior credit accounts.
3. AA bank statement: steady but small turnover (INR 5L/month); DSCR 1.1.
4. EPFO employee count: 3 employees.
5. `expected_credit_outcome: MANUAL_REVIEW`; `explainability_tags: ["NEW_TO_CREDIT", "DSCR_OK"]`.

---

### US-ESE-S1-011 — Startup Persona (SCN-005: TechBoost Solutions)
**Epic**: EP-ESE-003 Banking Personas  
**Persona**: Banking Domain Expert  
**Story Points**: 2  
**Priority**: High

**User Story**:  
As a Banking Domain Expert, I want the IT Startup persona to showcase AI credit underwriting for high-growth, low-asset businesses, so that demos highlight the platform's ability to assess non-traditional creditworthiness.

**Acceptance Criteria**:
1. `fhc_score_target: 79`, `gst_profile: HIGH_GROWTH`, `aa_cash_flow_profile: STRONG_CASHFLOW`.
2. GST revenue growing at ≥ 40% YoY; 24-month history.
3. Low fixed assets but high cash inflows from SaaS contracts.
4. EPFO: 12 employees, growing 30% YoY.
5. `expected_credit_outcome: APPROVED`; `explainability_tags: ["GST_GROWTH_STRONG", "DSCR_OK"]`.

---

### US-ESE-S1-012 — Exporter Persona (SCN-004: Kavitha Exports Ltd)
**Epic**: EP-ESE-003 Banking Personas  
**Persona**: Banking Domain Expert  
**Story Points**: 2  
**Priority**: High

**User Story**:  
As a Banking Domain Expert, I want the Exporter persona to represent an MSME with foreign exchange receipts and export-linked GST filings, so that demos showcase the platform's capability for trade finance and ECGC-aligned credit assessment.

**Acceptance Criteria**:
1. `fhc_score_target: 88`, `gst_profile: HIGH_GROWTH`, `aa_cash_flow_profile: STRONG_CASHFLOW`.
2. AA transactions include regular SWIFT inflows (tagged as export receipts).
3. GST filings include zero-rated export invoices.
4. `expected_credit_outcome: APPROVED`; `explainability_tags: ["DSCR_OK", "GST_GROWTH_STRONG", "FHC_STRONG"]`.
5. ECGC coverage indicator: `true` in persona JSON.

---

### US-ESE-S1-013 — Women Entrepreneur Persona (SCN-012: Deepa Handicrafts)
**Epic**: EP-ESE-003 Banking Personas  
**Persona**: Banking Domain Expert  
**Story Points**: 2  
**Priority**: High

**User Story**:  
As a Banking Domain Expert, I want the Women Entrepreneur persona to showcase MUDRA and Mahila Udyam Nidhi scheme eligibility, so that demos highlight the platform's social lending and financial inclusion capabilities.

**Acceptance Criteria**:
1. `fhc_score_target: 85`, `gst_profile: STABLE`, `aa_cash_flow_profile: STRONG_CASHFLOW`.
2. `mudra_eligible: true` and `scheme_tags: ["MUDRA", "MAHILA_UDYAM_NIDHI"]` in persona JSON.
3. Business category: Artisan / Handicraft (registered under MSME).
4. `expected_credit_outcome: APPROVED`; `explainability_tags: ["DSCR_OK", "FHC_STRONG"]`.

---

### US-ESE-S1-014 — Agri Enterprise Persona (SCN-013: Green Valley Farms)
**Epic**: EP-ESE-003 Banking Personas  
**Persona**: Banking Domain Expert  
**Story Points**: 2  
**Priority**: High

**User Story**:  
As a Banking Domain Expert, I want the Agri Enterprise persona to exhibit seasonal cash flows consistent with agricultural crop cycles, so that demos highlight the platform's seasonal income underwriting capability.

**Acceptance Criteria**:
1. `fhc_score_target: 74`, `gst_profile: SEASONAL`, `aa_cash_flow_profile: SEASONAL_CASHFLOW`.
2. AA transactions show high inflows in Oct–Dec (Rabi harvest) and Apr–Jun (Kharif).
3. GST filings reflect seasonal turnover — Q1 and Q3 high, Q2 and Q4 lower.
4. `expected_credit_outcome: APPROVED`; `explainability_tags: ["DSCR_OK", "GST_GROWTH_STRONG"]`.
5. KCC (Kisan Credit Card) eligibility: `true` in persona JSON.

---

### US-ESE-S1-015 — CKYC Simulation Adapter (Reference Implementation)
**Epic**: EP-ESE-004 CKYC Simulator  
**Persona**: Technical Lead  
**Story Points**: 3  
**Priority**: Critical

**User Story**:  
As a Technical Lead, I want the CKYC simulation adapter to serve as the reference implementation of the adapter pattern, demonstrating how every subsequent simulation adapter should be built, so that Sprint 2 engineers have a clear, working template.

**Acceptance Criteria**:
1. `SimulationCKYCAdapter` inherits from `ExternalIntegrationAdapter`.
2. `fetch(request)` looks up the customer's PAN in the ESE dataset and returns a CKYC response.
3. Response includes: `kycId`, `name`, `pan`, `aadhaar_masked`, `dob`, `address`, `kyc_status`.
4. `kyc_status` is driven by the persona's `ckyc_status` field (CLEAN / EXPIRED / INCOMPLETE).
5. Adapter returns `AdapterResponse(simulated=True)` in all cases.
6. Latency simulation: response delayed by `random.uniform(200, 400)` ms in Demo/Training modes; 0ms in Testing mode.
7. Unit tests: valid PAN returns correct CKYC data; unknown PAN returns 404 AdapterResponse.
8. Adapter passes the `GET /health/adapters` health check.
9. Full adapter developer guide written as a docstring in the class.

---

### US-ESE-S1-016 — Synthetic Data Generation Rules Documentation
**Epic**: EP-ESE-002 Demo Dataset Engine  
**Persona**: Technical Lead  
**Story Points**: 2  
**Priority**: High

**User Story**:  
As a Technical Lead, I want the synthetic data generation rules documented in a formal specification, so that Sprint 2 engineers generating transaction and GST datasets apply consistent, realistic rules.

**Acceptance Criteria**:
1. `ese/docs/synthetic_data_generation_rules.md` created and committed.
2. Rules defined for: GST filing amounts, bank transaction patterns, EPFO contribution schedules, seasonal adjustment factors.
3. Revenue consistency rule documented: GST revenue must equal AA inflows within ±15%.
4. Date relativization rule: all dates are expressed as offsets from seed date (e.g., `-36 months`), never hardcoded calendar dates.
5. Reviewed and signed off by Banking Domain Expert.

---

### US-ESE-S1-017 — ESE Docker Compose Demo Configuration
**Epic**: EP-ESE-001 Simulation Core  
**Persona**: DevOps Engineer  
**Story Points**: 2  
**Priority**: Critical

**User Story**:  
As a DevOps Engineer, I want a `docker-compose.ese.yml` file that launches all 16 services in Demo Mode with a single command, so that any team member can run a fully functional ESE environment in under 5 minutes.

**Acceptance Criteria**:
1. `docker-compose -f docker-compose.ese.yml up` starts all 16 production services + ese-admin service.
2. All services have `ESE_MODE=DEMO` set in environment.
3. Services use `ese_dataset.db` (not production databases).
4. A `healthcheck` block is defined for each service.
5. Compose file includes a `seed` init container that runs `seed_demo_data.py` before services start.
6. README updated with ESE quickstart: `git clone → docker-compose -f docker-compose.ese.yml up`.

---

## 7. Story Points

| Story ID | Title | Epic | SP | Priority |
| :--- | :--- | :---: | :---: | :---: |
| US-ESE-S1-001 | Simulation Mode Switching | EP-ESE-001 | 3 | Critical |
| US-ESE-S1-002 | Adapter Interface ABC | EP-ESE-001 | 2 | Critical |
| US-ESE-S1-003 | Adapter Factory Registry | EP-ESE-001 | 3 | Critical |
| US-ESE-S1-004 | Adapter Health Check | EP-ESE-001 | 2 | High |
| US-ESE-S1-005 | Dataset Repository Schema | EP-ESE-002 | 5 | Critical |
| US-ESE-S1-006 | Dataset Seed Loader | EP-ESE-002 | 5 | Critical |
| US-ESE-S1-007 | Dataset Reset API | EP-ESE-002 | 2 | Critical |
| US-ESE-S1-008 | Persona Schema & Validation | EP-ESE-003 | 3 | Critical |
| US-ESE-S1-009 | SCN-001 Priya Textile (Manufacturing) | EP-ESE-003 | 2 | Critical |
| US-ESE-S1-010 | SCN-002 Ramesh Kirana (Retail) | EP-ESE-003 | 2 | Critical |
| US-ESE-S1-011 | SCN-005 TechBoost (Startup) | EP-ESE-003 | 2 | High |
| US-ESE-S1-012 | SCN-004 Kavitha Exports (Exporter) | EP-ESE-003 | 2 | High |
| US-ESE-S1-013 | SCN-012 Deepa Handicrafts (Women) | EP-ESE-003 | 2 | High |
| US-ESE-S1-014 | SCN-013 Green Valley (Agri) | EP-ESE-003 | 2 | High |
| US-ESE-S1-015 | CKYC Simulation Adapter (Reference) | EP-ESE-004 | 3 | Critical |
| US-ESE-S1-016 | Synthetic Data Rules Documentation | EP-ESE-002 | 2 | High |
| US-ESE-S1-017 | ESE Docker Compose Demo Config | EP-ESE-001 | 2 | Critical |
| **TOTAL** | | | **38 SP** | |

**Sprint Capacity**: 40 SP | **Committed**: 38 SP | **Buffer**: 2 SP

---

## 8. Risks

| Risk ID | Description | Likelihood | Impact | Mitigation |
| :--- | :--- | :---: | :---: | :--- |
| R-S1-001 | Dataset seeder takes > 5 minutes for 6 personas | Low | Medium | Profile seed script early; use bulk SQLite inserts |
| R-S1-002 | Adapter factory pattern incompatible with FastAPI `Depends()` | Low | High | Prototype adapter injection in Sprint 1 Day 1; resolve before persona work begins |
| R-S1-003 | Persona JSON schema too rigid for Sprint 2 adapter requirements | Medium | Medium | Banking Domain Expert validates schema against all 10 adapter response contracts before sign-off |
| R-S1-004 | ESE Docker Compose port conflicts with production services | Low | Low | ESE services use port range 9000–9099; production uses 8000–8099 |
| R-S1-005 | `ese_dataset.db` file locking under concurrent seed + API access | Low | Medium | Use SQLite WAL mode from Sprint 1 initialization |

---

## 9. Dependencies

| Dependency | Type | Required By | Owner |
| :--- | :--- | :--- | :--- |
| v1.1.0 production codebase | Internal | All Sprint 1 stories | Tech Lead |
| `ese-core` Python module location agreed | Architecture | US-ESE-S1-001 | Enterprise Architect |
| Persona JSON schema signed off by Banking Domain Expert | Business | US-ESE-S1-008 | Banking Domain Expert |
| ESE port range (9000–9099) approved | Infrastructure | US-ESE-S1-017 | DevOps Engineer |
| SQLite WAL mode confirmed as sufficient for Sprint 1 load | Technical | US-ESE-S1-005 | Technical Lead |
| Synthetic PAN format `SIMxxNNNNS` legal review | Compliance | US-ESE-S1-008 | Banking Domain Expert |

---

## 10. Deliverables

| # | Deliverable | Owner | Acceptance |
| :---: | :--- | :--- | :--- |
| 1 | `ese-core/adapters/base.py` — Adapter interface ABC | Technical Lead | Unit tests pass |
| 2 | `ese-core/adapter_factory.py` — Factory with registry | Technical Lead | Factory tests pass |
| 3 | `ese-core/adapters/simulation/ckyc.py` — Reference adapter | Backend Lead | CKYC adapter tests pass; health check green |
| 4 | `ese/personas/schema.json` — Canonical persona schema | Enterprise Architect | JSON Schema validates all 6 persona files |
| 5 | 6 × Persona JSON files (`SCN-001` to `SCN-013` subset) | Banking Domain Expert | Schema validation passes; outcomes verified |
| 6 | `ese/seed_demo_data.py` — Seed loader script | Backend Lead | Completes in < 5 min; idempotent |
| 7 | `POST /ese/admin/dataset/reset` — Reset endpoint | Backend Lead | Completes in < 60 seconds |
| 8 | `GET /health/adapters` — Adapter health endpoint | Backend Lead | Returns all adapter statuses |
| 9 | `ese/docs/synthetic_data_generation_rules.md` | Technical Lead | Banking Domain Expert sign-off |
| 10 | `docker-compose.ese.yml` — Demo deployment config | DevOps Engineer | All services start healthy in Demo Mode |
| 11 | `ese_dataset_version.json` — Dataset version file | Backend Lead | Updated after each seed |

---

## 11. Definition of Done

A Sprint 1 User Story is **Done** when all of the following are true:

- [ ] All Acceptance Criteria are verified and passing
- [ ] Code committed to `feature/ese-sprint-1` branch (not `main`)
- [ ] Unit tests written and passing (coverage ≥ 80% for new code)
- [ ] No new linting errors introduced
- [ ] Code reviewed by at least one peer
- [ ] Relevant documentation (docstrings, README sections) updated
- [ ] `GET /health/adapters` returns green for affected adapters
- [ ] Sprint 1 acceptance test (from Sprint Goal) passes for relevant story
- [ ] Banking Domain Expert has approved persona accuracy for persona stories

**Sprint Done** when:
- [ ] All 17 user stories marked Done
- [ ] Sprint 1 acceptance test (all 5 criteria) passes in a clean environment
- [ ] Sprint Review demo successfully launches ESE in Demo Mode from `docker-compose.ese.yml up`
- [ ] Sprint Retrospective conducted

---

## 12. Sprint KPIs

| KPI | Target | Measurement |
| :--- | :---: | :--- |
| Story Points Committed | 38 SP | Sprint Planning |
| Story Points Delivered | ≥ 36 SP | Sprint Review |
| Sprint Velocity | ≥ 36 SP | Sprint Review |
| Unit Test Coverage (new code) | ≥ 80% | CI pipeline |
| Adapter health check pass rate | 100% | `GET /health/adapters` |
| Seed loader execution time | < 5 minutes | Timing log |
| Dataset reset execution time | < 60 seconds | API response `duration_seconds` |
| Persona schema validation pass rate | 100% | JSON Schema validation |
| Defects introduced | 0 Critical / 0 High | Sprint Review |
| Peer review coverage | 100% of stories | Code review log |

---

*ESE Sprint 1 | Enterprise Simulation Engine v1.0*  
*Project AAROHAN — IDBI Bank MSME Digital Lending Platform*  
*Sprint: 2026-07-08 to 2026-07-21*
