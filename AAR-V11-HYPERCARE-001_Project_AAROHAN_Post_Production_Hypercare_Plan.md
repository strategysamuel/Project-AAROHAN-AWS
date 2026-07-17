# AAR-V11-HYPERCARE-001: Project AAROHAN Post-Production Hypercare & Operations Plan

**Document Classification**: Enterprise Production Operations  
**Version**: 1.0  
**Status**: 🟢 ACTIVE — HYPERCARE IN EFFECT  
**Release Version**: v1.1.0  
**Hypercare Start Date**: 2026-07-08  
**Hypercare End Date**: 2026-07-22  
**Confidentiality**: IDBI Bank Internal

---

## 1. Executive Summary

This document defines the official **Post-Production Hypercare and Operations Plan** for **Project AAROHAN Version 1.1 (v1.1.0)**, the IDBI Bank MSME Digital Lending Platform. Following the Golden Release Certification (`AAR-V11-GOLD-001`) and issuance of the Official Release Package (`AAR-V11-REL-001`), this plan governs all production support, monitoring, incident management, and knowledge transfer activities for the 14-day hypercare window and the subsequent transition to Business-as-Usual (BAU) operations.

During hypercare, the Project AAROHAN engineering team and IDBI Bank Operations team operate in a co-support model with elevated monitoring, rapid incident response SLAs, and daily operational stand-ups. At the conclusion of hypercare, full operational ownership is transferred to IDBI Bank's BAU Production Support team.

---

## 2. Hypercare Objectives

| Objective | Success Criterion |
| :--- | :--- |
| Ensure zero P1 production incidents during hypercare | 0 P1 incidents in 14-day window |
| Validate all SLAs under live production traffic | All P95 latencies within target throughout |
| Transfer operational knowledge to IDBI Bank Ops team | Knowledge transfer sign-off by 2026-07-20 |
| Identify and document any operational anomalies | All anomalies logged and triaged within 4 hours |
| Confirm fraud registry validation functioning in production | 100% fraud check coverage on all credit evaluations |
| Confirm Cloud Armor WAF protecting production traffic | Zero WAF bypass incidents |
| Validate AI credit decisions under real MSME applicant data | Decision audit trail verified |
| Formally close hypercare and initiate BAU transition | BAU sign-off by 2026-07-22 |

---

## 3. Hypercare Duration

| Phase | Period | Activity |
| :--- | :--- | :--- |
| **Week 1 — High Intensity** | 2026-07-08 to 2026-07-14 | 24/7 on-call; daily stand-ups; elevated monitoring |
| **Week 2 — Stabilization** | 2026-07-15 to 2026-07-21 | Business-hours primary support; on-call for P1/P2 |
| **Closure Day** | 2026-07-22 | Hypercare review; BAU handover ceremony; sign-off |

**Total Hypercare Duration**: 14 calendar days (2026-07-08 to 2026-07-22)

---

## 4. Production Support Model

### 4.1 Co-Support Model (Hypercare)

| Tier | Team | Responsibility | Coverage |
| :---: | :--- | :--- | :---: |
| **L1** | IDBI Bank Operations | First-line monitoring; alerting; ticket triage | 24/7 |
| **L2** | Project AAROHAN Engineering | Investigation; hotfix assessment; configuration changes | 24/7 (Week 1); Business hours (Week 2) |
| **L3** | Google Cloud Professional Services | GCP infrastructure incidents; Vertex AI issues | On-call SLA < 1 hour |

### 4.2 Daily Operating Rhythm

| Activity | Time (IST) | Participants |
| :--- | :---: | :--- |
| Morning Operational Stand-up | 09:00 | IDBI Ops + AAROHAN Engineering + SRE Lead |
| Cloud Monitoring Dashboard Review | 09:15 | SRE Lead + Google Cloud Ops |
| Evening Incident Summary | 18:00 | IDBI Ops + AAROHAN Engineering |
| On-call Handover | 22:00 | On-call rotation handover |

### 4.3 Communication Channels

| Channel | Purpose |
| :--- | :--- |
| Primary Incident Bridge | P1/P2 incident war room (dedicated video/phone) |
| Operations Chat Channel | Daily updates; non-critical communications |
| Incident Tracker | JIRA / ServiceNow ticket management |
| Email Distribution | Executive escalation and status updates |

