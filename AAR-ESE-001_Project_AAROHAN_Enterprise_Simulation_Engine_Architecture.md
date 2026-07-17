# AAR-ESE-001: Project AAROHAN Enterprise Simulation Engine (ESE) v1.0 Architecture

**Document Classification**: Enterprise Architecture & Product Strategy  
**Version**: 1.0  
**Status**: 🟢 APPROVED FOR DESIGN  
**Date**: 2026-07-08  
**Platform**: Project AAROHAN — Companion Platform  
**Confidentiality**: IDBI Bank Internal

---

## 1. Executive Summary

The **Enterprise Simulation Engine (ESE)** is a strategic companion platform to **Project AAROHAN v1.1.0** that delivers a fully self-contained, production-like Digital Public Infrastructure (DPI) ecosystem. The ESE preserves the entire production microservice architecture and business logic while replacing all external integrations with realistic, deterministic simulation adapters.

The ESE enables four high-value use cases without requiring access to live RBI, GSTN, CKYC, or banking APIs:
* **Enterprise Demonstrations** — One-click end-to-end banking journeys for executive and investor audiences
* **Hackathon & Competition Presentations** — Safe, scripted, always-available simulation environment
* **Product Training** — Realistic MSME lending workflows for credit officers and relationship managers
* **Integration Sandbox** — External partner integration testing against stable, predictable API responses

The ESE is not a Version 1.2 feature — it is a parallel-track platform that shares the Version 1.1 codebase and can be deployed and operated completely independently.

---

## 2. Vision & Objectives

### 2.1 Vision

> *"A banking executive should be able to walk into a boardroom anywhere in India, open a laptop, and demonstrate a complete AI-powered MSME credit journey — from PAN entry to loan disbursement — in under five minutes, with no internet connectivity required."*

### 2.2 Objectives

| Objective | Success Metric |
| :--- | :--- |
| Zero external API dependencies in simulation mode | 100% offline capability |
| Preserve production business logic exactly | Zero changes to core service code |
| Support multiple concurrent demo personas | ≥ 13 predefined MSME borrower scenarios |
| Enable one-click scenario execution | < 30 seconds per scenario launch |
| Support hackathon multi-team environments | ≥ 20 concurrent demo sessions |
| Provide realistic AI-generated narratives | Vertex AI Gemini integration in Demo Mode |
| Enable rapid dataset reset | < 60 seconds for full dataset reset |

---

## 3. Business Justification

| Stakeholder | Value Delivered |
| :--- | :--- |
| **Banking Executives** | Risk-free demonstration with realistic data; no dependency on production systems |
| **Sales & Presales Teams** | Always-available demo environment; scriptable journeys for client pitches |
| **Hackathon Participants** | Safe sandbox to build integrations without touching production APIs |
| **Training Departments** | Repeatable, controllable training scenarios with known outcomes |
| **Compliance Teams** | UAT execution against a stable, isolated environment |
| **AI Research Teams** | Controlled experimentation with credit models and prompt engineering |
| **IDBI Bank Leadership** | Showcase regulatory compliance (RBI fraud, OCEN, CKYC) to regulators |

---

## 4. Enterprise Simulation Engine Overview

### 4.1 What the ESE IS

* A **deployment profile** of the existing AAROHAN microservices stack
* A **simulation adapter layer** that intercepts external API calls and returns realistic synthetic responses
* A **scenario engine** that seeds, scripts, and controls MSME customer journeys
* An **admin console** that manages datasets, modes, and resets
* A **demo journey library** of pre-scripted, one-click end-to-end demonstrations

### 4.2 What the ESE IS NOT

* It is NOT a separate codebase — it reuses all production service code
* It is NOT a mock server — simulation adapters produce stateful, consistent responses
* It is NOT a testing framework — it is a full-stack operational platform
* It is NOT Version 1.2 — it runs on v1.1.0 with zero feature additions

### 4.3 Relationship to Production

```
┌─────────────────────────────────────────────────────────┐
│                  PRODUCTION (v1.1.0)                    │
│  16 Microservices + Real GCP APIs + Live RBI/GSTN/AA   │
└─────────────────────────────────────────────────────────┘
              ↕  Shared business logic code
┌─────────────────────────────────────────────────────────┐
│          ENTERPRISE SIMULATION ENGINE (ESE v1.0)        │
│  16 Microservices + Simulation Adapters + Demo Console  │
└─────────────────────────────────────────────────────────┘
```

