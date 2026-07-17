# Project AAROHAN Enterprise Simulation Engine (ESE) / Enterprise Digital Banking Twin
## AAR-ESE-006: Sprint 2 Planning Document

**Sprint Duration:** July 9, 2026 – July 22, 2026  
**Velocity:** 38 Story Points  
**Approved By:** Agile Product Delivery Team (Product Owner, Scrum Master, Architects)  

---

### 1. Executive Summary
Following the successful completion of Sprint 1, which established the foundational simulation architecture and dynamic profiling engine, Sprint 2 is designed to transform the Enterprise Simulation Engine (ESE) into a rich, high-fidelity **Digital Banking Twin**. 

This sprint expands our synthetic datasets, establishes a robust library of banking personas, builds out 12 complex scenario profiles, integrates deterministic AI risk/appraisal explanations, builds an executive dashboard, and introduces one-click demo journeys. This enables immersive executive demonstrations and advanced user training without changing production systems.

---

### 2. Sprint Goal
Empower relationship managers, risk officers, and executives to simulate, evaluate, and demonstrate the end-to-end MSME lending lifecycle across 12 high-fidelity banking scenarios using expanded synthetic datasets and interactive executive dashboards.

---

### 3. Sprint Scope
The scope of Sprint 2 is organized into six functional pillars:
1.  **Enterprise Dataset Expansion**: Expand synthetic schemas to support over 1,000 customers, 500 MSMEs, and associated transaction streams.
2.  **Banking Persona Expansion**: Add 10 diverse sector personas (e.g., Healthcare Clinic, Textile Manufacturer, Agriculture Cooperative) to demonstrate underwriting versatility.
3.  **Scenario Library Expansion**: Introduce 12 reusable underwriting scenarios (e.g., Seasonal Cash Flow, GST Non-compliance, Startup Funding).
4.  **AI Demonstration Enhancements**: Seed deterministic Vertex AI summaries to explain credit decisions and generate CAM sheets.
5.  **Executive Dashboard API**: Aggregate metrics for portfolio analysis, credit distribution, risk heatmaps, and fraud monitoring.
6.  **Demo Journey Expansion**: Implement one-click scriptable journeys (e.g., Board Meeting, Credit Committee, Fraud Investigation).

---

### 4. Selected Epics
*   **EPIC-ESE-002: Enterprise Data Volume & Diversity Expansion**
*   **EPIC-ESE-003: Core Banking Persona & Behavioral Simulation Library**
*   **EPIC-ESE-004: Risk Scenarios & Exception Simulation Library**
*   **EPIC-ESE-005: AI Explanation & CAM Summary Engine Integration**
*   **EPIC-ESE-006: Executive Portfolio Dashboard & Analytics Engine**
*   **EPIC-ESE-007: Command Center One-Click Journey Orchestrator**

---

### 5. Selected Features
*   **FEAT-ESE-201: High-Volume Synthetic Seeder Extension**
*   **FEAT-ESE-202: 10 Core MSME Industry Sector Personas**
*   **FEAT-ESE-203: 12 Underwriting Risk Scenarios & Data Profiles**
*   **FEAT-ESE-204: Deterministic AI Credit Risk Explainer**
*   **FEAT-ESE-205: ESE Executive Dashboard Metrics Aggregator**
*   **FEAT-ESE-206: One-Click Demo Journey Runner**

---

### 6. User Stories & Story Points

| ID | Title | Story Points | Description |
|---|---|---|---|
| **US-ESE-S2-001** | **Customer & Transaction Scaling** | 8 SP | Extend the seeder framework to generate 1,000+ customers, 500+ MSMEs, and 10,000+ referentially consistent transactions. |
| **US-ESE-S2-002** | **10 Core Banking Personas** | 5 SP | Code and seed behavioral rules for 10 sector personas including Restaurants, Clinics, Textiles, Logistics, Export, etc. |
| **US-ESE-S2-003** | **12 Underwriting Scenarios** | 5 SP | Implement 12 risk scenarios (e.g., Cash Flow Stress, EPFO Defaults, GST Non-compliance) inside the database. |
| **US-ESE-S2-004** | **AI Credit & CAM Explainer** | 8 SP | Seed deterministic, high-fidelity Vertex AI/Gemini responses for credit committee briefs, risk alerts, and FHC metrics. |
| **US-ESE-S2-005** | **Executive Dashboard API** | 5 SP | Create endpoints returning aggregated portfolio volumes, NPA distribution, and FHC health distributions. |
| **US-ESE-S2-006** | **One-Click Scripted Journeys** | 7 SP | Add orchestrations in the Demo Journey Engine for Credit Committee Demo, Fraud Demo, and Portfolio Review. |

**Total Sprint 2 Scope: 38 Story Points**

---

### 7. Sprint Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation Strategy |
|---|---|---|---|
| **Data Generation Latency** | High | Medium | Optimize the SQLite insert logic using bulk inserts, transaction batches, and pre-indexed tables. |
| **Complex Persona Conflicts** | Medium | Medium | Implement automated schema validation checks in the seeder script to check data sanity and balance sheet calculations. |
| **AI Mock Synchronization** | High | Low | Lock contract schemas between simulation services and production adapters to prevent regression. |

---

### 8. Dependencies
*   **Sprint 1 Core Adapters**: Fully dependent on the dynamic `AdapterFactory` and integration profiles established in Sprint 1.
*   **Database Schema Compliance**: Seeding relies on the production SQLite tables (`aarohan_local.db`) remaining stable.

---

### 9. Deliverables
1.  **Extended Seeding Engine**: Updated `seed_all.py` generating scalable tenant datasets.
2.  **Dataset Marketplace Packages**: Complete MSME scenario catalogs packaged under `ese/datasets/`.
3.  **Dynamic Dashboard Service**: Expanded routes in `ese-admin-service` exposing aggregated executive metrics.
4.  **Journey Console Runners**: Programmatic scripts in the Admin API to trigger one-click journeys.
5.  **Sprint 2 Validation Suite**: Extensive tests demonstrating demographic expansions and scenario triggers.

---

### 10. Definition of Done (DoD)
*   All code conforms to the Project AAROHAN engineering standards.
*   Unit tests cover at least 90% of the newly added simulation and seeding code.
*   The database seeder executes referential validation checks without errors.
*   Regression tests for production pipelines remain completely green.
*   All endpoints are documented inside Swagger and verified via TestClient.

---

### 11. Sprint KPIs
*   **Seeding Execution Speed**: Under 3 seconds for 1,000+ customers.
*   **Namespace Crossover Isolation**: 0 namespace collisions between monorepo services.
*   **Demo API Response Time**: p95 latency under 150ms for simulated endpoints.

---

### 12. Demo Success Criteria
*   The presenter can switch between the "Excellent Borrower" and "Cash Flow Stress" scenarios via a single API call.
*   The Executive Dashboard renders instantly with realistic numbers matching the active profile.
*   Vertex AI mocks return detailed, sector-specific credit analysis matching the selected industry.

---

### 13. Expected Business Value
Sprint 2 unlocks the ability to show the product's full range of capabilities directly to stakeholders, credit committee members, and UAT testers using diverse, realistic data patterns, dramatically speeding up client onboarding and product sign-off.