---

## 5. Incident Management Process

### 5.1 Incident Lifecycle

```
Detected → Triaged → Classified → Assigned → Investigated → Resolved → Post-Mortem
```

| Stage | Action | Owner | SLA |
| :--- | :--- | :--- | :---: |
| **Detection** | Alert fires in Cloud Monitoring or L1 observation | L1 Ops | Immediate |
| **Triage** | Confirm validity; gather initial context | L1 Ops | < 5 min |
| **Classification** | Assign severity P1–P4 | L1 + L2 | < 10 min |
| **Assignment** | Route to appropriate resolver team | L1 Ops | < 5 min |
| **Investigation** | Root cause analysis; impact assessment | L2 Engineering | Per SLA |
| **Resolution** | Apply fix or workaround; confirm recovery | L2 Engineering | Per SLA |
| **Post-Mortem** | P1/P2 incidents require 48-hour post-mortem | SRE Lead | < 48 hours |

---

## 6. Severity Classification

| Severity | Definition | Examples |
| :---: | :--- | :--- |
| **P1 — Critical** | Complete service unavailability or data loss affecting lending operations | All microservices down; fraud registry not responding; loan disbursements failing |
| **P2 — High** | Core feature degraded; significant business impact | Credit engine returning errors; WAF blocking legitimate traffic; AI decisions timing out |
| **P3 — Medium** | Non-core feature degraded; moderate business impact | Executive dashboard slow; RM Workspace partial failure; EWS alerts delayed |
| **P4 — Low** | Minor issue; no business impact | Cosmetic UI issue; log formatting anomaly; non-critical deprecation warning |

---

## 7. Escalation Matrix

| Severity | Response Target | L1 Action | L2 Escalation | L3 Escalation | Executive Notification |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **P1** | 15 min | Immediately notify L2; open incident bridge | Engage SRE Lead within 15 min | GCP PS if GCP root cause (within 30 min) | CTO + CISO within 30 min |
| **P2** | 30 min | Open ticket; notify L2 | Engage within 30 min | GCP PS if required | Engineering Manager within 1 hour |
| **P3** | 4 hours | Open ticket; assign to L2 | Engage during business hours | — | Weekly summary report |
| **P4** | Next business day | Open ticket | Assign to dev team | — | Monthly summary report |

### 7.1 Escalation Contacts

| Role | Contact Trigger |
| :--- | :--- |
| SRE Lead | All P1/P2 incidents |
| DevSecOps Lead | Any security incident or WAF anomaly |
| AI Engineering Lead | Credit engine failures or AI decision anomalies |
| Google Cloud Operations Lead | Any GCP service degradation |
| CTO | P1 incidents; any incident with banking compliance impact |
| CISO | Any security breach, PII exposure, or fraud system failure |

---

## 8. Monitoring Strategy

### 8.1 Core Monitoring Principles

* **Observe, Don't Poll**: All monitoring driven by Cloud Monitoring alert policies — no manual polling.
* **Signal Before Impact**: SLO-based alerting triggers before SLA thresholds are breached.
* **Correlated Observability**: Logs, metrics, and traces correlated via Cloud Logging + Cloud Trace for rapid root cause identification.

### 8.2 Monitoring Coverage

| Layer | Tool | Coverage |
| :--- | :---: | :--- |
| Infrastructure | Cloud Monitoring | CPU, memory, instance count, cold-start times |
| API layer | Cloud Monitoring + Custom metrics | Request rate, latency (P50/P95/P99), error rate |
| Application | Cloud Logging | Structured audit logs; exception stack traces |
| AI/ML | Cloud Logging + Custom dashboard | Credit decision volume; tag distribution; timeout rate |
| Security | Cloud Armor logs + BigQuery | WAF block events; attack pattern analysis |
| Database | SQLite WAL metrics | Write queue depth; connection errors |

---

## 9. Google Cloud Monitoring

### 9.1 Alert Policies Configured