---

## 5. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                     ESE v1.0 — Platform Layers                       │
├──────────────────────────────────────────────────────────────────────┤
│  PRESENTATION LAYER                                                  │
│  ┌─────────────┐  ┌──────────────────┐  ┌─────────────────────────┐ │
│  │ Demo Portal │  │ RM Workspace UI  │  │ Admin Console           │ │
│  │ (Journey    │  │ (Training Mode)  │  │ (Dataset Management)    │ │
│  │  Library)   │  │                  │  │                         │ │
│  └─────────────┘  └──────────────────┘  └─────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────┤
│  API GATEWAY / ORCHESTRATION LAYER                                   │
│  Scenario Engine · Journey Controller · Mode Manager                │
├──────────────────────────────────────────────────────────────────────┤
│  BUSINESS LOGIC LAYER  (Unchanged Production Code)                   │
│  Onboarding · CKYC · GST · AA · FHC · Credit Engine · CAM          │
│  RM Workspace · Exec Dashboard · EWS · OCEN/ULI · TReDS · EPFO     │
├──────────────────────────────────────────────────────────────────────┤
│  SIMULATION ADAPTER LAYER                                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  CKYC    │ │  GSTN    │ │    AA    │ │  RBI FR  │ │ Vertex AI│  │
│  │ Adapter  │ │ Adapter  │ │ Adapter  │ │ Adapter  │ │ Adapter  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  EPFO    │ │   MCA    │ │   FHC    │ │   CAM    │ │ OCEN/ULI │  │
│  │ Adapter  │ │ Adapter  │ │ Adapter  │ │ Adapter  │ │ Adapter  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
├──────────────────────────────────────────────────────────────────────┤
│  SYNTHETIC DATASET LAYER                                             │
│  Customer Master · Transaction History · GST Returns · Fraud Cases  │
│  Bank Statements · Loan Portfolio · OCEN Lenders · RM Leads         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 6. Simulation Layer Design

### 6.1 Core Design Principles

* **Stateful Simulation**: Simulation adapters maintain state. A GSTN registered for Customer A returns consistent data across every call during a session.
* **Scenario-Bound Responses**: Adapter responses are seeded by the active Scenario profile, not random.
* **Deterministic Outcomes**: The same scenario always produces the same credit decision, enabling reliable demos.
* **Zero Code Change**: The ESE adapter layer is injected at the dependency injection level, requiring zero changes to service business logic.

### 6.2 Adapter Injection Mechanism

Each microservice uses a factory pattern for external API clients:

```
┌──────────────────────┐
│   Service Startup    │
│   reads ESE_MODE     │
│   environment var    │
└──────────┬───────────┘
           │
    ┌──────▼──────┐
    │ ESE_MODE =  │
    │ SIMULATION? │
    └──┬──────┬───┘
       │ Yes  │ No
       ▼      ▼
 Simulation  Production
  Adapter     Adapter
```

Environment variable `ESE_MODE` controls adapter selection:

| `ESE_MODE` Value | Adapter Loaded | Data Source |
| :---: | :---: | :--- |
| `SIMULATION` | SimulationAdapter | Synthetic dataset |
| `DEMO` | SimulationAdapter + Vertex AI | Synthetic data + Live AI narrative |
| `TRAINING` | SimulationAdapter (slow-mode) | Synthetic dataset |
| `PRODUCTION` | ProductionAdapter | Live external APIs |

---

## 7. Adapter Pattern Architecture

Every external integration exposes a common interface that is implemented by both adapters:

### 7.1 Adapter Interface Contract

```python
class ExternalIntegrationAdapter(ABC):
    """
    Base contract for all external integrations.
    Implemented by both SimulationAdapter and ProductionAdapter.
    Business logic calls ONLY this interface — never the adapter directly.
    """

    @abstractmethod
    async def fetch(self, request: AdapterRequest) -> AdapterResponse:
        """Fetch data from the external integration."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify the integration is reachable."""
        ...
```

### 7.2 Adapter Pair Pattern

