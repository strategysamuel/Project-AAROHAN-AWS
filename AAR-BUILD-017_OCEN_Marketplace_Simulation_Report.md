# AAR-BUILD-017 – OCEN Marketplace Simulation & Intelligent Loan Matching Service
## Build Report

**Date:** 2026-07-09  
**Status:** ✅ COMPLETE  
**Test Result:** 65 passed / 65 total

---

## Components Added

| File | Purpose |
|---|---|
| `services/ocen-uli-service/app/models.py` | Full ORM: `Lender` (rich policy), `LoanProduct`, `LoanApplication` (upstream intelligence), `LoanOffer` (match score + explainability), `MarketplaceMatch`, `MarketplaceConfig`, `AuditLog` |
| `services/ocen-uli-service/app/schemas.py` | Pydantic V2 schemas: Lender, Offer, Comparison, Dashboard, Search, Config |
| `services/ocen-uli-service/app/adapters.py` | SimulationAdapter (full matching engine + EMI + explainability), SandboxAdapter, ProductionAdapter |
| `services/ocen-uli-service/app/database.py` | Bootstrap with full OCEN table migration and 10-lender seed |
| `services/ocen-uli-service/app/main.py` | FastAPI application – 30+ endpoints |
| `services/ocen-uli-service/tests/test_ocen_uli.py` | 65-test suite across 15 test classes |

---

## APIs Implemented

### Marketplace
| Method | Endpoint | Description |
|---|---|---|
| POST | `/ocen/marketplace/search` | Search eligible lenders with ranked match scores |
| POST | `/ocen/apply` | Submit application + run matching engine + generate ranked offers |
| GET | `/ocen/applications/{id}` | Retrieve application details |
| GET | `/ocen/applications/{id}/offers` | Get all ranked offers for an application |
| GET | `/ocen/offers/compare/{id}` | Compare offers (best rate / best match / best amount) |
| POST | `/ocen/offers/accept` | Accept loan offer (expires all others) |
| POST | `/ocen/offers/reject` | Reject a specific offer with reason |
| GET | `/ocen/marketplace/status/{id}` | Marketplace status (lenders screened, matched, best score) |
| POST | `/ocen/eligibility` | Pre-check eligibility before application |
| POST | `/ocen/disburse/{id}` | Disburse accepted loan |

### Lender Registry
| Method | Endpoint | Description |
|---|---|---|
| GET | `/ocen/lenders` | List all lenders (filterable by type / active status) |
| GET | `/ocen/lenders/{id}` | Retrieve lender details |
| POST | `/ocen/lenders` | Register new lender |
| PUT | `/ocen/lenders/{id}` | Update lender policy |
| DELETE | `/ocen/lenders/{id}` | Disable lender |

### Loan Products
| Method | Endpoint | Description |
|---|---|---|
| GET | `/ocen/products` | List all active loan products |

### AI / Recommendations
| Method | Endpoint | Description |
|---|---|---|
| GET | `/ocen/ai-advisor/{id}` | AI-driven best offer recommendation with breakdown |

### Dashboard
| Method | Endpoint | Description |
|---|---|---|
| GET | `/ocen/dashboard` | Marketplace dashboard (aggregated KPIs, recent applications) |

### Workflow Integration
| Method | Endpoint | Description |
|---|---|---|
| GET | `/ocen/cam-summary/{id}` | CAM Generator payload (selected lender, approved terms) |
| GET | `/ocen/executive-summary` | Executive Dashboard feed (disbursed, accepted, totals) |

### Administration
| Method | Endpoint | Description |
|---|---|---|
| GET | `/ocen/config` | Get active adapter and match parameters |
| POST | `/ocen/config` | Update adapter / match rules |
| POST | `/ocen/admin/replay` | Replay matching process for an application |
| GET | `/ocen/admin/export/{id}` | Export marketplace results (JSON / PDF) |
| GET | `/ocen/audit-logs` | Retrieve audit trail |

### Health
| GET | `/healthz` | Liveness probe |
| GET | `/readyz` | Readiness probe |

---

## Lender Registry (10 Lenders)

