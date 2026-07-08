# AAR-DEP-001: Project AAROHAN Deployment & Installation Guide

---

## 1. Cover Page

* **Project Name**: Project AAROHAN (Enterprise MSME Underwriting & Embedded Credit Platform)
* **Version**: v1.0.0
* **Deployment Guide Version**: v1.0.0
* **Release Classification**: CONFIDENTIAL - BANK INTERNAL
* **Document Owner**: Enterprise Platform DevOps & Infrastructure Team
* **Approval Matrix**:
  - Chief Information Security Officer (CISO): APPROVED
  - Head of Infrastructure Operations: APPROVED
  - Chief Technology Officer (CTO): APPROVED

---

## 2. Purpose

This document provides comprehensive, step-by-step instructions for deploying, installing, and validating Project AAROHAN v1.0.0 across multi-stage environments (Development, QA, UAT, and Production) on Google Cloud Platform (GCP).

---

## 3. Intended Audience

This guide is written for DevOps Engineers, Site Reliability Engineers (SREs), Platform Architects, Database Administrators (DBAs), and DevSecOps Leads responsible for release delivery and infrastructure reliability.

---

## 4. Deployment Overview

Project AAROHAN is packaged as a standard containerized monorepo. Frontend React code compiles to static assets served via a CDN, and the backend FastAPI services are deployed as independent, autoscaling containers on Google Cloud Run. Database state is managed by a centralized, production-grade AlloyDB cluster.

---

## 5. Solution Architecture Overview

Project AAROHAN utilizes a distributed microservices architecture:
* **API Gateway & Routing**: Handles cross-cutting policies, rate limiting, and request routing.
* **Core Microservices**: Independent containers for Onboarding, Consent, GST, AA, FHC, Credit Decisioning, CAM Generation, RM Workspace, and OCEN-ULI.
* **Storage Layer**: Relational transactions reside in AlloyDB; unstructured document PDFs are archived in Google Cloud Storage.

---

## 6. Google Cloud Architecture

### Cloud Run
* Deployment target for all microservices. 
* Autoscaling configured between 1 and 100 instances based on CPU utilization (default threshold: 70%).

### AlloyDB
* Centralized managed PostgreSQL database.
* High Availability (HA) enabled with primary read/write nodes and read-pools spanning multiple Zones.

### BigQuery
* Dedicated analytics database for historical GST trends, EPFO logs, and EWS watchlist events.

### Cloud Storage (GCS)
* Secure storage buckets configured with Uniform Bucket-Level Access (UBLA) for document PDFs and audit artifacts.

### Artifact Registry
* Secure repository hosting Docker image tags (e.g., `asia-south1-docker.pkg.dev/aarohan-prod/registry/onboarding-service:v1.0.0`).

### Cloud Build
* Automated CI/CD pipeline triggered by Git tags and branch promotions.

### Secret Manager
* Encrypted database URLs, API secrets, and encryption keys.

### Identity & Access Management (IAM)
* Principle of Least Privilege (PoLP) applied using granular Service Accounts.

### Pub/Sub & Eventarc
* Event-driven communication for downstream events (e.g., `consent.approved`).

### Cloud Logging, Monitoring & Trace
* Centralized dashboards, liveness probes, tracing, and metric alerts.

### Vertex AI & Gemini
* Vertex AI APIs enabled for generating Credit Assessment Memorandums (CAM) and advisory prompts.

---

## 7. Environment Strategy

* **Development (DEV)**: Local developer sandbox / ephemeral test environments.
* **Quality Assurance (QA)**: Manual testing and automated regression suites.
* **User Acceptance Testing (UAT)**: Business validator verification and compliance sign-off.
* **Production (PROD)**: Live traffic environment with strict HA and multi-zone failovers.

---

## 8. Infrastructure Requirements

* GCP Project: Enabled for billing and APIs.
* Virtual Private Cloud (VPC): Subnets in primary region (e.g., `asia-south1`).
* AlloyDB Cluster: Minimum 4 vCPUs, 32 GB RAM per instance.

---

## 9. Software Prerequisites

* **Docker**: v20.10+
* **Google Cloud SDK (gcloud CLI)**: v450.0.0+
* **Python**: v3.11+
* **Node.js & NPM**: Node v18+, NPM v9+
* **Alembic**: v1.11+