For every external integration:

```
┌──────────────────────────────────┐
│  External Integration Interface  │
│  (e.g., CKYCAdapter)            │
└────────┬─────────────────────────┘
         │ implements
    ┌────┴──────────────────────┐
    │                           │
    ▼                           ▼
SimulationCKYCAdapter     ProductionCKYCAdapter
(reads from dataset)      (calls live CKYC API)
```

### 7.3 Adapter Registry

| Integration | SimulationAdapter | ProductionAdapter |
| :--- | :--- | :--- |
| CKYC | `SimulationCKYCAdapter` | `ProductionCKYCAdapter` |
| GSTN | `SimulationGSTNAdapter` | `ProductionGSTNAdapter` |
| Account Aggregator | `SimulationAAAdapter` | `ProductionAAAdapter` |
| RBI Fraud Registry | `SimulationFraudAdapter` | `ProductionFraudAdapter` |
| EPFO | `SimulationEPFOAdapter` | `ProductionEPFOAdapter` |
| MCA | `SimulationMCAAdapter` | `ProductionMCAAdapter` |
| Vertex AI (Gemini) | `SimulationGeminiAdapter` | `ProductionGeminiAdapter` |
| OCEN / ULI | `SimulationOCENAdapter` | `ProductionOCENAdapter` |
| CAM Generation | `SimulationCAMAdapter` | `ProductionCAMAdapter` |
| FHC Engine | `SimulationFHCAdapter` | `ProductionFHCAdapter` |

---

## 8. Simulation Modes

### 8.1 Demo Mode
**Purpose**: Executive presentations, sales demonstrations, investor showcases  
**Characteristics**:
* Vertex AI Gemini generates live, fresh AI narratives for each demo run
* All external integrations use simulation adapters with curated scenario data
* Pre-seeded dataset of 13 named MSME personas
* Admin console available for presenter to switch personas between sessions
* One-click journey library available

### 8.2 Training Mode
**Purpose**: Credit officer and RM onboarding training, product familiarization  
**Characteristics**:
* All external integrations use simulation adapters
* API response times artificially throttled to realistic latency ranges (300–800ms) for naturalistic training
* Trainee actions are logged for trainer review and assessment
* Dataset reset available at end of each training session
* Scenarios expose a broader range of edge cases (rejections, compliance failures, partial data)

### 8.3 Testing Mode
**Purpose**: UAT, integration testing, QA, hackathon team development sandboxes  
**Characteristics**:
* All external integrations use simulation adapters
* Deterministic, zero-latency responses for fast test execution
* Full API contract preserved — external partners can validate integrations
* Dataset reset via Admin Console or API endpoint
* Parallel session isolation — each team/test runner operates on an independent dataset namespace

### 8.4 Production Mode
**Purpose**: Live banking operations — IDBI Bank MSME Digital Lending  
**Characteristics**:
* All external integrations use Production Adapters
* Simulation layer is inactive
* Admin Console restricted to read-only operational views
* This mode is governed by the v1.1.0 BAU Operations Plan (`AAR-V11-BAU-001`)

---

## 9. Simulation Modules

### 9.1 CKYC Simulation Adapter
* **Data Source**: Synthetic CKYC records for all 50 customer personas
* **Response Fields**: `kycId`, `name`, `pan`, `aadhaar_masked`, `dob`, `address`, `kyc_status`
* **Scenarios Supported**: CLEAN, EXPIRED_KYC, INCOMPLETE_KYC
* **Latency (Demo Mode)**: 200–400ms simulated

### 9.2 GSTN Simulation Adapter
* **Data Source**: 12–36 months of synthetic GST filing history per customer
* **Response Fields**: `gstin`, `trade_name`, `filing_history[]`, `revenue_trend`, `gst_compliance_score`
* **Scenarios Supported**: HIGH_GROWTH, STABLE, SEASONAL, NON_COMPLIANT, FIRST_RETURN
* **Data Volume**: 6 monthly returns per customer minimum

