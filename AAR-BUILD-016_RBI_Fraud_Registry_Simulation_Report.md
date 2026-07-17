# AAR-BUILD-016 – RBI Fraud Registry Simulation & Fraud Risk Intelligence Service
## Build Report

**Date:** 2026-07-09  
**Status:** ✅ COMPLETE  
**Test Result:** 56 passed / 56 total

---

## Components Added

| File | Purpose |
|---|---|
| `services/rbi-fraud-service/app/models.py` | SQLAlchemy ORM – `RBIFraudRecord`, `FraudWatchlist`, `FraudServiceConfig` + read-only mapped models |
| `services/rbi-fraud-service/app/schemas.py` | Pydantic V2 request/response schemas incl. Dashboard & Assessment |
| `services/rbi-fraud-service/app/database.py` | SQLite engine, session, seed watchlist |
| `services/rbi-fraud-service/app/adapters.py` | Strategy adapters: Simulation, Sandbox, Production |
| `services/rbi-fraud-service/app/main.py` | FastAPI application – all endpoints, middleware, event publishing |
| `services/rbi-fraud-service/tests/test_rbi_fraud.py` | 56-test comprehensive suite |

---

## APIs Implemented

### Fraud Screening
| Method | Endpoint | Description |
|---|---|---|
| POST | `/rbi/verify/customer` | Generic entity fraud lookup |
| POST | `/rbi/verify/customer/{id}` | Customer lookup by ID (auto-resolves PAN) |
| POST | `/rbi/verify/business` | Business entity screening |
| POST | `/rbi/verify/pan` | Direct PAN verification |
| POST | `/rbi/verify/gstin` | Direct GSTIN verification |
| POST | `/rbi/verify/directors` | Director DIN verification |
| POST | `/rbi/verify/accounts` | Bank account verification |
| POST | `/rbi/assessment/{id}` | Full consolidated fraud assessment |

### Fraud Intelligence
| Method | Endpoint | Description |
|---|---|---|
| GET | `/rbi/history/{id}` | Retrieve all fraud records for customer (newest first) |
| GET | `/rbi/dashboard` | Aggregated fraud dashboard with risk tier counts |
| GET | `/rbi/dashboard/timeline/{id}` | Chronological fraud event timeline |

### Administration
| Method | Endpoint | Description |
|---|---|---|
| GET | `/rbi/watchlist` | List watchlist (filterable by type) |
| POST | `/rbi/watchlist` | Add single watchlist entry |
| DELETE | `/rbi/watchlist/{id}` | Remove watchlist entry |
| POST | `/rbi/watchlist/import` | Bulk import watchlist (skips duplicates) |
| POST | `/rbi/override/{id}` | Manual override with full audit trail |
| POST | `/rbi/rerun/{id}` | Re-run fraud check for customer |
| GET | `/rbi/config` | Get active adapter and rule parameters |
| POST | `/rbi/config` | Update adapter / rule parameters |
| GET | `/rbi/export/{id}` | Export fraud report (JSON or PDF) |

### Workflow Integration
| Method | Endpoint | Description |
|---|---|---|
| GET | `/rbi/ocen-clearance/{id}` | OCEN Marketplace clearance signal |
| GET | `/rbi/cam-summary/{id}` | CAM Generator fraud summary payload |

### Health
| GET | `/livez` | Liveness probe |
| GET | `/readyz` | Readiness probe (DB connectivity) |

---

## Fraud Rules

| Rule | Trigger | Outcome |
|---|---|---|
| Rule A – Blacklist Match | Entity value found in `rbi_fraud_watchlist` | Score 95 · Critical · BLACK_LIST_MATCH |
| Rule B – Identity Mismatch | CKYC match confidence < threshold or anomaly | Score 65 · High · IDENTITY_MISMATCH |
| Rule C – Suspicious Banking | Cheque bounce or frequent overdraft (AA data) | Score 45 · Medium · SUSPICIOUS_BANKING |
| Rule D – Director Fraud Link | MCA governance risk = Critical | Score 75 · High · DIRECTOR_LINKED_FRAUD |
| Rule E – Multi-Entity Fraud | ≥2 linked businesses with blacklisted GSTINs | Score 80 · Critical · MULTI_ENTITY_FRAUD |

