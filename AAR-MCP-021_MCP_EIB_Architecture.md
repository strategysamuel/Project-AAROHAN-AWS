# Enterprise Model Context Protocol (MCP) Architecture & Enterprise Intelligence Bus

**Document ID:** AAR-MCP-021  
**Document Name:** Enterprise Model Context Protocol (MCP) Architecture & Enterprise Intelligence Bus  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 through AAR-ADS-020 (All Previous Reference Architecture Volumes & Agentic Design Documents)  
**Next Artifact:** AAR-RAG-022 (Enterprise Knowledge, RAG & Vector Intelligence Architecture)  
**Target Audience:** IDBI Bank Board, Chief AI Officer, CIO, CTO, Google Cloud Principal AI Architects, and System Integrators  
**Document Owner:** Enterprise AI Integration Architect / Chief API Architect  
**Approval Authority:** AI Governance Committee (AIGC) / EARB  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Google Cloud Professional Services | Initial Release of Enterprise MCP & EIB Architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [PART 1: Enterprise MCP Vision](#part-1-enterprise-mcp-vision)
3. [PART 2: Enterprise Intelligence Bus Architecture](#part-2-enterprise-intelligence-bus-architecture)
4. [PART 3: MCP Communication Principles](#part-3-mcp-communication-principles)
5. [PART 4: Context Management Strategy](#part-4-context-management-strategy)
6. [PART 5: Enterprise Context Model](#part-5-enterprise-context-model)
7. [PART 6: Enterprise MCP Tool Registry](#part-6-enterprise-mcp-tool-registry)
8. [PART 7: Agent-to-Tool & Agent-to-Agent Communication](#part-7-agent-to-tool--agent-to-agent-communication)
9. [PART 8: Context Sharing & Memory Management](#part-8-context-sharing--memory-management)
10. [PART 9: Security, Trust, & Governance](#part-9-security-trust--governance)
11. [PART 10: Performance, Observability, & KPIs](#part-10-performance-observability--kpis)
12. [PART 11: Enterprise Intelligence Bus Reference Model](#part-11-enterprise-intelligence-bus-reference-model)
13. [PART 12: Conclusion](#part-12-conclusion)

---

## Executive Summary
This document defines the Enterprise Model Context Protocol (MCP) Architecture and Enterprise Intelligence Bus (AAR-MCP-021) for Project AAROHAN. It establishes MCP as the unified intelligence communication layer (EIB) connecting agents, core systems, registries, and data stores. The ERDA guidelines ensure that all MCP servers, clients, and tools are configured securely and performantly using native Google Cloud runtimes.

---

## PART 1: Enterprise MCP Vision
*   **Purpose:** Standardize the interaction layer between LLMs, data stores, and backend APIs.
*   **EIB Vision:** Establish a secure, model-neutral intelligence bus that decouples cognitive reasoning from database schemas.
*   **Architecture Goals:** Low-latency context transfers, zero hardcoded tool interfaces, and complete audit tracking.

---

## PART 2: Enterprise Intelligence Bus Architecture

The platform positions the EIB as a middleware layer:

```
  [ Vertex AI Agent Engine / Gemini ]
                 │
                 ▼ (MCP Protocol Client)
  [ Enterprise Intelligence Bus (Apigee / Cloud Run) ]
                 │
                 ▼ (MCP Server Tools)
  [ GSTN Tool ] [ Account Aggregator Tool ] [ AlloyDB Tool ]
```

*   **MCP Client:** Vertex AI Agent Engine hosts clients that initiate requests.
*   **MCP Server (EIB):** Container services route requests to specific database and API tools.
*   **Tools:** Standardized interfaces that wrap core Finacle and registry queries.

---

## PART 3: MCP Communication Principles
1.  **Strict Schema Isolation:** Agents may only interact with external systems using verified MCP tool schemas.
2.  **Consent Token Verification:** Tools must verify active customer authorization before querying records.
3.  **Auditable Execution:** All tool calls, input payloads, and output states must be logged in audit databases.

---

## PART 4: Context Management Strategy
Context is structured and routed dynamically to prevent token overload. The system separates static customer profiles from active conversation loops, passing only required indices during tool calls.

---

## PART 5: Enterprise Context Model
*   **Customer Context:** Master identity tags (PAN, CIN, registration status).
*   **Credit Context:** Alt-DSCR calculations, scoring tiers, limit histories.
*   **Risk Context:** Warning flags, concentration limits, late payment counts.
*   **Session Context:** Temporary conversation logs and prompt parameters.

---

## PART 6: Enterprise MCP Tool Registry

Below are the detailed specifications for key MCP tools:

### Tool 1: GST Invoice Fetch Tool
*   **Tool ID:** TOL-001
*   **Purpose:** Retrieve and normalise GST tax turnovers for limit calculations.
*   **Owner:** Chief API Architect.
*   **Inputs:** Valid consent token, customer GSTIN.
*   **Outputs:** Normalized JSON transaction logs.
*   **Access Rules:** Restricted to Credit and Underwriter Agents.
*   **Authentication:** Mutual TLS with registry servers.
*   **Authorization:** Verified against the active consent database.
*   **Audit Logging:** Log customer ID, timestamps, and API response sizes.
*   **Security Controls:** Mask invoice details dynamically.
*   **AI Usage:** Used by the Credit Agent to compile spreading sheets.
*   **Business Value:** Speeds up limit calculations.
*   **KPIs:** API connection latency, payload size.
*   **Future GCP Service Mapping:** Apigee, Cloud Run.

---

### Tool 2: Account Aggregator Statement Pull Tool
*   **Tool ID:** TOL-002
*   **Purpose:** Pull verified bank statements for cash flow assessments.
*   **Owner:** Chief Data Officer (CDO).
*   **Inputs:** Consent token, AA transaction ID.
*   **Outputs:** Structured bank ledger logs.
*   **Access Rules:** Restricted to Credit and Risk Agents.
*   **Authentication:** Secure OAuth token validations.
*   **Authorization:** Verified against active customer tokens.
*   **Audit Logging:** Log call events and file size.
*   **Security Controls:** Encrypt file payloads at-rest and in-transit.
*   **AI Usage:** Used by Credit and Risk Agents to calculate cash flows and EWS ratings.
*   **Business Value:** Replaces manual statement collection.
*   **KPIs:** Retrieval success rate.
*   **Future GCP Service Mapping:** Apigee, Cloud Run, Cloud KMS.

---

*Note: All other 22 MCP tools (UPI, EPFO, MCA, PAN, Aadhaar, Credit Bureau, CGTMSE, TReDS, GeM, Bank CBS, CRM, Document Repository, Knowledge Repository, BigQuery, AlloyDB, Document AI, Looker, Vertex AI Search, RAG Engine, Vector Search, Cloud Storage, and Notifications) follow the same structured design specification, conceptually mapped to their respective native Google Cloud services.*

---

## PART 7: Agent-to-Tool & Agent-to-Agent Communication
*   **Agent-to-Tool:** Initiated using standard JSON-RPC calls over secure connection lines.
*   **Agent-to-Agent:** Coordinates queues using Eventarc and Pub/Sub event brokers.
*   **Agent-to-Human:** Routes exceptions and overrides to human workspaces using tasks managers.

---

## PART 8: Context Sharing & Memory Management
*   **Short-term Memory:** Active session context stored in cache databases.
*   **Long-term Memory:** Customer profiles, scoring histories, and warning metrics stored in AlloyDB.
*   **Decision Memory:** Grounded audit trails storing reason chains and override logs.

---

## PART 9: Security, Trust, & Governance
*   **Governance Board:** Reviews and approves all new MCP tool schemas.
*   **Access Control:** IAM roles protect tool execution pathways.
*   **Data Masking:** PII is automatically masked from tool payloads.

---

## PART 10: Performance, Observability, & KPIs

AAROHAN monitors and reports KPIs across four MCP dimensions:

| Category | KPI | Target Baseline | Formula | GCP Mapping |
| :--- | :--- | :---: | :--- | :--- |
| **Performance** | Tool Call Latency | < 100ms | $\text{Execution Time} - \text{Invoke Time}$| Cloud Trace |
| **Reliability** | Tool Failure Rate | < 0.1% | $\text{Failed Calls} / \text{Total Calls}$ | Error Reporting |
| **Security** | Access Violations | 0 | $\text{Blocked Calls} / \text{Total Invokes}$ | IAM, SCC |
| **Governance** | Schema Conformance | 100% | $\text{Valid Schemas} / \text{Total Registry}$ | Apigee |

---

## PART 11: Enterprise Intelligence Bus Reference Model

The reference model connects all MCP components:

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                    AAROHAN INTELLIGENCE Reference MODEL                │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 1. Clients: Vertex AI Agent Engine, Gemini models, CRM workflows       │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 2. EIB Layer: Apigee API proxies, JSON-RPC routers, IAM validators     │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 3. Server Tools: GSTN, AA, AlloyDB, Document AI, SMS notifications     │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 4. Logs & Monitors: Cloud Trace tracking, Cloud Logging repositories   │
  └────────────────────────────────────────────────────────────────────────┘
```

*   **Client Layer:** Hosts the agents that trigger tool calls.
*   **EIB Layer:** Manages routing, authentication, and validation.
*   **Server Tools:** Integrates with backend databases and registries.

---

## PART 12: Conclusion
*   **Purpose:** Conclude the MCP & EIB Architecture document.
*   **Business Objective:** Approve the target business integration and tool registry lifecycles.
*   **Banking Objective:** Baselines all credit and risk designs under a single framework.
*   **Regulatory Considerations:** Prepares the platform for integration security audits.
*   **Deliverables:** Approved MCP & EIB Reference Architecture.
*   **Owner:** Chief API Architect.
*   **Review Authority:** Board of Directors.
