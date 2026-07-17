# AAR-V11-BAU-001: Project AAROHAN Business-as-Usual (BAU) Transition Plan

**Document Classification**: Enterprise IT Service Management  
**Version**: 1.0  
**Status**: 🟢 APPROVED FOR BAU OPERATIONS  
**Effective Date**: 2026-07-22  
**Release Version**: v1.1.0  
**Confidentiality**: IDBI Bank Internal  
**ITIL Alignment**: ITIL 4 Service Transition

---

## 1. Executive Summary

This document constitutes the official **Business-as-Usual (BAU) Transition & Operations Handover Plan** for **Project AAROHAN Version 1.1 (v1.1.0)** — the IDBI Bank MSME Digital Lending Platform. It governs the controlled transition of operational ownership from the Project AAROHAN delivery team to the IDBI Bank IT Operations and Service Management organization, effective **2026-07-22**.

Following a successful 14-day hypercare period (2026-07-08 to 2026-07-22) with zero P1 incidents, all SLA targets met, and all eight knowledge transfer sessions completed, the platform is fully ready for BAU operations. This document defines the ongoing production support model, ITSM processes, SLAs, monitoring strategy, security operations, AI operations governance, patch management, and the Version 1.2 product intake process.

**The Project AAROHAN delivery team will provide 90-day warranty support (until 2026-10-06) for critical defect resolution only.**

---

## 2. Hypercare Exit Criteria

The following criteria have been satisfied, confirming readiness for BAU transition:

| Exit Criterion | Target | Result | Status |
| :--- | :---: | :---: | :---: |
| P1 incidents during hypercare | 0 | 0 | ✅ Met |
| P2 incidents unresolved | 0 | 0 | ✅ Met |
| All SLA targets maintained throughout hypercare | 100% endpoints | 100% | ✅ Met |
| API P95 latency within target | < 1000ms | < 750ms | ✅ Met |
| Fraud registry operational throughout | 100% | 100% | ✅ Met |
| WAF zero false-positive blocking | 0 | 0 | ✅ Met |
| Knowledge transfer sessions completed | 8 / 8 | 8 / 8 | ✅ Met |
| IDBI Ops runbook sign-off | Signed | Signed | ✅ Met |
| Cloud Monitoring access verified | Confirmed | Confirmed | ✅ Met |
| L1 readiness assessment passed | Passed | Passed | ✅ Met |

**All hypercare exit criteria satisfied. BAU transition is approved.**

---

## 3. BAU Entry Criteria

Before BAU is formally activated, the following entry criteria must be confirmed:

| Entry Criterion | Owner | Status |
| :--- | :--- | :---: |
| IDBI Ops team on-call roster live for BAU | Operations Manager | ✅ Ready |
| ITSM tooling (JIRA/ServiceNow) project space configured | ITSM Lead | ✅ Ready |
| All production access credentials transferred | DevSecOps Lead | ✅ Ready |
| Cloud Monitoring dashboard ownership transferred | SRE Lead | ✅ Ready |
| Secret Manager access provisioned for Ops team | DevSecOps Lead | ✅ Ready |
| Runbook documentation published in operations knowledge base | SRE Lead | ✅ Ready |
| Escalation matrix distributed to all support tiers | Service Delivery Manager | ✅ Ready |
| Warranty support SLA agreement signed | CTO + Banking Ops Head | ✅ Ready |

---

## 4. Operations Handover Checklist

| # | Item | Owner | Status |
| :---: | :--- | :--- | :---: |
| 1 | Production Cloud Run access transferred to IDBI Ops | DevOps Lead | ✅ Done |
| 2 | Cloud Monitoring dashboard access granted | SRE Lead | ✅ Done |
| 3 | Cloud Logging access granted | SRE Lead | ✅ Done |
| 4 | BigQuery WAF analytics dataset access granted | GCP Ops Lead | ✅ Done |
| 5 | Secret Manager read access for production secrets | DevSecOps Lead | ✅ Done |
| 6 | Production runbook published to Ops knowledge base | SRE Lead | ✅ Done |
| 7 | Incident escalation contacts updated in ITSM tool | ITSM Lead | ✅ Done |
| 8 | Fraud registry alert notification configured to Ops | DevSecOps Lead | ✅ Done |
| 9 | WAF block rate alert routed to Security Ops | DevSecOps Lead | ✅ Done |
| 10 | GCP IAM service account ownership transferred | GCP Ops Lead | ✅ Done |
| 11 | Backup verification schedule configured in Ops calendar | SRE Lead | ✅ Done |
| 12 | Warranty support SLA agreement executed | CTO | ✅ Done |

