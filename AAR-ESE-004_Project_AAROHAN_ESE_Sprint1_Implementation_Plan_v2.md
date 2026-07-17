# AAR-ESE-004: Project AAROHAN Enterprise Simulation Engine — Sprint 1 Implementation Plan (v2)

**Document Classification**: Implementation Architecture Blueprint  
**Sprint**: ESE Sprint 1 of 5  
**Version**: 2.0  
**Status**: 🟡 APPROVED FOR ARCHITECTURAL BASELINE  
**Date**: 2026-07-08  
**Platform**: Enterprise Simulation Engine (ESE) v2.0  

---

## 1. Executive Summary

This document establishes the revised technical implementation baseline for Sprint 1 of the **Project AAROHAN Enterprise Simulation Engine (ESE)**. It incorporates seven key enterprise-grade architectural improvements. The goal is to evolve ESE from a simple mock-switching mechanism into a long-term simulation platform supporting multi-tenant environments (Hackathons, Board Demos, Executive Showcases, training, UAT, performance testing, and production fallback).

All simulation capabilities will exist as isolated plug-in modules, maintaining 100% backward compatibility with Project AAROHAN v1.1 production services. No production code logic will be modified.

---

## 2. Integration Profile Framework (Improvement 1)

Rather than using a single binary flag (`ESE_MODE`), ESE utilizes an `INTEGRATION_PROFILE` framework. This allows the system to change behavior dynamically per microservice instance without code alterations.

### Supported Profiles

| Profile Name | Underwriting Mode | Target Audience / Use Case | Adapter Behavior |
| :--- | :--- | :--- | :--- |
| `DEMO` | Simulated | Sales & Boardroom Showcases | Fully simulated, low latency, Vertex AI enabled |
| `TRAINING` | Simulated | Internal Bank Trainees | Deterministic datasets with injected artificial latency |
| `UAT` | Mixed | Quality Assurance & Testing | Mixed mode: simulated external sources, live internal APIs |
| `PERFORMANCE` | Simulated | Performance/Stress Testing | High-volume synthetic datasets, minimal latency overhead |
| `PRODUCTION` | Live | Real-world Digital Lending | Fully live banking APIs and production adapters |

### AdapterFactory Matching Matrix

The `AdapterFactory` maps requests based on `(integration_name, integration_profile)` keys. If a profile doesn't have a customized adapter for a specific integration, it falls back to default mapping rules:

```
[Profile Request] ──> [AdapterFactory] ──> [Match Profile?]
                                                │
                                    ┌───────────┴───────────┐
                                   YES                      NO
                                    │                       │
                                    ▼                       ▼
                        [Load Profile Adapter]      [Default to SIM/PROD]
```

### Profile Extensibility

Adding new profiles (e.g., `REGULATORY_AUDIT` or `SANDBOX`) is achieved by updating the profile registration registry in `adapter_factory.py` without modifying the concrete adapter classes or microservice logic.

---

## 3. Expanded Adapter Framework (Improvement 2)

We will establish the interface contracts and initial placeholders/reference classes for both **Simulation** and **Production** modes across all 10 integrations.

```
                   ┌──────────────────────────────┐
                   │  ExternalIntegrationAdapter  │
                   └──────────────┬───────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌─────────────────┐                               ┌─────────────────┐
│  Simulation     │                               │  Production     │
│  Adapters       │                               │  Adapters       │
│  (Fully Mocked) │                               │  (Live Client)  │
└─────────────────┘                               └─────────────────┘
 - SimulationCKYCAdapter                           - ProductionCKYCAdapter
 - SimulationGSTNAdapter                           - ProductionGSTNAdapter
 - SimulationAAAdapter                             - ProductionAAAdapter
 - SimulationEPFOAdapter                           - ProductionEPFOAdapter
 - SimulationMCAAdapter                            - ProductionMCAAdapter
 - SimulationRBI_FRAUDAdapter                      - ProductionRBI_FRAUDAdapter
 - SimulationOCENAdapter                           - ProductionOCENAdapter
 - SimulationVERTEX_AIAdapter                      - ProductionVERTEX_AIAdapter
 - SimulationCAMAdapter                            - ProductionCAMAdapter
 - SimulationFHCAdapter                            - ProductionFHCAdapter
```

### Adapter Interface Contracts

All adapters inherit from `ExternalIntegrationAdapter` and implement:
* `fetch(request: AdapterRequest) -> AdapterResponse`
* `health_check() -> bool`

Production adapters initially raise `NotImplementedError` for methods not yet integrated, preserving the architecture for Sprint 2+ live connection work.

---

## 4. Dataset Package Architecture (Improvement 3 & 5)

To support multiple banking domains and test environments, we replace the single sqlite database with a structured **Dataset Packages** directory under `ese/datasets/`.

### Directory Layout

```
ese/
└── datasets/
    ├── v1/
    │   ├── dataset_manifest.json     # Package definition, metrics, metadata
    │   ├── banking.db                # SQLite database for this package
    │   └── personas/                 # Persona JSON files for v1
    │       ├── SCN-001_priya.json
    │       └── SCN-002_ramesh.json
    └── v2/
        ├── dataset_manifest.json
        └── banking.db
```

