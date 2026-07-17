# AAR-BUILD-010: Enterprise GSTN Simulation & Business Financial Analysis Service Report

**Status:** **🟢 GSTN SIMULATION SERVICE IMPLEMENTED – READY FOR ACCOUNT AGGREGATOR INTEGRATION**

---

### Components Added

1. **[providers.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/gst-service/app/providers.py)** — GSTN Adapter Interface.
   - Defines unified adapter contract `GSTNAdapter`.
   - Implements `SimulationGSTNAdapter` (queries onboarding & `ese_gst_records` from the shared local database), `SandboxGSTNAdapter` (offline test), and `ProductionGSTNAdapter` (production integration API stub).
   - Allows configuration-based switching via environment variable `GST_ADAPTER_PROFILE`.

2. **[main.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/gst-service/app/main.py)** — Microservice Endpoints.
   - Hosts REST endpoints for profile sync, return history fetches, annual summaries, re-running spreading analytics, and admin overrides.

3. **[models.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/gst-service/app/models.py)** — Database Tables.
   - Maps `gst_profiles`, `gst_returns` (stores sales, purchases, tax paid, input tax credit, delays), and `gst_analytics` (stores average turnover, growth rates, stability, volatility, working capital estimates, and risk flags).

4. **[schemas.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/gst-service/app/schemas.py)** — Schema Validation Models.
   - Handles Pydantic validation for return records, analytics metrics, and risk override requests.

5. **[GSTPage.tsx](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/apps/customer-portal/src/pages/GSTPage.tsx)** — Business Financial Analysis & Spreading Dashboard.
   - Includes monthly turnover trends, seasonality chart, return filing grids, compliance timeline logs, AI narrative insights console, and override dialogs.

6. **[test_gst.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/gst-service/tests/test_gst.py)** — Validation and analytics calculation checks.

---

### APIs Implemented

| Method | Path | Description |
|---|---|---|
| POST | `/gst/sync/{customer_id}` | Ingests return history, maps profiles, calculates compliance scores, and computes financial metrics. |
| GET | `/gst/profile/{customer_id}` | Returns basic registration profile details. |
| GET | `/gst/returns/{customer_id}` | Retrieves Return history list for GSTR-1 and GSTR-3B filings. |
| GET | `/gst/returns/{customer_id}/gstr1` | Returns list of GSTR-1 returns. |
| GET | `/gst/returns/{customer_id}/gstr3b` | Returns list of GSTR-3B returns. |
| GET | `/gst/returns/{customer_id}/annual` | Aggregates GSTR-1 filings to calculate annual sales, purchases, tax liability, and total ITC. |
| GET | `/gst/analytics/{customer_id}` | Fetches spreading calculations, volatility, risk levels, and AI narrative insights. |
| POST | `/gst/analytics/{customer_id}/re-run` | Re-evaluates compliance calculations and financial insights. |
| POST | `/gst/override/{customer_id}` | [Administrator] Overrides the business risk classification with comments and RM signatures. |
| POST | `/gst/reset` | Resets all synced profiles and return records. |

---

### Dataset Integration

- Fetches data directly from `ese_gst_records` within the shared development dataset (`aarohan_local.db`).
- Extracts business registration fields, constitution type, filing frequency, and return filing history (gross turnover, purchases, tax paid, and delays).

---

### Financial Analytics

The analytical engine dynamically computes:
- **Monthly Revenue:** Sales trends derived from GSTR-1 gross turnover.
- **Average Monthly Turnover:** Sum of GSTR-1 turnover divided by filing months.
- **MoM Revenue Growth Rate:** Mean MoM growth change percentage.
- **Seasonality Index:** Max turnover / min turnover.
- **Working Capital Estimate:** Annualized operating margin estimate.
- **Revenue Volatility:** Coefficient of variation (Std Dev / Mean).
- **Business Stability Score:** Percentage representation of revenue consistency.

---

### Compliance Engine

Monitors:
- **Late Filings:** Detects filing date delays.
- **Non-Filers:** Flags missing filings.
- **Nil Returns:** Flags tax periods with zero sales.
- **Return Mismatches:** Discrepancy > 5% between GSTR-1 and GSTR-3B gross sales.
- **Sudden Revenue Drop:** Revenue drop > 50% comparing last 3 months vs previous 3 months.
- **Suspicious Behaviour:** Checks for repeated consecutive delays or nil returns.
- **Inactive / Cancelled states.**

- **Overall Compliance Score (0–100):** Percentage of tax returns filed on time.
- **Risk Levels Assigned:** `Low`, `Medium`, `High`, `Critical` based on compliance anomalies.

---

### Business Events

Publishes the following events to the central ESE Core event engine:
- **`GST Verification Started`** — Dispatched on starting tax profile sync.
- **`GST Verification Completed`** — Dispatched on successful sync and spreading.
- **`Compliance Calculated`** — Dispatched with the final compliance score.
- **`Financial Analysis Completed`** — Dispatched with Average turnover and Working Capital metrics.
- **`High Risk Identified`** — Dispatched if risk level escalates to High or Critical.
- **`GST Analysis Failed`** — Dispatched on data mismatch or computation errors.

---

### Test Results

All service integration tests completed successfully:
- `test_gst_validation_error` — **PASS**
- `test_gst_sync_and_analytics` — **PASS**