### 9.3 Account Aggregator Simulation Adapter
* **Data Source**: 24-month synthetic bank statement with realistic MSME cash flow patterns
* **Response Fields**: `accounts[]`, `transactions[]`, `avg_monthly_inflow`, `avg_monthly_outflow`, `min_eod_balance`
* **Scenarios Supported**: STRONG_CASHFLOW, SEASONAL_CASHFLOW, STRESSED_CASHFLOW, NEW_ACCOUNT
* **Realism Features**: Salary runs, GST payments, EMI deductions, seasonal revenue spikes

### 9.4 Financial Health Card Simulation Adapter
* **Data Source**: Pre-computed FHC scores per scenario, derived from synthetic AA data
* **Response Fields**: `fhc_score`, `dscr`, `revenue_growth_pct`, `debt_burden_ratio`, `liquidity_ratio`
* **Scenarios Supported**: EXCELLENT (score 85–100), GOOD (65–84), MODERATE (45–64), WEAK (< 45)

### 9.5 Credit Engine Simulation Adapter
* **Data Source**: Scenario-bound credit decision outcomes
* **Response Fields**: `recommendation`, `confidence_score`, `ai_narrative`, `explainability_tags[]`, `policy_status`
* **Demo Mode**: Calls live Vertex AI Gemini for fresh narrative generation
* **Training/Testing Mode**: Returns pre-generated synthetic narratives
* **Scenarios Supported**: APPROVED, REJECTED, MANUAL_REVIEW

### 9.6 RBI Fraud Registry Simulation Adapter
* **Data Source**: Curated list of 5 blacklisted synthetic PANs seeded in the dataset
* **Response Fields**: `rbi_fraud_status`, `rbi_verification_log`
* **Blacklisted PANs**: `FRAUD0001F`, `FRAUD0002F`, `FRAUD0003F`, `FRAUD0004F`, `FRAUD0005F`
* **Scenarios Supported**: CLEAN, BLACKLISTED
* **Fraud Scenario Behavior**: Auto-rejection + CRITICAL SECURITY ALERT log (preserving production behavior)

### 9.7 EPFO Simulation Adapter
* **Data Source**: Synthetic employee strength and provident fund contribution history
* **Response Fields**: `epfo_id`, `employee_count`, `pf_contribution_months`, `compliance_status`
* **Scenarios Supported**: GROWING_WORKFORCE, STABLE, DECLINING, NON_COMPLIANT

### 9.8 MCA Simulation Adapter
* **Data Source**: Synthetic company registry records
* **Response Fields**: `cin`, `company_name`, `incorporation_date`, `directors[]`, `annual_returns_filed`
* **Scenarios Supported**: ACTIVE_COMPLIANT, ACTIVE_PENDING_FILING, DORMANT

### 9.9 OCEN / ULI Simulation Adapter
* **Data Source**: Synthetic OCEN lender pool (5 simulated lenders)
* **Response Fields**: `offer_id`, `lender_name`, `loan_amount`, `interest_rate`, `tenure_months`, `disbursement_status`
* **Scenarios Supported**: OFFER_AVAILABLE, OFFER_PENDING, DISBURSED, DECLINED

### 9.10 CAM Generation Simulation Adapter
* **Data Source**: Pre-structured CAM template with scenario-specific financial parameters
* **Demo Mode**: Vertex AI Gemini generates live CAM narrative
* **Training/Testing Mode**: Returns synthetic pre-generated CAM document
* **Output**: Full CAM document in JSON + PDF-ready Markdown format

### 9.11 Executive Dashboard Simulation Adapter
* **Data Source**: Portfolio-level synthetic KPIs aggregated from all customer scenarios
* **Response Fields**: Portfolio volume, approval rates, fraud matches, average FHC score, disbursement velocity
* **Refresh Simulation**: KPIs update dynamically as demo journeys are completed

### 9.12 Vertex AI Simulation Adapter
* **Demo Mode**: Routes to live Vertex AI Gemini API — real AI, synthetic financial data
* **Training/Testing Mode**: Returns curated, pre-generated AI narratives from a narrative library
* **Narrative Library**: 13 scenario-specific pre-generated credit narratives
* **Explainability Tags**: Hardcoded scenario-appropriate tags (e.g., `["DSCR_OK", "GST_GROWTH_STRONG"]`)

---

## 10. Dataset Strategy

### 10.1 Synthetic Dataset Composition

