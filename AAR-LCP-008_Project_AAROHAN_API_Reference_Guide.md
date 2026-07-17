# Project AAROHAN: Developer API Reference Guide
## AAR-LCP-008: RESTful Endpoints, Schema Payloads, and System Integration Specification

**Document Classification:** Technical API Reference Manual  
**Platform Version:** ESE v1.0.0 (GA)  
**Security Scope:** Public Developer API & Private Admin Controls  
**Status:** **🟢 PUBLISHED & INTEGRATION READY**  

---

## 1. Executive Summary
This document provides the official API specification for **Project AAROHAN Enterprise Digital Banking Twin v1.0.0**. It outlines design standards, payload schemas, authentication protocols, and integration pathways to support software developers, banking technical staff, and system integrators.

---

## 2. API Design Philosophy
The AAROHAN API is built on **RESTful design principles**:
- Uses standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).
- JSON-formatted payloads.
- Clear distinction between tenant read operations and admin/simulation control commands.

---

## 3. System Architecture Overview
The platform exposes unified HTTP ports, backed by a microservices router:
- `ese-admin-service` handles all clock, branding, and simulation control endpoints.
- Underlying adapters route queries to internal sandboxes or external live registries based on active environment profiles.

---

## 4. Authentication & Authorization
- **Sandbox Modes (DEMO/TRAINING)**: Requires a static token passed in the header:
  `Authorization: Bearer aarohan_sandbox_secret`
- **UAT & Production Modes**: Integrates with corporate OAuth2 or JWT identity providers.

---

## 5. API Versioning Strategy
APIs are versioned explicitly via URL prefixes:
- `/v1/*` represent stable platform interfaces (Version 1.1 production equivalent).
- `/ese/*` represent simulation controls and Twin sandbox control interfaces.

---

## 6. Base URLs
- **Demo Environment**: `http://localhost:8000/`
- **Training Environment**: `https://training-twin.aarohan.internal/`
- **UAT Environment**: `https://uat-twin.idbi.co.in/`
- **Production Environment**: `https://twin.idbi.co.in/`

---

## 7. Request/Response Standards
- Content-type must always be `application/json`.
- Dates follow ISO-8601 formatting (`YYYY-MM-DDTHH:MM:SSZ`).
- Large numbers represent currency values in decimal formats (e.g. `2500000.0`).

---

## 8. Error Handling
Failed calls return consistent JSON envelopes:
```json
{
  "status_code": 400,
  "detail": "Detailed explanation of validation or system failure."
}
```

---

## 9. Rate Limiting
- **Sandbox/DEMO**: 1000 requests per minute per IP.
- **Production**: Rate-limited dynamically based on user role assignments.

---

## 10. Security Model
- Access control is managed via role-based permissions (Presenter vs. System Administrator).
- Staged production environments restrict `/ese/control/*` routes using API gateway rules.

---

## 11. Service Catalog
The following microservices are exposed via the Gateway:
1.  **Onboarding Service**: Customer and company profile registration.
2.  **CKYC Service**: KYC compliance searches.
3.  **GST Service**: Retreives trade and invoice ledgers.
4.  **Account Aggregator (AA) Service**: Consent requests and bank statement feeds.
5.  **EPFO Service**: Employee and salary payment records validation.
6.  **MCA Service**: Company registry status validation.
7.  **Financial Health Card Service**: Calculates metrics (DSCR, margins).
8.  **Credit Engine**: Underwrites limits based on scores and risk rules.
9.  **CAM Service**: Generates Credit Appraisal Memorandums.
10. **Executive Dashboard Service**: Aggregates portfolio metrics.
11. **Enterprise Simulation Engine**: Manages timeline clock and regional profiles.
12. **Demo Control Center**: Triggers one-click journeys, brand changes, and comparisons.

---

## 12. Endpoint Reference

### Endpoint 1: Scenario Comparison
*   **Method**: `POST`
*   **URL**: `/ese/control/compare`
*   **Purpose**: Perform side-by-side delta evaluations of two scenarios.
*   **Headers**: 
    - `Content-Type: application/json`
    - `Authorization: Bearer <token>`
*   **Request Body**:
    ```json
    {
      "left_scenario": "EXCELLENT_BORROWER",
      "right_scenario": "CASH_FLOW_STRESS"
    }
    ```
