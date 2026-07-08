# Project AAROHAN - Monorepo Codebase

Welcome to the Project AAROHAN engineering codebase repository. This repository houses the complete digital MSME lending platform, structured as a monorepo containing frontend applications, microservices, shared libraries, data models, and deployment configurations.

## Codebase Directory Structure

```
aarohan-monorepo/
├── .github/                  - GitHub Actions workflows and templates
├── apps/                     - Frontend web and mobile applications
│   ├── customer-portal/      - Self-service portal for MSMEs
│   ├── employee-workspace/   - Workspaces for RMs, Credit Analysts, and Committee
│   └── admin-console/        - Settings and administrative dashboard
├── services/                 - Backend Cloud Run microservices
│   ├── auth-service/         - Identity validation and OIDC auth
│   ├── onboarding-service/   - Onboarding state managers
│   ├── spreading-service/    - Financial statement spreading calculator
│   ├── credit-service/       - Credit assessment and risk scoring
│   ├── workflow-service/     - Lifecycle workflow state orchestration
│   └── agent-coach-service/  - Gemini-powered business coach
├── packages/                 - Shared libraries and components
│   ├── common-types/         - Shared TS type definitions and API interfaces
│   ├── ui-components/        - Material Design 3 shared frontend components
│   └── mcp-core/             - Model Context Protocol utilities
├── platform/                 - Database and platform integrations
│   ├── database/             - AlloyDB schema and migration logs
│   ├── analytics/            - BigQuery table structures and Looker files
│   └── apigee/               - Apigee API Gateway bundle structures
├── infrastructure/           - CI/CD and IaC configurations
│   ├── terraform/            - Terraform configuration files
│   └── cloudbuild/           - Cloud Build YAML triggers
├── docs/                     - Technical engineering documentation
├── tests/                    - Global integration, contract, and E2E test suites
└── scripts/                  - Operational automation scripts
```

---

## Core Engineering Conventions

1. **Language & Runtimes:**
   * Frontend: TypeScript & React (Vite-based).
   * Backend Services: TypeScript / Node.js (Express / NestJS).
   * Data & AI Workloads: Python 3.11 (Vertex AI SDK, ADK, MCP).
2. **Coding Standards:**
   * Run lint checks before commiting code: `npm run lint`.
   * Format code automatically using: `npm run format`.
3. **Secret Management:**
   * Do not commit sensitive credentials to the repository. Use `infrastructure/cloudbuild/` configurations to inject secrets from Google Cloud Secret Manager at runtime.

---

## Developer Quickstart

1. **Install Prerequisites:**
   Ensure Node.js (v18+), Python (v3.11+), and Docker are installed locally.
2. **Authenticate with Google Cloud:**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
3. **Initialize Repository:**
   ```bash
   npm install
   ```

---

**Lead Software Architect**  
*Enterprise Engineering, Project AAROHAN*
