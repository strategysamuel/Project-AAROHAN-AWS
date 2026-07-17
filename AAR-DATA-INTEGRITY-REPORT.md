# Project AAROHAN - Data Integrity & Consistency Report

## Executive Summary
This report summarizes the data lineage and relational integrity fixes applied to the Project AAROHAN AWS Hackathon environment. The core issue was identified as isolated application state across microservices, resulting in disjointed records. 

By unifying the database connections to a single shared SQLite volume (`aarohan_local.db`), all services now reference the exact same business records. The schema was robustly unified, missing schema columns were added dynamically, and validation errors due to missing constraints (`last_synced_at`, `revenue_health_score`, etc.) were patched.

## Microservice Audit & Lineage Check

| Service Module | Endpoint | Original Database Connection | Current Unified Connection | Functional Status |
|---|---|---|---|---|
| **Onboarding** | `/onboarding/customers/99` | Standalone `create_engine` | Shared `SessionLocal` | ✅ 200 OK |
| **GST Service** | `/gst/profile/99` | Standalone `create_engine` | Shared `SessionLocal` | ✅ 200 OK |
| **CKYC Service** | `/ckyc/records/99` | Standalone `create_engine` | Shared `SessionLocal` | ✅ 200 OK |
| **Account Aggregator** | `/aa/links/99` | Standalone `create_engine` | Shared `SessionLocal` | ✅ 200 OK |
| **EPFO Service** | `/epfo/profile/99` | Standalone `create_engine` | Shared `SessionLocal` | ✅ 200 OK |
| **MCA Service** | `/mca/profile/99` | Standalone `create_engine` | Shared `SessionLocal` | ✅ 200 OK |
| **FHC Service** | `/fhc/99` | Standalone `create_engine` | Shared `SessionLocal` | ✅ 200 OK |
| **Executive** | `/exec/briefing` | Standalone `create_engine` | Shared `SessionLocal` | ✅ 200 OK |

## Relational Integrity Validations

Every service was verified to preserve identical keys for the single logical entity:
1. **Customer ID:** `99` (Preserved identically across all microservices via Foreign Key)
2. **PAN:** `PRXPT0001K` (Consistent lookup)
3. **GSTIN:** `27SIMPT0001K1Z5` (Consistent lookup)
4. **EPFO Establishment ID:** `MHBAN0000012000` (Consistent lookup)

## Resolution Details
- **No Mock Data:** We completely avoided injecting placeholder HTTP mock responses.
- **No Duplicated Records:** All seed data inserts use `INSERT OR REPLACE` mapping to the identical logical `Customer 99`.
- **Database Unification:** We deprecated standalone SQLite files and engines. Every service imports the shared `engine` and `SessionLocal` from `app.database`, which resolves to `/app/data/aarohan_local.db`.
- **Schema & Validation Patching:** We identified that Pydantic `ResponseValidationError`s were occurring due to partial schema creation (missing `last_synced_at` and 40+ `fhc_cards` dimension columns). This was resolved by forcing a full schema compile (`create_all_tables.py`) and migrating missing null values (`fix_fhc.py`).

**Result:** The application journey from Onboarding to the Executive Dashboard is now fully interconnected, sharing a unified business reality.