---

## 5. Service Ownership Matrix

| Service Component | Business Owner | Technical Owner | Operational Owner |
| :--- | :--- | :--- | :--- |
| MSME Customer Onboarding | IDBI MSME Business Unit | AAROHAN Tech Lead (warranty) | IDBI Ops — Application Support |
| AI Credit Decision Engine | IDBI Credit Risk | AAROHAN AI Engineering Lead (warranty) | IDBI Ops — AI Operations |
| RBI Fraud Registry | IDBI Compliance | AAROHAN Security Lead (warranty) | IDBI Ops — Security Ops |
| Google Cloud Infrastructure | IDBI IT | GCP Solutions Architect (advisory) | IDBI Ops — Cloud Ops |
| Cloud Armor WAF | IDBI CISO | AAROHAN DevSecOps Lead (warranty) | IDBI Ops — Security Ops |
| Financial Health Card Engine | IDBI Credit Risk | AAROHAN Engineering (warranty) | IDBI Ops — Application Support |
| OCEN / ULI Disbursement | IDBI Retail Lending | AAROHAN Engineering (warranty) | IDBI Ops — Application Support |
| TReDS Trade Finance | IDBI MSME Business Unit | AAROHAN Engineering (warranty) | IDBI Ops — Application Support |
| Executive Dashboard | IDBI Leadership | AAROHAN Engineering (warranty) | IDBI Ops — Application Support |

---

## 6. Roles & Responsibilities (RACI)

### RACI Key: R = Responsible | A = Accountable | C = Consulted | I = Informed

| Activity | IDBI L1 Ops | IDBI L2 App Support | AAROHAN Engineering (Warranty) | GCP Ops | SRE Lead | DevSecOps | ITSM Lead | CTO |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| P1 Incident Detection | R | I | I | I | A | I | I | I |
| P1 Incident Resolution | C | R | C | C | A | C | I | I |
| P2 Incident Resolution | C | R | C | — | C | — | I | I |
| Security Incident | I | C | C | — | C | R/A | I | I |
| WAF Rule Update | I | I | C | — | C | R | I | A |
| Secret Rotation | I | I | C | — | — | R/A | I | I |
| Change Approval | I | C | C | C | C | C | R | A |
| Patch Deployment | I | C | R | — | C | C | I | A |
| SLA Reporting | R | C | — | — | A | — | R | I |
| DR Drill Execution | C | R | C | C | A | — | I | I |

---

## 7. Production Support Model

### 7.1 BAU Tiered Support Model

| Tier | Team | Scope | Hours | Escalation SLA |
| :---: | :--- | :--- | :---: | :---: |
| **L1** | IDBI Bank Production Support | Monitoring; alert triage; P1–P4 ticket creation | 24/7 | 5 min to L2 for P1/P2 |
| **L2** | IDBI Application & Cloud Support | Investigation; configuration; GCP management; P1–P3 resolution | 24/7 (P1/P2), Business hours (P3/P4) | 30 min to L3 for P1 |
| **L3 (Warranty)** | Project AAROHAN Engineering | Critical defect fixes; architecture guidance; P1 escalation | On-call (P1 only) | < 1 hour response |
| **L4** | Google Cloud Professional Services | GCP infrastructure failures; Vertex AI outages | Per GCP SLA | GCP SLA |

### 7.2 BAU Support Hours

| Incident Severity | Primary Hours | On-Call |
| :---: | :--- | :---: |
| **P1** | 24/7 | Yes |
| **P2** | 24/7 | Yes |
| **P3** | Business hours (09:00–18:00 IST) | No |
| **P4** | Business hours | No |

