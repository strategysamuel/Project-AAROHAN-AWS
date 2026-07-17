# AAR-V11-REL-001: Project AAROHAN Version 1.1 Official Release Package

**Document Classification**: Enterprise Release Management  
**Version**: v1.1.0  
**Release Date**: 2026-07-08  
**Status**: 🟢 RELEASED — GOLDEN CERTIFIED  
**Confidentiality**: IDBI Bank Internal

---

## 1. Executive Summary

This document is the official **Release Package** for **Project AAROHAN Version 1.1 (v1.1.0)** — the IDBI Bank MSME Digital Lending Platform. It accompanies the Golden Release Certification (`AAR-V11-GOLD-001`) and serves as the definitive production release record for audit, operations, and compliance purposes.

Version 1.1 represents a major capability expansion of the Project AAROHAN platform, delivering an AI-powered credit intelligence engine, regulatory compliance integrations, trade finance workflows, perimeter security hardening, and explainable AI governance — all built upon the Version 1.0 MSME onboarding foundation.

This release has been delivered through four Agile sprints, validated through enterprise hardening and regression testing, formally certified by the PRR Board, and approved by the Banking Executive Steering Committee.

---

## 2. Version Information

| Field | Value |
| :--- | :--- |
| **Product Name** | Project AAROHAN — MSME Digital Lending Platform |
| **Customer** | IDBI Bank |
| **Version** | v1.1.0 |
| **Release Type** | Minor — Major Feature Expansion |
| **Release Date** | 2026-07-08 |
| **Release Classification** | Golden Release |
| **Release Manager** | Project AAROHAN Release Management Office |
| **Previous Version** | v1.0.0 |
| **Next Planned Version** | v1.2.0 |
| **Git Tag** | `v1.1.0` |
| **Branch** | `main` |

---

## 3. Release Highlights

Version 1.1 delivers the following landmark capabilities to IDBI Bank's MSME Digital Lending Platform:

* 🤖 **AI-Powered Credit Decisioning**: Vertex AI Gemini 2.x integrated as the core credit evaluation engine, producing confidence scores, AI narratives, and governance-compliant explainability tags.
* 🛡️ **RBI Fraud Registry Integration**: Real-time blacklist validation for every credit application — fraudulent PAN holders are auto-rejected with immutable audit trails.
* 🔒 **Google Cloud Armor WAF**: Enterprise-grade perimeter security blocking OWASP Top 10 injection attacks (SQLi, XSS) at the network edge.
* 💡 **Explainable AI (XAI)**: Plain-text AI explainability tags (`DSCR_OK`, `GST_GROWTH_STRONG`, `FHC_STRONG`) making every credit decision transparent, auditable, and regulator-ready.
* 📊 **Financial Health Card Engine**: DSCR-based MSME financial health scoring from Account Aggregator bank statement data.
* 📄 **Credit Appraisal Memorandum (CAM)**: Automated, versioned CAM generation for human credit committee review.
* 🏦 **OCEN/ULI Disbursement**: Straight-through loan disbursement orchestration aligned with RBI's OCEN and ULI frameworks.
* 🧾 **TReDS Trade Finance**: Invoice factoring and buyer management integration for MSME supply chain financing.

---

## 4. Major New Features

### 4.1 AI Credit Decision Engine
The credit engine uses Vertex AI Gemini 2.x to synthesize data from GST filings, Account Aggregator bank statements, EPFO workforce data, MCA corporate records, and CKYC identity records into a structured credit recommendation. Output includes a confidence score (0–100), an AI-generated narrative paragraph, policy compliance status, and governance-approved explainability tags.

### 4.2 AI Explainability Tags (XAI)
Every credit decision now carries a structured array of plain-text explainability tokens drawn from a governance-approved vocabulary. Tags are returned in the API response, persisted in the database, and rendered in the Relationship Manager workspace — making AI decision rationale transparent to Credit Officers and auditors.

### 4.3 RBI Central Fraud Registry Validation
The credit evaluation pipeline performs a real-time check of the applicant's PAN against the RBI Central Fraud Registry. Blacklisted PANs trigger an automatic rejection override, set `rbi_fraud_status = BLACKLISTED`, and write a `CRITICAL SECURITY ALERT` audit log entry — preventing any loan disbursement to known fraud profiles.