| Dataset | Count | Notes |
| :--- | :---: | :--- |
| MSME Customer Personas | 50 | 13 named scenarios + 37 supporting records |
| Business Entities | 50 | 1:1 with customer records |
| Loan Applications | 75 | Multiple applications per business (lifecycle) |
| GST Filing Records | 1,800 | 36 months × 50 customers |
| Bank Transactions | 60,000 | ~100 transactions × 24 months × 25 active accounts |
| Bank Accounts | 75 | ~1.5 accounts per customer |
| CKYC Records | 50 | One per customer |
| EPFO Records | 50 | One per business |
| MCA Corporate Records | 50 | One per business |
| Credit Decisions | 75 | Matching loan applications |
| AI Explainability Records | 75 | One per credit decision |
| Fraud Cases | 5 | Blacklisted PANs |
| OCEN Lenders | 5 | Simulated lender pool |
| TReDS Buyers | 10 | For trade finance scenarios |
| RM Leads | 50 | One per customer |
| EWS Watchlist Records | 10 | For distressed portfolio scenarios |

### 10.2 Dataset Realism Standards

* Bank transaction amounts are realistically scaled to MSME business size (INR 5L–50L monthly turnover).
* GST filing revenues are consistent with AA cash flows (within 15% variance to simulate real-world gaps).
* Employee counts (EPFO) are proportional to business type and revenue size.
* Credit decisions are scenario-deterministic — the same persona always receives the same outcome.

### 10.3 Dataset Namespacing

In Testing Mode, each team or test runner receives an isolated dataset namespace (e.g., `TEAM_A`, `TEAM_B`) to prevent cross-contamination in hackathon environments.

---

## 11. Scenario Engine

### 11.1 Scenario Definitions

| Scenario ID | Persona Name | Business Type | FHC Score | Credit Outcome | Special Condition |
| :--- | :--- | :--- | :---: | :---: | :--- |
| SCN-001 | Priya Textile Works | Apparel Manufacturer | 92 | APPROVED | Excellent — showcase scenario |
| SCN-002 | Ramesh Kirana Store | Retail — New to Credit | 58 | MANUAL_REVIEW | No credit history |
| SCN-003 | Sunrise Agri Seeds | Agribusiness | 72 | APPROVED | Seasonal revenue pattern |
| SCN-004 | Kavitha Exports Ltd | Exporter | 88 | APPROVED | Export income in USD |
| SCN-005 | TechBoost Solutions | IT Startup | 79 | APPROVED | High-growth, low asset base |
| SCN-006 | Mehta Traders | Wholesale — GST | 31 | REJECTED | GST non-compliance |
| SCN-007 | Buildwell Infra | Construction | 44 | REJECTED | EPFO defaults |
| SCN-008 | Raja Motors Pvt Ltd | Auto Dealership | N/A | REJECTED | RBI Fraud Blacklist |
| SCN-009 | Ananya Spices Co | Food Processing | 48 | MANUAL_REVIEW | Cash-flow stress |
| SCN-010 | Bharat Steel Works | Manufacturing | 81 | APPROVED | Asset-heavy MSME |
| SCN-011 | Shree Sweets | Retail Food | 67 | APPROVED | Steady retail |
| SCN-012 | Deepa Handicrafts | Women Entrepreneur | 85 | APPROVED | MUDRA eligible |
| SCN-013 | Green Valley Farms | Agri Enterprise | 74 | APPROVED | KCC integration |

### 11.2 Scenario Execution

* Each scenario is a structured JSON configuration specifying the CKYC, GSTN, AA, FHC, and credit adapter response parameters.
* Scenarios are activated by the Admin Console or Demo Journey Library with a single click.
* Scenario state is persisted for the duration of the session; reset via Admin Console or API.

---

## 12. AI Demonstration Framework

### 12.1 Demo Mode AI Generation

In Demo Mode, the ESE routes credit evaluation requests to live Vertex AI Gemini with synthetic financial data. The AI generates a fresh, contextually accurate credit narrative for every demonstration — avoiding repetitive pre-canned content while remaining safe (no real customer data is processed).

### 12.2 AI-Generated Artefacts

