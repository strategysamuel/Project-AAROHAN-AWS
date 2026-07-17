# Project AAROHAN: Technical White Paper
## AAR-LCP-005: Architecture, Causal Modeling, and Digital Public Infrastructure Sandboxing

**Document Classification:** Technical White Paper & Research Specification  
**Version:** ESE v1.0.0 (GA)  
**Publish Date:** July 8, 2026  
**Board approval:** Chief Technology Officer (CTO), Enterprise Architect, Principal Software Engineer, AI Engineering Lead, Banking Domain Architect, Cloud Solutions Architect, Technical Writer, Research & Innovation Lead  

---

## 1. Executive Summary
This paper details the design, engineering principles, and deployment model of **Project AAROHAN**, a Living Enterprise Digital Banking Twin designed to transform MSME underwriting. By sandboxing India’s Digital Public Infrastructure (DPI) registries locally, AAROHAN offers banks and FinTechs a zero-network-dependency, secure environment to run cash-flow credit evaluations, test policies, and train relationship teams.

---

## 2. Background & Problem Statement
Small and Medium Enterprises (MSMEs) form the backbone of emerging economies. In India, a massive credit gap persists due to the friction of manually verifying business records (GSTN, EPFO, CKYC, MCA) and the lack of asset collateral. Furthermore, financial institutions lack isolated staging environments to stress-test credit models under varying macroeconomic indicators.

---

## 3. Product Vision
AAROHAN aims to replace static JSON mock architectures with a dynamic, transaction-level digital banking twin. By modeling macroeconomic variables (such as repo rates, inflation, fuel costs) and propagating events through a localized event broker, the twin replicates the behavior of a real lending ecosystem.

---

## 4. System Overview
The platform consists of two principal components:
1.  **Enterprise Simulation Engine (ESE)**: Manages timeline clock ticks, persona state transitions, and downstream ledger generation.
2.  **Digital Banking Twin Core**: Replicates external public registries and handles credit, risk, and fraud verifications.

---

## 5. Solution Architecture
AAROHAN adopts **Clean Architecture** patterns, separating the application layer, domain entity formulas, and infrastructure adapters:
- **Domain Layer**: Contains invariant math models (DSCR, FHC, credit scores).
- **Use Cases Layer**: Coordinates the 10-step digital onboarding journey.
- **Infrastructure Layer**: Declares API routers and database handlers.

---

## 6. Microservices Architecture
The platform is organized into three microservices:
1.  **ese-admin-service**: The orchestration control center exposing APIs for journey simulation, clock progression, branding, and report exports.
2.  **document-service**: Manages generation of PDF/Excel compliance reports.
3.  **portfolio-service**: Tracks loan accounts, collections, and outstanding aggregates.

---

## 7. Enterprise Simulation Engine (ESE)
The ESE acts as the simulation coordinator, managing:
- **clock.py**: Progresses dates and schedules recurring batch calculations.
- **replay_engine.py**: Serializes active parameters to allow presenters to replay demo runs.

---

## 8. Digital Banking Twin
The Twin acts as the local registry database representing:
- **DPI Registries**: Simulated endpoints for CKYC, GSTN (tax compliance), EPFO (payroll stability), and MCA (corporate health).
- **Lenders Network**: Five classes (PSB, Private, NBFC, FinTech, Cooperative) matching unique credit rules.

---

## 9. AI Components
Appraisals utilize Vertex AI nodes, returning **Deterministic Explainability Records (DER)**. Decision narratives are heuristic-driven, ensuring identical inputs yield consistent outputs.

---

## 10. Event-Driven Simulation
The event engine (`event_engine.py`) enforces a publish-subscribe dispatch loop. An initial event (e.g. tax file upload) publishes a topic, triggering recalculations of FHC indices, credit scores, and active banking offers.

---