---

## 8. Incident Management Process

**ITIL 4 Aligned — Incident Management Practice**

### 8.1 Incident Workflow

```
Alert / User Report → L1 Triage → Severity Classification → Assignment →
Investigation → Workaround / Fix → Resolution → Review → Closure
```

### 8.2 Incident SLA Targets

| Severity | Response Time | Resolution Time | Post-Mortem |
| :---: | :---: | :---: | :---: |
| **P1 — Critical** | 15 minutes | 2 hours | Mandatory (48 hours) |
| **P2 — High** | 30 minutes | 8 hours | Recommended |
| **P3 — Medium** | 4 hours | 2 business days | Optional |
| **P4 — Low** | 1 business day | 5 business days | Not required |

### 8.3 Incident Record Requirements

All incidents must be logged in the ITSM tool with:
* Incident ID, severity, affected service, detection time
* Impact description and affected user count
* Timeline of events and actions taken
* Resolution steps and root cause (P1/P2)
* Linked Change or Problem ticket (where applicable)

---

## 9. Problem Management Process

**ITIL 4 Aligned — Problem Management Practice**

* A **Problem record** is created for any P1 incident or recurring P2 incidents (2+ within 30 days for the same root cause).
* Problem investigations target permanent root cause elimination, not workaround management.
* Known errors are documented in the Known Error Database (KEDB) with available workarounds.
* Problem closure requires evidence of root cause fix or formal risk acceptance.

| Step | Owner |
| :--- | :--- |
| Problem identification | SRE Lead |
| Root cause investigation | L2 + AAROHAN Engineering (warranty) |
| Known error documentation | ITSM Lead |
| Fix implementation | L2 (or warranty team for code defects) |
| Problem closure | Service Delivery Manager |

---

## 10. Change Management Process

**ITIL 4 Aligned — Change Enablement Practice**

### 10.1 Change Categories

| Change Type | Definition | Approval Required | Lead Time |
| :--- | :--- | :---: | :---: |
| **Standard** | Pre-approved, low-risk (config updates, secret rotation) | Pre-approved | Immediate |
| **Normal** | Routine changes (patch deployment, WAF rule update) | Change Advisory Board (CAB) | 5 business days |
| **Emergency** | Critical defect or security hotfix | Emergency CAB (ECAB) | < 2 hours |

### 10.2 Change Advisory Board (CAB) Members

* IDBI IT Operations Manager (Chair)
* IDBI ITSM Lead
* IDBI Security Representative
* Project AAROHAN Technical Lead (warranty — advisory)
* Google Cloud Operations Lead (advisory)

### 10.3 Emergency Change Process

```
Emergency identified → ECAB notified → Risk assessed (< 30 min) →
Approval granted → Change implemented → Post-implementation review within 24 hours
```

---

## 11. Service Level Objectives (SLOs)

| Service | Availability SLO | Latency SLO (P95) | Error Rate SLO |
| :--- | :---: | :---: | :---: |
| MSME Customer Onboarding | 99.9% / month | < 200ms | < 0.5% |
| AI Credit Decision Engine | 99.9% / month | < 1000ms | < 0.5% |
| RBI Fraud Registry Validation | 99.95% / month | < 500ms | < 0.1% |
| Financial Health Card Engine | 99.9% / month | < 500ms | < 0.5% |
| CAM Generation | 99.5% / month | < 1000ms | < 1% |
| OCEN / ULI Disbursement | 99.9% / month | < 2000ms | < 0.5% |
| TReDS Trade Finance | 99.9% / month | < 1000ms | < 0.5% |
| RM Workspace | 99.5% / month | < 1000ms | < 1% |
| Executive Dashboard | 99.5% / month | < 2000ms | < 1% |

---

## 12. Service Level Agreements (SLAs)

### 12.1 BAU Incident SLAs

| Severity | Response | Resolution | Credit (if breached) |
| :---: | :---: | :---: | :---: |
| P1 | 15 min | 2 hours | Formal incident review + root cause report |
| P2 | 30 min | 8 hours | Report to Service Delivery Manager |
| P3 | 4 hours | 2 business days | Tracked in monthly SLA report |
| P4 | 1 business day | 5 business days | Monthly summary |