*   **Response Body**:
    ```json
    {
      "left_id": "EXCELLENT_BORROWER",
      "right_id": "CASH_FLOW_STRESS",
      "metrics_comparison": {
        "dscr": {"left": 2.1, "right": 0.85, "diff": -1.25, "impact": "CRITICAL DEGRADATION"}
      },
      "visual_explanations": "Under stress scenario, DSCR degrades below critical 1.0 threshold."
    }
    ```
*   **Error Codes**: `400 Bad Request`

### Endpoint 2: Enterprise Report Generation
*   **Method**: `POST`
*   **URL**: `/ese/control/report`
*   **Purpose**: Export compliance files in PDF, Excel, or Markdown formats.
*   **Headers**:
    - `Content-Type: application/json`
    - `Authorization: Bearer <token>`
*   **Request Body**:
    ```json
    {
      "report_type": "FHC",
      "format_type": "markdown",
      "data": {
        "customer_id": 120,
        "score": 90,
        "status": "EXCELLENT"
      }
    }
    ```
*   **Response Body**:
    ```json
    {
      "report_type": "FHC",
      "format": "markdown",
      "content": "# PROJECT AAROHAN - FHC REPORT\n..."
    }
    ```
*   **Error Codes**: `422 Unprocessable Entity`

### Endpoint 3: AI Explanation Generation
*   **Method**: `POST`
*   **URL**: `/ese/control/narrate`
*   **Purpose**: Get deterministic explanation text for credit decisions or risk markers.
*   **Request Body**:
    ```json
    {
      "category": "CREDIT_DECISION",
      "data": {"credit_score": 750}
    }
    ```
*   **Response Body**:
    ```json
    {
      "category": "CREDIT_DECISION",
      "narration": "The Credit appraisal decision is APPROVED..."
    }
    ```

---

## 13. Webhooks & Events
Webhook notifications are dispatched on simulation changes:
- `simulation.clock.ticked`: Fired when dates advance.
- `underwriting.verdict.appraised`: Fired when credit assessments complete.

---

## 14. Business Event Engine APIs
Trigger custom events in the system:
- `POST /ese/control/events` payload: `{"event_name": "GST_FILING_DEFAULT", "customer_id": 12}`.

---

## 15. Integration Profiles
Manage profiles using the admin settings endpoint:
- `POST /ese/control/profile` payload: `{"active_profile": "UAT"}`.

---

## 16. Dataset Marketplace APIs
- `GET /ese/datasets`: Lists all seeded datasets.
- `POST /ese/control/dataset` payload: `{"dataset": "agro"}` (switches active database).

---

## 17. Demo Journey APIs
- `GET /ese/journeys`: Lists all available demo scripts.
- `POST /ese/control/journey` payload: `{"journey_name": "MSME Lending Journey"}`.

---

## 18. Replay APIs
- `POST /ese/control/replay/record` (starts recording).
- `GET /ese/control/replay/summary` (returns step logs).

---

## 19. Health & Monitoring APIs
- `GET /livez`: Fast probe returning service UP state.
- `GET /health`: Complete microservice status checklist.

---

## 20. SDK Recommendations
We recommend using standard REST generators like `httpx` (Python), `axios` (JavaScript), or `HttpClient` (.NET) to interact with the endpoints.

---

## 21. OpenAPI / Swagger Guidance
OpenAPI 3.0 specs are hosted natively. Access the interactive UI at:
- `http://localhost:8000/docs` (Swagger)
- `http://localhost:8000/redoc` (ReDoc)

---

## 22. Testing APIs
Automated integrations can run regression scripts by calling target endpoints in sequence against the local sandbox.

---

## 23. Mock APIs
Mock APIs are fully active under the `DEMO` integration profile. Mocks require no third-party network connectivity.

---

## 24. Production Migration Guidelines
1. Configure credentials securely in Secret Manager.
2. Deploy Docker images to Cloud Run or GKE.
3. Switch config parameters to target `INTEGRATION_PROFILE=PRODUCTION`.

---

## 25. Troubleshooting
If endpoints return `503 Service Unavailable`, verify that target microservice components are running and accessible on the local network.

---

## 26. Glossary
- **DER**: Deterministic Explainability Record.
- **REST**: Representational State Transfer.
- **WAL**: Write-Ahead Logging.

---

## 27. Appendix
- **Common Payload Example**: Complete customer profile registry record.
- **Error Codes Matrix**: Lists standard system error codes and mitigations.