| Artefact | AI Generation | Example Output |
| :--- | :---: | :--- |
| Credit Decision Narrative | Live Gemini (Demo) / Pre-generated (Training) | 3-paragraph credit appraisal commentary |
| CAM Report | Live Gemini (Demo) / Template (Training) | Full Credit Appraisal Memorandum |
| Loan Recommendation Summary | Live Gemini | Single-paragraph recommendation with rationale |
| Risk Explanation | Pre-generated from tag vocabulary | Tag-based explanation mapped to human language |
| FHC Commentary | Pre-generated per FHC score range | Narrative interpreting DSCR and cash flow metrics |

### 12.3 Explainability Tag → Human Language Mapping

| Tag | Human Language |
| :--- | :--- |
| `DSCR_OK` | Debt Service Coverage Ratio is healthy — the business can comfortably service the proposed EMI. |
| `GST_GROWTH_STRONG` | GST filing history shows consistent revenue growth over the past 12 months. |
| `FHC_STRONG` | Financial Health Card score is in the excellent range, indicating strong financial management. |
| `RBI_FRAUD_BLACKLIST` | PAN is listed in the RBI Central Fraud Registry. Credit application auto-rejected. |
| `POLICY_VIOLATION` | Application has been blocked due to a regulatory compliance policy violation. |
| `CASH_FLOW_STRESSED` | Bank statement analysis shows periods of negative cash flow requiring further review. |
| `GST_NON_COMPLIANT` | GST filings are incomplete or show significant gaps in compliance. |
| `NEW_TO_CREDIT` | No prior credit history found. Manual review recommended for underwriting. |

---

## 13. Admin Console

### 13.1 Admin Console Capabilities

| Feature | Description |
| :--- | :--- |
| **Switch Mode** | Toggle between Demo / Training / Testing / Production modes |
| **Load Scenario** | Activate a named scenario (SCN-001 through SCN-013) |
| **Generate Customer** | Seed a new synthetic MSME customer with configurable parameters |
| **Reset Dataset** | Wipe and re-seed the entire synthetic dataset in < 60 seconds |
| **Reset Session** | Reset a single customer's journey without affecting others |
| **Inject Fraud Case** | Mark a specified customer PAN as RBI Fraud Blacklisted |
| **Trigger GST Default** | Set a customer's GST filing to non-compliant status |
| **Simulate Repayment** | Record synthetic EMI repayments to demonstrate portfolio aging |
| **Generate Loan Offers** | Create OCEN-compatible loan offers for a specified customer |
| **View Audit Logs** | Browse the complete audit trail for all AI credit decisions |
| **View Fraud Alerts** | Dashboard of all fraud registry matches in the current session |
| **Export Demo Report** | Generate a PDF summary of a completed demo journey |
| **Namespace Management** | Create, reset, or delete team namespaces (Testing Mode) |
| **AI Configuration** | Switch between Live Gemini and pre-generated narrative libraries |

### 13.2 Admin Console Access Control

| Role | Access Level |
| :--- | :---: |
| Super Admin (AAROHAN Team) | Full access — mode switching, dataset management |
| Demo Admin (IDBI Sales) | Scenario loading, session reset, audit log view |
| Trainer | Session reset, scenario loading |
| Read-Only | Audit logs and dashboard only |

---

## 14. Demo Journey Library

### 14.1 One-Click Demo Journeys

| Journey ID | Title | Scenarios Used | Duration | Highlights |
| :--- | :--- | :--- | :---: | :--- |
| DJ-001 | **The Perfect Borrower** | SCN-001 (Priya Textiles) | ~4 min | Onboarding → AI Approval → CAM → Disbursement |
| DJ-002 | **Fraud Registry in Action** | SCN-008 (Raja Motors) | ~2 min | Onboarding → Fraud Match → Auto-Reject → Alert |
| DJ-003 | **New-to-Credit MSME** | SCN-002 (Ramesh Kirana) | ~5 min | Onboarding → Manual Review → RM Workflow |
| DJ-004 | **Women Entrepreneur** | SCN-012 (Deepa Handicrafts) | ~4 min | MUDRA eligibility + DSCR + AI explainability |
| DJ-005 | **GST Compliance Failure** | SCN-006 (Mehta Traders) | ~3 min | GST gaps → AI tags → REJECTED decision |
| DJ-006 | **High-Growth Startup** | SCN-005 (TechBoost) | ~4 min | Rapid revenue growth → AI approval |
| DJ-007 | **Portfolio Overview** | All active scenarios | ~6 min | Executive Dashboard → EWS → Portfolio KPIs |
| DJ-008 | **Trade Finance** | SCN-010 (Bharat Steel) | ~4 min | TReDS invoice → factoring → disbursement |
| DJ-009 | **Seasonal Business** | SCN-003 (Sunrise Agri) | ~5 min | Seasonal cash flow → adjusted underwriting |
| DJ-010 | **Full MSME Lifecycle** | SCN-001 (Priya Textiles) | ~8 min | Registration → Disburse → EWS Monitoring |

