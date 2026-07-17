# AAR-ESE-004: Project AAROHAN Enterprise Simulation Engine (ESE) & Enterprise Digital Banking Twin — Sprint 1 Implementation Plan (v3)

**Document Classification**: Enterprise Architecture Blueprint  
**Sprint**: ESE Sprint 1 of 5  
**Version**: 3.0  
**Status**: 🟢 SPRINT PLANNING BASELINE APPROVED  
**Date**: 2026-07-08  
**Platform**: Project AAROHAN Enterprise Digital Banking Twin v3.0  

---

## 1. Executive Summary

This document defines the final Sprint 1 Implementation Plan baseline for the **Project AAROHAN Enterprise Simulation Engine (ESE)**, also referred to as the **Enterprise Digital Banking Twin**. ESE operates as an isolated digital mirror of the entire MSME credit lending ecosystem, simulating customers, businesses, regulators, lenders, banking systems, AI systems, and Digital Public Infrastructure (DPI) without modifying Project AAROHAN's production services.

This v3 baseline enhances the engine by introducing:
1. **Scenario Engine**: Decoupling Persona (WHO) from Scenario (WHAT).
2. **Demo Journey Engine**: Executing end-to-end digital lending workflows.
3. **Dataset Marketplace**: Hosting domain-specific datasets (MSME, Retail, Agriculture, etc.).
4. **Demo Control Center API**: Dynamic environment switching.
5. **AI Demonstration Mode**: Deterministic and explainable AI twins.

---

## 2. Integration Profile Framework (Improvement 1)

The system utilizes an `INTEGRATION_PROFILE` environment setting which dictates the dynamic selection of active adapters at startup:

* `DEMO`: Fully simulated, low latency, Vertex AI enabled.
* `TRAINING`: Deterministic datasets with artificial response latency enabled.
* `UAT`: Mixed mode (simulated external dependencies, live internal APIs).
* `PERFORMANCE`: High-volume synthetic datasets optimized for low latency overhead.
* `PRODUCTION`: Live banking integrations and actual production adapters.

---

## 3. Scenario Engine: Decoupling Persona & Scenario (Enterprise Improvement 1)

A **Persona** defines **WHO** the customer is (business profile, structure, baseline parameters).  
A **Scenario** defines **WHAT** happens to that customer (financial compliance events, transaction histories, risk events).

### Folder Structure
```
ese/
└── scenarios/
    ├── SCN-001_EXCELLENT_BORROWER.json
    ├── SCN-002_GST_DEFAULTER.json
    ├── SCN-003_CASHFLOW_STRESS.json
    ├── SCN-004_EXPORT_SUCCESS.json
    ├── SCN-005_NEW_TO_CREDIT.json
    ├── SCN-006_RBI_BLACKLIST.json
    ├── SCN-007_EPFO_DEFAULT.json
    ├── SCN-008_HIGH_GROWTH_STARTUP.json
    ├── SCN-009_MANUFACTURING_EXPANSION.json
    └── SCN-010_SEASONAL_BUSINESS.json
```

### Dynamic Combination Protocol
When a simulation is executed, the Digital Banking Twin combines the selected Persona profile data with the active Scenario JSON rules. The Scenario JSON overrides the default persona attributes (e.g., overriding compliance status to `NON_COMPLIANT` or injecting a blacklisted PAN), generating transaction tables, GST files, and credit outcomes dynamically matching the scenario definition.

---

## 4. Demo Journey Engine (Enterprise Improvement 2)

The **Demo Journey Engine** orchestrates and tracks multi-service workflows. It allows administrators to run complete end-to-end workflows using a single command or API call.

### Supported Journeys

1. **Journey 1: Customer Onboarding**
2. **Journey 2: Financial Health Card**
3. **Journey 3: Complete MSME Lending Journey**
4. **Journey 4: Fraud Detection Journey**
5. **Journey 5: OCEN Marketplace Journey**
6. **Journey 6: AI Credit Decision Journey**
7. **Journey 7: Board Presentation Journey**

### Lending Journey Orchestration Workflow
```
Customer Onboard ──> CKYC Verify ──> GST Sync ──> AA Fetch ──> EPFO Sync ──> MCA Profile
                                                                              │
┌─────────────────────────────────────────────────────────────────────────────┘
▼
FHC Calculation ──> AI Credit Appraisal ──> RBI Fraud Registry ──> OCEN Marketplace ──> CAM Generation
```

### Operational Features
* **One-Click Execution**: Simple orchestrator execution.
* **Execution Timeline**: Microsecond-level tracking of step transitions.
* **Audit Log & Summary**: Event-driven transaction tracing.

---

## 5. Dataset Marketplace (Enterprise Improvement 3)

Instead of a single directory, the engine supports a directory-based **Dataset Marketplace** to isolate domain data:

### Directory Layout
```
ese/
└── datasets/
    ├── msme/
    │   ├── banking.db
    │   ├── dataset_manifest.json
    │   └── personas/
    ├── retail/
    ├── manufacturing/
    ├── agriculture/
    ├── startup/
    ├── corporate/
    ├── training/
    ├── executive-demo/
    └── performance/
```

### Manifest Schema (`dataset_manifest.json`)
Tracks dataset name, version, description, personas, scenarios, supported demo journeys, record counts, checksums, and generation metadata. Domain switching is done through the Admin Control API without code rebuilds.

---

## 6. Demo Control Center (Enterprise Improvement 4)

We extend the simulation administration APIs into a unified **Demo Control Center** matching these endpoints:

* `GET /ese/control`: Exposes current system state and configuration.
* `POST /ese/control/profile`: Switches the active `INTEGRATION_PROFILE`.
* `POST /ese/control/persona`: Binds a customer profile to a selected persona.
* `POST /ese/control/scenario`: Applies a specific scenario override.
* `POST /ese/control/journey`: Executes one of the 7 predefined Demo Journeys.
* `POST /ese/control/dataset`: Switches the active marketplace domain (e.g., `agriculture`).
* `POST /ese/control/reset`: Resets the database back to clean seeded values.
* `GET /ese/control/status`: Returns health, system metrics, and history.

---

## 7. AI Demonstration Mode (Enterprise Improvement 5)

The **AI Demonstration Mode** ensures that the Digital Banking Twin provides repeatable, high-fidelity, and deterministic mock LLM evaluations:

* **CAM Generation**: Deterministic summaries outlining debt service capability.
* **Credit Recommendation**: Output matches scenario-driven targets.
* **Explanations**: Returns clear explainability tags for credit, risk, and fraud scenarios.

---

## 8. File and Path Matrix

### New Files
* [services/ese-core/adapters/base.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/adapters/base.py) — Base requests and interfaces.
* [services/ese-core/adapter_factory.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/adapter_factory.py) — Adapter factory registry.
* [services/ese-core/adapters/simulation/](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/adapters/simulation/) — Placeholders for all 10 simulation adapters.
* [services/ese-core/adapters/production/](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/adapters/production/) — Placeholders for all 10 production adapters (raising `NotImplementedError`).
* [services/ese-core/admin_api.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/admin_api.py) — unified `/ese/control` routers.
* [ese/personas/schema.json](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/ese/personas/schema.json) — Persona JSON validation schema.
* [ese/seed/](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/ese/seed/) — Modular data seeder scripts.
* [ese/docs/synthetic_data_generation_rules.md](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/ese/docs/synthetic_data_generation_rules.md) — Cash flow rules documentation.
* [docker-compose.ese.yml](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/docker-compose.ese.yml) — Compose manifest.

### Modified Files
* [pytest.ini](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/pytest.ini) — Add `services/ese-core` to `pythonpath`.