## 11. Financial Causal Model
The model (`causal_model.py`) calculates values based on:
$$\text{DSCR} = \frac{\text{Net Operating Income}}{\text{Total Debt Service}}$$
The system models seasonal patterns and regional profiles (monsoons in Tamil Nadu, logistics in Maharashtra) to simulate realistic credit variances.

---

## 12. Security Architecture
- **Production Isolation**: Database sandboxing isolates simulation datasets to local folder directories (`ese/datasets/`), protecting production instances.
- **PII Scrubbing**: Pre-deployment validators redact real Aadhaar/PAN formats.

---

## 13. Cloud Architecture
AAROHAN is containerized with Docker and optimized for GCP Cloud Run and GKE. Standard Cloud SQL manages system parameters, while Cloud Storage caches exported compliance files.

---

## 14. Technology Stack
- **Language**: Python 3.13.
- **Framework**: FastAPI, Pydantic, SQLAlchemy.
- **Database**: SQLite WAL (Write-Ahead Logging) Mode.
- **Infrastructure**: Docker, poetry.

---

## 15. Data Model Overview
The system tracks core tables:
- `borrower_profile`: Metadata, sector, regional indicators.
- `financial_ledger`: Ledger balances, tax compliance records.
- `loan_offer`: Limits, interest rates, SLA periods.

---

## 16. API Design Principles
- **RESTful Endpoints**: Predictable routing (`/ese/control/journey`, `/ese/control/compare`).
- **Profile Decoupling**: API payloads are identical across DEMO, UAT, and PRODUCTION environments.

---

## 17. Integration Strategy
Lenders connect systems by registering microservice endpoints with the **Adapter Factory**. The factory intercepts standard API requests and routes them to simulation mocks or live endpoints based on active profiles.

---

## 18. Production vs Simulation Architecture
- **Simulation**: Uses localized SQLite datasets, mock registries, and local simulation clock loops.
- **Production**: Seamlessly switches to enterprise databases, live public registries, and real credit bureau endpoints.

---

## 19. Testing & Quality Strategy
The platform implements a multi-tier testing strategy:
- **Unit Tests**: Validates calculations (DSCR, FHC) and event dispatches.
- **Regression Tests**: Validates E2E onboarding flows.
- **Pass Gate**: Mandatory 100% pass rate before golden release.

---

## 20. Performance & Scalability Considerations
The use of SQLite WAL mode and local cache decorators keeps API response latencies below 50ms, allowing smooth live demonstrations.

---

## 21. DevSecOps & CI/CD Readiness
- **Linting**: Automated flake8/black code checks.
- **CI Pipelines**: GitHub Actions runs test suites on every pull request.

---

## 22. Future Production Integration Roadmap
1.  **Phase 1**: Expand mock registries to cover regional cooperative bank schemas.
2.  **Phase 2**: Replace heuristic explainers with dynamic Vertex AI LLM calls.
3.  **Phase 3**: Establish live production pilot connectors.

---

## 23. Lessons Learned
- **Namespace Decoupling**: Separate test folders to prevent module conflicts during concurrent test execution.
- **Deterministic AI**: Using deterministic templates for AI responses ensures predictable demonstrations.

---

## 24. Future Enhancements
- **Redis State Cache**: Support multi-user concurrent presentation sessions.
- **Visual Event Propagation**: Graphic interfaces displaying cash flow changes.

---

## 25. Conclusion
AAROHAN introduces a high-fidelity digital banking twin paradigm. By modeling macroeconomic factors, propagating events, and sandboxing DPI stacks, it bridges the gap between software development and executive board approval.

---

## 26. References
- **AAR-ESE-011**: Sprint 3 Engineering Review Report.
- **AAR-ESE-014**: Golden Release Certification Report.
- **AAR-LCP-001**: Launch & Commercialization Strategy.

---

## 27. Appendix
- **API Spec**: Complete FastAPI OpenAPI JSON files.
- **Causal Formula Matrix**: Tables detailing formula coefficients under differing monsoon scenarios.