### 14.2 Journey Controller

The Journey Controller is a step-sequenced orchestrator that pre-calls APIs in order and presents results in a guided UI flow. Presenters advance through steps at their own pace, with the option to pause, replay, or branch to related journeys.

---

## 15. Security Model

### 15.1 ESE Security Principles

* **Data Isolation**: No real customer data ever enters the ESE. All data is synthetic.
* **No PII**: Synthetic PAN numbers follow the format `SIMxxNNNNS` (distinct from valid PAN format), preventing accidental production use.
* **Environment Separation**: ESE is deployed in a dedicated GCP project with no network access to production GCP resources.
* **Authentication**: Admin Console access requires IDBI SSO authentication; API endpoints require JWT tokens.
* **Audit Logging**: All Admin Console actions are logged with user ID, timestamp, and action performed.
* **Hackathon Isolation**: Each team namespace is isolated at the database level; cross-namespace access is blocked.

### 15.2 Synthetic PAN Format

To prevent confusion with real PAN numbers, all ESE personas use synthetic PANs in the format:
`SIM[2 chars][4 digits][1 char]` — e.g., `SIMPT0001K`, `SIMRD0002X`

These do not match the valid ABCDE1234F PAN pattern and cannot be used in production systems.

---

## 16. Google Cloud Compatibility

| GCP Service | ESE Usage | Notes |
| :--- | :---: | :--- |
| **Cloud Run** | ✅ Full | All 16 services + Admin Console deployed on Cloud Run |
| **Vertex AI (Gemini)** | ✅ Demo Mode | Live AI narratives in Demo Mode; bypassed in Training/Testing |
| **Cloud Armor WAF** | ✅ Full | ESE environment protected by the same WAF policy |
| **Cloud Logging** | ✅ Full | All simulation events and audit logs captured |
| **Cloud Monitoring** | ✅ Full | Separate ESE monitoring dashboard |
| **Secret Manager** | ✅ Full | Simulation API keys stored separately from production secrets |
| **Pub/Sub** | ✅ Full | Event relay functional in all modes |
| **BigQuery** | ✅ Full | Demo analytics and audit log export |
| **Cloud Storage** | ✅ Full | Pre-generated CAM and narrative library stored in GCS bucket |

### ESE GCP Project Separation

| Concern | Production Project | ESE Project |
| :--- | :---: | :---: |
| GCP Project ID | `aarohan-prod` | `aarohan-ese` |
| VPC network | Isolated | Isolated |
| IAM service accounts | Production roles | ESE-specific roles |
| Vertex AI quota | Production allocation | Separate ESE allocation |
| Secret Manager | Production secrets | Synthetic credentials |

---

## 17. Migration Strategy

### 17.1 Adapter Graduation Path

The ESE adapter pattern defines a clear migration path from simulation to production for any future integration:

```
Stage 1: Simulation Adapter (ESE) — synthetic data, no external dependency
Stage 2: Stub Adapter — validates contract against staging API schema
Stage 3: Shadow Adapter — calls live API in parallel, validates response match
Stage 4: Production Adapter — live integration, simulation deprecated
```

### 17.2 Per-Integration Migration Readiness

| Integration | Current State | Production Readiness |
| :--- | :---: | :---: |
| CKYC | Stage 4 (Production) in v1.1 | ✅ Done |
| GSTN | Stage 4 (Production) in v1.1 | ✅ Done |
| Account Aggregator | Stage 4 (Production) in v1.1 | ✅ Done |
| Vertex AI | Stage 4 (Production) in v1.1 | ✅ Done |
| RBI Fraud Registry | Stage 1 (Simulation) — mock in v1.1 | V1.2 |
| OCEN / ULI | Stage 2 (Stub) in v1.1 | V1.2 |
| TReDS | Stage 2 (Stub) in v1.1 | V1.2 |