### 12.2 Platform Availability SLA

* **Platform Availability SLA**: 99.9% monthly uptime for all Tier 1 services.
* **Planned Maintenance Window**: Sundays 02:00–04:00 IST (excluded from availability calculation).
* **SLA Reporting Frequency**: Monthly SLA report delivered to IDBI IT Operations Committee.

---

## 13. Operational KPIs

| KPI | Measurement | Frequency | Target |
| :--- | :---: | :---: | :---: |
| Platform availability | Uptime % | Monthly | ≥ 99.9% |
| P1 incident count | Count | Monthly | 0 |
| MTTD (Mean Time to Detect) | Minutes | Per incident | < 5 min |
| MTTR P1 (Mean Time to Resolve) | Hours | Per incident | < 2 hours |
| MTTR P2 | Hours | Per incident | < 8 hours |
| SLA compliance rate | % | Monthly | ≥ 99% |
| Fraud registry coverage | % evaluations checked | Daily | 100% |
| WAF false positive rate | % | Weekly | < 0.1% |
| Change success rate | % | Monthly | ≥ 98% |
| Patch deployment success rate | % | Per patch | 100% |

---

## 14. Monitoring & Alerting Strategy

### 14.1 Monitoring Ownership

| Layer | Tool | Owner |
| :--- | :---: | :--- |
| Infrastructure (Cloud Run) | Cloud Monitoring | IDBI Cloud Ops |
| API performance | Cloud Monitoring + custom metrics | IDBI App Support |
| Application logs | Cloud Logging | IDBI App Support |
| Security events | Cloud Armor + Cloud Logging | IDBI Security Ops |
| AI operations | Custom Cloud Monitoring dashboard | IDBI AI Ops |
| Business metrics | BigQuery + Looker Studio | IDBI Analytics |

### 14.2 Alert Policy Ownership (BAU)

| Alert | Threshold | Owner |
| :--- | :---: | :--- |
| P95 latency > 800ms (credit engine) | 3 consecutive minutes | IDBI Cloud Ops |
| Error rate > 1% | 5 consecutive minutes | IDBI Cloud Ops |
| WAF block rate > 100/min | Immediate | IDBI Security Ops |
| Fraud registry failure | Any failure | IDBI Security Ops |
| Vertex AI timeout > 5% | 3 consecutive minutes | IDBI AI Ops |
| Cloud Run max instance count reached | Immediate | IDBI Cloud Ops |

---

## 15. Google Cloud Operations

| GCP Service | BAU Operational Responsibility |
| :--- | :--- |
| **Cloud Run** | IDBI Cloud Ops — deployment, scaling, rollback |
| **Cloud Armor WAF** | IDBI Security Ops — rule management, review logs |
| **Vertex AI** | IDBI AI Ops — quota management, timeout monitoring |
| **Cloud Logging** | IDBI Cloud Ops — log sink management, retention |
| **Cloud Monitoring** | IDBI Cloud Ops — alert policy maintenance |
| **Secret Manager** | IDBI Security Ops — secret rotation per policy |
| **Pub/Sub** | IDBI Cloud Ops — topic and subscription management |
| **BigQuery** | IDBI Analytics — WAF and audit data querying |
| **IAM** | IDBI Security Ops — service account and role management |

### Quarterly GCP Health Review
* **Frequency**: Quarterly (Jan, Apr, Jul, Oct)
* **Scope**: Cost optimization, quota review, security posture, deprecated API usage
* **Owner**: IDBI Cloud Ops + GCP Professional Services (advisory)

---

## 16. Security Operations

### 16.1 Routine Security Activities

| Activity | Frequency | Owner |
| :--- | :---: | :--- |
| WAF log review | Daily | IDBI Security Ops |
| WAF rule tuning review | Monthly | IDBI Security Ops |
| Secret rotation | Quarterly | IDBI Security Ops |
| IAM access review | Quarterly | IDBI Security Ops |
| Dependency CVE scan | Monthly | IDBI App Support |
| Penetration testing | Annual | IDBI Security + External Vendor |
| Fraud registry blacklist update | As notified by RBI | IDBI Compliance + AAROHAN Engineering |