---

## 10. Environment Variables

### Required
* `DATABASE_URL`: AlloyDB database connection string. (Sensitive)
* `JWT_SECRET_KEY`: Symmetric key used to sign access tokens. (Sensitive)
* `GCP_PROJECT_ID`: Active Google Cloud Project ID. (Required)

### Optional
* `LOG_LEVEL`: Logger verbosity (e.g., `INFO`, `DEBUG`). (Optional)
* `ENABLE_MOCK_PROVIDERS`: If `True`, enables sandbox third-party providers. (Optional)

---

## 11. Secrets Management

All production configurations must resolve variables from Secret Manager:
```bash
# Retrieve a secret programmatically
gcloud secrets versions access latest --secret="DATABASE_URL"
```

---

## 12. Database Deployment

1. **Schema Initialization**: Execute Alembic migrations to build tables.
```bash
alembic upgrade head
```
2. **Rollback**: In case of schema failures:
```bash
alembic downgrade -1
```

---

## 13. Backend Deployment

Build and push containers to GCP Artifact Registry, then deploy:
```bash
gcloud run deploy ocen-uli-service \
  --image=asia-south1-docker.pkg.dev/$PROJECT_ID/registry/ocen-uli-service:v1.0.0 \
  --vpc-connector=aarohan-vpc-connector \
  --set-env-vars=GCP_PROJECT_ID=$PROJECT_ID \
  --update-secrets=DATABASE_URL=DATABASE_URL:latest \
  --region=asia-south1
```

---

## 14. Frontend Deployment

Compile static assets and sync to GCS Bucket configured for web hosting:
```bash
npm run build
gsutil web set -m index.html gs://aarohan-portal-bucket
```

---

## 15. AI Services Deployment

Ensure the following Vertex AI permissions are attached to the service account:
* `roles/aiplatform.user`

---

## 16. Networking

* **VPC Serverless Connector**: Connects Cloud Run instances directly to AlloyDB private IPs.
* **HTTPS Load Balancer**: Distributes traffic to services with attached SSL certificates.

---

## 17. CI/CD Pipeline

* **Cloud Build trigger**: Configured on Git tag push (e.g., `v*`).
* **Promotion**:
  - QA builds promote to UAT after automated checks pass.
  - UAT builds promote to Prod after manual approval.

---

## 18. Observability

* **Readiness/Liveness**: Configure `/healthz` and `/livez` probes on Cloud Run.
* **Trace**: Correlation ID middleware tracks execution across API boundaries.

---

## 19. Security

* Strict network firewalls restricting AlloyDB connections to the VPC IP range.
* Encryption-at-rest enabled on AlloyDB and GCS using Cloud KMS.

---

## 20. Deployment Validation Checklist

- [ ] All Cloud Run services report `Green` status.
- [ ] `/healthz` endpoints return `200 OK`.
- [ ] AlloyDB replica nodes successfully sync state.
- [ ] React Customer Portal loads correctly.

---

## 21. Rollback Procedure

To roll back a backend deployment to a previous revision:
```bash
gcloud run services update-traffic ocen-uli-service --to-revisions=ocen-uli-service-prev=100 --region=asia-south1
```

---

## 22. Disaster Recovery Preparation

* **Backups**: AlloyDB automated daily snapshots configured with a 30-day retention policy.
* **Failover**: Automated failover to secondary zones handles local outages.

---

## 23. Production Go-Live Checklist

- [ ] Secret variables loaded into Secret Manager.
- [ ] SSL certificates verified and active on HTTPS load balancers.
- [ ] Production database seeded with lookup records.
- [ ] Logging sinks redirected to enterprise storage buckets.

---

## 24. Troubleshooting Guide

* **Issue: Cloud Run Service Returns 503**
  - *Cause*: Service failed liveness check or container crashed during startup.
  - *Resolution*: Run `gcloud beta run services logs tail <service>` to view stderr.
* **Issue: Database Connection Timeouts**
  - *Cause*: VPC Serverless Connector is inactive or firewall rules block port 5432.
  - *Resolution*: Check VPC Connector status.

---

## 25. Appendix

* GCP CLI Reference: [gcloud run documentation](https://cloud.google.com/run/docs)
* Alembic Reference: [Alembic migrations guide](https://alembic.sqlalchemy.org/en/latest/)