All rule thresholds are configurable via `/rbi/config` (`identity_threshold`, `aml_threshold`, etc.).

---

## Risk Scoring Model

| Score Range | Risk Level |
|---|---|
| 0–29 | Low |
| 30–54 | Medium |
| 55–74 | High |
| 75–100 | Critical |

**Fraud Categories:** Identity Fraud · Financial Fraud · Document Fraud · Transaction Fraud · Corporate Fraud

---

## AML Risk

AML status is derived from the aggregate fraud score and active risk flags:

| Score | AML Assessment |
|---|---|
| < 30 | AML Risk: LOW – no indicators |
| 30–74 (SUSPICIOUS_BANKING) | AML Risk: MEDIUM – monitor for STR |
| 40–74 | AML Risk: HIGH – manual AML review required |
| ≥ 75 | AML Risk: CRITICAL – FIU-IND escalation |

AML status is embedded in `ai_insights` and surfaced in the full assessment response.

---

## AI Fraud Insights

Explainable observations generated for every screening:

- `No fraud indicators detected. Strong identity consistency observed.`
- `Entity matched RBI Central Fraud Registry blacklist record: <reason>.`
- `Repeated identity mismatch flagged by CKYC Verification service; match confidence X% below threshold.`
- `Suspicious transaction activity detected: cheque bounce history, frequent overdraft usage.`
- `Board member shares associations with flagged corporate shell entities; MCA governance risk rated Critical.`
- `Customer linked to N businesses with blacklisted GSTINs; multiple fraudulent entity network detected.`
- `AML Risk: <level> – <action narrative>.`

All observations are pipe-delimited in the `ai_insights` field and returned verbatim in the assessment response.

---

## Workflow Integration

### Business Events Published

| Event | Trigger |
|---|---|
| `Fraud Screening Started` | Any verify call |
| `Fraud Screening Completed` | Record persisted |
| `Fraud Risk Updated` | After scoring or override |
| `Fraud Alert Raised` | Risk level = High or Critical |
| `Manual Investigation Required` | Risk level = High |
| `Customer Cleared` | Risk level = Low / after override |

### Downstream Integrations
- **OCEN Marketplace** – `/rbi/ocen-clearance/{id}` signals go/no-go for loan-offer matching
- **CAM Generator** – `/rbi/cam-summary/{id}` delivers RBI fraud summary for credit appraisal memo
- **Financial Health Card** – FHC consumed screening records via shared DB
- **AI Credit Decision Engine** – assessed risk level embedded in lending recommendation

---

## Dashboard Components

| Component | Endpoint / Field |
|---|---|
| Fraud Risk Gauge | `total_screened`, `low_risk` … `critical_risk` |
| Investigation Queue | `investigation_queue` (High + Critical, not overridden) |
| Fraud Timeline | `/rbi/dashboard/timeline/{id}` |
| Recent Alerts | `recent_alerts` (paginated, newest-first) |
| AI Fraud Insights | `ai_insights` per record |
| Risk Indicators | `risk_flags` comma-separated per record |

---

## Adapter Architecture

| Adapter | Behaviour |
|---|---|
| `SimulationAdapter` | Deterministic dataset-driven simulation with Rules A–E + AML |
| `SandboxAdapter` | Delegates to Simulation; stamps `ai_insights = "Sandbox API Mock"` |
| `ProductionAdapter` | Interface stub; delegates to Simulation until RBI API is live |

Active adapter and rule parameters are switchable at runtime via `POST /rbi/config`.

---

## Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.0.1
collected 56 items