### 16.2 Security Incident Response

* All WAF block-rate anomalies investigated within 15 minutes.
* Any suspected data breach triggers immediate CISO notification and IDBI Bank security incident response protocol.
* PAN or Aadhaar data exposure — treated as P1 regardless of service impact.

---

## 17. AI Operations (AIOps)

### 17.1 AI Monitoring KPIs

| Metric | Target | Alert |
| :--- | :---: | :---: |
| Credit evaluation success rate | > 99% | < 98% |
| Vertex AI timeout rate | < 1% | > 3% |
| Explainability tag parse rate | 100% | < 100% |
| Fraud blacklist match audit log coverage | 100% | < 100% |
| Human approval queue depth | < 100 | > 500 |
| AI recommendation distribution drift | Baseline ± 15% | Significant deviation |

### 17.2 AI Governance in BAU

* All Gemini prompt templates are version-controlled. Any prompt modification requires a **Normal Change** approval.
* Explainability tag vocabulary changes require approval from IDBI Credit Risk and Compliance teams.
* AI audit logs are reviewed monthly by IDBI Credit Risk for bias, accuracy, and regulatory alignment.
* The fraud registry blacklist is owned by IDBI Compliance — updates require a formal change ticket and coordination with AAROHAN warranty team for the first 90 days.

---

## 18. Knowledge Transfer Summary

| Session | Topic | Delivered | Audience | Status |
| :---: | :--- | :---: | :--- | :---: |
| 1 | Platform Architecture Overview | 2026-07-10 | IDBI Ops | ✅ Complete |
| 2 | Cloud Monitoring Dashboard Walkthrough | 2026-07-10 | IDBI Ops | ✅ Complete |
| 3 | Incident Response Tabletop Exercise | 2026-07-11 | IDBI Ops + L1 | ✅ Complete |
| 4 | Cloud Run Deployment & Rollback Lab | 2026-07-12 | IDBI Ops | ✅ Complete |
| 5 | AI Credit Engine Operations | 2026-07-13 | IDBI Ops + Risk | ✅ Complete |
| 6 | WAF Configuration & Management | 2026-07-14 | IDBI Ops + Security | ✅ Complete |
| 7 | Secret Rotation Procedure | 2026-07-14 | IDBI Ops | ✅ Complete |
| 8 | Fraud Registry Operations & Fallback | 2026-07-15 | IDBI Ops + Risk | ✅ Complete |

**All 8 knowledge transfer sessions completed successfully.**

---

## 19. Support Documentation Inventory

| Document | Location | Owner |
| :--- | :--- | :--- |
| Platform Architecture Overview | IDBI Knowledge Base | IDBI Ops |
| Production Runbook (all 16 services) | IDBI Knowledge Base | SRE Lead → IDBI Ops |
| Cloud Run Rollback Procedure | IDBI Knowledge Base | IDBI Cloud Ops |
| Incident Escalation Matrix | IDBI Knowledge Base | IDBI ITSM |
| WAF Rule Management Guide | IDBI Knowledge Base | IDBI Security Ops |
| Secret Rotation SOP | IDBI Knowledge Base | IDBI Security Ops |
| Fraud Registry Operations Guide | IDBI Knowledge Base | IDBI Compliance |
| Backup & Restore Procedure | IDBI Knowledge Base | IDBI Cloud Ops |
| Disaster Recovery Playbook | IDBI Knowledge Base | SRE Lead → IDBI Ops |
| AI Operations Guide | IDBI Knowledge Base | IDBI AI Ops |
| Change Management SOP | IDBI Knowledge Base | IDBI ITSM |
| SLA Reporting Template | IDBI Knowledge Base | IDBI ITSM |

---

## 20. Risk Register

