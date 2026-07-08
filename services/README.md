# Services (services/)

This directory houses the containerized backend microservices that drive Project AAROHAN.

## Service Inventory & API Mapping

| Service Name | Purpose | Language / Runtime | Primary Database | Deployment Target |
| :--- | :--- | :--- | :--- | :--- |
| **auth-service/** | Session validation, OTP auth, active role checks | TypeScript / Node.js | Firestore | Cloud Run |
| **onboarding-service/** | Register business entity profiles, track onboarding states | TypeScript / Node.js | AlloyDB | Cloud Run |
| **spreading-service/** | Calculate financial ratios, parse statements | Python 3.11 | AlloyDB | Cloud Run |
| **credit-service/** | Evaluate credit rules, policy checks, run default ML models | Python 3.11 | AlloyDB / Vertex AI | Cloud Run |
| **workflow-service/** | Orchestrate workflow states and approvals | TypeScript / Node.js | Firestore | Cloud Run |
| **agent-coach-service/** | Host conversational business advisor agents | Python 3.11 (ADK/MCP) | Vector DB | Cloud Run |

---

## Coding Standards & Conventions

1. **REST APIs:** Express/NestJS (Node.js) or FastAPI (Python) returning standard error objects in case of failures.
2. **Containerization:** Keep base images minimal (use distroless/alpine runtimes). Configure health checks on port 8080.
3. **Database Execution:** Connect to databases using pool connectors. Maintain row-level data access limits.