| Alert Policy | Threshold | Notification Channel |
| :--- | :---: | :--- |
| API P95 latency > 800ms (credit engine) | 3 consecutive minutes | Ops Channel + SRE Lead |
| Cloud Run error rate > 1% | 5 consecutive minutes | Ops Channel + SRE Lead |
| Cloud Run instance count at max (10) | Immediate | SRE Lead + Engineering Manager |
| Cloud Armor blocked requests spike | > 100/min | DevSecOps Lead + CISO |
| Vertex AI API timeout rate > 5% | 3 consecutive minutes | AI Engineering Lead + SRE Lead |
| Service uptime check failure | 2 consecutive failures | L1 Ops + SRE Lead |

### 9.2 Dashboard Suite

* **Operations Dashboard**: Service health, request rates, latency, error rates across all 16 microservices.
* **Security Dashboard**: Cloud Armor WAF events, blocked requests by rule, attack source heatmap.
* **AI Dashboard**: Credit decision volume, recommendation distribution, explainability tag frequency, timeout rate.
* **Business Dashboard**: New customer registrations, credit approvals vs. rejections, fraud matches, loan disbursements.

---

## 10. AI Monitoring

| Metric | Target | Alert Threshold |
| :--- | :---: | :---: |
| Credit evaluation success rate | > 99% | < 98% |
| AI response timeout rate | < 1% | > 3% |
| Fraud registry match rate | Operational (no target) | Registry query failure > 0% |
| Explainability tag parse success | 100% | < 100% |
| Human approval queue depth | < 100 pending | > 500 pending |
| APPROVED recommendation rate | Baseline ± 15% | Significant deviation |

**AI Anomaly Protocol**: Any statistically significant shift in recommendation distribution (e.g., sudden spike in REJECTED decisions) triggers an immediate L2 AI Engineering investigation to rule out model drift, data quality issues, or configuration errors.

---

## 11. Performance Monitoring

| KPI | Baseline (Regression) | Production Alert Threshold |
| :--- | :---: | :---: |
| Credit evaluation P95 latency | 672ms | > 850ms |
| Customer onboarding P95 latency | 118ms | > 500ms |
| OCEN disbursement P95 latency | 890ms | > 1500ms |
| Cloud Run cold-start time | 2400ms | > 2800ms |
| Memory utilization | 61% | > 75% |
| Error rate | 0% | > 0.5% |

---

## 12. Security Monitoring

| Security Event | Monitoring Source | Response |
| :--- | :---: | :--- |
| WAF block event (SQLi/XSS) | Cloud Armor logs | Log; analyse pattern; no action if isolated |
| WAF block rate spike (> 100/min) | Cloud Monitoring alert | DevSecOps investigation within 15 min |
| Fraud registry match | Application audit log | Automatic; verify audit trail written |
| Fraud registry service failure | Cloud Monitoring | P1 incident; credit evaluations suspended |
| Authentication failure spike | Cloud Logging | L2 investigation within 30 min |
| Secret rotation due | Secret Manager policy | DevSecOps rotates per schedule |

---

## 13. Operational KPIs

| KPI | Measurement Period | Target |
| :--- | :---: | :---: |
| Production availability | Monthly | ≥ 99.9% |
| Mean Time to Detect (MTTD) | Per incident | < 5 minutes |
| Mean Time to Resolve (MTTR) P1 | Per incident | < 2 hours |
| Mean Time to Resolve (MTTR) P2 | Per incident | < 8 hours |
| Zero P1 incidents (hypercare) | 14-day window | 0 P1 incidents |
| API P95 latency compliance | Daily | 100% of endpoints within SLA |
| Fraud registry operational | Daily | 100% uptime |
| WAF blocking rate (false positives) | Weekly | < 0.1% |

---

## 14. SLA Targets

| Service | Availability SLA | P95 Latency SLA | Support Hours |
| :--- | :---: | :---: | :---: |
| MSME Customer Onboarding | 99.9% | < 200ms | 24/7 |
| AI Credit Decision Engine | 99.9% | < 1000ms | 24/7 |
| Fraud Registry Validation | 99.95% | < 500ms | 24/7 |
| Loan Disbursement (OCEN/ULI) | 99.9% | < 2000ms | 24/7 |
| RM Workspace | 99.5% | < 1000ms | Business hours |
| Executive Dashboard | 99.5% | < 2000ms | Business hours |
| TReDS Trade Finance | 99.9% | < 1000ms | Business hours |

