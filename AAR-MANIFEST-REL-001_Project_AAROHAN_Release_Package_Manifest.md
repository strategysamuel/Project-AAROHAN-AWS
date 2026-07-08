# AAR-MANIFEST-REL-001: Project AAROHAN Release Package Manifest

---

## 1. Cover Page

* **Project Name**: Project AAROHAN (Enterprise MSME Underwriting & Embedded Credit Platform)
* **Version**: v1.0.0
* **Manifest Version**: v1.0.0
* **Classification**: CONFIDENTIAL - BANK OPERATIONAL
* **Owner**: Enterprise Release Governance Board
* **Approval Matrix**:
  - Head of Release Governance: APPROVED
  - Chief Configuration Manager: APPROVED
  - Chief Information Officer (CIO): APPROVED

---

## 2. Executive Summary

This document serves as the official Release Package Manifest for Project AAROHAN v1.0.0. It acts as the master inventory, providing configuration management records, source code locations, API mappings, and document indexes to ensure complete traceability.

---

## 3. Purpose

The purpose of this manifest is to compile a complete list of deliverables, source codes, configuration templates, database scripts, and administrative documents included in the Version 1.0 release package.

---

## 4. Scope

This manifest tracks all source repositories, microservice container images, data schemas, API definitions, deployment scripts, and release documentation for Project AAROHAN.

---

## 5. Release Information

* **Release Name**: Project AAROHAN General Availability
* **Version**: v1.0.0
* **Release Date**: 2026-07-08
* **Git Branch**: `release/v1.0-rc1`
* **Git Tag**: `v1.0.0`
* **Build Number**: Build-20260708-GA
* **Release Classification**: Production Release (General Availability)

---

## 6. Repository Information

* **Repository Name**: `Project AAROHAN` (Enterprise Mono-Repo)
* **Branch Structure**: GitFlow (`main`, `develop`, `feature/*`, `release/*`)
* **Release Branch**: `release/v1.0-rc1`
* **Tag Strategy**: Semantic tags prefixed with "v" (e.g., `v1.0.0`)
* **Versioning Policy**: Strict semantic versioning (Major.Minor.Patch)

---

## 7. Source Code Inventory

### Frontend Applications
* `apps/customer-portal`: React-based customer dashboard.

### Backend Microservices
* `services/onboarding-service`: Handles customer profiling.
* `services/consent-service`: Manages digital user consents.
* `services/gst-service`: Syncs and evaluates tax records.
* `services/aa-service`: Aggregates bank statement ledgers.
* `services/fhc-service`: Financial Health Card scoring engine.
* `services/credit-engine`: Credit limits evaluation engine.
* `services/cam-service`: SWOT analysis and CAM compiler.
* `services/rm-workspace-service`: Relationship Manager dashboard backend.
* `services/exec-service`: Executive KPI aggregator.
* `services/ews-service`: Watchlist and risk alerts.
* `services/ckyc-service`: CKYC identity validation connector.
* `services/mca-service`: MCA corporate registry interface.
* `services/epfo-service`: EPFO payroll data connector.
* `services/treds-service`: Discounting platform sync.
* `services/ocen-uli-service`: OCEN-ULI gateway engine.

### Shared Packages
* `packages/common`: Base models, logging middlewares, and databases.

---

## 8. API Inventory

* **Onboarding Service**: `GET /customers`, `POST /customers/register`
* **Consent Service**: `POST /consents`, `POST /consents/{id}/approve`
* **GST Service**: `POST /gst/sync/{customer_id}`, `GET /gst/profile/{customer_id}`
* **AA Service**: `POST /aa/link/{customer_id}`, `POST /aa/sync/{customer_id}`
* **FHC Service**: `POST /fhc/calculate/{customer_id}`, `GET /fhc/{customer_id}`
* **Credit Engine**: `POST /credit/evaluate/{customer_id}`
* **CAM Service**: `POST /cam/generate/{customer_id}`, `GET /cam/{customer_id}`
* **OCEN-ULI Service**: `POST /ocen/eligibility`, `POST /ocen/apply`, `GET /healthz`

---

## 9. Database Inventory

