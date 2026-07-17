# AAR-BUILD-014: Enterprise Financial Health Card (FHC) Intelligence Engine Report

## Components Added
- **SQLAlchemy Database Models**: Extended `FinancialHealthCard` and `ScoreHistory` in [models.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/fhc-service/app/models.py) to store 14 financial dimensions, 10 sub-scores (value, weight, reasons, recommendations), rating grade, and administrative overrides/auditing trail.
- **Pydantic Validation Schemas**: Updated [schemas.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/fhc-service/app/schemas.py) with schemas for config updates, comparison inputs, score overrides, and serialized outputs including a backward-compatible validator for `fhc_score`.
- **API Router Controllers**: Rewrote [main.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/fhc-service/app/main.py) to process multi-source analytics data, compute overall scores, assign ratings, formulate explainability factors, publish lifecycle business events, and expose administration/configuration controllers.
- **Extended Test Suite**: Added [test_fhc_extended.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/fhc-service/tests/test_fhc_extended.py) to cover lifecycle validation, configuration adjustments, and exports.

## APIs Implemented
1. **POST `/fhc/calculate/{customer_id}`** / **POST `/fhc/generate/{customer_id}`**: Consolidation calculations.
2. **GET `/fhc/{customer_id}`**: Retrieves the current authoritative profile.
3. **POST `/fhc/refresh/{customer_id}`** / **POST `/fhc/recalculate/{customer_id}`**: Dynamic recalculation.
4. **GET `/fhc/history/{customer_id}`**: Retrieves chronological score logs.
5. **GET `/fhc/trend/{customer_id}`**: Computes monthly, quarterly, or yearly trajectory signals.
6. **POST `/fhc/compare`**: Parallel analysis across multiple customers.
7. **POST `/fhc/override/{customer_id}`**: Admin control surface to manually override scores with audit comments.
8. **GET `/fhc/config`** / **POST `/fhc/config`**: Dynamic adjustments to weighting rules and rating grade thresholds.
9. **GET `/fhc/export/{customer_id}`**: Downloads cards as PDF attachments or standard JSON schemas.

## Aggregated Services
Calculations directly reuse outputs stored in `aarohan_local.db` from:
- **Customer Onboarding** (`onboarding_customers`, `onboarding_businesses`)
- **CKYC** (`ckyc_records`, `ckyc_verification_logs`)
- **GST** (`gst_profiles`, `gst_analytics`)
- **Account Aggregator** (`aa_linked_accounts`, `aa_analytics`)
- **EPFO** (`epfo_profiles`, `epfo_analytics`)
- **MCA** (`mca_company_profiles`, `mca_governance_analytics`)

## Scoring Model & Rating Scale
### 10 Sub-Scores (Weighted Configurable Sum)
1. **Identity Score** (10%)
2. **Compliance Score** (10%)
3. **Liquidity Score** (15%)
4. **Revenue Score** (10%)
5. **Cash Flow Score** (15%)
6. **Business Stability Score** (10%)
7. **Governance Score** (5%)
8. **Workforce Score** (5%)
9. **Banking Behaviour Score** (10%)
10. **Growth Score** (10%)

### Rating Grade Thresholds
- **AAA**: $\ge$ 90.0
- **AA**: $\ge$ 80.0
- **A**: $\ge$ 70.0
- **BBB**: $\ge$ 60.0
- **BB**: $\ge$ 50.0
- **B**: $\ge$ 40.0
- **CCC**: $\ge$ 30.0
- **CC**: $\ge$ 20.0
- **C**: $\ge$ 10.0
- **D**: $<$ 10.0

## AI Explainability
Dynamically formulates explainability factors:
- **Strengths**: High compliance consistency, cash flow stability, board clean record.
- **Weaknesses**: Volatile sales margins, frequent overdraft triggers.
- **Opportunities**: Supply chain financing adoption, working capital enhancements.
- **Risk Factors**: High client revenue dependencies, low current account cash reserve.
- **Natural Language Summary**: Automated generation of text summaries indicating overall risk standing.

## Dashboard Components (Data Provided via API)
The APIs expose structures ready for front-end rendering:
- **Score Gauge**: `overall_score`
- **Sub-score Cards**: 10 distinct sub-scores with value, weight, reason, and recommendation.
- **Trend Charts**: Historical arrays formatted by group interval (Monthly/Quarterly/Yearly).
- **Risk Radar**: 14 financial dimensions mapped to $0\text{--}100$ ranges.
- **Explainability Panels**: Structured lists of strengths, weaknesses, opportunities, and risks.

## Workflow Integration
- Initiated directly as step 7 of the **MSME Lending Journey** via the [Workflow Orchestrator](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/workflow_engine.py).
- Consumed downstream by the **AI Credit Engine**, **RBI Fraud Registry**, **OCEN Marketplace**, **CAM Generator**, and **Executive Dashboards**.

## Business Events Published
Dispatched through `BusinessEventEngine` to notify downstream modules:
- `Financial Health Generated`: On first FHC creation.
- `Financial Health Updated`: On scoring refresh.
- `Score Changed`: When score deviates from previous calculated log.
- `Risk Increased`: Triggered if score drops.
- `Risk Reduced`: Triggered if score improves.
- `FHC_RECALCULATED`: Cascade trigger for credit-score updates.

## Test Results
Ran `pytest services/fhc-service/tests/` verifying all integration points:
```
collected 2 items

services\fhc-service\tests\test_fhc.py .                                 [ 50%]
services\fhc-service\tests\test_fhc_extended.py .                        [100%]

============================== 2 passed in 5.38s ==============================
```
