# Project AAROHAN

## Executive Summary

Project AAROHAN is an enterprise MSME lending platform monorepo designed to support digital onboarding, registry-driven credit assessment, CAM generation, executive monitoring, portfolio monitoring, risk monitoring, embedded lending, trade finance, and relationship management.

The business vision is to provide a DPI-aligned lending journey for Indian MSMEs: capture customer and business identities digitally, enrich the file with external registry and banking signals, evaluate risk and policy compliance, generate credit appraisal outputs, and expose operating views for relationship managers and executives. The repository also includes a digital banking twin / simulation layer that powers deterministic demos, seeded persona scenarios, and workflow replay.

Target users inferred from the repository are MSME borrowers, relationship managers, credit analysts, credit committee members, risk teams, executive leaders, platform engineers, and simulation/demo operators. The system exists to shorten underwriting cycle time, standardize decisioning, improve portfolio visibility, and provide a controlled simulation environment for demonstrations and validation.

Documentation repeatedly describes a production-grade Google Cloud target state. The current codebase is not yet fully aligned with that target and includes local/demo implementations, SQLite-backed development flows, and service-level fallbacks.

---

## Business Goals

The platform’s business goals are consistent across the architecture and release documents:

- MSME lending: digitize onboarding, underwriting, limit discovery, and drawdown journeys.
- Digital onboarding: collect customer, business, address, director, and document data with validation.
- Credit assessment: aggregate registry, tax, banking, payroll, and fraud signals into financial health and credit outputs.
- CAM generation: produce structured credit appraisal memos and narrative decision support for reviewers.
- Executive monitoring: provide KPI, portfolio, and operations dashboards for leadership.
- Portfolio monitoring: aggregate application status, approval rates, exposure, and health indicators.
- Risk monitoring: surface fraud, compliance, and early-warning signals.
- OCEN ecosystem: support embedded lending / offer matching / disbursement workflows.
- Trade finance: support TReDS-related flows and invoice discounting concepts.
- Relationship management: give RM and committee-facing workflow views for case progression and approvals.

The business documents also place the platform in a broader digital public infrastructure context, with integrations and concepts around CKYC, GSTN, AA, MCA, EPFO, RBI fraud registry, ULI, Apigee, and AI-driven decision support.

---

## Current Repository Status

Current implementation should be read in four buckets.

### Completed

- A working React customer portal exists in [apps/customer-portal](apps/customer-portal).
- A broad FastAPI service layer exists under [services](services), including auth, onboarding, consent, GST, AA, FHC, credit-engine, CAM, EWS, CKYC, MCA, EPFO, document, exec, RM workspace, portfolio, RBI fraud, TReDS, and OCEN/ULI services.
- A substantial simulation / workflow engine exists in [services/ese-core](services/ese-core) and [services/ese-admin-service](services/ese-admin-service).
- Automated tests exist for workflow orchestration, onboarding, and multi-service regression paths in [tests](tests).
- A large body of architecture, release, operating, testing, and readiness documentation exists at the repository root.

### Partially implemented

- Auth is implemented with JWT, refresh tokens, role-permission mapping, and a permission checker, but the repository still uses a local development secret and broad CORS in service entrypoints.
- Onboarding supports customer CRUD, validation, persona loading, and document creation, but it is still connected to local/demo flows and not a full enterprise integration stack.
- GST, AA, FHC, credit decisioning, CAM generation, exec dashboards, and OCEN matching all exist as services, but many paths use simulation defaults, fallback values, or local SQLite data.
- The frontend portal is functional and component-rich, but it is wired to localhost service URLs and demo fallbacks.
- CI/CD and deployment are documented and partially scaffolded, but the repository does not contain the full code for the platform and infrastructure described in the docs.

### Planned

- Version 1.1 roadmap items in the feature and epic catalogues, including secret rotation automation, RBI fraud registry sync, explainable underwriting improvements, and other modernization items.
- Cloud-native production hardening described in the deployment architecture and release notes.
- Shared packages and platform assets described in the documentation but not present as code.

### Documentation only

- Several folders and components described in docs are not present as implementation code in this workspace: employee-workspace, admin-console, common-types, ui-components, mcp-core, prompt-registry, platform/database, platform/analytics, platform/apigee, infrastructure/terraform, and infrastructure/cloudbuild.
- The repository manifest and release notes describe a much broader production system than the currently visible source tree.

### Explicit conflicts between documentation and implementation

- Root README and service docs describe TypeScript / Node.js services, but the visible backend services are FastAPI / Python services.
- Documentation claims completed production-ready cloud deployment artifacts, but the visible repo contains documentation for infrastructure rather than the concrete Terraform / Cloud Build code itself.
- Documentation claims multiple apps and shared packages, but only the customer portal exists under apps and the packages folder is documentation-only in this workspace.

---

## Repository Governance

### Branching strategy

- Not yet defined in the visible repository artifacts.
- Evidence does show a release-oriented branch reference in the release notes: `release/v1.0-rc1`.
- The repository also contains PR, dev deployment, and UAT workflow documentation, which implies a branch-driven delivery flow.

### Pull request expectations

- Not yet defined as a formal policy in the visible repository artifacts.
- The GitHub Actions workflow README indicates PR verification includes code checks, security scans, and unit tests.

### Code review rules

- Not yet defined in the visible repository artifacts.
- The repository evidence implies review should protect architecture boundaries, security controls, and regression coverage.

### Definition of Done

- Not yet defined as a single authoritative checklist in the visible repository artifacts.
- Repository evidence suggests a feature should be considered done only when code, tests, release documentation, and deployment readiness are aligned.

### Release process

- PR verification on pull request creation.
- Dev deployment on merges to the main branch.
- UAT release on tag creation events.
- Release notes, validation reports, and signoff documents are maintained at the repository root.

### Versioning policy

- Release artifacts use semantic-looking version identifiers such as `v1.0.0` and `v1.1.0`.
- The detailed semantic versioning policy is not yet defined in the visible repository artifacts.

---