* **Schema Engine**: SQLAlchemy ORMs mapping models globally.
* **Tables**: `lenders`, `partners`, `loan_applications`, `loan_offers`, `audit_logs`.
* **Migrations**: Executed via Alembic migrations files.
* **Seed Data**: Pre-seeded lists for lenders and partners.

---

## 10. AI Asset Inventory

* **Vertex AI Integrations**: Model connections to Google Vertex endpoints.
* **Gemini Integrations**: `gemini-1.5-pro` (CAM generation) and `gemini-1.5-flash` (advisory).
* **Prompt Templates**: Versioned prompt configurations for SWOT analysis and CAM generation.
* **AI Workflows**: Automated draft compilations.
* **Human Approval Workflows**: Triggers for Credit Officer override actions.

---

## 11. Google Cloud Resource Inventory

* **Cloud Run**: Containers deployed for each microservice.
* **AlloyDB**: Managed PostgreSQL cluster.
* **BigQuery Datasets**: Data repositories for analytics and early warning systems.
* **Cloud Storage Buckets**: Storage space for document PDFs.
* **Secret Manager**: Encrypted secrets vault.
* **Pub/Sub Topics**: Message topics for system notifications.
* **Eventarc Triggers**: Event routing configuration.
* **Cloud Monitoring**: Centralized SRE metric dashboards.

---

## 12. Documentation Inventory

| Document ID | Title | Version | Owner | Status |
| :--- | :--- | :---: | :--- | :--- |
| **AAR-REL-001** | Release Notes v1.0.0 | v1.0.0 | Release Manager | Completed |
| **AAR-DEP-001** | Deployment & Installation Guide | v1.0.0 | DevOps Lead | Completed |
| **AAR-OPS-001** | Enterprise Operations Runbook | v1.0.0 | SRE Lead | Completed |
| **AAR-ADM-001** | Enterprise Administrator Guide | v1.0.0 | IAM Architect | Completed |
| **AAR-USER-001** | Enterprise End User Guide | v1.0.0 | Documentation Lead | Completed |
| **AAR-ARCH-DEP-001** | Production Deployment Architecture | v1.0.0 | Solutions Architect | Completed |
| **AAR-DR-001** | Disaster Recovery & BCP Plan | v1.0.0 | Risk Officer | Completed |
| **AAR-SUP-001** | Support & Maintenance Guide | v1.0.0 | Support Manager | Completed |

---

## 13. Test Artifact Inventory

* **Unit Tests**: `services/ocen-uli-service/tests/test_ocen_uli.py` (3 passed).
* **Regression Tests**: `tests/test_regression_e2e.py` (6 passed).
* **E2E Tests**: Complete loan journey workflows verified.
* **AI Evaluation Tests**: Prompt testing using the evaluation dataset.

---

## 14. Deployment Artifact Inventory

* Dockerfiles, build configurations, and Cloud Build manifests.

---

## 15. Security Artifact Inventory

* IAM custom role profiles, Cloud KMS key configurations, and Cloud Armor rule scripts.

---

## 16. Compliance Artifact Inventory

* Database tables logging digital consent signatures, verification timestamps, and credit override reasons.

---

## 17. Known Limitations

* Defaults to SQLite in local developer sandboxes; AlloyDB configuration is required for multi-zone production deployments.

---

## 18. Version Compatibility Matrix

* **Python**: v3.11+
* **Node.js**: v18.x+
* **AlloyDB**: PostgreSQL v15 compatible engine

---

## 19. Release Acceptance Criteria

- [x] All 6 E2E regression tests pass.
- [x] Compilation completes without warnings or errors.
- [x] All security checks return no high-severity vulnerabilities.

---

## 20. Final Release Checklist

- [ ] Confirm all environment parameters are loaded in Secret Manager.
- [ ] Verify SSL certificate configurations on HTTPS load balancers.
- [ ] Push final Git tag `v1.0.0`.

---

## 21. Release Approval Matrix

* **IT Infrastructure Lead**: APPROVED
* **Lead DevSecOps Engineer**: APPROVED
* **Director of IT Operations**: APPROVED

---

## 22. Appendix

* Git Commit log references.
* System package dependency manifest trees.
