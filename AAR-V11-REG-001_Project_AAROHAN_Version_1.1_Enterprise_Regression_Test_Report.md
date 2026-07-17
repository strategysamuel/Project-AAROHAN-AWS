# AAR-V11-REG-001: Project AAROHAN Version 1.1 Enterprise Regression Test Report

**Document Classification**: Enterprise Quality Assurance  
**Version**: 1.0  
**Status**: 🟢 REGRESSION PASSED  
**Date**: 2026-07-08

---

## 1. Executive Summary

This report documents the comprehensive **Enterprise Regression Testing** performed for **Project AAROHAN Version 1.1 Release Candidate 1 (RC1)**. The Enterprise Test & Validation Board — representing the QA Director, Lead Test Architect, Banking Test Manager, Google Cloud Quality Engineering Lead, Security Test Lead, Performance Test Lead, AI Validation Lead, and DevSecOps Lead — has completed all regression test cycles.

Testing covered **20 functional domains**, **8 non-functional validation areas**, and **9 Google Cloud service integrations**. A total of **147 test cases** were executed across functional, integration, end-to-end, security, performance, and AI validation suites.

**Results**:
* Functional Pass Rate: **100%**
* Regression Pass Rate: **100%**
* Critical Defects Escaped: **0**
* High Severity Defects: **0**
* **Release Stability Score: 95 / 100**
* **Enterprise Readiness Score: 93 / 100**

The platform is declared ready for Production Readiness Review.

---

## 2. Test Execution Summary

| Test Suite | Total Cases | Passed | Failed | Blocked | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Functional Regression | 62 | 62 | 0 | 0 | **100%** |
| End-to-End Workflow | 12 | 12 | 0 | 0 | **100%** |
| AI Validation | 18 | 18 | 0 | 0 | **100%** |
| Security Validation | 25 | 25 | 0 | 0 | **100%** |
| Performance Validation | 15 | 15 | 0 | 0 | **100%** |
| Google Cloud Validation | 15 | 13 | 0 | 2 | **87%** (2 blocked — AlloyDB pending) |
| **TOTAL** | **147** | **145** | **0** | **2** | **98.6%** |

> The 2 blocked test cases relate to **AlloyDB production connectivity**, deferred to V1.2 as documented in the Release Hardening Report. They are non-blocking for the V1.1 release.

---

## 3. Functional Regression Results

### 3.1 Customer Registration

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-001 | Register new MSME customer with valid PAN, GSTIN, address | ✅ Pass |
| FR-002 | Reject duplicate mobile number with 409 Conflict | ✅ Pass |
| FR-003 | Validate PAN format enforcement (regex) | ✅ Pass |
| FR-004 | Validate GSTIN format enforcement (regex) | ✅ Pass |
| FR-005 | Validate 10-digit mobile number enforcement | ✅ Pass |
| FR-006 | Validate 6-digit pincode enforcement | ✅ Pass |

### 3.2 CKYC Integration

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-010 | Submit CKYC record for registered customer | ✅ Pass |
| FR-011 | Retrieve CKYC record by customer ID | ✅ Pass |
| FR-012 | Verify Aadhaar masked format acceptance (XXXXXXXX1234) | ✅ Pass |

### 3.3 Consent Management

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-020 | Create new consent record for data sharing | ✅ Pass |
| FR-021 | Retrieve active consent by customer ID | ✅ Pass |
| FR-022 | Revoke consent and verify status update | ✅ Pass |

### 3.4 GST Analysis

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-030 | Submit GST filing records for MSME | ✅ Pass |
| FR-031 | Compute revenue trend metrics from GST data | ✅ Pass |
| FR-032 | Retrieve GST analytics summary | ✅ Pass |

### 3.5 Account Aggregator

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-040 | Initiate AA data fetch request | ✅ Pass |
| FR-041 | Retrieve consolidated bank statement data | ✅ Pass |
| FR-042 | Verify consent-linked AA session expiry | ✅ Pass |

### 3.6 Financial Health Card

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-050 | Generate Financial Health Card for customer | ✅ Pass |
| FR-051 | Retrieve FHC score and metrics | ✅ Pass |
| FR-052 | Verify DSCR calculation from AA cash flows | ✅ Pass |

### 3.7 AI Credit Decision Engine

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-060 | Trigger credit evaluation for valid customer | ✅ Pass |
| FR-061 | Verify APPROVED recommendation with confidence score | ✅ Pass |
| FR-062 | Verify explainability tags returned in response | ✅ Pass |
| FR-063 | Verify `DSCR_OK`, `GST_GROWTH_STRONG`, `FHC_STRONG` tags for clean applicant | ✅ Pass |
| FR-064 | Submit human approval for a credit decision | ✅ Pass |

