# AAR-BUILD-009: Enterprise CKYC Simulation & Identity Verification Service Report

**Status:** **🟢 CKYC SIMULATION SERVICE IMPLEMENTED – READY FOR GSTN INTEGRATION**

---

### Components Added

1. **[adapters.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ckyc-service/app/adapters.py)** — CKYC Adapter Interface.
   - Defines standard interface `CKYCAdapter` for fetching registry records.
   - Implements `DemoDatasetAdapter` (pulls from ESE local simulation database), `SandboxCKYCAdapter` (mock test), and `RealCKYCAdapter` (production integration API stub).
   - Allows configuration-based switching via environment variable `CKYC_ADAPTER_PROFILE`.

2. **[main.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ckyc-service/app/main.py)** — REST API Controller.
   - Core identity verification checks, confidence score computation (0-100), risk indicators detection, admin overrides, manual review queue, and statistics dashboard APIs.

3. **[models.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ckyc-service/app/models.py)** — Database Models.
   - Maps CKYC schema tables `ckyc_records`, `ckyc_verification_logs`, and provides direct SQLAlchemy bindings to shared onboarding customer and address tables.

4. **[schemas.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ckyc-service/app/schemas.py)** — Pydantic validation structures.
   - Validates requests/responses, override sign-offs, and simulation records.

5. **[CKYCPage.tsx](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/apps/customer-portal/src/pages/CKYCPage.tsx)** — CKYC Admin & Review Dashboard.
   - Features real-time statistics dashboard, manual review queue, PAN search console, identity confidence score widget, detailed risk analysis, override dialog, and audit report exporter.

6. **[test_ckyc.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ckyc-service/tests/test_ckyc.py)** — Automated test suite verifying validation checks, registry search, confidence metrics, and verification logs.

---

### APIs Implemented

| Method | Path | Description |
|---|---|---|
| GET | `/ckyc/stats` | Returns aggregated count of verification statuses for dashboard visualization. |
| POST | `/ckyc/search` | Queries registry using active adapter and fetches or initializes the CKYC record. |
| POST | `/ckyc/records` | [Simulation Admin] Creates a new simulated CKYC record. |
| PUT | `/ckyc/records/{customer_id}` | [Simulation Admin] Updates fields on a simulated CKYC record. |
| GET | `/ckyc/records/{customer_id}` | Fetches synced CKYC profile details for a customer. |
| POST | `/ckyc/verify/{customer_id}` | Performs identity match checks, computes confidence score, generates risk indicators, and sets status outcome. |
| GET | `/ckyc/verification-logs` | Retrieves full verification audit history. |
| GET | `/ckyc/manual-queue` | Lists all pending logs flagged for `MANUAL REVIEW`. |
| POST | `/ckyc/override/{log_id}` | [Administrator] Sign-off override for manual review, updating status, audited by, and comments. |

---

### Database/Dataset Usage

- **Tables Used:**
  - `ckyc_records`: Stores CKYC number, masked Aadhaar, PAN, name, DOB, address, email, mobile, and sync status.
  - `ckyc_verification_logs`: Tracks confidence score, anomalies, specific risk indicators, verified date, and comments.
  - `onboarding_customers` & `onboarding_addresses`: Accessed directly to perform comparisons.
  - `ese_ckyc_records`: Shared central ESE dataset query source when `DemoDatasetAdapter` is enabled.

---

### Workflow Integration

- Onboarding completion calls `/ckyc/verify/{customer_id}` to verify the applicant's identity.
- Outbound event cascade:
  - Outcome: `VERIFIED` / `VERIFIED WITH WARNING` $\rightarrow$ Proceeds workflow to **GST Analysis**.
  - Outcome: `FAILED` / `DATA MISMATCH` $\rightarrow$ Pauses lending workflow.
  - Outcome: `MANUAL REVIEW` $\rightarrow$ Enqueues verification record to the admin manual review queue.

---

### Events Published

- **`CKYC Verification Started`** — Dispatched at start of comparative matching.
- **`CKYC Verification Completed`** — Dispatched on successful outcome matching or override approval.
- **`CKYC Verification Failed`** — Dispatched on validation error or matching score below fail threshold.
- **`Manual Review Required`** — Dispatched when record needs manual override/sign-off.

---

### UI Pages

- **Registry Search Console** — Input PAN to search and view CKYC profiles.
- **Confidence Score Widget** — Displays matching confidence percentage (0-100) and indicators.
- **Manual Review Queue Panel** — Shows exception cases, allowing administrators to approve overrides.
- **Audit History Log Table** — Monospaced audit details with CSV report export functionality.

---

### Test Results

All service integration tests completed successfully:
- `test_search_validation_error` — **PASS**
- `test_ckyc_search_and_verify` — **PASS**
