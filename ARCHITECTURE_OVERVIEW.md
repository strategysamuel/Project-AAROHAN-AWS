# Architecture Overview

## Frontend

The frontend is a React and Vite customer portal located in [apps/customer-portal](apps/customer-portal). It provides login, demo persona selection, guided journey navigation, report downloads, and executive dashboard access.

## Backend

The backend is implemented as FastAPI services under [services](services). The auth service handles sign-in and JWT issuance, while the domain services implement the lending journey, score aggregation, report generation, and executive views.

## Microservices

The visible service set includes:

- auth-service
- onboarding-service
- consent-service
- gst-service
- aa-service
- fhc-service
- credit-engine
- cam-service
- rm-workspace-service
- exec-service
- ews-service
- ckyc-service
- mca-service
- epfo-service
- document-service
- portfolio-service
- rbi-fraud-service
- treds-service
- ocen-uli-service
- ese-core
- ese-admin-service

## Workflow

The standard lending flow is:

1. Login
2. Onboarding
3. Identity verification
4. CKYC
5. GST
6. Account Aggregator
7. EPFO
8. MCA
9. Financial Health Card
10. Credit decision
11. Marketplace or OCEN routing
12. CAM generation
13. Executive dashboard review

The RC1 demo studio wraps this flow in a guided experience so judges can follow it without needing manual setup.

## AI Components

The repository uses AI-adjacent functionality in a controlled way:

- Explainable credit decision summaries.
- Report generation with fallback local markdown generation when a service is unavailable.
- Demo-oriented narrative outputs for presentation and review.

The simulation layer keeps the demo deterministic so that the judged result does not depend on live external APIs.

## Security

- JWT access and refresh tokens.
- Role-based permissions.
- Protected routes for authenticated portal flows.
- CORS middleware on service entrypoints for local and demo use.

## Deployment

The repository is prepared for local demo operation with:

- npm workspace builds for the portal.
- Poetry and Uvicorn for service startup.
- Docker Compose for the simulation stack.
- SQLite-backed demo datasets.

For the hackathon package, the main goal is deterministic local reproducibility rather than a production rollout sequence.