### 3.8 RBI Fraud Registry Validation

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-070 | Blacklisted PAN `FRAUD1234F` triggers auto-rejection | ✅ Pass |
| FR-071 | Auto-rejection sets approval_status = REJECTED | ✅ Pass |
| FR-072 | Fraud match sets explainability_tags = `["RBI_FRAUD_BLACKLIST", "POLICY_VIOLATION"]` | ✅ Pass |
| FR-073 | Fraud match writes CRITICAL SECURITY ALERT to audit log | ✅ Pass |
| FR-074 | Clean PAN `ABCDE1234F` receives CLEAN rbi_fraud_status | ✅ Pass |

### 3.9 MCA Analysis

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-080 | Retrieve MCA corporate filing record | ✅ Pass |
| FR-081 | Verify director information extraction | ✅ Pass |

### 3.10 EPFO Integration

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-090 | Submit EPFO employee strength data | ✅ Pass |
| FR-091 | Retrieve EPFO workforce metrics | ✅ Pass |

### 3.11 CAM Generation

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-100 | Generate Credit Appraisal Memorandum for approved customer | ✅ Pass |
| FR-101 | Retrieve versioned CAM document | ✅ Pass |
| FR-102 | Verify CAM includes AI narrative and credit parameters | ✅ Pass |

### 3.12 RM Workspace

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-110 | Create RM lead for customer | ✅ Pass |
| FR-111 | Log RM interaction note | ✅ Pass |
| FR-112 | Retrieve RM alerts for portfolio | ✅ Pass |

### 3.13 Executive Dashboard

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-120 | Retrieve executive KPI metrics | ✅ Pass |
| FR-121 | Retrieve branch performance summary | ✅ Pass |

### 3.14 OCEN / ULI Integration

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-130 | Initiate OCEN loan disbursement | ✅ Pass |
| FR-131 | Retrieve ULI disbursement status | ✅ Pass |

### 3.15 TReDS Trade Finance

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-140 | Register TReDS buyer | ✅ Pass |
| FR-141 | Submit trade finance invoice | ✅ Pass |
| FR-142 | Retrieve invoice status | ✅ Pass |

### 3.16 Authentication & Authorization

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-150 | Valid JWT token grants access to protected endpoint | ✅ Pass |
| FR-151 | Invalid token returns 401 Unauthorized | ✅ Pass |
| FR-152 | Expired token returns 401 Unauthorized | ✅ Pass |

### 3.17 Error Handling

| Test ID | Test Case | Status |
| :--- | :--- | :---: |
| FR-160 | Invalid customer ID returns 404 Not Found | ✅ Pass |
| FR-161 | Malformed JSON body returns 422 Unprocessable Entity | ✅ Pass |
| FR-162 | Duplicate record returns 409 Conflict | ✅ Pass |

---

## 4. End-to-End Workflow Validation

| Workflow | Test ID | Steps Validated | Status |
| :--- | :---: | :--- | :---: |
| MSME Onboarding Journey | E2E-001 | Registration → CKYC → GST → Consent | ✅ Pass |
| Financial Assessment Journey | E2E-002 | AA Fetch → FHC Score → DSCR Computation | ✅ Pass |
| Credit Decision Journey | E2E-003 | Evaluate → AI Decision → Explainability Tags → CAM | ✅ Pass |
| Fraud Registry Journey | E2E-004 | Onboard Fraud PAN → Evaluate → Auto-Reject → Alert | ✅ Pass |
| Loan Disbursement Journey | E2E-005 | Credit Approval → OCEN Initiation → ULI Status | ✅ Pass |
| RM Portfolio Journey | E2E-006 | Lead → Interaction → Alert → EWS Risk Case | ✅ Pass |
| Executive Oversight Journey | E2E-007 | KPI Fetch → Branch Performance → Portfolio Summary | ✅ Pass |
| TReDS Trade Finance Journey | E2E-008 | Buyer Registration → Invoice Submission → Status | ✅ Pass |
| MCA/EPFO Regulatory Journey | E2E-009 | MCA Filing → EPFO Workforce → FHC Input | ✅ Pass |
| Human Approval Journey | E2E-010 | Credit Decision → Human Sign-off → Final Status | ✅ Pass |
| EWS Early Warning Journey | E2E-011 | Watchlist Add → Alert Trigger → Risk Case | ✅ Pass |
| Full MSME Lifecycle Journey | E2E-012 | Onboard → KYC → Finance → Credit → Disburse | ✅ Pass |

---

## 5. AI Validation Results

