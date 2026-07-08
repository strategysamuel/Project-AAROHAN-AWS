# Enterprise Business Architecture

**Document ID:** AAR-BAR-003  
**Document Name:** Enterprise Business Architecture  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 (ERDA), AAR-EAV-002 (Enterprise Architecture Vision)  
**Next Artifact:** AAR-BKA-004 (Enterprise Banking Architecture)  
**Target Audience:** IDBI Bank Board, MD & CEO, Executive Directors, Business Leads, Credit & Risk Heads, and Operations Managers  
**Document Owner:** Chief Business Architect (CBA)  
**Approval Authority:** Executive Committee / Chief Banking Officer  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Business Architect | Initial Release for Executive and Board Review. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Document Metadata & Scope](#document-metadata--scope)
3. [PART 1: Business Transformation Vision](#part-1-business-transformation-vision)
4. [PART 2: Future MSME Business Operating Model](#part-2-future-msme-business-operating-model)
5. [PART 3: Enterprise Business Capability Model](#part-3-enterprise-business-capability-model)
6. [PART 4: Business Capability Heat Map](#part-4-business-capability-heat-map)
7. [PART 5: Business Value Streams](#part-5-business-value-streams)
8. [PART 6: Business Services Catalogue](#part-6-business-services-catalogue)
9. [PART 7: Stakeholder Ecosystem](#part-7-stakeholder-ecosystem)
10. [PART 8: Enterprise Personas](#part-8-enterprise-personas)
11. [PART 9: Customer Journey Maps](#part-9-customer-journey-maps)
12. [PART 10: Relationship Manager Journey](#part-10-relationship-manager-journey)
13. [PART 11: Credit Officer Journey](#part-11-credit-officer-journey)
14. [PART 12: Risk Officer Journey](#part-12-risk-officer-journey)
15. [PART 13: Executive Decision Journey](#part-13-executive-decision-journey)
16. [PART 14: Business Process Architecture](#part-14-business-process-architecture)
17. [PART 15: Business Rules Architecture](#part-15-business-rules-architecture)
18. [PART 16: Business Events Architecture](#part-16-business-events-architecture)
19. [PART 17: Business Decision Architecture](#part-17-business-decision-architecture)
20. [PART 18: Enterprise KPI Architecture](#part-18-enterprise-kpi-architecture)
21. [PART 19: Business Information Requirements](#part-19-business-information-requirements)
22. [PART 20: Business Governance Model](#part-20-business-governance-model)
23. [PART 21: Business Organization Model](#part-21-business-organization-model)
24. [PART 22: Business Risks](#part-22-business-risks)
25. [PART 23: Business Assumptions](#part-23-business-assumptions)
26. [PART 24: Business Success Measures](#part-24-business-success-measures)
27. [PART 25: Conclusion](#part-25-conclusion)

---

## Executive Summary
This document establishes the Enterprise Business Architecture for Project AAROHAN. It maps the transition of IDBI Bank's MSME division from traditional, document-heavy operations to a continuous, data-driven relationship model. By defining capabilities (onboarding, credit evaluation, risk tracking, and business advisory) and aligning them with national digital registries, this architecture ensures consistent, scalable, and risk-controlled credit operations.

---

## Document Metadata & Scope
*   **Purpose:** Establish the operational, credit, and product capabilities supporting AAROHAN.
*   **Scope:** Governs all MSME products, regional offices, and digital partnerships.
*   **Audience:** Board members, MD & CEO, credit/risk leadership, and IT architects.
*   **Strategic Drivers:** Priority Sector Lending growth, turnaround time (TAT) reduction, and default risk management.

---

## PART 1: Business Transformation Vision
*   **Purpose:** Establish the core business goals and target states of the platform.
*   **Business Objective:** Drive credit volume growth in priority sector manufacturing and services.
*   **Banking Objective:** Move to self-optimizing risk underwriting engines.
*   **Regulatory Considerations:** Aligns with Priority Sector Lending targets and RBI digital lending rules.
*   **Inputs:** Business strategy guidelines, priority sector targets.
*   **Outputs:** Target operational models.
*   **Dependencies:** Executive approval of the program vision.
*   **Deliverables:** Business Transformation Roadmap.
*   **Owner:** Chief Business Officer (CBO).
*   **Review Authority:** Board of Directors.
*   **Success Criteria:** Platform target models aligned with 5-year bank growth plans.

---

## PART 2: Future MSME Business Operating Model
*   **Purpose:** Define how the bank's business units will collaborate post-implementation.
*   **Business Objective:** Scale loan volumes safely while reducing operational overhead.
*   **Banking Objective:** Standardize automated workflow handoffs across regional branches.
*   **Regulatory Considerations:** Aligns with data residency and compliance guidelines.
*   **Inputs:** Operating guidelines, system capability specs.
*   **Outputs:** Target state organizational designs.
*   **Dependencies:** Human Resources and IT operations alignment.
*   **Deliverables:** Target Operating Model Specification.
*   **Owner:** Chief Operations Officer (COO).
*   **Review Authority:** Chief Enterprise Architect (CEA).
*   **Success Criteria:** Zero process silos across regional business offices.

---

## PART 3: Enterprise Business Capability Model

The business architecture uses a three-level capability structure:

### L1: MSME Relationship Banking
*   **L2: Lead Management**
    *   *L3: Partner Ecosystem Sourcing*
*   **L2: Customer Onboarding**
    *   *L3: Digital Identity Verification (UIDAI/CKYC)*
    *   *L3: Consent Token Validation (Account Aggregator)*

### L1: Credit Underwriting & Decisioning
*   **L2: Financial Assessment**
    *   *L3: Alternate Data Spreading (GST/EPFO)*
    *   *L3: Digital Financial Health Assessment*
*   **L2: Credit Scoring**
    *   *L3: Automated Policy Rule Evaluation*
    *   *L3: Multi-Agent Credit Memo Generation*

### L1: Portfolio Risk Management
*   **L2: Credit Monitoring**
    *   *L3: Continuous Cash Flow Tracking (GST/AA)*
    *   *L3: Early Warning Signal (EWS) Alert Routing*

### Level 3 Capability Specification Example: Digital Financial Health Assessment
*   **Purpose:** Aggregate and evaluate multi-registry data to build a live business health card.
*   **Business Owner:** Head of Credit Underwriting.
*   **Inputs:** Bank statements, GST tax returns, EPFO filings.
*   **Outputs:** Verified Business Health Cards, cash-flow coverage ratios.
*   **KPIs:** Assessment speed, analysis accuracy.
*   **Business Rules:** Limit calculation must use the Nayak Committee turnover method.
*   **Dependencies:** DPI integration gateway availability.
*   **Success Criteria:** Spreading completed in < 5 minutes with zero manual entry errors.
*   **Regulatory Considerations:** Aligns with RBI digital lending transparency guidelines.

---

## PART 4: Business Capability Heat Map

We classify AAROHAN's business capabilities into four strategic zones:

*   **Core Capabilities (Immediate Value):** Digital Identity Onboarding, Financial Health Assessment, Credit Limit Calculation.
*   **Strategic Capabilities (Competitive Advantage):** Alternate Data Scoring, Multi-Agent Credit Memo Generation, Continuous Risk Monitoring.
*   **Supporting Capabilities (Operations):** Account Management, Payment Clearing, Support Desk Triage.
*   **Emerging Capabilities (Future Innovation):** Financial Digital Twins, Agent-Guided Negotiation, ESG Rating Integrations.

---

## PART 5: Business Value Streams

The business processes run through a single continuous value stream:

$$\text{Lead Sourcing} \rightarrow \text{Digital Onboarding} \rightarrow \text{Financial Assessment} \rightarrow \text{Credit Approval} \rightarrow \text{Disbursement} \rightarrow \text{Continuous Monitoring} \rightarrow \text{Limit Renewal} \rightarrow \text{Risk Recovery} \rightarrow \text{Growth Advisory}$$

Every transition in this stream is event-driven and managed by automated system checks, minimizing manual processing delays.

---

## PART 6: Business Services Catalogue
*   **Identity Service:** Retrieves CKYC and DigiLocker files to verify borrower status.
*   **Spreading Service:** Aggregates bank statement and tax records to compile cash-flow coverage sheets.
*   **Scoring Service:** Runs the underwriting rule engine to calculate risk ratings.
*   **Monitoring Service:** Queries transaction logs daily to flag early warning signals (EWS).
*   **Disbursement Service:** Syncs with core banking ledgers to clear loan funds.

---

## PART 7: Stakeholder Ecosystem
*   **Internal Stakeholders:** Borrower, Relationship Manager, Underwriter, Risk Auditor, Compliance Analyst, Operations Staff, Executive Committee.
*   **External Registry Stakeholders:** Account Aggregator portals, GSTN API databases, ULI gateways, Credit Bureaus, EPFO systems, TReDS exchanges, ONDC networks.

---

## PART 8: Enterprise Personas
*   **The MSME Owner (Borrower):** Needs quick, paperless access to working capital without property collateral requirements.
*   **The Relationship Manager (RM):** Needs simple customer dashboards and sales targets that track lead statuses automatically.
*   **The Credit Underwriter:** Needs pre-compiled credit memos and policy check checklists to focus on exception handling.
*   **The Risk Officer:** Needs real-time portfolio health cards and predictive EWS alerts to prevent delinquencies.

---

## PART 9: Customer Journey Maps
*   **Existing Journey:** Manual document submissions, physical branch visits, and ratio calculations. High rejection rate for asset-light firms.
*   **Future Journey:** Paperless onboarding using AA consent tokens, automatic limit offers within 30 minutes, and online disbursements.
*   **Pain Points:** Document fraud, assessment delays, and lack of transparency.
*   **Opportunity Areas:** Embedded financing at point-of-sale and proactive advisory alerts.

---

## PART 10: Relationship Manager Journey
*   **Purpose:** Map RM sales and client advisory activities.
*   **Business Objective:** Increase customer acquisition and cross-sell coverage.
*   **Banking Objective:** RMs act as financial partners, using alerts to identify credit needs early.
*   **Regulatory Considerations:** Customer data access is restricted to authorized portfolios.
*   **Inputs:** Lead statuses, client transaction reports.
*   **Outputs:** Automated sales actions and client proposals.
*   **Dependencies:** User directory integrations.
*   **Deliverables:** RM Journey Map.
*   **Owner:** Head of Relationship Banking.
*   **Review Authority:** Chief Business Officer (CBO).
*   **Success Criteria:** RM administrative overhead reduced by 50%.

---

## PART 11: Credit Officer Journey
*   **Purpose:** Map credit officer files analysis and underwriting actions.
*   **Business Objective:** Speed up loan decision times while maintaining underwriting accuracy.
*   **Banking Objective:** Credit memos are prepared and delivered to the officer's queue automatically.
*   **Regulatory Considerations:** Final underwriting decisions must remain under human approval.
*   **Inputs:** Aggregated customer files, automated scorecards.
*   **Outputs:** Approved loan sanctions, rejection logs.
*   **Dependencies:** Workflow database integrations.
*   **Deliverables:** Credit Officer Journey Map.
*   **Owner:** Head of Underwriting.
*   **Review Authority:** Chief Credit Officer (CCO).
*   **Success Criteria:** Underwriting preparation time reduced by 90%.

---

## PART 12: Risk Officer Journey
*   **Purpose:** Map risk officer portfolio monitoring and alert review actions.
*   **Business Objective:** Lower default rates through transaction-level verification.
*   **Banking Objective:** Track warning signals across portfolios using Looker dashboards.
*   **Regulatory Considerations:** Aligns with RBI credit monitoring guidelines.
*   **Inputs:** Real-time transaction logs, external market alerts.
*   **Outputs:** Portfolio risk reports, EWS alerts.
*   **Dependencies:** Analytics database integrations.
*   **Deliverables:** Risk Officer Journey Map.
*   **Owner:** Head of Risk Operations.
*   **Review Authority:** Chief Risk Officer (CRO).
*   **Success Criteria:** Warning detection lead time > 45 days.

---

## PART 13: Executive Decision Journey
*   **Purpose:** Map executive dashboard reviews and strategic planning actions.
*   **Business Objective:** Align technical deployments with the bank's long-term business goals.
*   **Banking Objective:** Support steering committees with real-time portfolio metrics.
*   **Regulatory Considerations:** Complies with board-level accountability guidelines.
*   **Inputs:** Looker portfolio metrics, economic forecast data.
*   **Outputs:** Strategic capital allocation decisions.
*   **Dependencies:** Executive dashboard integrations.
*   **Deliverables:** Executive Decision Journey Map.
*   **Owner:** Chief Strategy Officer.
*   **Review Authority:** MD & CEO.
*   **Success Criteria:** Strategic decisions backed by real-time transaction data.

---

## PART 14: Business Process Architecture
*   **Purpose:** Document the end-to-end business workflows and queue systems.
*   **Business Objective:** Standardize application processing across all branches.
*   **Banking Objective:** Eliminate manual paperwork and processing bottlenecks.
*   **Regulatory Considerations:** Aligns with RBI digital lending directives.
*   **Inputs:** Target operating models, functional specs.
*   **Outputs:** BPMN-compliant process layouts.
*   **Dependencies:** Workflow engine configurations.
*   **Deliverables:** Business Process Blueprint.
*   **Owner:** Lead Process Engineer.
*   **Review Authority:** Chief Operations Officer (COO).
*   **Success Criteria:** Process steps completed within target durations.

---

## PART 15: Business Rules Architecture
*   **Credit Rules:** Underwriting limits must match Nayak/Tandon calculations.
*   **Eligibility Rules:** Applicants must possess a valid Udyam certificate and active GST registration.
*   **Compliance Rules:** Only query customer records with valid, active consent tokens.
*   **Risk Rules:** Flag and block disbursements to borrowers with active litigation alerts.
*   **Workflow Rules:** Route loan applications exceeding ₹5 crore to senior credit committees automatically.

---

## PART 16: Business Events Architecture
*   **Purpose:** Define the transactional events and triggers that coordinate microservices.
*   **Business Objective:** Build responsive, event-driven banking workflows.
*   **Banking Objective:** Use events to sync accounts across ledgers.
*   **Regulatory Considerations:** Event logs are stored in secure audit databases.
*   **Inputs:** Transaction feeds, API messages.
*   **Outputs:** Event messages.
*   **Dependencies:** Message queue configurations.
*   **Deliverables:** Business Event Registry.
*   **Owner:** Lead System Architect.
*   **Review Authority:** Chief Technology Officer (CTO).
*   **Success Criteria:** Event processing latencies < 100ms.

---

## PART 17: Business Decision Architecture
*   **Purpose:** Identify all decision points and decision owners.
*   **Business Objective:** Maintain clear lines of accountability across departments.
*   **Banking Objective:** Set approval thresholds for credit officers and committees.
*   **Regulatory Considerations:** Meets regulatory corporate governance guidelines.
*   **Inputs:** Policy handbooks, delegation tables.
*   **Outputs:** Decision matrix tables.
*   **Dependencies:** Governance configurations.
*   **Deliverables:** Business Decision Blueprint.
*   **Owner:** Chief Risk Officer (CRO).
*   **Review Authority:** Board of Directors.
*   **Success Criteria:** 100% of strategic decision paths documented.

---

## PART 18: Enterprise KPI Architecture
*   **Purpose:** Connect business capabilities directly to measurable KPIs.
*   **Business Objective:** Measure the commercial impact of all platform features.
*   **Banking Objective:** Map capabilities to NPA, conversion, and TAT metrics.
*   **Regulatory Considerations:** Meets priority lending regulations.
*   **Inputs:** Strategic bank KPIs, operational logs.
*   **Outputs:** Looker performance dashboards.
*   **Dependencies:** Analytics database integrations.
*   **Deliverables:** KPI Architecture Blueprint.
*   **Owner:** Chief Strategy Officer.
*   **Review Authority:** MD & CEO.
*   **Success Criteria:** KPI dashboards track metrics in real-time.

---

## PART 19: Business Information Requirements
*   **Purpose:** Define the data elements needed by each business function.
*   **Business Objective:** Protect borrower data privacy and enforce data quality standards.
*   **Banking Objective:** Map required fields for tax, financial, and credit registers.
*   **Regulatory Considerations:** Complies with national data protection laws (DPDP).
*   **Inputs:** Data taxonomy lists, registry API schemas.
*   **Outputs:** System data models.
*   **Dependencies:** Database design setups.
*   **Deliverables:** Business Information Matrix.
*   **Owner:** Chief Data Officer.
*   **Review Authority:** Chief Enterprise Architect (CEA).
*   **Success Criteria:** All required data fields mapped to secure schemas.

---

## PART 20: Business Governance Model
*   **Purpose:** Define governance responsibilities, committees, and ownership.
*   **Business Objective:** Protect banking intellectual property from data breaches.
*   **Banking Objective:** Enforce project rules and steering oversight.
*   **Regulatory Considerations:** Complies with RBI guidelines.
*   **Inputs:** Corporate governance plans.
*   **Outputs:** Governance checklists, meeting logs.
*   **Dependencies:** Internal governance systems.
*   **Deliverables:** Business Governance Policy.
*   **Owner:** Chief Risk Officer (CRO).
*   **Review Authority:** Board of Directors.
*   **Success Criteria:** 100% compliance with corporate governance guidelines.

---

## PART 21: Business Organization Model
*   **Purpose:** Describe how business teams collaborate after implementing AAROHAN.
*   **Business Objective:** Align team roles with the new automated underwriting platform.
*   **Banking Objective:** Underwriters act as exception managers, focusing on complex loans.
*   **Regulatory Considerations:** Meets regulatory standards for team governance.
*   **Inputs:** Organization charts, process manuals.
*   **Outputs:** Team structures.
*   **Dependencies:** Human Resources alignment.
*   **Deliverables:** Business Organization Blueprint.
*   **Owner:** Chief Operations Officer (COO).
*   **Review Authority:** Chief Business Officer (CBO).
*   **Success Criteria:** Operational team handoffs completed without bottlenecks.

---

## PART 22: Business Risks
*   **Purpose:** Identify business risks and define mitigation actions.
*   **Business Objective:** Prevent budget overruns and operational delays.
*   **Banking Objective:** Review credit risk, model drift, and security risks.
*   **Regulatory Considerations:** Complies with risk management rules.
*   **Inputs:** Industry risk reports, operational logs.
*   **Outputs:** Business risk registries.
*   **Dependencies:** Risk management databases.
*   **Deliverables:** Business Risk Register.
*   **Owner:** Chief Risk Officer (CRO).
*   **Review Authority:** Risk Committee.
*   **Success Criteria:** High-risk issues resolved within targets.

---

## PART 23: Business Assumptions
*   **Purpose:** Verify key business parameters and assumptions.
*   **Business Objective:** Verify market demand indicators before development.
*   **Banking Objective:** Assume core API systems remain available.
*   **Regulatory Considerations:** Assume regulations remain consistent.
*   **Inputs:** Strategic bank plans, technology guidelines.
*   **Outputs:** Assumption registries.
*   **Dependencies:** Strategy planning databases.
*   **Deliverables:** Business Assumption Register.
*   **Owner:** PMO Lead.
*   **Review Authority:** Steering Committee.
*   **Success Criteria:** Zero project delays caused by invalid assumptions.

---

## PART 24: Business Success Measures
*   **Purpose:** Define baseline criteria to verify business success.
*   **Business Objective:** Achieve market leadership in Indian MSME cash-flow lending.
*   **Banking Objective:** Lower transaction and processing overhead.
*   **Regulatory Considerations:** Flawless compliance audits from RBI inspectors.
*   **Inputs:** Strategic success metrics, business logs.
*   **Outputs:** Performance reviews.
*   **Dependencies:** Steering committee evaluations.
*   **Deliverables:** Business Success Measures Guide.
*   **Owner:** Chief Business Officer (CBO).
*   **Review Authority:** Board of Directors.
*   **Success Criteria:** Project success measures met on schedule.

---

## PART 25: Conclusion
*   **Purpose:** Conclude the Enterprise Business Architecture document.
*   **Business Objective:** Commit IDBI Bank to the target digital operating system.
*   **Banking Objective:** Approve the transition to cash-flow-based underwriting.
*   **Regulatory Considerations:** Prepares the project for regulatory audits.
*   **Inputs:** Business architecture blueprints, policy manuals.
*   **Outputs:** Approved business architecture files.
*   **Dependencies:** Design authority sign-off.
*   **Deliverables:** Approved Business Architecture.
*   **Owner:** Chief Business Architect (CBA).
*   **Review Authority:** Board of Directors.