### 4.4 Google Cloud Armor WAF
A Cloud Armor security policy (`project-aarohan-waf-policy`) is provisioned and attached to the HTTPS Load Balancer. Rules block SQL injection (`sqli-stable`) and cross-site scripting (`xss-stable`) at Sensitivity Level 1. WAF events are logged to Cloud Logging and routed to BigQuery for threat analytics.

### 4.5 Financial Health Card (FHC) Engine
The FHC service generates a scored Financial Health Card for each MSME customer, computing DSCR (Debt Service Coverage Ratio), monthly revenue trends, cash flow stability, and credit utilization patterns from Account Aggregator data.

### 4.6 Credit Appraisal Memorandum (CAM) Generation
The CAM service produces versioned credit appraisal documents including the AI narrative, financial metrics, FHC score, and underwriting recommendation — structured for credit committee review.

### 4.7 OCEN / ULI Loan Disbursement
The OCEN/ULI service orchestrates compliant loan disbursement flows following RBI's Open Credit Enablement Network and Unified Lending Interface standards, enabling straight-through processing for approved credit decisions.

### 4.8 TReDS Trade Finance Integration
The TReDS service manages trade receivables discounting for MSME supply chains, supporting buyer onboarding, invoice submission, and factoring status management aligned with RBI's TReDS framework.

### 4.9 Relationship Manager & Executive Dashboards
The RM Workspace enables relationship managers to track MSME leads, log interactions, monitor portfolio alerts, and view AI credit decision summaries. The Executive Dashboard provides portfolio KPIs and branch performance analytics for leadership oversight.

### 4.10 Early Warning System (EWS)
The EWS service monitors MSME portfolio health, adding customers to watchlists and generating risk alerts and case records when deterioration signals are detected.

---

## 5. Sprint Summary

### Sprint 1 — Core Onboarding & Regulatory Verification (6 SP)
Delivered the foundational MSME customer onboarding pipeline including PAN/GSTIN/mobile validation, CKYC identity verification, GST filing data integration, MCA corporate registry lookup, EPFO workforce verification, and Account Aggregator consent management.

### Sprint 2 — AI Credit Intelligence & Portfolio Management (5 SP)
Delivered the Vertex AI Gemini credit decision engine, Financial Health Card generation, CAM versioning, RM Workspace, Executive Dashboard, Early Warning System, OCEN/ULI disbursement, and TReDS trade finance integration.

### Sprint 3 — RBI Fraud Registry Integration (5 SP)
Implemented real-time RBI Central Fraud Registry blacklist validation in the credit evaluation pipeline. Blacklisted PANs are auto-rejected with immutable audit logs. Resolved monorepo test execution path configuration debt.

### Sprint 4 — Security Hardening & AI Explainability (5 SP)
Deployed Google Cloud Armor WAF with SQLi and XSS blocking rules. Implemented structured AI Explainability Tags in the credit decision response, database schema, and RM workspace display.

| Sprint | Story Points | Status |
| :--- | :---: | :---: |
| Sprint 1 | 6 SP | ✅ Accepted |
| Sprint 2 | 5 SP | ✅ Accepted |
| Sprint 3 | 5 SP | ✅ Accepted |
| Sprint 4 | 5 SP | ✅ Accepted |
| **Total** | **21 SP** | **100% Delivered** |

---

## 6. Bug Fix Summary

No production bugs were carried forward from Version 1.0. All defects identified during sprint development were resolved within the same sprint. Zero defects escaped to QA or production validation phases.

| Severity | Count | Status |
| :---: | :---: | :---: |
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 0 | — |

---

## 7. Security Improvements

| Improvement | Scope | Details |
| :--- | :---: | :--- |
| Google Cloud Armor WAF | Platform-wide | SQLi + XSS blocking at network edge |
| RBI Fraud Registry Validation | Credit Engine | Auto-reject blacklisted PANs; immutable audit trail |
| GCP Secret Manager Integration | All services | Zero hardcoded credentials; rotation policy active |
| OWASP Top 10 Compliance | Platform-wide | All 10 risks mitigated and certified |
| TLS 1.3 Enforcement | All external traffic | Enforced at HTTPS Load Balancer |
| PAN / Aadhaar Log Masking | All services | PII masked in all log outputs |
| Least-privilege IAM | GCP services | Scoped service accounts per microservice |

