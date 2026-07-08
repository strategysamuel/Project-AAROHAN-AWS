# Enterprise Event-Driven Banking Architecture & Intelligent Event Mesh

**Document ID:** AAR-EDA-027  
**Document Name:** Enterprise Event-Driven Banking Architecture & Intelligent Event Mesh  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 through AAR-APS-026 (All Previous Reference Architecture & API Volumes)  
**Next Artifact:** AAR-OBS-028 (Enterprise Observability, AIOps & Platform Operations Architecture)  
**Target Audience:** IDBI Bank Board, CIO, CTO, Platform Engineers, and AI Integration Teams  
**Document Owner:** Enterprise Event Architect / Cloud Workflows Architect  
**Approval Authority:** Enterprise Architecture Review Board (EARB)  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Google Cloud Professional Services | Initial Release of Enterprise Event-Driven Architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Enterprise Event Vision & Event Mesh Strategy](#enterprise-event-vision--event-mesh-strategy)
3. [Event Domains Reference Catalogue (30 Domains)](#event-domains-reference-catalogue-30-domains)
4. [Event Processing Patterns](#event-processing-patterns)
5. [AI Event Orchestration](#ai-event-orchestration)
6. [Event Governance Framework](#event-governance-framework)
7. [Google Cloud Conceptual Mapping](#google-cloud-conceptual-mapping)
8. [Event Traceability Matrix](#event-traceability-matrix)
9. [Conclusion](#conclusion)

---

## Executive Summary
This document defines the Enterprise Event-Driven Banking Architecture and Intelligent Event Mesh (AAR-EDA-027) for Project AAROHAN. It maps the asynchronous messaging patterns, Eventarc routing filters, pub/sub queues, and event choreography rules needed to run a secure, distributed commercial lending system. The ERDA guidelines ensure that all event topics, schema contracts, and retry loops are configured according to Google Cloud SRE best practices.

---

## Enterprise Event Vision & Event Mesh Strategy
*   **Vision:** Transition from traditional, batch-processed point-to-point connections to a real-time, event-driven banking architecture. This mesh decouples systems, enabling reactive workflows and proactive risk management.
*   **Event Mesh Strategy:** Deploy Pub/Sub as the main messaging backbone and use Eventarc to route events from cloud systems to target agents and microservices.

---

## Event Domains Reference Catalogue (30 Domains)

Below are the detailed specifications for key event domains:

### Event Domain 7: GST Events
*   **Event Domain ID:** EVD-007
*   **Business Purpose:** Publish notification events when customer tax returns are filed.
*   **Trigger:** GSTN registry update notification.
*   **Producer:** GSTN API Adapter.
*   **Consumers:** Credit Analyst Agent, Risk Assessment Agent.
*   **Payload (conceptual):** Customer identifier (GSTIN), tax period, turnover total.
*   **Priority:** Medium.
*   **Criticality:** High.
*   **Ordering Requirements:** Strictly ordered by filing date.
*   **Retention:** 7 days in active message logs.
*   **Replay Requirements:** Replay capability required for audit and scoring updates.
*   **Security Classification:** Restricted.
*   **Audit Requirements:** Log message correlation IDs and delivery metrics.
*   **SLA:** Event delivery latency < 1 second.
*   **KPIs:** Event processing latency, pipeline throughput.
*   **Future Google Cloud Service Mapping:** Eventarc, Pub/Sub, Cloud Functions.

---

### Event Domain 13: Risk Events
*   **Event Domain ID:** EVD-013
*   **Business Purpose:** Publish alert events when borrower risk ratings shift.
*   **Trigger:** Risk calculation updates or EWS threshold triggers.
*   **Producer:** Risk Assessment Agent, EWS Engine.
*   **Consumers:** CRM console, RM Copilot Agent, Executive dashboard.
*   **Payload (conceptual):** Account ID, old risk score, new risk score, triggered alert factors.
*   **Priority:** High.
*   **Criticality:** Critical.
*   **Ordering Requirements:** Sequenced by timestamp.
*   **Retention:** 30 days in active logs.
*   **Replay Requirements:** Replay capability required for risk trend audits.
*   **Security Classification:** Restricted.
*   **Audit Requirements:** Log all generated risk alerts and recipient reads.
*   **SLA:** Event delivery latency < 500ms.
*   **KPIs:** Warning detection windows, alert read rates.
*   **Future Google Cloud Service Mapping:** Eventarc, Pub/Sub, Looker.

---

*Note: All other 28 event domains (Customer, Authentication, Consent, Onboarding, KYC, Alternate Data, Account Aggregator, UPI, Financial Health, Credit, CAM, Pricing, Loan Lifecycle, Document, AI Decision, Agent Collaboration, MCP, Knowledge, RAG, Knowledge Graph, Fraud, Compliance, Regulatory, Portfolio, Executive Dashboard, Notification, Workflow, and System Health Events) follow the same structured design specification, conceptually mapped to their respective native Google Cloud services.*

---

## Event Processing Patterns
*   **Publish/Subscribe:** Microservices register to specific topics to consume event updates asynchronously.
*   **Event Orchestration:** Centralized Cloud Workflows coordinate transaction sequences (onboarding loop).
*   **Dead Letter Queue (DLQ):** Failed messages route to a DLQ for investigation, preventing pipeline blocks.
*   **Idempotency:** Enforce unique transaction correlation IDs to prevent duplicate processing.

---

## AI Event Orchestration
Events trigger models to calculate risks and prepare documents:
*   *Consent Granted Event:* Triggers the Credit Agent to start statement spreading.
*   *GST Updated Event:* Triggers the Risk Agent to run limit evaluations.
*   *EWS Alert Event:* Triggers the RM Copilot Agent to draft client emails.

---

## Event Governance Framework
*   **Event Review Board:** Approves all new event topics and schema changes.
*   **Naming Standards:** Standard naming patterns (Domain.Entity.Event, e.g., credit.loan.approved).
*   **Schema Registry:** Conceptually tracks and versions all message payloads to ensure compatibility.

---

## Google Cloud Conceptual Mapping
*   **Event Mesh & Routing:** Pub/Sub, Eventarc, Cloud Workflows.
*   **Processing:** Cloud Run, Cloud Functions, Cloud Tasks.
*   **Telemetry & Logs:** Cloud Monitoring, Cloud Logging, Firebase Cloud Messaging.

---

## Event Traceability Matrix

This matrix traces event capabilities to business, functional, and API requirements:

| Event Domain ID | Business Capability | Functional Module | API Domain Reference | Requirement ID | GCP Target Service |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EVD-007** | Financial Health | Module 5 | API-031 | FR-002 | Eventarc, Pub/Sub |
| **EVD-013** | Risk Assessment | Module 10 | API-008 | FR-004 | Eventarc, Pub/Sub |
| **EVD-003** | Onboarding KYC | Module 4 | API-003 | FR-001 | Eventarc, Run |
| **EVD-017** | AI RM Copilot | Module 17 | API-013 | FR-003 | Pub/Sub, Gemini |

---

## Conclusion
*   **Purpose:** Conclude the Event-Driven Architecture document.
*   **Business Objective:** Approve the target business event topics and lifecycles.
*   **Banking Objective:** Baselines all credit and risk designs under a single framework.
*   **Regulatory Considerations:** Prepares the platform for transaction trace audits.
*   **Deliverables:** Approved Event Mesh Reference Architecture.
*   **Owner:** Enterprise Event Architect.
*   **Review Authority:** Board of Directors.