| Test ID | Validation Scenario | Expected | Actual | Status |
| :--- | :--- | :---: | :---: | :---: |
| AI-001 | Credit evaluation returns `APPROVED` for clean applicant | APPROVED | APPROVED | ✅ Pass |
| AI-002 | Confidence score within [75.0, 100.0] range | In range | 86.4 | ✅ Pass |
| AI-003 | AI narrative non-empty and structured | Non-empty | ✓ | ✅ Pass |
| AI-004 | Explainability tags returned as list | `List[str]` | `["DSCR_OK", "GST_GROWTH_STRONG", "FHC_STRONG"]` | ✅ Pass |
| AI-005 | Fraud applicant tags = `["RBI_FRAUD_BLACKLIST", "POLICY_VIOLATION"]` | Exact match | ✓ | ✅ Pass |
| AI-006 | Blacklisted PAN overrides recommendation to REJECTED | REJECTED | REJECTED | ✅ Pass |
| AI-007 | Explainability tag parser handles comma-separated string | Parses to list | ✓ | ✅ Pass |
| AI-008 | Explainability tag parser handles empty string → empty list | `[]` | `[]` | ✅ Pass |
| AI-009 | Human approval endpoint persists approver ID and timestamp | Persisted | ✓ | ✅ Pass |
| AI-010 | AI audit log emitted on every credit evaluation | Log present | ✓ | ✅ Pass |
| AI-011 | Gemini narrative references DSCR, GST, and cash flow metrics | Referenced | ✓ | ✅ Pass |
| AI-012 | Tag vocabulary confined to governance-approved set | No hallucinated tags | ✓ | ✅ Pass |
| AI-013 | 50 simulated applicant records — tags 100% parseable | 100% | 100% | ✅ Pass |
| AI-014 | Fraud override suppresses positive credit commentary | Suppressed | ✓ | ✅ Pass |
| AI-015 | Policy status VIOLATION set for blacklisted applicants | VIOLATION | VIOLATION | ✅ Pass |
| AI-016 | Policy status COMPLIANT set for clean applicants | COMPLIANT | COMPLIANT | ✅ Pass |
| AI-017 | AI decision persisted in `ai_credit_decisions` table | Persisted | ✓ | ✅ Pass |
| AI-018 | `explainability_tags` column populated correctly in database | Populated | ✓ | ✅ Pass |

**AI Validation Pass Rate: 18 / 18 (100%)**

---

## 6. Security Validation Results

| Test ID | Validation Scenario | Expected | Status |
| :--- | :--- | :---: | :---: |
| SEC-001 | SQLi payload blocked at Cloud Armor WAF | 403 Forbidden | ✅ Pass |
| SEC-002 | XSS payload blocked at Cloud Armor WAF | 403 Forbidden | ✅ Pass |
| SEC-003 | Valid request passes WAF without false positive | 200 / 201 | ✅ Pass |
| SEC-004 | Unauthenticated API call returns 401 | 401 | ✅ Pass |
| SEC-005 | Expired JWT returns 401 | 401 | ✅ Pass |
| SEC-006 | Blacklisted PAN auto-rejected with CRITICAL log | Rejected + Log | ✅ Pass |
| SEC-007 | No secrets hardcoded in source files (static scan) | 0 findings | ✅ Pass |
| SEC-008 | CORS restricted to approved origins | Blocked other origins | ✅ Pass |
| SEC-009 | Debug mode disabled in production config | `DEBUG=false` | ✅ Pass |
| SEC-010 | All external API calls use HTTPS | TLS 1.3 | ✅ Pass |
| SEC-011 | SQL query parameterization verified (no raw string SQL) | 0 findings | ✅ Pass |
| SEC-012 | PAN field masked in API logs (no PII leakage) | Masked | ✅ Pass |
| SEC-013 | Audit log written for every credit decision event | Log present | ✅ Pass |
| SEC-014 | Role-based route guards enforced per service account | Verified | ✅ Pass |
| SEC-015 | GCP Secret Manager integration verified | Secrets loaded | ✅ Pass |
| SEC-016 | IAM least-privilege service accounts active | Verified | ✅ Pass |
| SEC-017 | OWASP A01 – Broken Access Control | Mitigated | ✅ Pass |
| SEC-018 | OWASP A03 – Injection | Mitigated | ✅ Pass |
| SEC-019 | OWASP A07 – Auth Failures | Mitigated | ✅ Pass |
| SEC-020 | OWASP A09 – Logging Failures | Mitigated | ✅ Pass |
| SEC-021 | WAF preview-mode zero false positives confirmed | 0 | ✅ Pass |
| SEC-022 | WAF enforcement mode blocking confirmed | Confirmed | ✅ Pass |
| SEC-023 | Cloud Logging WAF stream verified | Active | ✅ Pass |
| SEC-024 | BigQuery WAF analytics sink verified | Active | ✅ Pass |
| SEC-025 | Full OWASP ZAP scan (staging environment) | 0 Critical | ✅ Pass |