---

## 18. Future Roadmap

| Version | Planned Enhancements |
| :--- | :--- |
| **ESE v1.0** (Current) | 13 scenarios, 50-customer dataset, 10 demo journeys, Admin Console |
| **ESE v1.1** | Live RBI Fraud Registry integration in Demo Mode; 100-customer dataset |
| **ESE v1.2** | Multi-bank simulation (3 simulated AA banks); Loan repayment lifecycle |
| **ESE v2.0** | Generative AI scenario creation (new personas generated by Gemini); voice-driven demo mode |
| **ESE v2.1** | Regulator demonstration mode — RBI-facing audit-ready showcase |
| **ESE v3.0** | Multi-language demo journeys (Hindi, Tamil, Telugu) |

---

## 19. Executive Approval

| Role | Decision | Date |
| :--- | :---: | :---: |
| **Chief Product Officer** | ✅ APPROVED | 2026-07-08 |
| **Chief Technology Officer** | ✅ APPROVED | 2026-07-08 |
| **Enterprise Architect** | ✅ APPROVED | 2026-07-08 |
| **Principal Banking Solution Architect** | ✅ APPROVED | 2026-07-08 |
| **Google Cloud Principal Solutions Architect** | ✅ APPROVED | 2026-07-08 |
| **AI Platform Architect** | ✅ APPROVED | 2026-07-08 |
| **Banking Domain Expert** | ✅ APPROVED | 2026-07-08 |
| **Product Manager** | ✅ APPROVED | 2026-07-08 |

**Unanimous approval. ESE v1.0 architecture is approved for implementation planning.**

---

## 20. Appendix

### A. ESE v1.0 Microservice Inventory

| Service | ESE Port | Simulation Adapters |
| :--- | :---: | :--- |
| auth-service | 9000 | JWT (unchanged) |
| onboarding-service | 9001 | — (pure business logic) |
| consent-service | 9002 | SimulationAAAdapter |
| gst-service | 9003 | SimulationGSTNAdapter |
| aa-service | 9004 | SimulationAAAdapter |
| fhc-service | 9005 | SimulationFHCAdapter |
| credit-engine | 9006 | SimulationGeminiAdapter + SimulationFraudAdapter |
| cam-service | 9007 | SimulationCAMAdapter |
| rm-workspace-service | 9008 | — (pure business logic) |
| exec-service | 9009 | SimulationDashboardAdapter |
| ews-service | 9010 | — (pure business logic) |
| ckyc-service | 9011 | SimulationCKYCAdapter |
| mca-service | 9012 | SimulationMCAAdapter |
| epfo-service | 9013 | SimulationEPFOAdapter |
| treds-service | 9014 | SimulationOCENAdapter |
| ocen-uli-service | 9015 | SimulationOCENAdapter |
| **ese-admin-console** | **9099** | **New service — Admin Console** |

### B. ESE Implementation Phases

| Phase | Scope | Duration |
| :--- | :--- | :---: |
| Phase 1 | Adapter interface design + 3 core adapters (CKYC, GSTN, AA) | 1 sprint |
| Phase 2 | Remaining 9 adapters + synthetic dataset seeding | 1 sprint |
| Phase 3 | Scenario Engine + Admin Console | 1 sprint |
| Phase 4 | Demo Journey Library + Vertex AI Demo Mode integration | 1 sprint |
| Phase 5 | Hackathon namespace isolation + security hardening | 0.5 sprint |
| **Total** | | **~4.5 sprints** |

### C. Key Design Decisions

| Decision | Rationale |
| :--- | :--- |
| No production code changes | Adapter injection at startup preserves zero-diff production codebase |
| Separate GCP project | Prevents any possibility of ESE traffic reaching production resources |
| Synthetic PAN format | Prevents accidental use of ESE data in production workflows |
| Live Gemini in Demo Mode | Ensures AI narratives are fresh and contextually impressive for executive audiences |
| Scenario-bound determinism | Ensures demo outcomes are predictable and rehearsable |