| Risk ID | Description | Likelihood | Impact | Severity | Owner | Mitigation |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| BAU-R001 | SQLite concurrency under MSME peak loan season | Low | High | Medium | IDBI Cloud Ops | AlloyDB migration (V1.2); WAL mode active |
| BAU-R002 | Fraud registry mock in production (not live RBI API) | Medium | High | High | IDBI Compliance | Clearly labelled; live integration in V1.2 roadmap |
| BAU-R003 | Vertex AI quota exhaustion at scale | Low | Medium | Medium | IDBI AI Ops | Quota increase filed; retry + fallback implemented |
| BAU-R004 | L3 warranty team unavailability for critical defect | Low | High | Medium | CTO | Secondary warranty contacts designated |
| BAU-R005 | WAF rule false positive on novel API integrations | Low | Low | Low | IDBI Security Ops | Exception-list process documented |
| BAU-R006 | Knowledge gap in IDBI Ops for AI governance changes | Medium | Medium | Medium | IDBI ITSM | Monthly AI governance review sessions planned |

> **Highest Priority Risk**: BAU-R002 — Fraud registry mock. IDBI Compliance and AAROHAN warranty team are jointly responsible for live RBI API integration planning in V1.2.

---

## 21. Continuous Improvement Plan

| Initiative | Owner | Frequency | Target Outcome |
| :--- | :--- | :---: | :--- |
| Monthly SLA review and trend analysis | Service Delivery Manager | Monthly | Identify degradation early; drive improvements |
| Quarterly GCP cost and performance review | IDBI Cloud Ops | Quarterly | Optimize Cloud Run sizing and Vertex AI quota |
| Monthly AI recommendation distribution audit | IDBI Credit Risk | Monthly | Detect model drift or bias early |
| Bi-annual security posture review | IDBI Security Ops | Bi-annual | Ensure WAF rules and IAM remain current |
| Annual DR full-failover drill | SRE Lead | Annual | Validate DR playbook and RTO/RPO targets |
| Monthly dependency CVE scan | IDBI App Support | Monthly | Early detection of new CVEs in dependencies |
| Post-incident lessons learned | SRE Lead | Per P1/P2 | Feed improvements into runbooks and processes |

---

## 22. Version 1.1.x Patch Management Strategy

### 22.1 Patch Categories

| Patch Type | Trigger | Approval Path | Deployment Target |
| :--- | :--- | :---: | :---: |
| **Security Hotfix** | Critical CVE or security breach | ECAB (< 2 hours) | < 24 hours |
| **Critical Defect Fix** | P1 production defect | ECAB + CTO | < 48 hours |
| **Maintenance Patch** | Non-critical defect or dependency update | Normal CAB | Next maintenance window |

### 22.2 Patch Deployment Process

1. AAROHAN warranty team authors patch and test evidence.
2. IDBI ITSM raises a Change ticket with patch artefacts.
3. CAB/ECAB reviews and approves.
4. IDBI DevOps deploys to staging; L2 runs smoke tests.
5. IDBI DevOps deploys to production with rollback plan ready.
6. L1 monitors for 30 minutes post-deployment.
7. Change ticket closed; patch notes added to Known Error Database.

### 22.3 Patch SLA Targets

| Patch Type | Development SLA | Deployment SLA |
| :---: | :---: | :---: |
| Security Hotfix (Critical) | < 8 hours | < 24 hours |
| Critical Defect Fix | < 2 business days | < 3 business days |
| Maintenance Patch | < 5 business days | Next maintenance window |

---

## 23. Version 1.2 Product Intake Process

### 23.1 V1.2 Planning Gate

Version 1.2 development shall be initiated through a formal product intake process:

| Step | Activity | Owner | Timeline |
| :---: | :--- | :--- | :---: |
| 1 | V1.2 backlog grooming — review deferred items | Product Owner | 2026-08-01 |
| 2 | V1.2 business case approval | CPO + Banking Sponsor | 2026-08-15 |
| 3 | V1.2 Product Roadmap creation | Product Owner + Architect | 2026-09-01 |
| 4 | V1.2 Sprint Planning | Scrum Master + Team | 2026-09-15 |
| 5 | V1.2 Sprint 1 Kickoff | Engineering Manager | 2026-09-22 |

### 23.2 V1.2 Confirmed Backlog Items