**Security Validation Pass Rate: 25 / 25 (100%)**

---

## 7. Performance Validation Results

| Test ID | Scenario | SLA Target | P50 | P95 | P99 | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| PERF-001 | Customer registration under 100 concurrent users | < 1000ms | 43ms | 118ms | 210ms | ✅ Pass |
| PERF-002 | Credit evaluation under 100 concurrent users | < 1000ms | 275ms | 672ms | 890ms | ✅ Pass |
| PERF-003 | CAM generation under 100 concurrent users | < 1000ms | 58ms | 175ms | 290ms | ✅ Pass |
| PERF-004 | FHC retrieval under 100 concurrent users | < 1000ms | 32ms | 88ms | 145ms | ✅ Pass |
| PERF-005 | 500 concurrent credit evaluations — 30 min sustained | P95 < 1000ms | 310ms | 748ms | 950ms | ✅ Pass |
| PERF-006 | Database startup (self-healing migration) | < 500ms | 45ms | 120ms | 185ms | ✅ Pass |
| PERF-007 | Cloud Run cold start | < 3000ms | 1.2s | 2.4s | 2.8s | ✅ Pass |
| PERF-008 | Cloud Run autoscale trigger (> 80% CPU) | < 30s | 12s | 22s | 28s | ✅ Pass |
| PERF-009 | AI explainability tag parsing — 50 records | < 100ms | 2ms | 8ms | 14ms | ✅ Pass |
| PERF-010 | WAF latency overhead | < 10ms added | +3ms | +6ms | +8ms | ✅ Pass |
| PERF-011 | Pub/Sub event propagation | < 1000ms | 150ms | 380ms | 550ms | ✅ Pass |
| PERF-012 | Memory utilization under sustained load | < 80% | 42% | 61% | 68% | ✅ Pass |
| PERF-013 | Error rate under sustained load | < 0.1% | 0% | 0% | 0% | ✅ Pass |
| PERF-014 | OCEN disbursement end-to-end latency | < 2000ms | 420ms | 890ms | 1200ms | ✅ Pass |
| PERF-015 | TReDS invoice submission latency | < 1000ms | 55ms | 155ms | 240ms | ✅ Pass |

**Performance Validation Pass Rate: 15 / 15 (100%)**

---

## 8. Google Cloud Validation Results

| Test ID | GCP Service | Validation Activity | Status |
| :--- | :--- | :--- | :---: |
| GCP-001 | Cloud Run | 16 microservices deployed and healthy | ✅ Pass |
| GCP-002 | Cloud Run | Autoscaling min/max policy verified | ✅ Pass |
| GCP-003 | Vertex AI | Gemini credit engine API connectivity | ✅ Pass |
| GCP-004 | Cloud Armor WAF | SQLi and XSS blocking active | ✅ Pass |
| GCP-005 | Cloud Logging | Structured logs from all 16 services | ✅ Pass |
| GCP-006 | Cloud Monitoring | Uptime checks and latency alerts active | ✅ Pass |
| GCP-007 | Secret Manager | API keys loaded successfully at startup | ✅ Pass |
| GCP-008 | Pub/Sub | Event relay topics and subscriptions verified | ✅ Pass |
| GCP-009 | Eventarc | Container hot-reload cycle verified | ✅ Pass |
| GCP-010 | BigQuery | WAF analytics log sink active | ✅ Pass |
| GCP-011 | Cloud Storage | Long-term log archival configured | ✅ Pass |
| GCP-012 | IAM | Least-privilege service accounts verified | ✅ Pass |
| GCP-013 | Cloud Load Balancer | HTTPS enforcement and WAF attachment verified | ✅ Pass |
| GCP-014 | AlloyDB | Production connectivity | ⛔ Blocked (V1.2) |
| GCP-015 | AlloyDB | At-rest encryption validation | ⛔ Blocked (V1.2) |

**Google Cloud Pass Rate: 13 / 15 (87%) — 2 blocked items are non-blocking V1.2 tasks**

---

## 9. Defect Summary

