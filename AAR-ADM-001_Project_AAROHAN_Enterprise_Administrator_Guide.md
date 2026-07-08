# AAR-ADM-001: Project AAROHAN Enterprise Administrator Guide

---

## 1. Cover Page

* **Project Name**: Project AAROHAN (Enterprise MSME Underwriting & Embedded Credit Platform)
* **Version**: v1.0.0
* **Guide Version**: v1.0.0
* **Classification**: CONFIDENTIAL - BANK INTERNAL
* **Owner**: Enterprise Identity & Access Management Board
* **Approval Matrix**:
  - Head of IT Governance: APPROVED
  - Principal Platform Administrator: APPROVED
  - Chief Information Security Officer (CISO): APPROVED

---

## 2. Purpose

This guide outlines configuration parameters, security privileges, role mappings, third-party interface switches, and administrative procedures required to manage Project AAROHAN.

---

## 3. Scope

This document details administrative controls across both Google Cloud infrastructure resources and application-level systems (such as the React customer portal, microservice environment tables, database models, and Vertex AI parameters).

---

## 4. Intended Audience

This guide is written for Platform Administrators, Identity & Access Management (IAM) Administrators, DBAs, DevOps Engineers, and Security Compliance Officers.

---

## 5. System Overview

Project AAROHAN aggregates public and private APIs (Consent, GST, AA, CKYC, EPFO, MCA, TReDS, and OCEN-ULI) to facilitate automated MSME credit underwriting. Administrators manage security groups, model templates, and connection profiles.

---

## 6. Administrative Architecture

* **Cloud Run**: Administered via the GCP Console or `gcloud run` command line to update container scaling, ingress policies, and revision routing.
* **AlloyDB**: Administered to manage clusters, primary/read replica states, instance scaling, and connection limits.
* **BigQuery**: Governed through dataset level access controls (IAM) and execution slot limits.
* **Cloud Storage**: Administered via Storage Class policies, lifecycle rules, and IAM permissions on document buckets.
* **Secret Manager**: Holds sensitive environment values. Authorized admins control key replication and access log trails.
* **Identity & Access Management (IAM)**: Governed using custom Service Accounts with least-privilege roles.
* **Vertex AI & Gemini**: Administered to update model configurations, parameters, and logging tables.
* **Pub/Sub & Eventarc**: Controls topic subscriptions, message retention thresholds, and push endpoints.
* **Cloud Monitoring & Logging**: Governs dashboard variables, log exclusions, and alert distributions.

---

## 7. User Administration

* **User Lifecycle**: Provisioning is initiated through the enterprise Active Directory (AD) mapping. Deactivations instantly revoke active OAuth sessions.
* **Password Policies**: Enforce minimum 14 characters, complexity rules, and 90-day rotation schedules.
* **Multi-Factor Authentication (MFA)**: Strictly required for all administrators via hardware keys or authenticator apps.
* **Session Management**: Session tokens (JWT) expire in 15 minutes; refresh tokens are valid for 8 hours with strict fingerprint checks.

---

## 8. Role-Based Access Control (RBAC)

The platform supports the following role permissions:
* **Super Administrator**: Full system access (infrastructure + application controls).
* **Platform Administrator**: Infrastructure operations, Secret Manager updates, and scaling rules.
* **Business Administrator**: Configures business metrics, interest tiers, and RM assignments.
* **Credit Administrator**: Overrides credit evaluation decisions and authorizes CAM drafts.
* **Relationship Manager (RM)**: Manages tasks, leads, and schedules customer follow-ups.
* **Operations User**: Direct verification tasks (e.g., manually checking uploaded files).
* **Read-only Auditor**: Audits logs, signatures, consent timestamps, and report exports.

### Permissions Matrix

| Operations / Roles | Super Admin | Platform Admin | Credit Admin | RM | Auditor |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Manage Infrastructure** | Yes | Yes | No | No | No |
| **Rotate Secrets** | Yes | Yes | No | No | No |
| **Approve Credit Override** | Yes | No | Yes | No | No |
| **Manage Client Tasks** | Yes | No | No | Yes | No |
| **Read Audit Logs** | Yes | Yes | Yes | Yes | Yes |