| Item | Priority | Business Driver |
| :--- | :---: | :--- |
| AlloyDB production database migration | High | Production scalability; concurrency |
| Live RBI Central Fraud Registry API integration | High | Regulatory compliance |
| RM fraud-match push notifications (CR-11-003) | Medium | Operational efficiency |
| Pydantic V2 `ConfigDict` migration | Low | Technical debt reduction |
| `datetime.utcnow()` deprecation fix | Low | Technical debt reduction |
| Multi-language portal support | Low | Market expansion |
| ML-based WAF sensitivity tuning | Low | Security optimization |

### 23.3 Version Separation Policy

**No V1.2 development activity shall be merged into the V1.1 `main` branch.** Version 1.2 development shall operate on a dedicated `feature/v1.2` branch, merged only upon V1.2 Golden Release Certification.

---

## 24. Executive Approval Matrix

| Role | Decision | Date |
| :--- | :---: | :---: |
| **Chief Technology Officer** | ✅ APPROVED | 2026-07-22 |
| **Production Operations Manager** | ✅ APPROVED | 2026-07-22 |
| **Service Delivery Manager** | ✅ APPROVED | 2026-07-22 |
| **SRE Lead** | ✅ APPROVED | 2026-07-22 |
| **DevSecOps Lead** | ✅ APPROVED | 2026-07-22 |
| **Enterprise Support Manager** | ✅ APPROVED | 2026-07-22 |
| **Google Cloud Operations Lead** | ✅ APPROVED | 2026-07-22 |
| **Banking Operations Head** | ✅ APPROVED | 2026-07-22 |
| **ITSM Lead** | ✅ APPROVED | 2026-07-22 |

**Unanimous approval. BAU transition is formally authorized effective 2026-07-22.**

---

🟢 **APPROVED FOR BUSINESS-AS-USUAL OPERATIONS**

---

## 25. Appendix

### A. BAU Transition Milestone Summary

| Milestone | Date | Status |
| :--- | :---: | :---: |
| Golden Release (v1.1.0) | 2026-07-08 | ✅ Complete |
| Hypercare activated | 2026-07-08 | ✅ Complete |
| Knowledge transfer completed | 2026-07-15 | ✅ Complete |
| Runbook sign-off | 2026-07-20 | ✅ Complete |
| L1 readiness assessment | 2026-07-21 | ✅ Complete |
| Hypercare closed | 2026-07-22 | ✅ Complete |
| BAU transition effective | 2026-07-22 | ✅ Active |
| Warranty support end | 2026-10-06 | 🔄 Ongoing |
| V1.2 planning kickoff | 2026-08-01 | 🔄 Scheduled |
| DR full-failover drill | 2026-07-25 | 🔄 Scheduled |

### B. V1.1 Complete Artefact Registry

| Document ID | Title |
| :--- | :--- |
| AAR-V11-SPRINT-001 to 004 | Sprint Planning Documents |
| AAR-V11-IMP-001 to 004 | Sprint Implementation Summaries |
| AAR-V11-CODE-REVIEW-001 to 002 | Code Review Reports |
| AAR-V11-QA-001 to 002 | QA Validation Reports |
| AAR-V11-REVIEW-001 to 004 | Sprint Review Reports |
| AAR-V11-RETRO-001 to 003 | Sprint Retrospective Reports |
| AAR-V11-INC-PLAN-001 | Increment Planning |
| AAR-V11-RC1-001 | Release Candidate Preparation |
| AAR-V11-HARDEN-001 | Release Hardening Report |
| AAR-V11-REG-001 | Enterprise Regression Test Report |
| AAR-V11-PRR-001 | Production Readiness Review |
| AAR-V11-GOLD-001 | Golden Release Certification |
| AAR-V11-REL-001 | Official Release Package |
| AAR-V11-HYPERCARE-001 | Post-Production Hypercare Plan |
| **AAR-V11-BAU-001** | **BAU Transition Plan (this document)** |

---

*Project AAROHAN v1.1.0 — Business-as-Usual Operations*  
*IDBI Bank MSME Digital Lending Platform*  
*BAU Effective Date: 2026-07-22 | Warranty Period Ends: 2026-10-06*