| ID | Name | Type | Base Rate | Max Loan | TAT | Risk |
|---|---|---|---|---|---|---|
| LEND-IDBI-001 | IDBI Bank – MSME Division | BANK | 8.75% | ₹1 Cr | 5d | MEDIUM |
| LEND-HDFC-001 | HDFC Bank – Business Banking | BANK | 9.25% | ₹75L | 3d | MEDIUM |
| LEND-SBI-001 | State Bank of India – SME Finance | BANK | 8.50% | ₹2.5 Cr | 10d | LOW |
| LEND-TATA-001 | Tata Capital – SME Lending | NBFC | 11.00% | ₹50L | 2d | HIGH |
| LEND-BAJAJ-001 | Bajaj Finserv – Business Loan | NBFC | 12.00% | ₹35L | 1d | HIGH |
| LEND-KOTAK-001 | Kotak Mahindra Bank – Business Credit | BANK | 9.75% | ₹60L | 4d | MEDIUM |
| LEND-SIDBI-001 | SIDBI – MSME Credit Line | BANK | 7.75% | ₹2 Cr | 7d | LOW |
| LEND-FLEX-001 | FlexiLoans – Digital NBFC | FINTECH | 13.50% | ₹20L | 1d | HIGH |
| LEND-MUDRA-001 | MUDRA – Tarun Scheme | MFI | 9.00% | ₹10L | 5d | MEDIUM |
| LEND-IIFL-001 | IIFL Finance – SME Division | NBFC | 12.50% | ₹40L | 2d | HIGH |

**Lender Types:** BANK (4) · NBFC (4) · FINTECH (1) · MFI (1)  
**Geographic Coverage:** PAN India (all lenders)  
**Women Entrepreneur Schemes:** IDBI, HDFC, SBI, BAJAJ, SIDBI, MUDRA  
**Startup-Friendly:** HDFC, TATA, BAJAJ, KOTAK, SIDBI, FLEX, MUDRA, IIFL

---

## Loan Products (10 Products)

| Code | Product Name |
|---|---|
| WCL | Working Capital Loan |
| TERM | Term Loan |
| MACH | Machinery Loan |
| INV | Invoice Financing |
| SCF | Supply Chain Finance |
| EXP | Export Finance |
| WEL | Women Entrepreneur Loan |
| STL | Startup Loan |
| AGRI | Agriculture Loan |
| ECL | Emergency Credit Line |

---

## Matching Rules (SimulationAdapter)

### Match Score Formula (0–100)
```
Match Score = 
    FHC Score          × 0.35 (Financial Health Card composite)
  + Credit Decision    × 0.30 (APPROVE=100, CONDITIONAL=65, REJECT=20)
  + Fraud Cleanliness  × 0.20 (Low=100, Medium=70, High=30, Critical=0)
  + Loan Size Fit      × 0.15 (1 - pct of lender cap, min 20)
  + Lender Bonuses     (up to +10 for HIGH risk appetite, no collateral, TAT≤2d)
```

### Hard-Block Gates (Eligibility)
| Gate | Condition |
|---|---|
| Fraud Critical Block | `fraud_risk_level == Critical` → ALL lenders blocked |
| Credit Reject Block | `credit_decision == REJECT` → lender blocked |
| Loan Ceiling | `requested_amount > max_loan_amount` → lender skipped |
| Loan Floor | `requested_amount < min_loan_amount` → lender skipped |
| Tenure Cap | `requested_tenure > max_tenure_months` → lender skipped |
| Product Match | Product not in lender's supported products → lender skipped |

All parameters configurable via `POST /ocen/config`.

---

## Offer Generation Logic

### Per-Eligible-Lender Computation
| Field | Logic |
|---|---|
| `offered_amount` | = `requested_amount` (full ask if within cap) |
| `interest_rate` | Base rate + risk spread (FHC < 40 → +2%, FHC < 55 → +1%, fraud Medium → +0.5%, High → +1.5%) capped at `max_interest_rate` |
| `emi` | Reducing-balance formula: `P × r(1+r)^n / ((1+r)^n − 1)` |
| `total_interest` | `EMI × tenure − principal` |
| `processing_fee` | `lender.processing_fee_pct / 100 × offered_amount` |
| `approval_probability` | Base 0.70 + FHC bonus (+0.15 if ≥75, +0.08 if ≥60) + APPROVE bonus (+0.10) + fraud penalty (−0.15 if High) |
| `expected_disbursal_days` | = `lender.tat_days` |
| `conditions` | Auto-generated from collateral requirement, conditional credit decision, elevated fraud |

### Offer Ranking
Offers ranked by `match_score` descending. `rank=1` = best match.

---

## Explainable Matching

Every offer contains a structured `match_explanation` JSON:

```json
{
  "why_selected": "IDBI Bank – MSME Division offers 'Working Capital Loan' with a base rate of 8.75% p.a. and a match score of 87.5/100.",
  "why_customer_qualifies": "Customer's FHC score of 72.5, credit decision of 'APPROVE', and Low fraud risk satisfy IDBI Bank's lending policy.",
  "key_strengths": [
    "Strong Financial Health Card score (72.5/100)",
    "AI Credit Decision: APPROVED",
    "Clean RBI Fraud Registry status",
    "No collateral required"
  ],
  "key_constraints": [],
  "suggested_next_steps": [
    "Complete digital KYC on lender portal",
    "Upload last 2 years GST returns",
    "Await lender credit approval (typically 5 working days)"
  ]
}
```

---

## Workflow Integration

### Upstream Inputs Consumed
| Source | Field | Usage |
|---|---|---|
| Financial Health Card | `fhc_score` (0–100) | Match score component (35% weight) |
| AI Credit Decision | `credit_decision` (APPROVE/CONDITIONAL/REJECT) | Match score component (30% weight) + hard block gate |
| RBI Fraud Registry | `fraud_risk_level` (Low/Medium/High/Critical) | Match score component (20% weight) + critical block |
| RBI Fraud Registry | `fraud_score` (0–100) | Risk-adjusted interest rate spread |

### Downstream Outputs
| Consumer | Endpoint | Data Provided |
|---|---|---|
| CAM Generator | `/ocen/cam-summary/{id}` | Selected lender, approved amount, rate, EMI, tenure, match score |
| Executive Dashboard | `/ocen/executive-summary` | Total disbursed, accepted, avg rate, total loan value |
| Reporting Engine | `/ocen/admin/export/{id}` | JSON or PDF offer report |

---

## Business Events

| Event | Trigger |
|---|---|
| `Marketplace Search Started` | `POST /ocen/apply` or `/ocen/marketplace/search` called |
| `Lender Matched` | Each eligible lender generates an offer |
| `Loan Offer Generated` | Offers committed to database |
| `Offer Accepted` | `POST /ocen/offers/accept` |
| `Offer Rejected` | `POST /ocen/offers/reject` |
| `Marketplace Completed` | Application reaches terminal state (ACCEPTED / NO_OFFERS / BLOCKED_FRAUD) |

### Event Flow
```
Offer Accepted
     ↓
Marketplace Completed → CAM Generator (/ocen/cam-summary)
                      → Executive Dashboard (/ocen/executive-summary)
                      → Disburse (/ocen/disburse)

No Eligible Offers (NO_OFFERS)
     ↓
Marketplace Completed → Manual Review flag set
```

---

## Dashboard Components

| Component | Source |
|---|---|
| Total Applications | Count of all `LoanApplication` records |
| Offers Generated | Count of all `LoanOffer` records |
| Offers Accepted | Offers with `status == ACCEPTED` |
| Offers Rejected | Offers with `status == REJECTED` |
| Active Lenders | Lenders with `is_active == True` |
| Avg Match Score | Average `match_score` across all offers |
| Avg Interest Rate | Average `interest_rate` across all offers |
| Top Lender | Lender with most accepted offers |
| Recent Applications | Latest N applications (configurable `limit`) |
| Marketplace Status | Per-application: lenders screened, matched, best score, best rate |

---

## Adapter Architecture

| Adapter | Behaviour |
|---|---|
| `SimulationAdapter` | Deterministic matching engine (Rules, EMI, risk-adjustment, explainability) |
| `SandboxAdapter` | Delegates to Simulation; stamps `SANDBOX MODE` in offer conditions |
| `ProductionAdapter` | Interface stub; delegates to Simulation pending real OCEN gateway |

Active adapter switchable at runtime:
```
POST /ocen/config
{ "active_adapter": "SANDBOX", "match_params": { "fhc_weight": 0.40, ... } }
```

---

## Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.0.1
collected 65 items