TestFraudLookup::test_clean_pan_returns_low_risk         PASSED
TestFraudLookup::test_blacklisted_pan_returns_critical   PASSED
TestFraudLookup::test_blacklisted_gstin_returns_critical PASSED
TestFraudLookup::test_blacklisted_account_returns_critical PASSED
TestFraudLookup::test_blacklisted_director_returns_critical PASSED
TestAllVerifyEndpoints::test_verify_customer_generic     PASSED
TestAllVerifyEndpoints::test_verify_business_endpoint    PASSED
TestAllVerifyEndpoints::test_verify_pan_endpoint         PASSED
TestAllVerifyEndpoints::test_verify_gstin_endpoint       PASSED
TestAllVerifyEndpoints::test_verify_directors_endpoint   PASSED
TestAllVerifyEndpoints::test_verify_accounts_endpoint    PASSED
TestAllVerifyEndpoints::test_verify_customer_by_path     PASSED
TestAllVerifyEndpoints::test_verify_accounts_blacklisted PASSED
TestRiskScoring::test_fraud_score_clean_is_zero          PASSED
TestRiskScoring::test_fraud_score_blacklisted_is_95      PASSED
TestRiskScoring::test_risk_level_mapping                 PASSED
TestRiskScoring::test_fraud_categories_present           PASSED
TestRiskScoring::test_aml_assessment_low                 PASSED
TestRiskScoring::test_aml_assessment_high                PASSED
TestRiskScoring::test_aml_assessment_critical            PASSED
TestAIInsights::test_clean_entity_has_no_fraud_narrative PASSED
TestAIInsights::test_blacklisted_entity_insight_mentions_registry PASSED
TestAIInsights::test_aml_annotation_always_present       PASSED
TestWatchlist::test_list_watchlist_returns_seeded        PASSED
TestWatchlist::test_add_to_watchlist                     PASSED
TestWatchlist::test_add_duplicate_returns_409            PASSED
TestWatchlist::test_new_watchlist_item_causes_fraud_hit  PASSED
TestWatchlist::test_bulk_import                          PASSED
TestWatchlist::test_filter_watchlist_by_type             PASSED
TestDashboardAndHistory::test_history_returns_records    PASSED
TestDashboardAndHistory::test_history_ordered_newest_first PASSED
TestDashboardAndHistory::test_dashboard_structure        PASSED
TestDashboardAndHistory::test_dashboard_totals_non_negative PASSED
TestDashboardAndHistory::test_fraud_timeline             PASSED
TestDashboardAndHistory::test_investigation_queue_contains_high_risk PASSED
TestFraudAssessment::test_assessment_structure           PASSED
TestFraudAssessment::test_assessment_recommendation_clean PASSED
TestAdapterSwitching::test_default_adapter_is_simulation PASSED
TestAdapterSwitching::test_switch_to_sandbox_and_verify  PASSED
TestAdapterSwitching::test_switch_to_production_and_verify PASSED
TestAdapterSwitching::test_switch_back_to_simulation     PASSED
TestOverride::test_override_clears_blacklisted_customer  PASSED
TestOverride::test_override_missing_record_returns_404   PASSED
TestOverride::test_rerun_after_override                  PASSED
TestExport::test_export_json                             PASSED
TestExport::test_export_pdf                              PASSED
TestExport::test_export_unsupported_format               PASSED
TestExport::test_export_missing_customer_404             PASSED
TestWorkflowIntegration::test_ocen_clearance_clean_customer PASSED
TestWorkflowIntegration::test_ocen_clearance_blacklisted_customer PASSED
TestWorkflowIntegration::test_cam_summary_structure      PASSED
TestHealth::test_livez                                   PASSED
TestHealth::test_readyz                                  PASSED
TestBusinessEvents::test_fraud_screening_started_event_logged PASSED
TestBusinessEvents::test_customer_cleared_event_logged   PASSED
TestBusinessEvents::test_fraud_alert_raised_for_blacklisted PASSED

======================= 56 passed in 8.32s =======================
```

**Coverage:** Fraud lookup ✓ · Risk scoring ✓ · Rule execution ✓ · AI insights ✓ · Workflow integration ✓ · Business event publication ✓ · Dashboard functionality ✓ · Adapter switching ✓

---

🟢 RBI FRAUD REGISTRY SIMULATION IMPLEMENTED – READY FOR OCEN MARKETPLACE INTEGRATION