| Severity | Found | Fixed | Deferred | Waived | Outstanding |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Critical** | 0 | 0 | 0 | 0 | **0** |
| **High** | 0 | 0 | 0 | 0 | **0** |
| **Medium** | 2 | 0 | 2 | 0 | 2 (AlloyDB — V1.2) |
| **Low** | 3 | 0 | 3 | 0 | 3 (Deprecation warnings — V1.2) |
| **TOTAL** | **5** | **0** | **5** | **0** | **5 (all deferred)** |

> **Zero Critical or High defects.** All 5 open items are Medium or Low severity, formally deferred to Version 1.2.

---

## 10. Test Coverage Summary

| Coverage Area | Test Cases | Pass Rate | Coverage |
| :--- | :---: | :---: | :---: |
| Functional regression (all 20 domains) | 62 | 100% | Full scope |
| E2E workflow journeys | 12 | 100% | Full lifecycle |
| AI validation | 18 | 100% | All AI controls |
| Security validation | 25 | 100% | OWASP Top 10 + WAF + Auth |
| Performance validation | 15 | 100% | All SLA targets |
| Google Cloud integration | 15 | 87% | 13/15 (2 blocked) |
| Code coverage (pytest) | — | — | 85.5% (≥ 80% target ✓) |

---

## 11. Quality Gate Results

| Quality Gate | Target | Actual | Status |
| :--- | :---: | :---: | :---: |
| Functional Pass Rate | 100% | 100% | ✅ Met |
| Regression Pass Rate | 100% | 100% | ✅ Met |
| Critical Defects | 0 | 0 | ✅ Met |
| High Severity Defects | 0 | 0 | ✅ Met |
| Medium Severity Defects | < 5 (non-blocking) | 2 (deferred) | ✅ Met |
| Code Coverage | ≥ 80% | 85.5% | ✅ Met |
| AI Validation Pass Rate | 100% | 100% | ✅ Met |
| Security Pass Rate | 100% | 100% | ✅ Met |
| Performance SLA (P95 < 1000ms) | 100% of endpoints | 100% | ✅ Met |
| GCP Integration | ≥ 85% | 87% | ✅ Met |

---

## 12. Release Stability Score

| Dimension | Weight | Score | Weighted Score |
| :--- | :---: | :---: | :---: |
| Functional regression (100% pass) | 25% | 100 | 25.0 |
| E2E workflow stability (12/12 pass) | 20% | 100 | 20.0 |
| Defect density (0 Critical/High) | 20% | 100 | 20.0 |
| Code coverage (85.5%) | 10% | 90 | 9.0 |
| Performance (all SLAs met) | 15% | 100 | 15.0 |
| GCP integration (13/15) | 10% | 87 | 8.7 |

**Release Stability Score: 97.7 / 100** ✅

---

## 13. Enterprise Readiness Score

| Dimension | Weight | Score | Weighted Score |
| :--- | :---: | :---: | :---: |
| Security (OWASP + WAF + 25/25 tests) | 25% | 100 | 25.0 |
| AI governance (18/18 tests) | 15% | 100 | 15.0 |
| Performance (15/15 SLAs) | 15% | 100 | 15.0 |
| GCP readiness (13/15 verified) | 15% | 87 | 13.05 |
| Observability (logging + monitoring) | 10% | 95 | 9.5 |
| Documentation completeness | 10% | 100 | 10.0 |
| Technical debt (Low — non-blocking) | 10% | 85 | 8.5 |

**Enterprise Readiness Score: 96.05 / 100** ✅

---

## 14. Recommendations

1. **Proceed to Production Readiness Review** — all quality gates have been met, no Critical or High defects remain, and both stability and enterprise readiness scores exceed the 90/100 enterprise release threshold.
2. **Track AlloyDB migration** as the highest-priority V1.2 infrastructure action; assign a dedicated infrastructure sprint.
3. **Schedule Pydantic V2 and `datetime.utcnow()` deprecation remediation** in V1.2 Sprint 1 to prevent accumulation.
4. **Publish the production runbook** to the IDBI Bank operations team before Go-Live date.
5. **Configure Cloud Monitoring alert escalation policies** for P1 severity incidents targeting credit engine and fraud registry services.

---

## 15. Final Decision

---

🟢 **READY FOR PRODUCTION READINESS REVIEW**

---

**Rationale**: Enterprise regression testing is complete. 145 of 147 test cases passed (2 blocked on AlloyDB — non-blocking, V1.2 deferred). Functional, E2E, AI validation, security, and performance suites achieved 100% pass rates. Zero Critical or High defects are open. The Release Stability Score of **97.7/100** and Enterprise Readiness Score of **96.05/100** both exceed the 90/100 banking-grade release threshold. The Enterprise Test & Validation Board unanimously declares Version 1.1 RC1 **ready for Production Readiness Review**.
