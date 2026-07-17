# AAR-BUILD-015: Enterprise AI Credit Decision & Explainable Lending Engine Report

## Components Added
- **SQLAlchemy Database Models**: Extended `AICreditDecision`, `HumanApprovalLog`, and `CreditEngineConfig` in [models.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/credit-engine/app/models.py) to handle credit recommendation parameters, explainability factors, rule settings, adapter config, and RBI blacklist attributes.
- **Pydantic Validation Schemas**: Updated [schemas.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/credit-engine/app/schemas.py) with schemas for dynamic configuration, evaluation updates, comparisons, and list attribute field validators.
- **API Router Controllers**: Rewrote [main.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/credit-engine/app/main.py) to manage the decision engine workflow, human approvals, admin overrides, configuration parameters, and exports.
- **Adapter Model Framework**: Added [adapters.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/credit-engine/app/adapters.py) implementing the adapter pattern separating scoring/rules evaluation from underlying engine integrations (Rule Engine, Vertex AI, Custom ML, and OpenAI/LLM).
- **Extended Test Suite**: Added [test_credit_extended.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/credit-engine/tests/test_credit_extended.py) to verify dynamic rule calculations, parameters updates, adapter switching, and report exports.

## APIs Implemented
1. **POST `/credit/evaluate/{customer_id}`** / **POST `/credit/generate/{customer_id}`**: Consolidation calculations and AI underwriter appraisal.
2. **POST `/credit/evaluate`**: Body-payload structured evaluation.
3. **GET `/credit/decision/{customer_id}`** / **GET `/credit/decisions/{customer_id}`**: Retrieves current/historical credit decisions.
4. **POST `/credit/recalculate/{customer_id}`** / **POST `/credit/refresh/{customer_id}`**: Force recalculates credit decisions.
5. **GET `/credit/history/{customer_id}`**: Historical credit decision logs.
6. **POST `/credit/compare`**: Compares decision results across multiple customer IDs.
7. **POST `/credit/approve/{decision_id}`**: Approves decision status via human-in-the-loop underwriter credentials.
8. **GET `/credit/config`** / **POST `/credit/config`**: Dynamic rule parameter settings, risk thresholds, and active model adapter switching.
9. **GET `/credit/export/{customer_id}`**: Downloads credit memorandum files as PDF attachments or standard JSON schemas.

## Decision Rules
Configurable parameters include:
- **Identity Trust Check**: Trigger `Manual Review` if `identity_score < identity_threshold` (default: 80).
- **FHC Score Check**: Trigger `Reject` if `overall_score < 50`.
- **Cash Flow Balance Rule**: Deduct 30% from the eligible loan amount if cash flow is declining.
- **Compliance Rules**: Elevate risk grade to `High` if GST compliance score falls below 70.
- **Cheque Bounce Rules**: Apply a score penalty (default: 20 points) if bounces are detected.

## Scoring Model
Produces decision attributes:
- **Confidence Score**: Model confidence ($0\text{--}100$).
- **Decision Score**: Consolidated decision rating ($0\text{--}100$).
- **Risk Grade**: Grade level (`Low`, `Medium`, `High`, `Critical`).
- **Approval Probability**: Probability grade ($0.0$ to $1.0$).

## Explainability Features
Exposes key reasoning panels:
- **Top Positive Factors**: Structured indicators like high FHC standing, clean corporate status, strong cash flows.
- **Top Negative Factors**: Critical alerts like overdraft usage, cheque bounces, or short history vintage.
- **Risk Drivers**: Primary negative metrics triggering risk grade elevation.
- **Decision Explanation**: Narrative breakdown explaining underwriting reasons.
- **Recommended Actions**: Clear banker instructions for credit execution.

## Loan Recommendation Logic
Generates credit offers:
- **Eligible Loan Amount**: Dynamic limit determined by turnover stability and debt-service capacity.
- **Recommended Product**: Custom product assignment (e.g. Unsecured Working Capital Limit).
- **Recommended Tenure**: Period range ($12\text{--}36$ months).
- **Recommended Interest Rate**: Base rate adjusted by risk grade ($9.8\%\text{--}12.5\%$).
- **Collateral Recommendation**: CGTMSE cover or hypothecation requirements.
- **EMI Estimate**: Computed repayment burden.

## Workflow Integration
- Executes automatically downstream of **Financial Health Card** generation.
- Feeds credit data into **RBI Central Fraud Registry**, **OCEN Marketplace**, **CAM Generator**, and **Executive Dashboards**.

## Business Events Published
Dispatched through `BusinessEventEngine` to notify downstream modules:
- `Credit Evaluation Started`: On trigger.
- `Credit Score Calculated`: When composite decision score is finalized.
- `Decision Generated`: When underwriting recommendation is formulated.
- `Manual Review Required`: Triggered when parameters mandate human auditing.
- `Decision Approved`: On underwriter approval.
- `Decision Rejected`: On decision rejection.

## Test Results
Ran `pytest services/credit-engine/tests/` verifying all integration points:
```
collected 2 items

services\credit-engine\tests\test_credit.py .                            [ 50%]
services\credit-engine\tests\test_credit_extended.py .                   [100%]

============================== 2 passed in 5.25s ==============================
```
