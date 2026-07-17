# AAR-BUILD-008: Enterprise Customer Onboarding Module Report

**Status:** **🟢 CUSTOMER ONBOARDING MODULE IMPLEMENTED – READY FOR CKYC INTEGRATION**

---

### Components Added

1. **[CustomerOnboardingPage.tsx](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/apps/customer-portal/src/pages/CustomerOnboardingPage.tsx)** — Onboarding wizard frontend component.
   - Handles multi-step registration (6 stages: Persona Selection, Customer Registration, Business Registration, validation, document upload, dashboard view).
   - Fully integrated with the FastAPI backend validation, document upload, and workflow initiation APIs.
   
2. **[main.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/onboarding-service/app/main.py)** — Onboarding Backend Controller.
   - Hosts endpoints for registration `/customers`, list `/customers`, update `/customers/{id}`, validation `/customers/validate`, persona loading `/customers/load-persona`, document upload `/customers/{id}/documents`, and workflow launch `/customers/{id}/start-workflow`.

3. **[models.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/onboarding-service/app/models.py)** — SQLAlchemy Database Models.
   - Defines schemas for `onboarding_customers`, `onboarding_businesses`, `onboarding_directors`, `onboarding_addresses`, and `onboarding_documents`.

4. **[schemas.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/onboarding-service/app/schemas.py)** — Pydantic Validation schemas.
   - Enforces formatting for Indian registry entities (PAN, GSTIN, Aadhaar, Mobile, Email, Pincode).

5. **[test_onboarding_module.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/tests/test_onboarding_module.py)** — 19-case automated validation and workflow integration test suite.

---

### APIs Added

| Method | Path | Description |
|---|---|---|
| POST | `/customers` | Register a new MSME customer profile, addresses, and businesses. Enforces uniqueness. |
| GET | `/customers` | List or search registered customers with optional limit, offset, and query filters. |
| GET | `/customers/{id}` | Retrieve profile details for a specific customer. |
| PUT | `/customers/{id}` | Update core customer information. |
| DELETE | `/customers/{id}` | Soft delete customer profile. |
| POST | `/customers/load-persona` | Auto-populate forms from ESE dataset (e.g., Priya Textile Works, GreenAgro, QuickLogistics). |
| POST | `/customers/validate` | Dry-run validation of fields and duplicate checks (PAN, mobile, GSTIN). |
| POST | `/customers/{id}/documents` | Upload/link a simulated document (PAN, Aadhaar, GST, Udyam, Statements) to a customer profile. |
| GET | `/customers/{id}/documents` | List uploaded/linked documents. |
| POST | `/customers/{id}/start-workflow` | Publish events and launch the "MSME Lending Journey" workflow orchestrator. |

---

### Database Changes

- **Table:** `onboarding_customers`
  - Stores customer details (legal_name, mobile_number, email, pan, aadhaar_masked, district, workflow_id, persona_name, onboarding_status, active, deleted flags).
- **Table:** `onboarding_businesses`
  - Stores MSME business details (trade_name, gstin, udyam_number, cin, constitution_type, annual_turnover, industry_segment, business_vintage_years, employee_count, existing_banking, lifecycle_state).
- **Table:** `onboarding_directors`
  - Maps proprietors/directors (full_name, pan, aadhaar_masked, mobile).
- **Table:** `onboarding_addresses`
  - Stores location details (address_line1, city, state, pincode, type).
- **Table:** `onboarding_documents`
  - Tracks uploads (doc_type, doc_name, source, status, timestamp).

---

### UI Pages

- **Customer List / Search Dashboard** — Search, view, and filter existing customer records.
- **New Customer Onboarding Wizard** — Multi-step wizard layout for registering new applicants.
- **Business Profile Form** — Input parameters for trade name, GSTIN, UDYAM, CIN, vintage, and financial turnover.
- **Document Manager Panel** — Toggle document uploads or select records directly from the Simulation Dataset.
- **Orchestration Status Dashboard** — Tracks active workflow logs, timeline progression, and risk profile.

---

### Workflow Integration

- Successful onboarding publishes:
  1. `Customer Registered`
  2. `Business Registered`
  3. `Workflow Started`
- Instantiates a new workflow instance in the ESE Core engine under the template name **"MSME Lending Journey"**.

---

### Test Results

All 19 test cases in the onboarding module test suite passed successfully:

- `test_register_customer` — **PASS**
- `test_customer_list` — **PASS**
- `test_customer_get_by_id` — **PASS**
- `test_business_udyam_field` — **PASS**
- `test_validate_valid_customer` — **PASS**
- `test_validate_invalid_pan` — **PASS**
- `test_validate_invalid_mobile` — **PASS**
- `test_duplicate_pan_rejected` — **PASS**
- `test_duplicate_detection_via_validate` — **PASS**
- `test_load_persona_priya` — **PASS**
- `test_load_persona_not_found` — **PASS**
- `test_upload_document` — **PASS**
- `test_upload_document_from_dataset` — **PASS**
- `test_list_documents` — **PASS**
- `test_start_workflow` — **PASS**
- `test_workflow_id_persisted` — **PASS**
- `test_update_customer` — **PASS**
- `test_delete_customer` — **PASS**
- `test_search_by_name` — **PASS**