TestLenderRegistry::test_list_lenders_returns_10          PASSED
TestLenderRegistry::test_lender_types_diverse             PASSED
TestLenderRegistry::test_get_lender_by_id                 PASSED
TestLenderRegistry::test_get_nonexistent_lender_404       PASSED
TestLenderRegistry::test_register_new_lender              PASSED
TestLenderRegistry::test_register_duplicate_lender_409    PASSED
TestLenderRegistry::test_disable_test_lender              PASSED
TestLoanProducts::test_list_products_returns_10           PASSED
TestLoanProducts::test_product_names_correct              PASSED
TestLenderSearch::test_search_eligible_lenders_good_profile   PASSED
TestLenderSearch::test_search_critical_fraud_blocks_all   PASSED
TestLenderSearch::test_search_results_ranked_by_score     PASSED
TestLenderSearch::test_search_amount_too_high_rejected    PASSED
TestOfferGeneration::test_good_application_generates_offers   PASSED
TestOfferGeneration::test_blocked_application_returns_blocked_status  PASSED
TestOfferGeneration::test_offers_have_match_score         PASSED
TestOfferGeneration::test_offers_ranked_best_first        PASSED
TestOfferGeneration::test_offer_has_emi_computed          PASSED
TestOfferGeneration::test_offer_has_total_interest        PASSED
TestOfferGeneration::test_offer_has_approval_probability  PASSED
TestOfferGeneration::test_offer_processing_fee_positive   PASSED
TestMatchScore::test_adapter_score_calculation            PASSED
TestMatchScore::test_high_fhc_gives_higher_score          PASSED
TestMatchScore::test_fraud_critical_gives_zero_component  PASSED
TestMatchScore::test_fraud_low_gives_max_component        PASSED
TestMatchScore::test_approve_decision_gives_max_cd_component  PASSED
TestMatchScore::test_emi_calculation                      PASSED
TestMatchScore::test_risk_adjusted_rate_higher_for_low_fhc   PASSED
TestExplainability::test_offer_has_match_explanation      PASSED
TestExplainability::test_explanation_strengths_populated_for_good_profile PASSED
TestExplainability::test_ai_advisor_recommendation        PASSED
TestExplainability::test_ai_advisor_includes_lender_name  PASSED
TestOfferComparison::test_comparison_structure            PASSED
TestOfferComparison::test_best_rate_has_lowest_rate       PASSED
TestOfferLifecycle::test_accept_offer                     PASSED
TestOfferLifecycle::test_accept_expires_other_offers      PASSED
TestOfferLifecycle::test_reject_offer                     PASSED
TestOfferLifecycle::test_disburse_after_accept            PASSED
TestOfferLifecycle::test_disburse_without_accept_fails    PASSED
TestOfferLifecycle::test_accept_nonexistent_offer_404     PASSED
TestDashboard::test_marketplace_status_structure          PASSED
TestDashboard::test_dashboard_structure                   PASSED
TestDashboard::test_dashboard_active_lenders_count        PASSED
TestDashboard::test_dashboard_totals_non_negative         PASSED
TestEligibility::test_good_profile_eligible               PASSED
TestEligibility::test_low_credit_score_not_eligible       PASSED
TestEligibility::test_amount_exceeds_revenue_ceiling      PASSED
TestEligibility::test_critical_fraud_blocks_eligibility   PASSED
TestAdapterSwitching::test_default_adapter_simulation     PASSED
TestAdapterSwitching::test_switch_to_sandbox              PASSED
TestAdapterSwitching::test_switch_to_production           PASSED
TestAdapterSwitching::test_switch_back_to_simulation      PASSED
TestAdmin::test_replay_matching                           PASSED
TestAdmin::test_export_json                               PASSED
TestAdmin::test_export_pdf                                PASSED
TestAdmin::test_export_unsupported_format                 PASSED
TestAdmin::test_audit_logs_non_empty                      PASSED
TestWorkflowIntegration::test_cam_summary_structure       PASSED
TestWorkflowIntegration::test_executive_summary           PASSED
TestWorkflowIntegration::test_cam_summary_shows_selected_lender_after_accept PASSED
TestBusinessEvents::test_marketplace_search_started_event PASSED
TestBusinessEvents::test_lender_matched_event             PASSED
TestBusinessEvents::test_offer_accepted_event             PASSED
TestHealth::test_liveness                                 PASSED
TestHealth::test_readiness                                PASSED

======================= 65 passed in 5.78s =======================
```

**Coverage:** Lender matching ✓ · Offer generation ✓ · Match score calculation ✓ · Ranking logic ✓ · Explainable recommendations ✓ · Workflow integration ✓ · Business event publication ✓ · Dashboard functionality ✓ · Adapter switching ✓

---

🟢 OCEN MARKETPLACE SIMULATION IMPLEMENTED – READY FOR CAM GENERATION
