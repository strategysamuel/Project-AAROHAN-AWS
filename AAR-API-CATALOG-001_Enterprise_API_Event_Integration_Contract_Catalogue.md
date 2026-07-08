# Enterprise API, Event & Integration Contract Catalogue

**Document ID:** AAR-API-CATALOG-001  
**Document Name:** Enterprise API, Event & Integration Contract Catalogue  
**Version:** 1.0  
**Status:** Approved for Core Integration & API Gateway Assembly  
**Dependencies:** Entire Enterprise Repository, Engineering Build Blueprint (AAR-BLD-001), Screen Blueprint (AAR-SCR-001), and UX Playbook (AAR-UX-PLAYBOOK-001)  
**Target Audience:** Backend/Frontend Engineers, AI/Data/QA/DevSecOps Engineers, Integration Partners, and Google Cloud Professional Services  
**Document Owner:** Chief API Architect  
**Approval Authority:** Enterprise Architecture Review Board (EARB)

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief API Architect | Initial Strategic Release of API & Integration Contract Catalogue. | EARB Approved |

---

## Table of Contents
1. [Executive Summary & Architectural Standards](#executive-summary--architectural-standards)
2. [API Governance, Naming & Security Framework](#api-governance-naming--security-framework)
3. [Enterprise API Contract Catalogue (25 Domains)](#enterprise-api-contract-catalogue-25-domains)
4. [Enterprise Event Catalogue](#enterprise-event-catalogue)
5. [External Integration Contracts](#external-integration-contracts)
6. [Google Cloud Service Mapping & Apigee Setup](#google-cloud-service-mapping--apigee-setup)

---

## Executive Summary & Architectural Standards

This catalogue establishes the core contract interfaces, event payloads, and external integration points for Project AAROHAN. Managed centrally via **Google Cloud Apigee**, all contracts enforce a zero-trust model, request verification, strict schema validation, and transaction idempotency. 

### Design Principles:
1. **JSON-Standard Payload Structures:** All payloads must conform to RFC 8259 guidelines.
2. **Context-Based Security Filters:** Field-level masking rules are automatically applied by the gateway prior to external routing.
3. **Transaction Tracking:** Every API transaction must include the tracing header `X-Correlation-ID` to ensure end-to-end traceability across services.

---

## API Governance, Naming & Security Framework

### 1. Naming & URI Conventions
*   **Base URL Structure:** `https://api.idbi.aarohan.bank/v{major_version}/`
*   **Path Rules:** Use lower-case names separated by hyphens (e.g., `/msme-onboarding/registration-status`). Avoid verbs in resource paths; use standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).

### 2. Error Standards
All error responses must return the standard structure:
```json
{
  "errorCode": "AAR-ERR-XXX",
  "message": "Human-readable error explanation",
  "correlationId": "UUID-string",
  "timestamp": "ISO-8601-String",
  "details": []
}
```

### 3. Authentication & Authorization
*   **Access Control:** Every call must include an OAuth2 Bearer JWT in the `Authorization` header.
*   **Signatures:** High-value banking transactions must include a payload signature payload inside the header `X-Payload-Signature`.

---

## Enterprise API Contract Catalogue (25 Domains)

### 1. Authentication
*   **API ID:** AAR-API-ATH-001 (Request OTP / Validate Session)
*   **Business Purpose:** Authenticate user mobile credentials and issue access tokens.
*   **Consumer:** MSME Customer Portal, Employee Workspace, Partner Portal.
*   **Provider:** Identity & Authentication Service.
*   **Business Process:** Onboarding, customer/employee login.
*   **Input:** Mobile Number, Auth Type (OTP/Password), Role.
*   **Output:** Auth Token (JWT), Expiry (seconds), Session State, Masked Name.
*   **Validation Rules:** Mobile must contain exactly 10 digits; role must be validated against configured system categories.
*   **Business Rules:** Session duration is capped at 15 minutes for customer roles, and 10 minutes for employee roles.
*   **Authentication & Authorization:** None (Public Endpoint).
*   **Rate Limiting:** 5 requests per minute per IP.
*   **Error Responses:** `400 Bad Request` (Invalid number), `401 Unauthorized` (Bad credentials), `429 Too Many Requests`.
*   **Idempotency:** N/A (GET/POST key generation).
*   **Audit Requirements:** Log auth attempts to Security logs with masked IP.
*   **Versioning:** v1.0.
*   **Google Cloud Service Mapping:** Apigee, Identity Platform, Secret Manager.

---

### 2. Authorization
*   **API ID:** AAR-API-ATH-002 (Authorize Scope Permissions)
*   **Business Purpose:** Determine if a token session has permissions for specific actions.
*   **Consumer:** Microservices.
*   **Provider:** Policy & IAM Server.
*   **Input:** User Token (JWT), Action Target Path, Context parameters.
*   **Output:** Status (Allowed/Denied), Role Scope parameters, Row-level visibility restrictions.
*   **Validation Rules:** Header token must be a valid, signed JWT.
*   **Authentication & Authorization:** Authenticated token signature validation.
*   **Rate Limiting:** 500 requests per second per microservice instance.
*   **Google Cloud Service Mapping:** Apigee, Cloud IAM, AlloyDB.

---

### 3. User Management
*   **API ID:** AAR-API-USR-003 (Manage Profile Registry)
*   **Business Purpose:** Create, retrieve, and update operational roles and user metadata profiles.
*   **Consumer:** Administration Panel, Partner Portal.
*   **Provider:** User Registry Service.
*   **Input:** User ID, Profile Details (Name, Email, Branch Code).
*   **Output:** Updated Profile Record, active status state.
*   **Authentication & Authorization:** L5 Admin Role Token scope.
*   **Rate Limiting:** 100 requests per minute.
*   **Google Cloud Service Mapping:** Cloud Run, AlloyDB.

---

### 4. MSME Registration
*   **API ID:** AAR-API-MSM-004 (Register Business Entity)
*   **Business Purpose:** Capture core details (GSTIN, PAN, Director lists) and start the onboarding track.
*   **Consumer:** MSME Portal.
*   **Provider:** Onboarding Engine.
*   **Input:** Entity Legal Name, Registration Code (PAN/GSTIN), Contact Data.
*   **Output:** Lead Reference ID, Consent Status indicators.
*   **Validation Rules:** Inputs must pass checksum validation rules for tax registration numbers.
*   **Google Cloud Service Mapping:** Cloud Run, Firestore.

---

### 5. Consent Management
*   **API ID:** AAR-API-CON-005 (Verify Consent Request)
*   **Business Purpose:** Trigger and monitor data consent request flows.
*   **Consumer:** RM Workspace, Customer Portal.
*   **Provider:** Consent Engine.
*   **Input:** Customer Identifier, Scope of Data, Consent Period.
*   **Output:** Consent Request ID, Status (Pending/Approved/Expired).
*   **Google Cloud Service Mapping:** Cloud Workflows, Pub/Sub.

---

### 6. Account Aggregator
*   **API ID:** AAR-API-AA-006 (Retrieve Banking Statement Records)
*   **Business Purpose:** Fetch financial ledger details via Account Aggregator.
*   **Consumer:** Financial Health Card Engine.
*   **Provider:** Integration Gateway.
*   **Input:** Consent Artifact ID, Verification code.
*   **Output:** Signed financial statements (JSON/XML).
*   **Google Cloud Service Mapping:** Apigee, Cloud Run, Cloud Storage.

---

### 7. GST
*   **API ID:** AAR-API-GST-007 (Retrieve Tax Profile Data)
*   **Business Purpose:** Fetch tax statements and verify filing histories.
*   **Consumer:** Financial Health Card Engine, Credit Assessment.
*   **Provider:** DPI Gateway.
*   **Input:** GSTIN Number, Date Range (12 Months).
*   **Output:** Monthly GSTR filing statistics.
*   **Google Cloud Service Mapping:** Apigee, Cloud Run.

---

### 8. UPI
*   **API ID:** AAR-API-UPI-008 (Validate Payment Gateway)
*   **Business Purpose:** Initiate real-time payment transfers and resolve payment queries.
*   **Consumer:** Collections Portal, MSME Portal.
*   **Provider:** Payments Gateway.
*   **Input:** Virtual Payment Address (VPA), Transaction Value, Description.
*   **Output:** Payment Status (Success/Failure), UPI Ref ID.
*   **Google Cloud Service Mapping:** Apigee, Cloud Run.

---

### 9. EPFO
*   **API ID:** AAR-API-EPF-009 (Verify Employment Records)
*   **Business Purpose:** Fetch payroll data to verify employee count trends.
*   **Consumer:** Credit Assessment Engine.
*   **Provider:** DPI Gateway.
*   **Input:** Establish ID, date parameters.
*   **Output:** Active employee registration counts.
*   **Google Cloud Service Mapping:** Cloud Run.

---

### 10. TReDS
*   **API ID:** AAR-API-TRD-010 (Fetch Receivables Ledger)
*   **Business Purpose:** Query invoice registration lists to verify unpaid sales assets.
*   **Consumer:** Spreading Engine, Risk Management.
*   **Provider:** TReDS Gateway.
*   **Input:** GSTIN, Verification codes.
*   **Output:** Invoices status details (Settled/Pending).
*   **Google Cloud Service Mapping:** Cloud Run.

---

### 11. MCA
*   **API ID:** AAR-API-MCA-011 (Verify Corporate Registries)
*   **Business Purpose:** Query Ministry of Corporate Affairs database to verify registry filings.
*   **Consumer:** Onboarding Engine.
*   **Provider:** DPI Gateway.
*   **Input:** Corporate Identification Number (CIN).
*   **Output:** Director lists, active balance sheet metadata logs.
*   **Google Cloud Service Mapping:** Cloud Run.

---

### 12. CKYC
*   **API ID:** AAR-API-CKY-012 (Retrieve Central KYC Records)
*   **Business Purpose:** Verify client background details using official government registries.
*   **Consumer:** Onboarding Engine, Compliance Portal.
*   **Provider:** KYC Registry Connector.
*   **Input:** ID Type (PAN, Aadhaar), Document ID Code.
*   **Output:** Verified KYC records, profile photo string.
*   **Google Cloud Service Mapping:** Cloud Run.

---

### 13. DigiLocker
*   **API ID:** AAR-API-DGL-013 (Fetch Digital Document Store)
*   **Business Purpose:** Access verified digital documents.
*   **Consumer:** Customer Portal, RM Workspace.
*   **Provider:** DPI Gateway.
*   **Input:** Customer Authorization Code, Document Class.
*   **Output:** PDF download file link.
*   **Google Cloud Service Mapping:** Cloud Storage, Cloud Run.

---

### 14. Financial Health Card
*   **API ID:** AAR-API-FHC-014 (Generate Spreading Scores)
*   **Business Purpose:** Calculate cash flow statements, debt service coverage, and alternate risk scores.
*   **Consumer:** Credit Assessment Engine, RM Workspace.
*   **Provider:** Spreading Engine.
*   **Input:** Customer ID, Statement Source file tags.
*   **Output:** Financial health scorecard.
*   **Google Cloud Service Mapping:** Cloud Run, AlloyDB.

---

### 15. AI Decision Engine
*   **API ID:** AAR-API-AID-015 (Calculate Credit Scores)
*   **Business Purpose:** Run AI/ML scoring models to calculate default risk metrics.
*   **Consumer:** Credit Assessment Engine.
*   **Provider:** Data & AI Squad.
*   **Input:** Scorecard data vectors.
*   **Output:** Risk Score values, Probability of Default (PD).
*   **Google Cloud Service Mapping:** Vertex AI, BigQuery ML.

---

### 16. Credit Assessment
*   **API ID:** AAR-API-CAS-016 (Evaluate Loan Limits)
*   **Business Purpose:** Apply credit limits and process policy exception checks.
*   **Consumer:** RM Workspace, Credit Analyst Portal.
*   **Provider:** Credit Core Engine.
*   **Input:** Customer ID, proposed loan details.
*   **Output:** Evaluated credit limit, exception warnings list.
*   **Google Cloud Service Mapping:** Cloud Workflows, AlloyDB.

---

### 17. CAM Generation
*   **Module ID:** AAR-API-CAM-017 (Compile CAM Files)
*   **Business Purpose:** Generate the text drafts and compile the final Credit Assessment Memo (CAM).
*   **Consumer:** Credit Analyst Portal, Committee Workspace.
*   **Provider:** CAM Compiler.
*   **Input:** Transaction ID, template parameters.
*   **Output:** PDF File URL.
*   **Google Cloud Service Mapping:** Vertex AI (Gemini), Cloud Run.

---

### 18. Workflow
*   **API ID:** AAR-API-WFE-018 (Process Stage Transitions)
*   **Business Purpose:** Orchestrate loan life-cycle states and manage case approvals.
*   **Consumer:** All Workspace Portals.
*   **Provider:** Workflow Engine.
*   **Input:** Case ID, target state, validation parameters.
*   **Output:** Updated workflow state, active SLA status.
*   **Google Cloud Service Mapping:** Cloud Workflows, Firestore.

---

### 19. Portfolio Intelligence
*   **API ID:** AAR-API-PTI-019 (Retrieve Portfolio Statistics)
*   **Business Purpose:** Query aggregations of active loans, yields, and overall portfolio risk levels.
*   **Consumer:** Executive Portal, Risk Management Portal.
*   **Provider:** Portfolio Engine.
*   **Input:** Segment filters (Region, Sector, Limit tier).
*   **Output:** Aggregate portfolio yield metrics.
*   **Google Cloud Service Mapping:** Looker API, BigQuery.

---

### 20. Executive Dashboard
*   **API ID:** AAR-API-EXD-020 (Fetch Executive Dashboard Metrics)
*   **Business Purpose:** Aggregate high-level operational statistics and yield data.
*   **Consumer:** Executive Cockpit.
*   **Provider:** Looker Dashboard services.
*   **Input:** Date parameters.
*   **Output:** KPI summaries, regional yield distributions.
*   **Google Cloud Service Mapping:** Looker.

---

### 21. Reporting
*   **API ID:** AAR-API-RPT-021 (Generate PDF Reports)
*   **Business Purpose:** Queue and generate PDF reporting files.
*   **Consumer:** All workspaces.
*   **Provider:** Reporting Engine.
*   **Input:** Report Type, Parameter values.
*   **Output:** Downloadable file references.
*   **Google Cloud Service Mapping:** Cloud Storage, Cloud Run.

---

### 22. Notifications
*   **API ID:** AAR-API-NOT-022 (Dispatch Notifications)
*   **Business Purpose:** Queue and dispatch real-time SMS, emails, and alerts.
*   **Consumer:** All internal system services.
*   **Provider:** Notifications Engine.
*   **Input:** User ID, Delivery template, messaging channels.
*   **Output:** Message reference code.
*   **Google Cloud Service Mapping:** Pub/Sub, Firebase Cloud Messaging.

---

### 23. Audit
*   **API ID:** AAR-API-AUD-023 (Log System Events)
*   **Business Purpose:** Write immutable log audit events.
*   **Consumer:** All services.
*   **Provider:** Audit Engine.
*   **Input:** Target Event Details, Correlation ID, Actor ID.
*   **Output:** Log status confirmation.
*   **Google Cloud Service Mapping:** Cloud Logging, Pub/Sub.

---

### 24. Administration
*   **API ID:** AAR-API-ADM-024 (Update Policy Rule Settings)
*   **Business Purpose:** Update system policy configurations and rate calculations dynamically.
*   **Consumer:** Admin Console.
*   **Provider:** Admin Service.
*   **Input:** Parameter Code, Value parameters.
*   **Output:** Status (Success/Failure).
*   **Google Cloud Service Mapping:** Cloud Run, AlloyDB.

---

### 25. AI Business Coach
*   **API ID:** AAR-API-ABC-025 (Process Coach Queries)
*   **Business Purpose:** Process natural language questions for MSME business advisory.
*   **Consumer:** MSME Customer Portal.
*   **Provider:** Conversational Engine.
*   **Input:** User Query string, Session context ID.
*   **Output:** Assistant Response text, action recommendations.
*   **Google Cloud Service Mapping:** Vertex AI (Gemini), Agent Development Kit.

---

## Enterprise Event Catalogue

All internal messages use Google Cloud Pub/Sub and Eventarc to route events asynchronously.

```
+───────────────────────────────────────────────────────────────+
| Pub/Sub Event Wrapper                                         |
+───────────────────────────────────────────────────────────────+
| Header: {                                                     |
|   "eventId": "UUID-String",                                   |
|   "eventType": "bank.aarohan.lead.registered",                |
|   "timestamp": "ISO-8601-String",                             |
|   "correlationId": "UUID-String"                              |
| }                                                             |
| Data: {                                                       |
|   "leadId": "LEAD-10029",                                     |
|   "entityName": "XYZ Logistics",                              |
|   "rmId": "RM-209"                                            |
| }                                                             |
+───────────────────────────────────────────────────────────────+
```

### 1. Business Events
*   `bank.aarohan.lead.registered`: Triggered when an RM creates a new client lead record.
*   `bank.aarohan.consent.completed`: Dispatched when a customer approves a data access consent request.

### 2. Domain Events
*   `bank.aarohan.spreading.completed`: Dispatched when the financial health data is calculated and ready.
*   `bank.aarohan.score.calculated`: Dispatched when the risk assessment scorecard calculation is complete.

### 3. AI Events
*   `bank.aarohan.summary.drafted`: Sent when Gemini completes narrative generation for a CAM.
*   `bank.aarohan.coaching.triggered`: Sent to suggest cash-flow advisory steps based on ledger changes.

### 4. Workflow Events
*   `bank.aarohan.workflow.stepped`: Triggered when a case transitions between stages.
*   `bank.aarohan.sla.breached`: Fired if a stage remains uncompleted past SLA thresholds.

### 5. Notification & Audit Events
*   `bank.aarohan.notification.queued`: Fired to queue delivery of email or SMS messages.
*   `bank.aarohan.security.anomaly`: Dispatched on failed login validation warnings.

---

## External Integration Contracts

| Partner Interface | Protocol | Encryption | Authentication | Data Format |
| :--- | :--- | :--- | :--- | :--- |
| **GSTN Gateway** | REST API | AES-256 Payload | OAuth2 + OTP | JSON |
| **Account Aggregator**| REST API | Diffie-Hellman / JWS | Custom Key Tokens | JSON / XML |
| **OCEN** | REST API | JWS Signature | OAuth2 Client Credentials| JSON |
| **ULI** | SOAP/REST | TLS 1.3 | mTLS Certificate | XML / JSON |
| **UPI** | ISO 8583 | HSM Encryption | Private Signatures | Key-value |
| **TReDS** | REST API | AES-256 | API Key + JWT | JSON |
| **CGTMSE** | REST API | TLS 1.3 | Client Token | JSON |
| **CKYC** | SFTP/REST | PGP / TLS | Cert mTLS | Binary / JSON |
| **MCA** | SOAP/REST | TLS 1.3 | API Key Credentials | XML / JSON |

---

## Google Cloud Service Mapping & Apigee Setup

```
┌──────────────────────────────────────────────────────────────┐
│                  APIGEE API GATEWAY SYSTEM                   │
├──────────────────────────────┬───────────────────────────────┤
│    Security / Rate Limit     │     Transformation / Audit    │
│  - OAuth Verification        │  - XML to JSON mapping        │
│  - Spike Arrest Policies     │  - Correlation Log Tracing    │
└──────────────────────────────┴───────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌───────────────────────┐             ┌────────────────────────┐
│     CLOUD RUN GRID    │             │   EVENTARC / PUB/SUB   │
│  - Business APIs      │             │  - Asynchronous Events │
└───────────────────────┘             └────────────────────────┘
```

1. **Apigee:** Central gateway for routing external integrations, validating tokens, and rate limiting (Spike Arrest).
2. **Cloud Run:** Hosts internal and business APIs within isolated containers.
3. **Pub/Sub & Eventarc:** Message queues for decoupled event-driven services.
4. **Cloud Logging & Monitoring:** Aggregates correlation IDs to trace API latency.

---

**Approved & Signed By:**  
*Chief API Architect, Project AAROHAN*  
*Director, Google Cloud Professional Services*  
*Head, Digital Transformation Office (DTO), IDBI Bank*