## Current Build Status

- Current build status: Not yet defined from a verified CI run in the visible repository artifacts.
- Last verified build: Not yet defined.
- Latest verified backend regression slice: `tests/test_regression_e2e.py` passed with 7/7 tests green after the RC1 hotfix.
- Development environment: Local demo / simulation mode with Docker, npm workspaces, Poetry, SQLite, and localhost service endpoints.
- Known build warnings: Root pytest configuration ignores many service-level test folders; documentation promises infrastructure and shared packages that are not physically present; several adapters and production paths are placeholders.
- Active frontend application: [apps/customer-portal](apps/customer-portal).
- Active backend services: auth-service, onboarding-service, consent-service, gst-service, aa-service, fhc-service, credit-engine, cam-service, exec-service, ews-service, ckyc-service, mca-service, epfo-service, document-service, rm-workspace-service, portfolio-service, rbi-fraud-service, treds-service, ocen-uli-service, and the ESE core/admin services.

---

## Current Development Phase

Project Phase: Production hardening and documentation/code reconciliation.

Current Milestone: Stabilized v1.0 implementation with a strong simulation layer and partial production-facing service coverage.

Next Milestone: Secret rotation, fraud registry sync, and explainable underwriting improvements from the v1.1 roadmap.

Overall Completion Estimate: Not yet defined precisely; the repository shows a mature demo and documentation baseline, but production implementation is still partial.

Highest Priority Work: Reconcile the documented enterprise target state with the implemented code, then harden security and external integrations.

---

## Repository Structure

### apps/

User-facing frontend applications. In the visible workspace, only [apps/customer-portal](apps/customer-portal) exists. The docs describe additional apps, but they are not present here.

### services/

Backend microservices and the simulation layer. This is the primary implementation surface. It contains domain services such as onboarding, auth, GST, AA, credit, CAM, EWS, CKYC, MCA, EPFO, OCEN, TReDS, exec, RM workspace, portfolio, RBI fraud, and the ESE core/admin services.

### packages/

The documentation describes shared libraries, common types, UI components, MCP utilities, and prompt registries. In the visible workspace this folder is documentation-only, which is an implementation gap.

### platform/

The documentation describes persistent platform assets such as database schemas, analytics tables, and Apigee bundles. In the visible workspace, this folder contains a README only and no implementation code.

### docs/

Engineering documentation, onboarding guidance, architecture references, and runbook directories. The folder is described as the canonical documentation hub but the visible workspace is still largely root-level markdown files.

### scripts/

Operational automation helpers. The README describes bootstrap, pre-deploy validation, and seed scripts; one visible example is [scripts/rotate_secrets.py](scripts/rotate_secrets.py).

### tests/

Repository-level integration, regression, workflow, and onboarding tests. The current suite exercises the end-to-end lending journey and workflow engine behavior.

### infrastructure/

The documentation describes Terraform and Cloud Build configuration. The workspace currently contains a README only, so this is another documentation-first area rather than a source-complete implementation area.

### ese/

The simulation and demo data layer: personas, scenarios, seeded datasets, SQLite databases, and seed scripts. This folder powers deterministic demo and validation behavior for the digital banking twin.

### .github/

GitHub Actions workflow documentation exists, describing PR verification, dev deployment, and UAT release pipelines. The folder contains a README but no workflow YAML files in the visible workspace.

### Root-level architecture and release documents

The repository root contains a very large architecture, governance, release, backlog, and validation corpus that serves as the canonical business and engineering narrative for Project AAROHAN.

---

## Technology Stack

### Frontend

- React 19
- TypeScript
- Vite
- Material UI
- Emotion
- Zustand
- TanStack React Query
- TanStack Router
- React Hook Form
- Zod
- Axios

### Backend

- Python 3.12 in [pyproject.toml](pyproject.toml)
- FastAPI
- Uvicorn
- Pydantic v2
- SQLAlchemy
- Alembic

### Databases

- Local SQLite for development and demo flows
- Documentation target: AlloyDB / PostgreSQL-style managed relational storage
- Documentation target: BigQuery for analytics
- Documentation target: Cloud Storage for archival and documents

### Authentication

- JWT access tokens
- Refresh tokens
- Role-permission model
- OAuth2PasswordBearer integration in the auth service
- Documentation target: secret-managed signing keys and stronger production IAM controls

### Testing

- pytest
- FastAPI TestClient
- Repository-level regression and workflow tests
- Service-level tests inside many service folders

### Build tools

- npm workspaces
- Turbo
- Prettier
- TypeScript compiler
- Poetry

### DevOps

- Docker
- docker-compose.ese.yml for local multi-service simulation
- GitHub Actions workflow design documented in [.github/workflows/README.md](.github/workflows/README.md)
- Cloud Build / Cloud Run / deployment architecture documented, but not fully present as code artifacts

### Cloud

- Google Cloud is the documented target platform
- Cloud Run
- Secret Manager
- Artifact Registry
- Cloud Build
- Cloud Armor
- Apigee
- AlloyDB
- BigQuery
- Cloud Logging / Monitoring / Trace

### AI

- Vertex AI
- Gemini / Google Gen AI libraries
- ADK / MCP are heavily referenced in architecture documents
- Simulation and explainability layers are present in the credit and CAM services

### Messaging

- Pub/Sub is referenced in the backend dependency list
- Event publishing is implemented as local dispatch patterns via the ESE core event engine
- Event-driven architecture is documented across the repository

### API technologies

- REST APIs
- OpenAPI-style FastAPI endpoints
- JSON request / response models with Pydantic

### Monitoring

- Structured JSON logging with correlation IDs is implemented across services
- Documentation references Cloud Logging, Monitoring, Trace, and observability frameworks

---

## Architecture Overview

### Frontend architecture

The customer portal is a single React application with a large state container built around Zustand and a Material UI component system. It contains multiple domain screens: onboarding, CKYC, GST, AA, EPFO, MCA, CAM, and executive command center.