---

## 15. Backup Strategy

| Data Type | Backup Method | Frequency | Retention | Recovery Target |
| :--- | :---: | :---: | :---: | :---: |
| SQLite database files | Cloud Storage bucket sync | Every 6 hours | 30 days | RPO < 6 hours |
| Cloud Logging export | BigQuery log sink | Continuous | 90 days | Immutable |
| GCP Secret Manager | Version history | Per change | Indefinite | Immediate |
| Cloud Run container images | Artifact Registry | Per deployment | 10 versions | Immediate |
| Terraform state | GCS remote state | Per apply | Versioned | Immediate |

---

## 16. Disaster Recovery Validation

### 16.1 DR Scenarios and Targets

| Scenario | RTO | RPO | Validation Status |
| :--- | :---: | :---: | :---: |
| Single Cloud Run instance failure | < 2 min | 0 | ✅ Verified (autoscale) |
| Multi-service failure | < 5 min | 0 | ✅ Verified (redeploy) |
| Cloud Run revision rollback | < 60 sec | 0 | ✅ Verified |
| Full data restore from backup | < 4 hours | < 6 hours | 🔄 Drill scheduled Week 3 |
| WAF policy re-provision | < 30 min | N/A | ✅ Verified (Terraform) |
| Fraud registry fallback | < 1 min | N/A | ✅ Verified (fallback status) |

### 16.2 DR Drill Schedule

* **Full Failover Drill**: Scheduled for 2026-07-25 (Week 3 post hypercare), conducted in the staging environment.
* **Data Restore Drill**: Scheduled for 2026-07-28, validating SQLite backup restoration from Cloud Storage.

---

## 17. Operational Risks

| Risk ID | Description | Likelihood | Impact | Mitigation |
| :--- | :--- | :---: | :---: | :--- |
| OR-001 | SQLite write contention under high concurrent MSME applications | Low | High | WAL mode active; AlloyDB migration in V1.2 |
| OR-002 | Vertex AI API quota exhaustion at MSME loan season peak | Low | Medium | Retry + timeout fallback + quota increase request filed |
| OR-003 | Fraud registry mock replaced by live RBI API — integration gap | Medium | High | Mock clearly documented; live integration in V1.2 roadmap |
| OR-004 | On-call engineer unavailability during hypercare | Low | High | Secondary on-call roster confirmed for all shifts |
| OR-005 | WAF rule false positive on newly onboarded enterprise client | Low | Medium | Exception-list process documented; 15-min resolution SLA |

---

## 18. Knowledge Transfer

### 18.1 Knowledge Transfer Plan

| Topic | Format | Owner | Target Audience | Completion |
| :--- | :---: | :--- | :--- | :---: |
| Platform Architecture Overview | Workshop | Enterprise Architect | IDBI Ops Team | 2026-07-10 |
| Cloud Monitoring Dashboard Walkthrough | Hands-on session | SRE Lead | IDBI Ops Team | 2026-07-10 |
| Incident Response Runbook Training | Tabletop exercise | SRE Lead | IDBI Ops + L1 | 2026-07-11 |
| Cloud Run Deployment & Rollback | Hands-on lab | DevOps Lead | IDBI Ops Team | 2026-07-12 |
| AI Credit Engine Operations | Presentation | AI Engineering Lead | IDBI Ops + Risk | 2026-07-13 |
| WAF Configuration & Management | Workshop | DevSecOps Lead | IDBI Ops + Security | 2026-07-14 |
| Secret Rotation Procedure | Hands-on | DevSecOps Lead | IDBI Ops Team | 2026-07-14 |
| Fraud Registry Operations & Fallback | Presentation | AI Engineering Lead | IDBI Ops + Risk | 2026-07-15 |

### 18.2 Knowledge Transfer Artefacts Delivered

* Production Runbook (all 16 services)
* Cloud Monitoring dashboard access and orientation guide
* Incident escalation matrix with contact details
* Backup and restore procedure guide
* WAF rule management guide
* Secret rotation SOP

---

## 19. Transition to Business-as-Usual (BAU)

### 19.1 BAU Transition Criteria

