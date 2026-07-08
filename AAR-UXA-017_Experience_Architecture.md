# Enterprise Experience Architecture

**Document ID:** AAR-UXA-017  
**Document Name:** Enterprise Experience Architecture  
**Version:** 1.0  
**Status:** Ready for Board Approval  
**Dependencies:** AAR-ERDA-001 through AAR-NFR-016 (All Previous Volumes, BRD, FRS, and NFR)  
**Next Artifact:** AAR-BPM-018 (Enterprise Business Process & Workflow Architecture)  
**Target Audience:** IDBI Bank Board, Product Design Teams, UX Architects, Google Cloud Consulting, and Delivery Teams  
**Document Owner:** Chief Experience Officer (CXO) / Enterprise UX Architect  
**Approval Authority:** Enterprise Architecture Review Board (EARB)  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Customer Experience Office | Initial Release of Enterprise Experience Architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Experience Vision & Principles](#experience-vision--principles)
3. [Persona Architecture](#persona-architecture)
4. [Customer Journey Architecture](#customer-journey-architecture)
5. [Employee Experience & Workspace Design](#employee-experience--workspace-design)
6. [AI Experience (AIX) Strategy](#ai-experience-aix-strategy)
7. [Omnichannel & Accessibility Strategy](#omnichannel--accessibility-strategy)
8. [Experience Metrics & GCP Service Mapping](#experience-metrics--gcp-service-mapping)
9. [UX Requirements Traceability Matrix](#ux-requirements-traceability-matrix)
10. [Conclusion](#conclusion)

---

## Executive Summary
This document defines the Enterprise Experience Architecture (AAR-UXA-017) for Project AAROHAN. It details the customer experience (CX), employee experience (EX), and AI interaction models (AIX) necessary to support IDBI Bank's digital credit platform. This architecture ensures that systems are inclusive, accessible (WCAG-compliant), and optimized to deliver fast, transparent cash-flow lending journeys.

---

## Experience Vision & Principles
*   **Vision:** Deliver a seamless, transparent, and inclusive banking experience that empowers MSME entrepreneurs and helps RMs act as proactive financial advisors.
*   **Experience Principles:** Trust by Design, Accessibility First (WCAG 2.1), Omnichannel Consistency, and AI Explainability in User Interfaces.

---

## Persona Architecture
We define distinct customer and employee personas to guide interface design:

*   **New-to-Credit (NTC) MSME:** Needs a simple, paperless onboarding flow that explains terms in regional languages.
*   **Existing MSME Borrower:** Needs quick access to limit top-ups and invoice financing tools.
*   **Women & Rural Entrepreneurs:** Need voice-first interfaces, low-bandwidth optimizations, and simplified verification templates.
*   **Relationship Manager (RM):** Needs consolidated client cockpits showing active leads, alerts, and proposal drafts.
*   **Credit Officer (Underwriter):** Needs pre-compiled credit assessment memos (CAM) with clear citations.
*   **Risk & Executive Officers:** Need Looker dashboard interfaces showing portfolio yields, credit metrics, and NPA forecasts.

---

## Customer Journey Architecture

Customers navigate a unified journey with automated transitions:

```
[ Discovery ] ──> [ Onboarding ] ──> [ Consent ] ──> [ Assessment ] ──> [ Approval ]
                                                                           │
[ Advisory ] <── [ Limit Renewal ] <── [ Monitoring ] <── [ Disbursement ] ◄┘
```

1.  **Lead & Discovery:** Mobile portals match borrower profiles to optimal credit schemes.
2.  **Consent & Aggregation:** Simple consent screens explain what data is fetched (GST/bank statements).
3.  **Appraisal & Approval:** Progress trackers show the status of the credit check in real-time.
4.  **Disbursement:** Online validation leading to core banking fund transfers.
5.  **Monitoring & Growth:** Automated advisory alerts suggest local buyers and suppliers.

---

## Employee Experience & Workspace Design
*   **RM Workspace:** Mobile-first CRM showing client cards, task lists, and alert warnings.
*   **Credit Workspace:** Queue management console displaying credit memo checklists and policy exceptions.
*   **Risk & Executive Workspace:** High-level Looker dashboards showing portfolio distributions, sector limits, and EWS alert frequencies.

---

## AI Experience (AIX) Strategy
*   **Conversational Assistant:** Gemini assistant provides natural-language answers to client queries.
*   **RM Copilot UI:** Interactive chat interfaces draft emails and client proposals.
*   **Decision Explanations:** Loan approval pages show simple, human-readable reason chains explaining the credit limit.

---

## Omnichannel & Accessibility Strategy
*   **Omnichannel Consistency:** Save user progress across web, mobile, branch kiosks, and call center channels.
*   **Accessibility (WCAG 2.1):** High-contrast UI views, screen-reader support, and voice-assisted navigation.
*   **Multilingual Support:** Portals available in major Indian regional languages.
*   **Low-Bandwidth Mode:** Text-only interfaces designed for rural networks.

---

## Experience Metrics & GCP Service Mapping

AAROHAN monitors and reports KPIs across four experience dimensions:

| Category | Key Performance Indicator (KPI) | Target Baseline | Formula | GCP Mapping |
| :--- | :--- | :---: | :--- | :--- |
| **Customer** | Net Promoter Score (NPS) | NPS > 75 | $\text{\% Promoters} - \text{\% Detractors}$| Firebase, Looker |
| **Employee** | RM Processing Capacity | +50% | $\text{Accounts Per RM} - \text{Baseline}$ | Gemini, ADK |
| **Accessibility**| Multilingual Completion | > 90% | $\text{Onboards Completed} / \text{Registrations}$| Translation API |
| **AI Experience**| Rec Acceptance Rate | > 85% | $\text{Accepted Recs} / \text{Total Recs}$ | Vertex AI Engine |

---

## UX Requirements Traceability Matrix

This matrix traces experience requirements to functional and quality parameters:

| UX ID | Business Target | Functional Module | Quality Attribute | Target GCP Service | Acceptance Test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **UX-001** | Onboarding TAT < 15 mins | Customer Onboarding | Usability | Firebase, Identity | Flow Completion Tests|
| **UX-002** | Multi-language access | Self-Service Portal | Accessibility | Translation API | Lang selection check |
| **UX-003** | Explainable Credit | Credit Appraisal | Explainability | Vertex AI, Looker | Reason chain display |
| **UX-004** | RM Lead Conversion +25%| RM Workspace | Productivity | Gemini, ADK, MCP | Proposal draft latency|

---

## Conclusion
*   **Purpose:** Conclude the Experience Architecture document.
*   **Business Objective:** Approve the target customer, employee, and AI experience designs.
*   **Banking Objective:** Align RM workspaces and client portals under a single framework.
*   **Regulatory Considerations:** Prepares the interfaces for WCAG and accessibility audits.
*   **Deliverables:** Approved Experience Architecture.
*   **Owner:** Chief Experience Officer (CXO).
*   **Review Authority:** Board of Directors.