The app is designed to call backend APIs directly, mostly on localhost ports. It also contains demo/offline fallback behavior so the UI can remain usable when services are unavailable.

### Backend architecture

Backend services are organized as separate FastAPI applications, each with its own database models, schemas, and endpoint set. Services generally follow a consistent pattern: logging, CORS, correlation ID middleware, exception shaping, database initialization, and REST endpoints for the domain.

### Service architecture

The visible service layer is a microservice collection rather than a single unified API. Each service owns a domain slice such as onboarding, tax, banking, KYC, credit decisioning, or executive reporting. Several services read from the shared SQLite simulation store and the ESE core modules.

### Microservices

The codebase includes microservices for auth, onboarding, consent, GST, AA, FHC, credit, CAM, EWS, CKYC, MCA, EPFO, document management, exec reporting, RM workspace, portfolio, RBI fraud, TReDS, OCEN/ULI, and ESE admin control.

### Data flow

The intended data flow is: onboarding and consent establish the customer file; registry and banking services enrich the file; FHC and credit services aggregate and score the customer; CAM and exec services summarize the decision; OCEN and TReDS support downstream lending and trade-finance flows; ESE provides deterministic simulation, replay, and demo control.

### Authentication flow

Auth service issues access and refresh JWTs, stores refresh tokens, and exposes /auth/me plus a permission-guarded test endpoint. The frontend login flow fetches tokens from /auth/login and then calls /auth/me to populate the user profile.

### Workflow orchestration

Workflow orchestration is implemented in the ESE core and validated by tests. The workflow engine supports templates, execution, cancellation, replay, cloning, event publication, and audit/timeline capture.

### CAM generation pipeline

The CAM service aggregates upstream context from onboarding, CKYC, GST, AA, EPFO, and MCA-style tables, then compiles a structured appraisal memo. It is designed to produce JSON/HTML/PDF-style outputs and version history.

### Credit decision pipeline

The credit engine pulls financial health, onboarding, CKYC, GST, AA, EPFO, and MCA data, applies rule-engine or AI-style adapter logic, checks fraud conditions, computes recommendation fields, and persists a decision record.

### Document processing

Document handling is present in onboarding and document-service code paths, but the repository does not yet show a full enterprise document pipeline. The implementation is currently closer to metadata capture and mock/document registration than to a full content-management system.

### Simulation layer

The simulation layer is a major architectural element. It contains scenario JSON, persona JSON, seed scripts, state files, and the ESE core engine. This layer powers demo journeys, deterministic test outcomes, and the interactive control plane exposed by the ESE admin service.

---

## Architecture Constraints

The following rules must not be violated when extending Project AAROHAN:

- Preserve service boundaries.
- Never bypass authentication.
- Keep business logic inside services.
- Preserve API contracts.
- Maintain backward compatibility.
- Avoid duplicate implementations.
- Keep UI components reusable.
- Keep workflows event-driven.
- Keep demo and production logic separate whenever possible.
- Do not hardcode secrets in source code.
- Do not introduce uncontrolled cross-service imports.
- Do not weaken validation to force a feature to pass.

---

## Coding Principles

The repository should be maintained using the following principles:

- SOLID.
- DRY.
- KISS.
- Clean Architecture.
- Separation of Concerns.
- Defensive Programming.
- Explicit Typing.
- Enterprise Logging.
- Validation First.
- Fail Fast.

---

## AI Working Agreement

Future AI assistants working in this repository must:

1. Read PROJECT_CONTEXT.md first.
2. Never rewrite completed modules.
3. Preserve architecture.
4. Modify only the requested milestone.
5. Build successfully before completion.
6. Run tests before completion.
7. Update PROJECT_CONTEXT.md when major milestones finish.

---

## Business Modules

### Auth Service

- Purpose: identity validation, token issuance, and permission enforcement.
- Dependencies: local database models, password hashing, JWT helpers.
- Primary APIs: /auth/login, /auth/token/refresh, /auth/logout, /auth/me, /auth/test-permission.
- Current implementation status: implemented, but still local-development oriented.
- Future roadmap: stronger secret management, environment-based auth config, and production IAM alignment.

### Onboarding Service

- Purpose: customer registration, business registration, address capture, document metadata, validation, persona loading.
- Dependencies: validation schemas, local DB, ESE persona templates.
- Primary APIs: /customers, /customers/{id}, /customers/load-persona, /customers/validate, /customers/{id}/documents.
- Current implementation status: substantially implemented.
- Future roadmap: integrate real document processing, downstream workflow orchestration, and production identity sources.

### Consent Service

- Purpose: consent orchestration for account aggregator and GSTN-style flows.
- Dependencies: provider abstraction and ESE eventing.
- Primary APIs: described in code and tests; the service is part of the workflow but not fully documented in the visible reads.
- Current implementation status: partially implemented / mock-driven.
- Future roadmap: external consent connector integration.

### GST Service

- Purpose: GST profile synchronization, return analysis, compliance scoring, and risk profiling.
- Dependencies: provider layer, local models, ESE event engine.
- Primary APIs: GST sync/profile/analytics endpoints in the service.
- Current implementation status: implemented with analytics logic and mock provider fallback.
- Future roadmap: live registry integration and stronger data-source abstraction.

### Account Aggregator Service

- Purpose: linked account discovery, transaction ingestion, cash-flow analytics, behavior scoring.
- Dependencies: adapter factory, local SQLite simulation store, ESE event engine.
- Primary APIs: /aa/link, /aa/sync, /aa/accounts and related analytics endpoints.
- Current implementation status: implemented with strong simulation support.
- Future roadmap: production data-source integration and better connector isolation.

### Financial Health Card Service

- Purpose: compute aggregate financial health, ratings, and explainable sub-scores.
- Dependencies: onboarding, CKYC, GST, AA, EPFO, MCA, and local config tables.
- Primary APIs: /fhc/calculate and related card retrieval/override endpoints.
- Current implementation status: implemented.
- Future roadmap: align inputs with production data sources and shared scoring library.

### Credit Engine