### Dataset Package Manifest (`dataset_manifest.json`)
```json
{
  "dataset_name": "MSME Banking Demo Package",
  "dataset_version": "1.0.0",
  "compatibility_version": "v2.0",
  "generation_timestamp": "2026-07-08T13:48:33Z",
  "checksum": "sha256_hash_here",
  "supported_personas": ["SCN-001", "SCN-002", "SCN-004", "SCN-005", "SCN-012", "SCN-013"],
  "supported_scenarios": ["SHOWCASE_APPROVED", "MANUAL_REVIEW_NEW_CREDIT", "STARTUP_HIGH_GROWTH"],
  "record_counts": {
    "customers": 6,
    "businesses": 6,
    "gst_records": 72,
    "transactions": 300,
    "epfo_records": 6
  },
  "seed_modules_used": ["seed_customers", "seed_businesses", "seed_transactions", "seed_gst", "seed_ckyc", "seed_epfo"]
}
```

### Package Switching and Rollbacks
Switching datasets is controlled by changing the `ACTIVE_DATASET_VERSION` environment variable (e.g., `ACTIVE_DATASET_VERSION=v1`). The file system path will point dynamically to `ese/datasets/{ACTIVE_DATASET_VERSION}/banking.db`. Rollbacks are executed by pointing back to previous version folders.

---

## 5. Modular Seed Framework (Improvement 4)

We split data seeding into modular scripts under `ese/seed/` directed by a single orchestrator `seed_all.py`.

### Modular Directory Structure

```
ese/
└── seed/
    ├── seed_all.py                # Main orchestrator
    ├── seed_customers.py          # Onboarding profiles
    ├── seed_businesses.py         # Business entities
    ├── seed_transactions.py       # Bank statement transactions
    ├── seed_gst.py                # GSTR-1, GSTR-3B filings
    ├── seed_ckyc.py               # Central KYC registry records
    ├── seed_epfo.py               # EPFO payroll histories
    ├── seed_mca.py                # MCA business registries
    ├── seed_loans.py              # Historical loan applications
    ├── seed_fraud_registry.py     # RBI Fraud Registry entries
    └── validator.py               # Referential integrity validation rules
```

### Orchestration Sequence (`seed_all.py`)
1. **Clean state initialization**: Creates a fresh `banking.db` in the target package folder.
2. **Sequential execution** of seed modules based on foreign key dependencies.
3. **Referential Integrity Validation**: Validates that all records link correctly (e.g., transactions map to an existing account, which maps to a customer).
4. **Manifest Creation**: Computes database checksum, counts records, and outputs `dataset_manifest.json`.

---

## 6. Simulation Health Monitoring (Improvement 6)

A dedicated monitoring router will be exposed on `/ese/health` and related endpoints.

### Monitoring Endpoint Specifications

* `GET /ese/health`: Exposes active profile, database path, active dataset manifest summary, and system overall health.
* `GET /ese/datasets`: Returns list of available dataset packages on disk.
* `GET /ese/profiles`: Lists supported integration profiles.
* `GET /ese/scenarios`: Returns available simulation scenarios based on loaded personas.
* `GET /ese/personas`: Lists all loaded banking personas with their credit target score and outcome.
* `GET /ese/adapters`: Exposes detailed loading state, registry mapping, and connection health status of all 10 adapters.

---

## 7. Backward Compatibility Strategy (Improvement 7)

To ensure version 1.1 production code remains unmodified:
1. **Isolated Module**: All ESE packages reside in `/services/ese-core/` and `/ese/`.
2. **Environment Injection**: Adapter loading occurs during app startup using a generic factory resolver. Microservices query their dependencies through standard DI (FastAPI `Depends()`). The DI system calls `AdapterFactory.get_adapter(name)` which resolves automatically using the `INTEGRATION_PROFILE` environment variable.
3. **No Database Contamination**: All simulation database operations are read/written exclusively to `/ese/datasets/{version}/banking.db`, completely isolated from `aarohan_local.db`.

---

## 8. File and Path Matrix

### New Files
* [services/ese-core/adapters/base.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/adapters/base.py) — Base requests and interfaces.
* [services/ese-core/adapter_factory.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/adapter_factory.py) — Adapter factory and profile registration registry.
* [services/ese-core/adapters/simulation/](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/adapters/simulation/) — Placeholders for all 10 simulation adapters.
* [services/ese-core/adapters/production/](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/adapters/production/) — Placeholders for all 10 production adapters (raising `NotImplementedError`).
* [services/ese-core/admin_api.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/admin_api.py) — `/ese/health` and management endpoints.
* [ese/personas/schema.json](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/ese/personas/schema.json) — Persona JSON validation schema.
* [ese/seed/](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/ese/seed/) — Modular data seeder scripts.
* [ese/docs/synthetic_data_generation_rules.md](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/ese/docs/synthetic_data_generation_rules.md) — Documentation of cash flow relationships.
* [docker-compose.ese.yml](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/docker-compose.ese.yml) — Docker container configuration for ESE.

### Modified Files
* [pytest.ini](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/pytest.ini) — Add `services/ese-core` to `pythonpath`.