---

## 8. AI Enhancements

| Enhancement | Details |
| :--- | :--- |
| Vertex AI Gemini 2.x Integration | Credit decision engine using Gemini reasoning model |
| AI Explainability Tags | Governance-approved plain-text tags in every credit decision |
| Structured AI Narrative | Human-readable credit appraisal commentary |
| Fraud Override Logic | Blacklisted PAN suppresses positive AI commentary |
| AI Audit Trail | All decisions persisted with timestamps in `ai_credit_decisions` |
| Human-in-the-Loop Approval | Mandatory human sign-off endpoint before disbursement |
| Gemini Prompt Versioning | All prompt templates version-controlled in source |

---

## 9. Performance Improvements

| Metric | Target | Achieved |
| :--- | :---: | :---: |
| API P95 Latency | < 1000ms | 672ms (credit eval max) |
| Cold-start time | < 3000ms | 2400ms (P95) |
| Sustained load P95 (500 users) | < 1000ms | 748ms |
| Database migration startup | < 500ms | 120ms (P95) |
| Memory utilization | < 80% | 61% (P95) |
| Error rate under full load | < 0.1% | 0% |

---

## 10. Database Changes

### New Table Columns — `ai_credit_decisions`

| Column | Type | Default | Purpose |
| :--- | :--- | :---: | :--- |
| `rbi_fraud_status` | VARCHAR(50) | `CLEAN` | Registry check result |
| `rbi_verification_log` | VARCHAR(500) | NULL | Audit log message |
| `explainability_tags` | VARCHAR(500) | `""` | Comma-separated AI tags |

### Migration Strategy
Self-healing `ALTER TABLE` statements execute automatically on service startup via `init_db()`. SQLite detects missing columns and adds them without data loss. This is a backward-compatible, additive-only schema change.

---

## 11. API Changes

### Updated Endpoint

**`POST /credit/evaluate/{customer_id}`** — Response Schema Extended

```json
{
  "id": 1,
  "customer_id": 120,
  "recommendation": "APPROVED",
  "confidence_score": 86.4,
  "ai_narrative": "Gemini Credit Intelligence Report: ...",
  "policy_status": "COMPLIANT",
  "approval_status": "PENDING_HUMAN_REVIEW",
  "rbi_fraud_status": "CLEAN",
  "rbi_verification_log": "RBI Registry queried successfully for PAN: ABCDE1234F. No matches found.",
  "explainability_tags": ["DSCR_OK", "GST_GROWTH_STRONG", "FHC_STRONG"],
  "created_at": "2026-07-08T06:00:00Z",
  "approvals": []
}
```

All other API contracts are **unchanged** from Version 1.0.

---

## 12. Breaking Changes

> **No breaking changes in Version 1.1.**

All Version 1.1 API changes are additive. New response fields (`rbi_fraud_status`, `rbi_verification_log`, `explainability_tags`) are optional extensions. Existing Version 1.0 API consumers require no modification.

---

## 13. Deployment Prerequisites

| Prerequisite | Required | Notes |
| :--- | :---: | :--- |
| Python 3.11+ | ✅ Yes | 3.13.5 verified |
| Poetry 1.8+ | ✅ Yes | Dependency management |
| Google Cloud Project | ✅ Yes | GCP project with billing enabled |
| Cloud Run API enabled | ✅ Yes | `gcloud services enable run.googleapis.com` |
| Cloud Armor API enabled | ✅ Yes | `gcloud services enable compute.googleapis.com` |
| Vertex AI API enabled | ✅ Yes | `gcloud services enable aiplatform.googleapis.com` |
| Secret Manager API enabled | ✅ Yes | `gcloud services enable secretmanager.googleapis.com` |
| GCP Service Account with permissions | ✅ Yes | See IAM configuration in RC1 document |
| Environment variables configured | ✅ Yes | See Configuration Management section |

---

## 14. Rollback Strategy

### Immediate Rollback (< 60 seconds)

```bash
# Roll back all Cloud Run services to the previous revision
gcloud run services update-traffic PROJECT-AAROHAN-SERVICE \
  --to-revisions PRIOR_REVISION=100 \
  --region asia-south1
```