- Purpose: generate credit recommendations, risk grades, approval probabilities, and human-review outcomes.
- Dependencies: FHC, onboarding, CKYC, GST, AA, EPFO, MCA, ESE state, adapter implementations.
- Primary APIs: /credit/evaluate, /credit/generate, /credit/recalculate, /credit/refresh, /credit/approve.
- Current implementation status: implemented with rule-engine and AI-style adapter scaffolding.
- Future roadmap: replace hardcoded/demo overrides with production model integration and live fraud registry sync.

### CAM Service

- Purpose: generate credit appraisal memos and versioned decision narratives.
- Dependencies: upstream context tables, CAM engine, ESE event engine.
- Primary APIs: /cam/generate and related dashboard/version/approval endpoints.
- Current implementation status: implemented.
- Future roadmap: deeper production document formatting and approval workflow integration.

### Executive Command Center Service

- Purpose: aggregate KPIs, portfolio health, operations, journey views, and executive reporting.
- Dependencies: many domain tables across the simulation database.
- Primary APIs: /exec/command-center and related report/admin endpoints.
- Current implementation status: implemented with strong fallback behavior.
- Future roadmap: real reporting pipelines and production data aggregation.

### RM Workspace Service

- Purpose: relationship-manager worklists, case management, and lending workflow views.
- Dependencies: service-local models and simulation data.
- Primary APIs: /rm/* endpoints.
- Current implementation status: present, but less thoroughly evidenced than onboarding/credit/CAM/exec.
- Future roadmap: richer workflow integration and UI parity with the documented operating model.

### EWS Service

- Purpose: early warning and risk monitoring.
- Dependencies: local models and simulation state.
- Primary APIs: /ews/* endpoints.
- Current implementation status: present.
- Future roadmap: stronger event and portfolio integration.

### CKYC Service

- Purpose: customer identity registry search and verification.
- Dependencies: adapter abstraction, onboarding references, local records.
- Primary APIs: /ckyc/search, /ckyc/records, /ckyc/verify, /ckyc/stats.
- Current implementation status: implemented with mock / simulated registry behavior.
- Future roadmap: live registry connector and identity assurance hardening.

### MCA Service

- Purpose: corporate registry profile and governance enrichment.
- Dependencies: provider abstraction and local data.
- Primary APIs: /mca/* endpoints.
- Current implementation status: implemented with simulation support.
- Future roadmap: live company registry integration.

### EPFO Service

- Purpose: payroll / employment registry enrichment.
- Dependencies: provider abstraction and local data.
- Primary APIs: /epfo/* endpoints.
- Current implementation status: implemented with simulation support.
- Future roadmap: live payroll registry integration.

### Document Service

- Purpose: document metadata / document intake support.
- Dependencies: service-local models and schemas.
- Current implementation status: present but only partially evidenced in the workspace reads.
- Future roadmap: full document pipeline and object-storage integration.

### Portfolio Service

- Purpose: portfolio analytics and aggregation.
- Dependencies: local models and executive dashboards.
- Current implementation status: present.
- Future roadmap: formal analytics warehouse integration.

### RBI Fraud Service

- Purpose: fraud registry and blacklist-style risk checks.
- Dependencies: adapter layer and local data.
- Current implementation status: present; credit engine contains explicit blacklist logic.
- Future roadmap: real registry sync and stronger fraud cell workflow.

### TReDS Service

- Purpose: trade receivables discounting / invoice finance support.
- Dependencies: service-local models and simulation data.
- Current implementation status: present.
- Future roadmap: production marketplace integration.

### OCEN / ULI Service

- Purpose: embedded credit offer matching and lending lifecycle management.
- Dependencies: adapter layer, lender registry, and simulation data.
- Primary APIs: eligibility, application, offers, accept, disburse, health endpoints.
- Current implementation status: partially implemented with deterministic simulation and placeholder production adapters.
- Future roadmap: live lender and platform integrations.

### ESE Core and ESE Admin

- Purpose: workflow orchestration, simulation control, datasets, replay, scenario comparison, reports, and demo execution.
- Dependencies: simulation datasets, control state, adapter factory, seed scripts.
- Current implementation status: substantial and central to the repository.
- Future roadmap: production adapter implementations and cleaner service boundaries.

---

## API Landscape

The repository exposes many backend services. The list below summarizes the implemented service responsibilities and the visible consumers.

### auth-service

- Responsibilities: authentication, token refresh, current user lookup, permission checks.
- Endpoints: /auth/login, /auth/token/refresh, /auth/logout, /auth/me, /auth/test-permission, /livez.
- Dependencies: users/roles/permissions tables, password hashing, JWT helpers.
- Consumers: customer portal login flow and any secured internal clients.

### onboarding-service

- Responsibilities: customer creation, list/get/update/delete, validation, persona load, document registration.
- Endpoints: /customers, /customers/{id}, /customers/load-persona, /customers/validate, /customers/{id}/documents, /livez.
- Dependencies: onboarding models and ESE persona templates.
- Consumers: customer portal onboarding flow, regression tests, downstream credit and FHC services.

### consent-service

- Responsibilities: consent request/status orchestration.
- Endpoints: consent flows described by the service code and regression tests.
- Dependencies: provider abstraction and eventing.
- Consumers: onboarding / AA / GST journeys.

### gst-service

- Responsibilities: GST sync, profile retrieval, tax analytics.
- Endpoints: GST profile/sync/analytics endpoints and health endpoints.
- Dependencies: GST providers, ESE event engine, local models.
- Consumers: onboarding flow, FHC, credit engine, executive dashboards.

### aa-service

- Responsibilities: link accounts, sync transactions, compute cash-flow intelligence.
- Endpoints: AA account and sync endpoints.
- Dependencies: AA adapter, transaction models, event engine.
- Consumers: FHC, credit engine, customer portal AA page.

### fhc-service

- Responsibilities: health card calculation, score history, config management.
- Endpoints: FHC calculation and retrieval endpoints.
- Dependencies: onboarding, CKYC, GST, AA, EPFO, MCA models.
- Consumers: credit engine, executive dashboard, CAM service.

### credit-engine

- Responsibilities: credit evaluation, approval submission, recalc/refresh, config management, blacklist overrides.
- Endpoints: /credit/evaluate/{customer_id}, /credit/evaluate, /credit/generate/{customer_id}, /credit/recalculate/{customer_id}, /credit/refresh/{customer_id}, /credit/approve/{decision_id}.
- Dependencies: FHC, onboarding, CKYC, GST, AA, EPFO, MCA, adapters, ESE eventing.
- Consumers: CAM, exec dashboard, OCEN/ULI, workflow tests.

### cam-service

- Responsibilities: CAM compilation, version compare, approval logs, dashboard views, template management.
- Endpoints: CAM generation and related memo/version endpoints.
- Dependencies: upstream domain tables, CAM engine, ESE event engine.
- Consumers: executive and committee workflows.

### exec-service

- Responsibilities: KPI aggregation, portfolio snapshot, journey rows, dashboard reports.
- Endpoints: /exec/command-center plus report/admin endpoints.
- Dependencies: many domain tables and simulation defaults.
- Consumers: executive command center UI.

### rm-workspace-service

- Responsibilities: RM task/workqueue style APIs.
- Endpoints: /rm/* endpoints.
- Dependencies: local models and simulated records.
- Consumers: RM-facing UI and workflow tests.

### ews-service

- Responsibilities: early warning evaluation and watchlist reporting.
- Endpoints: /ews/* endpoints.
- Dependencies: local models and simulation records.
- Consumers: risk monitoring surfaces.

### ckyc-service

- Responsibilities: CKYC search, verification, override, record management, stats.
- Endpoints: /ckyc/stats, /ckyc/search, /ckyc/records, /ckyc/verify/{customer_id}.
- Dependencies: adapter abstraction, onboarding linkages, local records.
- Consumers: onboarding, credit, FHC, tests.

### mca-service

- Responsibilities: company profile sync and governance scoring.
- Endpoints: /mca/* endpoints.
- Dependencies: provider abstraction and local records.
- Consumers: FHC, credit engine, executive reporting.

### epfo-service

- Responsibilities: employment/payroll sync and analytics.
- Endpoints: /epfo/* endpoints.
- Dependencies: provider abstraction and local records.
- Consumers: FHC, credit engine, executive reporting.

### document-service

- Responsibilities: document metadata / intake handling.
- Endpoints: /document/* or service-specific document endpoints as defined by its code.
- Dependencies: service-local schemas/models.
- Consumers: onboarding and customer servicing.

### portfolio-service

- Responsibilities: portfolio analytics.
- Endpoints: /portfolio/* endpoints.
- Dependencies: local records and aggregated decision data.
- Consumers: exec dashboard.

### rbi-fraud-service

- Responsibilities: fraud registry and blacklist risk evaluation.
- Endpoints: /rbi-fraud/* endpoints.
- Dependencies: adapter layer and local registry data.
- Consumers: credit engine and risk workflows.

### treds-service

- Responsibilities: trade receivables and invoice finance support.
- Endpoints: /treds/* endpoints.
- Dependencies: service-local records.
- Consumers: trade finance flows and regression tests.

### ocen-uli-service

- Responsibilities: eligibility checks, application submission, offer generation, acceptance, disbursement, health checks.
- Endpoints: /healthz and /ocen/* lifecycle endpoints.
- Dependencies: matching engine adapters, lender registry, local database.
- Consumers: regression tests and portal embedded credit flows.

### ese-admin-service and ese-core

- Responsibilities: simulation control plane, personas, scenarios, datasets, replay, comparison, reporting, AI assistance, and adapter routing.
- Endpoints: /ese/control/*, /ese/health, /ese/datasets, /ese/profiles, /ese/scenarios, /ese/personas, /ese/adapters.
- Dependencies: simulation datasets, state file, adapter factory, engine modules.
- Consumers: portal demo controls and test harnesses.

---

## Frontend Applications

### customer-portal

- Purpose: self-service MSME portal with onboarding and operational views.
- Technology: React, TypeScript, Vite, Material UI, Zustand.
- Routing: app-level page switching is visible through imported pages and central state rather than a fully externalized router structure in the files read.
- State management: Zustand store in [apps/customer-portal/src/App.tsx](apps/customer-portal/src/App.tsx).
- Authentication: login against the auth service and token/profile hydration.
- API integration: direct fetch calls to local service URLs such as localhost:8000 and localhost:8090.
- Current maturity: functional demo-grade application with substantial UI coverage and local fallback logic.

Documented page modules visible in the source tree include onboarding, CKYC, GST, AA, EPFO, MCA, CAM, and executive command center.

### Missing documented frontend applications

- employee-workspace: documented but absent from the workspace.
- admin-console: documented but absent from the workspace.

---

## Backend Services

### auth-service

- Purpose: identity and permission service.
- Responsibilities: user authentication, token issuance, refresh, logout, profile lookup, permission enforcement.
- Current maturity: implemented.
- Known limitations: hardcoded local secret, broad CORS, local-development orientation.

### onboarding-service

- Purpose: customer onboarding and lifecycle capture.
- Responsibilities: create/update/search/delete customers, validate identifiers, load personas, capture business and address data, register documents.
- Current maturity: implemented.
- Known limitations: local/demo data dependence, no full document processing pipeline.

### consent-service

- Purpose: consent orchestration.
- Responsibilities: simulate consent requests and statuses.
- Current maturity: partially implemented.
- Known limitations: mock providers and simplified flows.

### gst-service

- Purpose: GST sync and analytics.
- Responsibilities: ingest and evaluate returns, produce compliance/risk analytics.
- Current maturity: implemented with simulation fallbacks.
- Known limitations: no evidence of live GSTN integration in workspace.

### aa-service

- Purpose: account aggregation and cash-flow analytics.
- Responsibilities: account discovery, transaction ledger sync, behavior scoring.
- Current maturity: implemented with simulation fallbacks.
- Known limitations: local SQLite-driven adapter behavior and placeholder production path.

### fhc-service

- Purpose: financial health scoring.
- Responsibilities: aggregate multi-source signals and produce score/rating output.
- Current maturity: implemented.
- Known limitations: still consumes local and simulation data.

### credit-engine

- Purpose: underwriting and recommendation generation.
- Responsibilities: evaluate customer risk, generate approval or review outputs, persist decisions, emit business events.
- Current maturity: implemented.
- Known limitations: hardcoded scenario overrides and local-data dependencies.

### cam-service

- Purpose: CAM generation.
- Responsibilities: compile memos, maintain versions, support approval logs and dashboards.
- Current maturity: implemented.
- Known limitations: production document and formatting integration still implicit rather than visible as infrastructure.

### exec-service

- Purpose: executive monitoring.
- Responsibilities: aggregate KPIs, journeys, operations, portfolio and risk views.
- Current maturity: implemented.
- Known limitations: fallback values imply incomplete live dependency integration.

### rm-workspace-service

- Purpose: RM operations workspace.
- Responsibilities: task management and case views.
- Current maturity: present, but less evidenced in the files read.
- Known limitations: insufficient visibility into the full workflow model.

### ews-service

- Purpose: risk and early-warning monitoring.
- Responsibilities: watchlists, signals, alerts.
- Current maturity: present.
- Known limitations: not fully validated against live source systems.

### ckyc-service

- Purpose: identity registry validation.
- Responsibilities: search, verify, store, override CKYC records and logs.
- Current maturity: implemented with simulated registry adapter support.
- Known limitations: mock adapter path remains central.

### mca-service

- Purpose: company registry and governance enrichment.
- Responsibilities: company profile sync, analytics, governance metrics.
- Current maturity: present.
- Known limitations: provider-driven mock behavior.

### epfo-service

- Purpose: payroll / workforce registry enrichment.
- Responsibilities: sync and profile EPFO-style records.
- Current maturity: present.
- Known limitations: provider-driven mock behavior.

### document-service

- Purpose: document intake and metadata.
- Responsibilities: document schemas and service APIs.
- Current maturity: present.
- Known limitations: full content-management and storage integration not evidenced.

### portfolio-service

- Purpose: portfolio aggregation.
- Responsibilities: portfolio KPIs and analytics.
- Current maturity: present.
- Known limitations: implementation detail not fully inspected in the files read.

### rbi-fraud-service

- Purpose: fraud registry and blacklist checks.
- Responsibilities: risk registry lookup and fraud signaling.
- Current maturity: present.
- Known limitations: production registry integration not visible.

### treds-service

- Purpose: trade finance / receivables discounting.
- Responsibilities: TReDS-style workflows.
- Current maturity: present.
- Known limitations: largely inferred from tests and file structure.

### ocen-uli-service

- Purpose: embedded credit offer matching.
- Responsibilities: eligibility, application, offers, acceptance, disbursement.
- Current maturity: implemented with strong simulation support.
- Known limitations: production adapters are placeholder-only.

### ese-core and ese-admin-service

- Purpose: simulation, orchestration, replay, reporting, and dataset/state control.
- Responsibilities: workflow engine, scenario comparison, financial causal model, clock, AI assistant, base adapters, seed/reset utilities.
- Current maturity: substantial and central.
- Known limitations: production adapters and some integrations are still intentionally stubbed.

---

## Shared Components

The repository does not yet expose shared runtime packages in the visible workspace, but several reusable patterns are present:

- Common utilities for JSON logging and correlation ID propagation across services.
- Common validation patterns using Pydantic models and regex constraints for PAN, GSTIN, CIN, Aadhaar, mobile, and pincode.
- Common JWT and role-permission logic in auth-service.
- Common SQLite / SQLAlchemy persistence patterns in services.
- Common simulation adapters and factories in ese-core and some domain services.
- Common event publication patterns through the ESE business event engine.
- Common fallback/demo patterns in frontend and backend modules.

Documented shared packages that are not physically present include common-types, ui-components, mcp-core, and prompt-registry.

---

## Security Model

### Authentication

Auth service issues JWT access and refresh tokens. Access tokens carry user id, mobile number, role, and permissions. The frontend uses /auth/login and then /auth/me to retrieve the profile.

### Authorization

Authorization is role and permission based. Permissions are stored as many-to-many mappings between roles and permissions, and the PermissionChecker dependency enforces route-level checks.

### JWT

JWT signing uses an in-repo development secret in the visible auth helper. This is acceptable for local development only and is a security gap for production.

### Permissions

The codebase uses explicit permission strings such as loan:approve and role names such as RELATIONSHIP_MANAGER / CUSTOMER in the auth data model.

### Secrets

Documentation expects Secret Manager–backed secrets in production, but the visible runtime still has hardcoded local values and local configs.

### CORS

Many service entrypoints enable allow_origins=["*"]. This is acceptable for demo/local development but is too broad for production banking workloads.

### Known security gaps

- Hardcoded JWT secret for local development.
- Broad CORS configuration across services.
- Multiple mock/placeholder adapters for sensitive external integrations.
- Demo-oriented localhost API wiring in the frontend.
- Checked-in local SQLite databases and simulation state files.

---

## Development Standards

Observed conventions in the repository:

- Service folders follow a consistent FastAPI pattern: app/main.py, app/models.py, app/schemas.py, app/database.py, optional app/providers.py or app/adapters.py, and tests.
- Frontend pages are organized under apps/customer-portal/src/pages.
- Service logging uses structured JSON-style strings with service names and correlation IDs.
- Naming is domain-oriented and prefixed by service role or architecture artifact code.
- Pydantic models are used for request validation and response shaping.
- SQLAlchemy is used for ORM persistence.
- Tests rely on FastAPI TestClient and dynamic service imports.
- Documentation is deeply structured and uses enterprise architecture and release governance naming.
- Repo scripts and manifests are aligned to a monorepo style even though the backend language is Python.

Observed gaps in standards:

- Documentation and implementation are not fully synchronized.
- Some services rely on hardcoded ports and local file paths.
- Some placeholder code uses pass or NotImplementedError intentionally, but without a clear production readiness boundary in code.

Commit conventions are not visible from source files alone; no explicit commit policy is implemented in the workspace beyond documentation references.

---

## Testing Strategy

### Unit tests

There are service-level tests in many service folders, and the root pytest configuration references service paths directly.

### Integration tests

The root test suite includes multi-service journey tests that validate cross-service scenarios such as onboarding, GST, AA, FHC, credit evaluation, CAM generation, RM workspace, exec dashboard, CKYC, MCA, EPFO, TReDS, and OCEN disbursement.

### Regression tests

The repository contains [tests/test_regression_e2e.py](tests/test_regression_e2e.py), which exercises the end-to-end lending journey and major business modules.

### Workflow tests

[tests/test_workflow_engine.py](tests/test_workflow_engine.py) validates workflow templates, execution, cancellation, replay, cloning, export, and concurrency.

### End-to-end tests

[tests/test_regression_e2e.py](tests/test_regression_e2e.py) acts as the main E2E scenario suite.

### Coverage observations

- The repository has meaningful test coverage for the simulation / demo path and the main business journey.
- The root pytest.ini explicitly ignores many service test folders, which suggests the visible root suite is curated and not exhaustive.
- Some service directories contain tests, but the pytest config excludes them from the root run.

---

## Deployment Architecture

### Development

Development is centered on local execution with Docker, SQLite, and localhost service endpoints. The React app and backend services are designed to run independently during local development.

### Testing

Testing is performed through pytest, service-level test clients, and the simulation layer. The docker-compose.ese.yml file seeds and coordinates local service behavior.

### Production

The documented target production platform is Google Cloud: Cloud Run services behind Cloud Armor / load balancer / API gateway patterns with AlloyDB, BigQuery, Cloud Storage, Secret Manager, Artifact Registry, and observability services.

### Containers

The root Dockerfile builds a Python 3.12 slim image and installs Poetry dependencies. The compose file launches many service containers and a seeder init container.

### Cloud Run

Cloud Run is the named deployment target across the service and architecture documents.

### Docker

Docker is used for local orchestration and as the basis of the documented cloud deployment path.

### CI/CD

The GitHub workflow documentation describes PR verification, dev deployment, and UAT release flows. The architecture docs also reference Cloud Build and deployment pipelines.

### Infrastructure

Infrastructure is described through Terraform, Cloud Build, and platform architecture documents, but the actual infrastructure code is not present in the visible workspace.

---

## Technical Debt

### Documentation drift

The largest debt is that the architecture documents describe a more complete enterprise platform than the code presently contains.

### Duplicated logic

Correlation ID middleware, JSON logging, CORS policy setup, and database bootstrapping are repeated across many services.

### Hardcoded configuration

Local URLs, local secrets, local file paths, and fallback values are embedded across the frontend and services.

### Mock implementations

Many services use simulated provider classes, sandbox fallbacks, or default records instead of live integrations.

### Placeholder adapters

Production adapters in the ESE and OCEN layers are intentionally empty or raise NotImplementedError.

### Missing shared libraries

The docs describe shared packages that are not physically present in the workspace.

### Performance concerns

The repo is optimized for determinism and demo reliability rather than production throughput; many services still read from local SQLite and in-process simulation state.

### Security improvements

The auth secret, permissive CORS, demo endpoints, and local data files need production hardening.

---

## Known Gaps

### Implemented

- Customer portal shell and onboarding journey.
- Auth service with JWT and permissions.
- Core domain services for onboarding, GST, AA, FHC, credit, CAM, exec, CKYC, MCA, EPFO, EWS, OCEN, TReDS, portfolio, and RBI fraud.
- ESE simulation and workflow orchestration.
- Repository-level regression and workflow tests.
- Extensive architecture and operations documentation.

### Missing

- Physical frontend apps described by docs but absent from workspace: employee-workspace and admin-console.
- Physical shared packages described by docs but absent from workspace.
- Physical platform and infrastructure implementation files described by docs but absent from workspace.
- Public API specification files under docs/api-specs are not visible in the current read.
- Workflow YAML files are not visible even though the workflows README describes them.
- Full production adapters for several external integrations.

### Roadmap

- Secret rotation automation.
- RBI Central Fraud Registry sync.
- Explainable underwriting enhancements.
- Production adapter completion for external registries and lenders.
- Cloud-native infrastructure implementation to match the architecture documents.
- Shared package implementation.
- Documentation reconciliation with actual codebase state.

---

## AI Development Rules

Every future AI coding assistant working on Project AAROHAN should follow these rules:

- Never modify unrelated modules.
- Preserve the enterprise architecture and the current folder conventions.
- Preserve API compatibility unless an explicit breaking-change approval exists.
- Maintain TypeScript strictness in the frontend.
- Preserve Python typing, Pydantic validation, and FastAPI response models.
- Do not remove documentation unless replacing it with a better authoritative document.
- Prefer root-cause fixes over superficial patches.
- Keep demo/simulation logic separate from production logic where possible.
- Build and test the touched slice before declaring completion.
- Update documentation when implementing or changing externally visible behavior.
- Do not introduce breaking changes without explicit approval.
- Keep security-sensitive values out of source code.
- Respect the existing logging and correlation-id patterns.

---

## Milestone History

The repository evidence supports the following maturity arc:

1. Repository foundation and monorepo bootstrap.
2. Frontend portal and backend service scaffolding.
3. Authentication and onboarding implementation.
4. Registry and financial enrichment services.
5. Financial Health Card and underwriting logic.
6. CAM generation and executive dashboarding.
7. ESE simulation layer, seed data, scenario control, and workflow engine.
8. Regression and release documentation, including v1.0 release notes and validation reports.

Current project maturity is best described as: documentation-complete, demo-strong, production-partial.

The AAR-BUILD-020 hackathon release candidate now adds a dedicated demo studio, sandbox reset path, guided walkthrough, and sample report pack on top of the existing simulation layer.

---

## Current Sprint

The AAR-BUILD-020 hackathon release candidate milestone is complete.

The next logical milestone is production hardening of the current v1.0 platform before broadening the feature set.

The most defensible next sprint is to reconcile the implementation with the v1.1 roadmap items that have the strongest dependency value: secret rotation, fraud registry sync, and explainable underwriting improvements. These items unlock both security and decisioning maturity while reducing reliance on hardcoded or mock behaviors.

---

## Future Roadmap

Recommended implementation order based on repository dependency shape:

1. Reconcile documentation with implementation and establish the canonical source of truth.
2. Implement secret management and configuration hardening.
3. Complete live fraud registry integration.
4. Improve explainable underwriting and CAM narrative quality.
5. Replace placeholder adapters with production connectors.
6. Add missing shared libraries and platform/IaC code.
7. Externalize repeated logging, config, and validation patterns into shared utilities.
8. Expand the UI into the missing documented applications.
9. Introduce production observability and deployment code matching the architecture documents.

This order reduces risk because it prioritizes security and integration dependencies before adding more surface area.

---

## Milestone Tracker

| Milestone | Status | Notes |
| --- | --- | --- |
| Repository bootstrap and monorepo scaffolding | Completed | Root workspace, Turbo, Poetry, Docker, and repo-wide documentation are present. |
| Customer portal shell | Completed | The React portal exists with onboarding and executive pages. |
| Authentication and permissions | Completed | JWT login, refresh tokens, role-permission mapping, and permission checks are implemented. |
| Customer onboarding | Completed | Customer CRUD, persona loading, validation, and document metadata capture are present. |
| Consent orchestration | Partially implemented | Consent providers and flows exist, but visible code indicates mock-driven behavior. |
| GST, AA, and FHC enrichment | Completed | Domain services and scoring logic are implemented with simulation fallbacks. |
| Credit decisioning and CAM generation | Completed | Credit-engine and CAM service are implemented with deterministic demo behavior and aggregation logic. |
| Executive and risk dashboards | Completed | Exec, EWS, portfolio, RM workspace, and dashboard surfaces are present. |
| CKYC, MCA, EPFO, TReDS, OCEN/ULI | Partially implemented | Services exist, but several production adapters and integrations remain placeholder-only. |
| ESE simulation and workflow engine | Completed | Workflow orchestration, replay, scenario control, seed data, and admin control are implemented. |
| Hackathon RC1 release candidate | Completed | Demo studio, guided walkthrough, reset orchestration, and sample report pack are implemented in the customer portal. |
| Shared packages and platform code | Planned | Documented in README files, but not physically present in the workspace. |
| Production infrastructure implementation | Planned | Architecture is documented, but concrete IaC and pipeline code are not visible. |
| v1.1 modernization items | Planned | Secret rotation, fraud registry sync, and explainable underwriting remain roadmap items. |

---

## Repository Health Score

Scores are from 0 to 10 and are based on visible repository evidence.

- Architecture: 8/10. The target architecture is comprehensive and internally coherent, but implementation is uneven across the tree.
- Code Quality: 6/10. The main code is readable and patterned, but there is duplication, hardcoded configuration, and many simulation fallbacks.
- Documentation: 10/10. The repository is exceptionally well documented and traceable.
- Testing: 8/10. There is real E2E and workflow coverage, but the root suite is curated and not exhaustive.
- Deployment Readiness: 5/10. The deployment story is well described but not fully implemented in source artifacts.
- Security: 5/10. Authentication exists, but there are hardcoded secrets, permissive CORS, and mock integrations.
- Maintainability: 6/10. The structure is understandable, but duplication and documentation drift increase maintenance cost.
- Overall Enterprise Readiness: 7/10. The program is strong as a documented enterprise platform and demo system, but production completeness still needs follow-through.

Score rationale:

- Architecture is high because the business and system decomposition is thorough and consistent.
- Code quality is moderate because much of the system is intentionally demo-oriented.
- Documentation is the strongest area by far.
- Testing is good for the visible journey paths but not comprehensive enough to claim full production readiness.
- Deployment readiness is limited by absent infrastructure code and missing live integrations.
- Security requires hardening before regulated production use.
- Maintainability is reduced by repeated middleware/config patterns and absent shared libraries.

---

## AI Session Memory

Project identity: Project AAROHAN is an enterprise MSME lending platform monorepo with a strong simulation and documentation layer.

Architecture: React customer portal; Python/FastAPI microservices; ESE workflow and simulation engine; local SQLite/demo mode today; Google Cloud production target in documentation.

Current implementation state: customer portal and core backend services are implemented; many production integrations, shared libraries, and infrastructure assets are still missing or documentation-only.

Important constraints: do not modify unrelated modules; preserve enterprise architecture; keep demo and production logic separate where possible; avoid hardcoded secrets and localhost assumptions in production work.

Coding standards: preserve TypeScript strictness, Python typing, Pydantic validation, structured logging, FastAPI response shapes, and the existing service folder conventions.

Current milestone: AAR-BUILD-020 hackathon release candidate completed; next focus is production hardening and documentation/code reconciliation.

Next milestone: implement secret rotation, fraud registry sync, and explainable underwriting improvements, then complete shared libraries and production infrastructure.

---

## Session Handover

Current Sprint: AAR-BUILD-020 RC1 complete; production hardening and repository reconciliation next.

Current Objective: Preserve the documented enterprise structure while keeping the knowledge base aligned to implemented code and visible gaps, now including the RC1 demo studio and report pack.

Next Objective: Implement the highest-priority v1.1 dependencies in order: secret rotation, fraud registry sync, and explainable underwriting.

Blocked Items: Not yet defined.

Known Risks: Documentation drift, placeholder production adapters, permissive security defaults, and absent shared/infrastructure code.

Recommended Next Prompt: Review the v1.1 roadmap and implement the next production-hardening milestone without breaking existing demo and test flows.