The following criteria must be satisfied before hypercare is formally closed and BAU ownership transfers to IDBI Bank:

| Criterion | Target | Status |
| :--- | :---: | :---: |
| Zero P1 incidents during hypercare | 0 | ✅ Target |
| All SLA targets met throughout hypercare | 100% endpoints | ✅ Target |
| Knowledge transfer sessions completed | 8/8 sessions | 🔄 In Progress |
| IDBI Ops team runbook sign-off | Signed | 🔄 Scheduled 2026-07-20 |
| Cloud Monitoring dashboard access verified | Confirmed | 🔄 Scheduled 2026-07-10 |
| L1 support team readiness assessment | Passed | 🔄 Scheduled 2026-07-21 |

### 19.2 BAU Support Model (Post-Hypercare)

| Tier | Team | Responsibility | Coverage |
| :---: | :--- | :--- | :---: |
| **L1** | IDBI Bank Production Support | All monitoring; P1–P4 initial triage | 24/7 |
| **L2** | IDBI Bank Application Support | Investigation; configuration; vendor escalation | Business hours (24/7 for P1) |
| **L3** | Project AAROHAN Engineering (warranty support) | Critical defect fixes only; architecture guidance | On-call (P1 escalation only) |
| **L4** | Google Cloud Professional Services | GCP infrastructure incidents | Per GCP SLA |

### 19.3 BAU Transition Date

**Formal BAU Transition**: **2026-07-22**  
**BAU Governance Body**: IDBI Bank IT Operations Committee  
**Warranty Support Period**: 90 days post-release (until 2026-10-06)

---

## 20. Executive Approval

| Role | Approval | Date |
| :--- | :---: | :---: |
| **Chief Technology Officer** | ✅ APPROVED | 2026-07-08 |
| **Production Operations Manager** | ✅ APPROVED | 2026-07-08 |
| **SRE Lead** | ✅ APPROVED | 2026-07-08 |
| **DevSecOps Lead** | ✅ APPROVED | 2026-07-08 |
| **Enterprise Support Manager** | ✅ APPROVED | 2026-07-08 |
| **Google Cloud Operations Lead** | ✅ APPROVED | 2026-07-08 |
| **Banking Production Support Lead** | ✅ APPROVED | 2026-07-08 |

**Hypercare plan is formally activated effective 2026-07-08.**

---

## 21. Appendix

### A. Hypercare Calendar

| Date | Week | Activity |
| :---: | :---: | :--- |
| 2026-07-08 | W1 | Go-Live + Hypercare activation |
| 2026-07-09 | W1 | First 24-hour operational review |
| 2026-07-10 | W1 | Architecture + Monitoring KT sessions |
| 2026-07-11 | W1 | Incident response tabletop exercise |
| 2026-07-12 | W1 | Cloud Run deployment lab |
| 2026-07-13 | W1 | AI credit engine operations session |
| 2026-07-14 | W1 | WAF + Secret management KT |
| 2026-07-15 | W2 | Fraud registry operations session |
| 2026-07-20 | W2 | Runbook sign-off |
| 2026-07-21 | W2 | L1 readiness assessment |
| 2026-07-22 | — | Hypercare closure + BAU handover ceremony |
| 2026-07-25 | Post | DR full-failover drill (staging) |

### B. Quick Reference — P1 Response

```
1. L1 detects alert or observation
2. Open P1 incident ticket immediately
3. Notify SRE Lead and Engineering Manager via incident bridge
4. SRE Lead confirms impact scope within 15 minutes
5. Engage L3 / GCP PS if infrastructure root cause suspected
6. CTO and CISO notified within 30 minutes
7. All-hands resolution; status updates every 30 minutes
8. Resolution confirmed by L1 monitoring for 15 minutes
9. Incident ticket closed; 48-hour post-mortem mandatory
```

### C. Reference Documents

| Document | ID |
| :--- | :--- |
| Official Release Package | AAR-V11-REL-001 |
| Golden Release Certification | AAR-V11-GOLD-001 |
| Production Readiness Review | AAR-V11-PRR-001 |
| Release Hardening Report | AAR-V11-HARDEN-001 |
| Enterprise Regression Test Report | AAR-V11-REG-001 |
