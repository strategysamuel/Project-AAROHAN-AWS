# AAR-BUILD-013: Enterprise MCA Simulation & Corporate Governance Intelligence Service Report

**Status:** **🟢 MCA SIMULATION SERVICE IMPLEMENTED – READY FOR FINANCIAL HEALTH CARD ENGINE**

---

### Components Added

1. **[providers.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/mca-service/app/providers.py)** — MCA Adapter Abstraction.
   - Defines unified `MCAAdapter` interface.
   - Implements `SimulationMCAAdapter` (queries corporate profiles, directors lists, and open/satisfied bank charges from the local onboarding databases), `SandboxMCAAdapter`, and `ProductionMCAAdapter`.
   - Supports runtime switching of providers through the `MCA_ADAPTER_PROFILE` config.

2. **[main.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/mca-service/app/main.py)** — Core REST Endpoints.
   - Handles establishment verification, director lookups, secure charges lists, annual return filings checks, governance score computations, and admin overrides.

3. **[models.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/mca-service/app/models.py)** — Database Tables.
   - Models `mca_company_profiles` (corporate identification details), `mca_directors` (DIN, board appointments), `mca_charges` (bank charges creation and amounts), `mca_company_filings` (AOC-4 and MGT-7 forms, delay days), `mca_financial_statements` (historical revenue, PAT, debt, net worth), and `mca_governance_analytics` (stores governance metrics and risk flags).

4. **[schemas.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/mca-service/app/schemas.py)** — Schema Validation.
   - Validates sync requests, director lists, charges, annual returns, and override bodies.

5. **[MCAPage.tsx](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/apps/customer-portal/src/pages/MCAPage.tsx)** — React UI Dashboard.
   - Provides company details card, board of directors list, filing history, secure charges table, financial statements, and compliance scoring gauges.

6. **[test_mca.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/mca-service/tests/test_mca.py)** — Integration testing script.

---

### APIs Implemented

| Method | Path | Description |
|---|---|---|
| POST | `/mca/sync/{customer_id}` | Imports corporate profiles, directors, charges, filings, and financials. Calculates governance analytics. |
| GET | `/mca/profile/{customer_id}` | Returns basic company profile. |
| GET | `/mca/directors/{customer_id}` | Retrieves Board of Directors list. |
| GET | `/mca/charges/{customer_id}` | Retrieves secure bank charges and creation dates. |
| GET | `/mca/filings/{customer_id}` | Returns statutory annual return filing status logs. |
| GET | `/mca/financials/{customer_id}` | Retrieves 3-year annual financials (revenue, PAT, debt, net worth). |
| GET | `/mca/analytics/{customer_id}` | Fetches corporate governance scores and risk categories. |
| POST | `/mca/analytics/{customer_id}/re-run` | Re-evaluates governance analytics and financial trends. |
| POST | `/mca/override/{customer_id}` | [Administrator] Overrides corporate governance scores with RM signatures. |
| POST | `/mca/reset` | Resets all synced profiles, directors, filings, and statement records. |

---

### Dataset Integration

- Syncs data directly from onboarding customer and business databases.
- Extracts registered office, Registrar of Companies (ROC) region, capitalization levels, board of directors, and open secured debt records.

---

### Corporate Analytics

Calculates:
- **Company Age:** Based on incorporation date.
- **Filing Consistency:** Verification of statutory AOC-4 and MGT-7 filings.
- **Director Stability:** Verifies board continuity and detects disqualified status.
- **Financial Trends:** Compares last two years of financials to identify Net Worth, Revenue, Profit, and Debt trends.

---

### Compliance Engine

Detects:
- **Late Annual Returns:** Verifies delayed filings.
- **Missing Filings:** Triggers alert if AOC-4 or MGT-7 is missing.
- **Director Disqualification:** Simulation checks.
- **Excessive Charges:** Triggers warning if open charges exceed authorized capital.
- **Overall MCA Compliance Score (0–100):** Starting at 100 with penalties for delayed filings.

---

### AI Corporate Insights

Generates narrative insights:
- *Strong governance practices.*
- *Timely statutory filings.*
- *Stable board of directors.*
- *Excellent long-term corporate stability.*

---

### Workflow Integration & Business Events

Dispatches ESE Core event signals:
- `MCA Verification Started`
- `Company Profile Retrieved`
- `Compliance Calculated`
- `Governance Analysis Completed`
- `Corporate Risk Updated`
- `MCA Verification Completed`

---

### Test Results

Integration checks executed:
- `test_cin_validation_error` — **PASS**
- `test_mca_sync_and_retrieval` — **PASS**
