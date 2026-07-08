# Google Cloud Engineering Bootstrap & Repository Initialization Guide

**Document ID:** AAR-BOOT-001  
**Document Name:** Google Cloud Engineering Bootstrap & Repository Initialization Guide  
**Version:** 1.0  
**Status:** Approved for Core Platform Engineering  
**Dependencies:** Entire Project AAROHAN Repository, Engineering Build Blueprint (AAR-BLD-001), API Catalogue (AAR-API-CATALOG-001), and Engineering Playbook (AAR-ENG-PLAYBOOK-001)  
**Target Audience:** Engineering Teams, DevSecOps, Platform Engineers, Backend/Frontend Developers, and AI Engineers  
**Document Owner:** Google Cloud Principal Delivery Engineer  
**Approval Authority:** Platform Engineering Review Board

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Google Cloud Principal Engineer | Initial strategic release of the repository and GCP bootstrap framework. | EARB Approved |

---

## Table of Contents
1. [Executive Summary & Landing Zone Strategy](#executive-summary--landing-zone-strategy)
2. [Google Cloud Folder & Project Hierarchy](#google-cloud-folder--project-hierarchy)
3. [Repository Bootstrap & Monorepo Structure](#repository-bootstrap--monorepo-structure)
4. [Identity, IAM & Secret Management Strategy](#identity-iam--secret-management-strategy)
5. [CI/CD Pipeline & Cloud Build Bootstrap](#cicd-pipeline--cloud-build-bootstrap)
6. [AI, Data & Analytics Platform Organization](#ai-data--analytics-platform-organization)
7. [Local Workspace Setup & Developer Checklists](#local-workspace-setup--developer-checklists)

---

## Executive Summary & Landing Zone Strategy

This document serves as the guide to establish the Google Cloud Landing Zone, monorepo configuration, and deployment automation pipelines for Project AAROHAN. It transitions the program from the planning phase into engineering execution. 

### Core Platform Standards:
*   **Infrastructure as Code (IaC):** All Google Cloud resources must be deployed and managed using Terraform configurations.
*   **Zero Trust Resource Access:** Services communicate using minimal IAM roles and credentials injected at runtime.
*   **Stateless Container Execution:** All microservices run inside autoscaling Cloud Run containers.

---

## Google Cloud Folder & Project Hierarchy

To isolate environments and control access, IDBI Bank organizes Google Cloud resources using a multi-project hierarchy:

```
  IDBI BANK ORGANIZATION
  └── idbi-aarohan-folder (Folder)
      ├── aarohan-shared-services-project (Shared services: Artifact Registry, DNS, Active Directory)
      ├── aarohan-dev-project             (Development Environment)
      ├── aarohan-qa-project              (QA Testing Environment)
      ├── aarohan-uat-project             (User Acceptance Testing)
      └── aarohan-prod-project            (Production Environment)
```

### Environment Naming and Purpose
1. **aarohan-shared-services:** Houses central code builders, container registries, DNS records, and IAM configurations.
2. **aarohan-dev:** Sandbox for developers. Features fast deployment cycles.
3. **aarohan-qa:** Used by QA teams to execute automated testing workflows.
4. **aarohan-uat:** Dedicated environment for business users to validate features against acceptance criteria.
5. **aarohan-prod:** Locked-down environment hosting active customer workloads.

---

## Repository Bootstrap & Monorepo Structure

Project AAROHAN uses a single monorepo layout managed via `Nx` or `Turborepo` to coordinate microservices and shared libraries:

```
  /aarohan-monorepo
  ├── .github/workflows/          - Global CI/CD workflow configuration files
  ├── apps/                       - Application deployment targets
  │   ├── customer-portal/        - MSME self-service portal
  │   ├── employee-workspace/     - RM and Credit Analyst dashboards
  │   └── admin-console/          - System admin panels
  ├── services/                   - Independent Cloud Run microservices
  │   ├── auth-service/           - IAM validation and OIDC connectors
  │   ├── onboarding-service/     - Registration processes
  │   ├── spreading-service/      - Financial health calculation engine
  │   ├── credit-service/         - Policy validations and risk scoring
  │   └── agent-coach-service/    - Conversational business coach
  ├── packages/                   - Shared business and integration libraries
  │   ├── common-types/           - Shared API and Canonical data schemas
  │   ├── mcp-core/               - Model Context Protocol utilities
  │   └── prompt-registry/        - Versioned prompt configurations (YAML)
  └── terraform/                  - Infrastructure configurations
      ├── environments/           - Environment folders (Dev, QA, Prod)
      └── modules/                - Reusable resource templates
```

---

## Identity, IAM & Secret Management Strategy

### 1. Identity & Access Management (IAM)
*   **Principle of Least Privilege:** System processes run using dedicated service accounts with minimal access permissions.
*   **Microservice Isolation:** Each Cloud Run service account is restricted to its required actions (e.g., `spreading-service-sa` can access `alloydb-database-spreader` but not `credit-rules-database`).

### 2. Secret Ingestion Strategy
*   No database passwords, API keys, or security certificates are permitted in source repositories.
*   Configurations retrieve secrets from Google Cloud Secret Manager at runtime. Service accounts must be granted the `roles/secretmanager.secretAccessor` role to access values.

---

## CI/CD Pipeline & Cloud Build Bootstrap

```
                     CLOUDBUILD AUTOMATION
  [ Git Commit Push ] ──► [ Cloud Build Trigger ] ──► [ Run Linter & Tests ]
                                                            │
  [ Cloud Deploy Promo ] ◄── [ Artifact Registry ] ◄────────┘
```

1. **Trigger Configuration:** Cloud Build triggers are set up for code repositories.
2. **Code Checks:** Every pull request triggers verification checks (linter, unit tests, security scans).
3. **Container Compilation:** Merging code into the main branch builds container images and pushes them to Artifact Registry.
4. **Environment Deployment:** Google Cloud Deploy manages container promotions from Dev to Staging and Production.

---

## AI, Data & Analytics Platform Organization

### 1. BigQuery & Vertex AI Architecture
*   **BigQuery:** Datasets are separated into distinct layers:
    *   `aarohan_raw_ingest`: Raw statements pulled from AA and GSTN registries.
    *   `aarohan_analytics`: Aggregated tables for Looker dashboards.
*   **Vertex AI:** Prompts are versioned and stored in `packages/prompt-registry/` as YAML templates. Use Vertex AI registries to validate models.

### 2. AlloyDB Configuration
*   Deploy databases in private VPC subnets.
*   Route external connections through VPC Connectors to ensure security.

### 3. MCP & ADK Layout
*   Model Context Protocol (MCP) servers run on Cloud Run, providing AI agents with read-only access to transactional data.
*   Manage Agent Development Kit (ADK) configurations inside `services/agent-coach-service/`.

---

## Local Workspace Setup & Developer Checklists

### 1. Developer Machine Prerequisites
*   Install Git, Node.js (v18+), Python (3.11+), and Docker.
*   Install the Google Cloud SDK and authenticate locally:
    `gcloud auth login` and `gcloud auth application-default login`.

### 2. First-Day Engineering Checklist
*   [ ] Clone the repository and configure project access keys.
*   [ ] Connect to the Dev environment using Google Cloud credentials.
*   [ ] Initialize node modules and verify package structures.
*   [ ] Run local development environments and confirm services load without errors.

### 3. Build Verification Checklist
*   [ ] Run local code formatter checks: `npm run format`.
*   [ ] Run automated unit test suites: `npm run test`.
*   [ ] Verify container image builds locally using Docker.
*   [ ] Trigger a build in the remote Dev pipeline and confirm deployment status in Google Cloud Console.

---

**Approved & Signed By:**  
*Google Cloud Principal Delivery Engineer, Project AAROHAN*  
*Director, Google Cloud Professional Services*  
*Head, Digital Transformation Office (DTO), IDBI Bank*
