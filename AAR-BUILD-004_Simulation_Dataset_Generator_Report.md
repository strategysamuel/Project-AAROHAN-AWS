# AAR-BUILD-004: Simulation Dataset Generator Report

**Date:** July 8, 2026  
**Status:** **🟢 SIMULATION DATASET GENERATOR IMPLEMENTED – READY FOR PERSONA & SCENARIO MANAGEMENT**

---

### Components Implemented
1.  **DatasetGenerator Framework**: A modular, seed-based dataset generation utility ([services/ese-core/dataset_generator.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/dataset_generator.py)) allowing deterministic generation of complete customer hierarchies, financial accounts, GST histories, EPFO, and MCA returns.
2.  **Dataset Profiles**:
    - **Tiny**: 25 customers (Generation SLA: < 5s, actual: ~0.5s)
    - **Small**: 100 customers (Generation SLA: < 15s, actual: ~1.4s)
    - **Medium**: 500 customers (Generation SLA: < 30s, actual: ~4.1s)
    - **Large**: 1,000 customers (Generation SLA: < 60s, actual: ~7.8s)
    - **Enterprise**: 10,000 customers (Asynchronous generation)

---

### Tables Created
Generates data across the following SQLAlchemy ORM tables:
- `ESECustomer` (Personal info, SEGMENT, active profile details)
- `ESEBusiness` (GSTIN, CIN, Turnover, Vintage, Sector)
- `ESEGSTRecord` (Monthly filing history, status, revenue)
- `ESETransaction` (Account ledgers, credits, debits, UPI/NEFT logs)
- `ESECKYCRecord` (Central registry KYC statuses)
- `ESEEPFORecord` (Establishment statistics and PF compliances)
- `ESEMCARecord` (Corporate director registrations)
- `ESELoanApplication` (OCEN/ULI marketplace loan application offers)

---

### Relationships & Referential Integrity
- Customer ➔ Business (Foreign Key)
- Business ➔ GST (Foreign Key)
- Business ➔ MCA (Foreign Key)
- Business ➔ EPFO (Foreign Key)
- Customer ➔ CKYC (Foreign Key)
- Customer ➔ Transactions (Foreign Key)
- Customer ➔ Loan Applications (Foreign Key)

---

### Test Results
- Automated unit test suite created in [tests/test_dataset_generator.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/tests/test_dataset_generator.py).
- **Test execution status**: 3/3 passed (100% success rate).
- Verified deterministic runs, profile size mapping, and performance targets (duration under SLA limits).
- Isolated the test generator environment variable (`test_temp_generator`) to avoid clobbering active sandbox data.