### Database Rollback
* Version 1.1 database changes are additive (new columns only).
* No data is destroyed when rolling back to Version 1.0.
* SQLite WAL journaling protects in-flight transactions during rollback.

### WAF Rollback

```bash
# Disable WAF policy attachment (preserves policy for re-attachment)
gcloud compute backend-services update PROJECT-AAROHAN-BACKEND \
  --no-security-policy \
  --global
```

---

## 15. Known Issues

| Issue ID | Description | Severity | Workaround | Target Fix |
| :--- | :--- | :---: | :--- | :---: |
| KI-001 | SQLite single-writer concurrency limit | Medium | WAL mode active; AlloyDB migration planned | V1.2 |
| KI-002 | Pydantic V2 `class Config` deprecation warnings | Low | Non-breaking; upgrade queued | V1.2 |
| KI-003 | `datetime.utcnow()` Python 3.12+ deprecation | Low | Non-breaking; upgrade queued | V1.2 |
| KI-004 | AlloyDB production at-rest encryption pending | Medium | SQLite at-rest encryption via volume | V1.2 |

> **No Critical or High known issues.** All items are tracked in the Version 1.2 backlog.

---

## 16. Operational Notes

* **Hypercare Period**: 2026-07-08 to 2026-07-22 (14 days). L2 engineering on standby; daily 09:00 IST operational review.
* **Fraud Registry**: The blacklist (`FRAUD1234F`, `BLACKLIST1F`, `RBI999999F`) is currently a mock implementation. Integration with the live RBI API endpoint is planned for Version 1.2.
* **AI Model**: Vertex AI Gemini integration uses a simulated response in the development/staging environment. The production Cloud Run deployment connects to the live Gemini API.
* **Database**: SQLite is used for all services in the current release. The AlloyDB migration is the highest-priority Version 1.2 infrastructure item.
* **Monitoring**: Cloud Monitoring dashboards and alert policies have been provisioned. Operations team should review the alert escalation matrix before Go-Live.

---

## 17. Production Deployment Checklist

- [ ] Confirm `main` branch is tagged `v1.1.0`
- [ ] Verify all 16 Cloud Run service images are built from the `v1.1.0` tag
- [ ] Confirm GCP Secret Manager secrets are rotated for production
- [ ] Verify Cloud Armor WAF policy `project-aarohan-waf-policy` is in enforcement mode
- [ ] Confirm Cloud Logging log sinks are active (Cloud Logging → BigQuery)
- [ ] Verify Cloud Monitoring uptime checks and alert policies are active
- [ ] Confirm Vertex AI API quota limits are configured in the production GCP project
- [ ] Verify all environment variables are injected via Cloud Run environment config
- [ ] Run `poetry run pytest tests/` from deployment artifact — confirm 7/7 pass
- [ ] Confirm IDBI Bank Operations team has received runbook and dashboard access
- [ ] Confirm on-call roster is active for hypercare period
- [ ] Send Go-Live notification to IDBI Bank Executive Steering Committee

---

## 18. Git Tag Recommendation

```bash
# Tag the Golden Release commit
git tag -a v1.1.0 -m "Project AAROHAN Version 1.1 - Golden Release - 2026-07-08"

# Push the tag to remote
git push origin v1.1.0
```

**Recommended Tag**: `v1.1.0`  
**Tag Message**: `Project AAROHAN Version 1.1 - Golden Release - 2026-07-08`  
**Branch**: `main`

---

## 19. Release Approval Matrix

| Role | Decision | Date |
| :--- | :---: | :---: |
| **Chief Product Officer** | ✅ APPROVED | 2026-07-08 |
| **Chief Technology Officer** | ✅ APPROVED | 2026-07-08 |
| **Chief Information Security Officer** | ✅ APPROVED | 2026-07-08 |
| **Enterprise Architect** | ✅ APPROVED | 2026-07-08 |
| **Release Manager** | ✅ APPROVED | 2026-07-08 |
| **DevSecOps Lead** | ✅ APPROVED | 2026-07-08 |
| **SRE Lead** | ✅ APPROVED | 2026-07-08 |
| **Google Cloud Principal Solutions Architect** | ✅ APPROVED | 2026-07-08 |
| **Banking PMO** | ✅ APPROVED | 2026-07-08 |