---

## 9. Identity & Access Management

IAM configurations map to custom GCP IAM roles:
* `roles/run.admin` for Platform Administrators.
* `roles/secretmanager.secretAccessor` only for active Cloud Run service accounts.

---

## 10. Environment Administration

Administrators configure specific environment parameters:
* **DEV**: Local SQLite fallback allowed; logs set to `DEBUG`.
* **QA**: Interconnected mock endpoints; regression metrics monitored.
* **UAT**: Replicas in isolation; connected to bank core sandbox.
* **Production (PROD)**: Locked repositories; connection pool alerts set at low thresholds.

---

## 11. Configuration Management

Application settings are injected via environment files. Deployments compile profiles from target branch maps (`release/v1.0-rc1` to production targets).

---

## 12. Secret Management

Create and version variables under `Secret Manager` with KMS envelope encryption enabled.

---

## 13. Database Administration

Administer AlloyDB parameters (e.g., `max_connections` and autovacuum triggers) using GCP CLI commands.

---

## 14. Storage Administration

Document storage buckets employ Lifecycle Policies to auto-archive files older than 365 days to Coldline Storage.

---

## 15. AI Administration

* **Prompt Templates**: Managed inside system environment variables or config files.
* **Model Configuration**: Defaults to `gemini-1.5-pro` for CAM formatting, with fallback to `gemini-1.5-flash` for inline scoring.
* **AI Policy Controls**: Strict safety settings block outputs containing offensive language or compliance violations.
* **Human Approval Configuration**: Triggers manual verification if the credit score falls between 600 and 700.
* **AI Audit Logs**: Retained in BigQuery tables for compliance audits.

---

## 16. Integration Administration

Administrators toggle mocks and sync parameters for external services:
* **GST/EPFO/MCA**: Manage synchronizer time schedules (cron frequency).
* **TReDS/CKYC/OCEN-ULI**: Configure endpoint gateway URLs and SSL credentials.

---

## 17. Monitoring Configuration

Manage Google Cloud Monitoring agent profiles across VM/Container namespaces.

---

## 18. Alert Configuration

Define alert routing via PagerDuty, Slack channels, and email distribution lists.

---

## 19. Logging Configuration

Logs must comply with JSON structures. Route sensitive payload exclusions to block PII leaks (such as PAN numbers) in the logging stream.

---

## 20. Backup Administration

Verify that nightly AlloyDB backups replicate to secondary regions for geographical safety.

---

## 21. Disaster Recovery Administration

Maintain secondary load-balancing routes for immediate traffic failover.

---

## 22. Security Administration

Govern encryption keys (Cloud KMS) and enforce secure HTTPS protocols (TLS 1.3) across all public APIs.

---

## 23. Certificate Management

Google-managed SSL certificates automatically renew; custom certificates must be monitored via Security Command Center (SCC).

---

## 24. API Administration

Apply Apigee gateways or local rate-limiting middleware to cap calls at 100 requests/minute per client token.

---

## 25. Performance Tuning

Tune FastAPI worker processes using Gunicorn configurations based on Cloud Run vCPU scaling metrics.

---

## 26. Capacity Planning

Set up alerts to trigger instance upgrades when AlloyDB CPU utilization averages > 60% over 24 hours.

---

## 27. Patch Management

Apply security patches and update Node/Python dependencies monthly.

---

## 28. Troubleshooting

Administrators should check Cloud Run stderr outputs and verify VPC Serverless connection paths when services fail to connect.

---

## 29. Administrative Checklists

- [ ] Confirm daily audit logs sync to cold storage.
- [ ] Verify SSL certificate expiry dates.
- [ ] Review Active Directory identity deactivation lists.

---

## 30. Operational Best Practices

Apply the Principle of Least Privilege across all administrator actions and keep secrets separated from code bases.

---

## 31. Compliance Considerations

System records must align with:
* **RBI DPI Guidelines**: Ensuring secure data processing and consent tracking.
* **IT Act Section 43A**: Enforcing strict protection of customer PII data.

---

## 32. Appendix

* GCP Administration Command Reference.
* Custom IAM Role Template Definitions (JSON).
