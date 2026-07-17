# Hackathon Submission Package

## Executive Summary

Project AAROHAN is a demo-ready MSME lending platform that simulates a real underwriting journey from customer login through data enrichment, credit evaluation, CAM generation, marketplace routing, and executive oversight. It is packaged for hackathon judging as a high-trust enterprise prototype with a deterministic demo studio and repeatable personas.

## Innovation

- Uses a digital banking twin pattern to make the lending journey repeatable for judges.
- Combines a customer portal, simulation control plane, and domain services in one guided experience.
- Makes credit outcomes explainable through financial-health and CAM outputs.
- Supports multiple borrower profiles so the demo can show approve, watchlist, and reject paths.

## Business Value

- Reduces underwriting friction by consolidating registry checks and scoring into one guided flow.
- Helps relationship managers and credit teams review files faster with structured outputs.
- Improves demo quality by removing the need for manual seed preparation.
- Gives executives a portfolio view that ties the operational journey to business outcomes.

## AI Usage

AI support in the repository is used in an assistive, demo-oriented way.

- Decision narratives and report summaries are presented in a way that is easy for reviewers to explain.
- The simulation layer keeps outcomes deterministic for judging.
- When a service is not available in the RC1 demo path, the reporting layer can fall back to local markdown generation.

## Architecture

- React portal for the user experience.
- FastAPI microservices for domain logic.
- ESE control plane for demo orchestration.
- SQLite-backed demo data for repeatable runs.
- JWT-based authentication and role-aware access.

## Technology

- Frontend: React, TypeScript, Vite, Material UI, Zustand, TanStack libraries.
- Backend: Python, FastAPI, Uvicorn, SQLAlchemy, Pydantic.
- Runtime: SQLite, Docker Compose, Poetry, npm workspaces, Turbo.

## Demo Flow

1. Sign in with a seeded demo account.
2. Open the Demo Studio or jump directly to the guided walkthrough.
3. Select a curated borrower persona.
4. Run onboarding and identity verification.
5. Review GST, Account Aggregator, EPFO, and MCA enrichment.
6. Open the Financial Health Card and credit decision output.
7. Show the marketplace or OCEN step.
8. Generate CAM and conclude on the executive dashboard.

## Known Limitations

- The repository is demo-oriented and not a fully production-hardened lending platform.
- Some infrastructure and shared-package descriptions are documentation-first rather than code-complete in this workspace.
- The portal bundle is large and emits a Vite chunk-size warning.

## Future Scope

- Complete the production deployment and infrastructure code path.
- Expand explainability and fraud registry integration.
- Add more robust observability and hardening for public release.
- Reconcile documentation-only packages with actual implementation modules.