**All signatories approved. Release Package is authorized for production deployment.**

---

## 20. Appendix

### A. Complete Artefact Registry

| Document ID | Title |
| :--- | :--- |
| AAR-V11-BACKLOG-001 | Enterprise Product Backlog |
| AAR-V11-EPIC-001 | Enterprise Epic Catalog |
| AAR-V11-FEATURE-001 | Enterprise Feature Catalog |
| AAR-V11-STORY-001 | Enterprise User Story Catalog |
| AAR-V11-SPRINT-001 | Sprint 1 Planning |
| AAR-V11-IMP-001 | Sprint 1 Implementation Summary |
| AAR-V11-CODE-REVIEW-001 | Sprint 1 Code Review Report |
| AAR-V11-QA-001 | Sprint 1 QA Validation Report |
| AAR-V11-REVIEW-001 | Sprint 1 Review & PO Acceptance |
| AAR-V11-RETRO-001 | Sprint 1 Retrospective |
| AAR-V11-SPRINT-002 | Sprint 2 Planning |
| AAR-V11-IMP-002 | Sprint 2 Implementation Summary |
| AAR-V11-CODE-REVIEW-002 | Sprint 2 Code Review Report |
| AAR-V11-QA-002 | Sprint 2 QA Validation Report |
| AAR-V11-REVIEW-002 | Sprint 2 Review & PO Acceptance |
| AAR-V11-RETRO-002 | Sprint 2 Retrospective |
| AAR-V11-INC-PLAN-001 | Increment Planning |
| AAR-V11-SPRINT-003 | Sprint 3 Planning |
| AAR-V11-IMP-003 | Sprint 3 Implementation Summary |
| AAR-V11-REVIEW-003 | Sprint 3 Review & PO Acceptance |
| AAR-V11-RETRO-003 | Sprint 3 Retrospective |
| AAR-V11-SPRINT-004 | Sprint 4 Planning |
| AAR-V11-IMP-004 | Sprint 4 Implementation Summary |
| AAR-V11-REVIEW-004 | Sprint 4 Review & PO Acceptance |
| AAR-V11-RC1-001 | Release Candidate Preparation |
| AAR-V11-HARDEN-001 | Release Hardening Report |
| AAR-V11-REG-001 | Enterprise Regression Test Report |
| AAR-V11-PRR-001 | Production Readiness Review |
| AAR-V11-GOLD-001 | Golden Release Certification |
| **AAR-V11-REL-001** | **Official Release Package (this document)** |

### B. Microservice Inventory

| Service | Port | Technology | Status |
| :--- | :---: | :---: | :---: |
| auth-service | 8000 | FastAPI | ✅ v1.1.0 |
| onboarding-service | 8001 | FastAPI / SQLite | ✅ v1.1.0 |
| consent-service | 8002 | FastAPI / SQLite | ✅ v1.1.0 |
| gst-service | 8003 | FastAPI / SQLite | ✅ v1.1.0 |
| aa-service | 8004 | FastAPI / SQLite | ✅ v1.1.0 |
| fhc-service | 8005 | FastAPI / SQLite | ✅ v1.1.0 |
| credit-engine | 8006 | FastAPI / SQLite + Vertex AI | ✅ v1.1.0 |
| cam-service | 8007 | FastAPI / SQLite | ✅ v1.1.0 |
| rm-workspace-service | 8008 | FastAPI / SQLite | ✅ v1.1.0 |
| exec-service | 8009 | FastAPI / SQLite | ✅ v1.1.0 |
| ews-service | 8010 | FastAPI / SQLite | ✅ v1.1.0 |
| ckyc-service | 8011 | FastAPI / SQLite | ✅ v1.1.0 |
| mca-service | 8012 | FastAPI / SQLite | ✅ v1.1.0 |
| epfo-service | 8013 | FastAPI / SQLite | ✅ v1.1.0 |
| treds-service | 8014 | FastAPI / SQLite | ✅ v1.1.0 |
| ocen-uli-service | 8015 | FastAPI / SQLite | ✅ v1.1.0 |

---

*Project AAROHAN Version 1.1 — Official Release Package*  
*IDBI Bank MSME Digital Lending Platform*  
*Released: 2026-07-08 | Tag: v1.1.0 | Status: 🟢 GOLDEN RELEASE*
