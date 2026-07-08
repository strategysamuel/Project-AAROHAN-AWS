# Enterprise Banking Architecture

**Document ID:** AAR-BKA-004  
**Document Name:** Enterprise Banking Architecture  
**Version:** 1.0  
**Status:** Draft for Executive Review  
**Dependencies:** AAR-ERDA-001 (ERDA), AAR-EAV-002 (EAV), AAR-BAR-003 (Business Architecture)  
**Next Artifact:** AAR-INA-005 (Enterprise Information Architecture)  
**Target Audience:** IDBI Bank Board, MD & CEO, Executive Directors, Chief Credit Officer, Chief Risk Officer, CIO, CTO, and Business Leads  
**Document Owner:** Chief Banking Architect (CBA)  
**Approval Authority:** Executive Steering Committee / Board of Directors  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Banking Architect | Initial Release of governing banking reference architecture. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Document Metadata & Scope](#document-metadata--scope)
3. [PART 1: Future MSME Banking Vision](#part-1-future-msme-banking-vision)
4. [PART 2: Current MSME Banking Ecosystem](#part-2-current-msme-banking-ecosystem)
5. [PART 3: Target Banking Operating Model](#part-3-target-banking-operating-model)
6. [PART 4: Enterprise Banking Capability Model](#part-4-enterprise-banking-capability-model)
7. [PART 5: MSME Product Reference Architecture](#part-5-msme-product-reference-architecture)
8. [PART 6: Complete Banking Value Chain](#part-6-complete-banking-value-chain)
9. [PART 7: Alternate Data Banking Framework](#part-7-alternate-data-banking-framework)
10. [PART 8: AI Powered Financial Health Framework](#part-8-ai-powered-financial-health-framework)
11. [PART 9: Credit Decision Architecture](#part-9-credit-decision-architecture)
12. [PART 10: Enterprise Risk Architecture](#part-10-enterprise-risk-architecture)
13. [PART 11: Portfolio Management Architecture](#part-11-portfolio-management-architecture)
14. [PART 12: Relationship Banking Architecture](#part-12-relationship-banking-architecture)
15. [PART 13: Customer Growth Architecture](#part-13-customer-growth-architecture)
16. [PART 14: Early Warning System Architecture](#part-14-early-warning-system-architecture)
17. [PART 15: Enterprise Banking Dashboards](#part-15-enterprise-banking-dashboards)
18. [PART 16: Enterprise Banking KPI Framework](#part-16-enterprise-banking-kpi-framework)
19. [PART 17: Regulatory Architecture](#part-17-regulatory-architecture)
20. [PART 18: Enterprise Banking Governance](#part-18-enterprise-banking-governance)
21. [PART 19: Strategic Banking Risks](#part-19-strategic-banking-risks)
22. [PART 20: Banking Assumptions](#part-20-banking-assumptions)
23. [PART 21: Five-Year Banking Transformation Roadmap](#part-21-five-year-banking-transformation-roadmap)
24. [PART 22: Enterprise Banking Reference Model](#part-22-enterprise-banking-reference-model)
25. [PART 23: Conclusion](#part-23-conclusion)

---

## Executive Summary
This document defines the Enterprise Banking Reference Architecture (AAR-BKA-004) for Project AAROHAN. It details the target credit products, risk frameworks, alternate data integrations, and operating interfaces required to modernize MSME banking. By establishing a composable, data-driven banking model, the architecture ensures consistent underwriting, proactive risk management, and scalable credit operations across all bank divisions.

---

## Document Metadata & Scope
*   **Purpose:** Establish the banking reference architecture for credit products, underwriting, and risk frameworks.
*   **Scope:** Governs all MSME loan portfolios, underwriting pipelines, relationship tools, and risk dashboards.
*   **Audience:** Board members, executive directors, credit/risk leadership, and IT architects.
*   **Banking Context:** Shifts operations from retrospective document checks to dynamic, transaction-based underwriting.

---

## PART 1: Future MSME Banking Vision
*   **Purpose:** Outline the target state of credit and relationship banking.
*   **Banking Objective:** Build a zero-toil credit pipeline that supports cash-flow lending.
*   **Business Objective:** Grow loan volumes safely while lowering acquisition costs.
*   **Business Owner:** Chief Business Officer (CBO).
*   **Inputs:** Bank strategic plans, market data.
*   **Outputs:** Target state product concepts.
*   **Banking Rules:** Credit pricing must adjust dynamically to transaction risk ratings.
*   **Regulatory Mapping:** RBI Priority Sector Lending rules and Digital Lending Guidelines.
*   **AI Opportunities:** Conversational sales assistance and portfolio analytics.
*   **KPIs:** NIM growth, market share.
*   **Risks:** Margin compression in competitive segments.
*   **Success Criteria:** Growth in micro-enterprise credit portfolios.

---

## PART 2: Current MSME Banking Ecosystem
*   **Purpose:** Analyze the competitive landscape and market segments.
*   **Banking Objective:** Identify product gaps across public sector, private sector, NBFCs, and FinTechs.
*   **Business Objective:** Capture market share by offering faster credit decision times.
*   **Business Owner:** Head of Market Strategy.
*   **Inputs:** Competitor product terms, credit bureau market reports.
*   **Outputs:** Competitive Position Report.
*   **Banking Rules:** Assessments must comply with current RBI lending directions.
*   **Regulatory Mapping:** RBI guidelines on commercial lending competition.
*   **AI Opportunities:** Competitor feature mapping using web scrapers.
*   **KPIs:** Market share growth, lead acquisition rate.
*   **Risks:** Low pricing margins from aggressive competitor offers.
*   **Success Criteria:** Product terms positioned competitively in the target market.

---

## PART 3: Target Banking Operating Model
*   **Purpose:** Define operational roles and collaborations for the banking team.
*   **Banking Objective:** Underwriters act as exception managers, focusing on high-risk files.
*   **Business Objective:** Scale loan volumes safely while reducing operational overhead.
*   **Business Owner:** Chief Operations Officer (COO).
*   **Inputs:** Operating guidelines, system specs.
*   **Outputs:** Target state operational blueprints.
*   **Banking Rules:** Credit approvals must follow the bank's delegation table.
*   **Regulatory Mapping:** Segregation of duties guidelines.
*   **AI Opportunities:** Automated routing of exceptions to specialists.
*   **KPIs:** Internal file turnaround time, task backlogs.
*   **Risks:** Operations team resistance to automated workflows.
*   **Success Criteria:** Operational handoff bottlenecks eliminated.

---

## PART 4: Enterprise Banking Capability Model

AAROHAN uses a structured, three-level capability layout:

### L1: Commercial Lending Operations
*   **L2: Product Configuration**
    *   *L3: Alternative Rate Settings*
        *   *Purpose:* Dynamically price loans based on risk metrics.
        *   *Banking Objective:* Align pricing margins to real-time risk tiers.
        *   *Business Objective:* Optimize portfolio yields and conversions.
        *   *Business Owner:* Head of Products.
        *   *Inputs:* Risk ratings, benchmark funding rates.
        *   *Outputs:* Loan interest spread schedules.
        *   *Banking Rules:* Base rates must not fall below treasury limits.
        *   *Regulatory Mapping:* RBI lending rate guidelines.
        *   *AI Opportunities:* Risk-based margin pricing.
        *   *KPIs:* Portfolio Yield, NIM.
        *   *Risks:* Competitive rate matching issues.
        *   *Success Criteria:* Interest spreads aligned with default risks.
*   **L2: Credit Assessment**
    *   *L3: Alternate Data Score Calculation*
        *   *Purpose:* Evaluate creditworthiness using tax and transaction records.
        *   *Banking Objective:* Automate financial ratio calculations.
        *   *Business Objective:* Enable credit access for new-to-credit (NTC) firms.
        *   *Business Owner:* Head of Underwriting.
        *   *Inputs:* GST tax returns, bank statements.
        *   *Outputs:* Verified customer health cards.
        *   *Banking Rules:* Limit calculations must use Nayak turnover rules.
        *   *Regulatory Mapping:* RBI digital lending guidelines.
        *   *AI Opportunities:* Anomaly detection in transaction logs.
        *   *KPIs:* Decision Turnaround Time (TAT).
        *   *Risks:* Incomplete tax transaction data.
        *   *Success Criteria:* Assessments completed in < 15 minutes.

---

## PART 5: MSME Product Reference Architecture

AAROHAN consolidates 22 core credit products into a unified, composable architecture:

*   **Working Capital & Cash Credit:** Limits are sized dynamically using the Nayak turnover method (fixed 25% of projected sales).
*   **Trade & Invoice Finance:** Real-time financing of GSTR invoice receivables through TReDS integration.
*   **CGTMSE Loans:** Automated registration for collateral-free micro-enterprise limits.
*   **Green & ESG Finance:** Lower interest spreads for energy-efficient or certified sustainable MSMEs.
*   **Dealer & Vendor Finance:** Structured financing integrated directly into supply chain network files.
*   **Embedded & Co-Lending:** Expose limit calculation APIs to digital merchants and partner NBFCs.

---

## PART 6: Complete Banking Value Chain

```
[ Lead Gen ] ──> [ Onboarding ] ──> [ Consent ] ──> [ Data Aggregation ] ──> [ Scoring ]
                                                                                │
[ Disburse ] <── [ Documentation ] <── [ Sanction ] <── [ Risk Appraisal ] <────┘
     │
     ▼
[ Utilization ] ──> [ Monitoring ] ──> [ EWS Flags ] ──> [ Renewal / Growth ] ──> [ Closure ]
```

1.  **Lead Generation:** Automated sourcing from ONDC, trade networks, and partner apps.
2.  **Consent & Data Aggregation:** Secure authorization via Account Aggregator to pull bank statement logs.
3.  **Appraisal & Score:** Automated rule checks evaluate alternate data (GST/EPFO) to build credit memos.
4.  **Sanction & Disbursement:** Direct verification clearances leading to ledger funding.
5.  **Monitoring & EWS:** Transaction checks update risk profiles and trigger early alerts.

---

## PART 7: Alternate Data Banking Framework
*   **GSTN Integration:** Analyzes 12-24 month turnover trends and customer concentration rates from invoices.
*   **Account Aggregator (AA):** Analyzes credits/debits consistency, verifies hidden EMIs, and checks cash flow seasons.
*   **EPFO & ESIC:** Confirms active employee counts and employer payment regularity.
*   **TReDS & GeM:** Finances confirmed purchase orders and verified corporate invoices.
*   **CKYC & DigiLocker:** Validates registration documents and identity certificates.

---

## PART 8: AI Powered Financial Health Framework

Borrower health is calculated across ten dimensions:

1.  **Financial Health:** Alt-DSCR and interest coverage ratios.
2.  **Behavioral Health:** Transaction patterns and bank statement consistency.
3.  **Operational Health:** Payroll stability and employee count changes.
4.  **Compliance Health:** GST and tax filing regularity.
5.  **Growth Trajectory:** Invoice value changes and buyer acquisition rates.
6.  **Market Positioning:** Marketplace reviews and buyer creditworthiness.
7.  **Risk Exposure:** Customer concentration limits.
8.  **Digital Maturity:** Digital receipt share.
9.  **Governance Health:** Corporate ownership structures.
10. **Sustainability/ESG:** Energy efficiency and labor safety compliance.

---

## PART 9: Credit Decision Architecture
*   **Fully Automated Path:** Auto-approval for low-risk, small-ticket micro loans where GST and bank data are verified.
*   **Semi-Automated Path:** AI compiles the credit memo and routes the file to the underwriter's queue for sign-off.
*   **Human Override:** Underwriters can override AI scores with written business justifications.
*   **Committee Approval:** Loans exceeding ₹5 crore are routed automatically to senior committees for voting.

---

## PART 10: Enterprise Risk Architecture
*   **Credit & Portfolio Risk:** Monitors industry sector and regional default rates using BigQuery datasets.
*   **Fraud Risk:** Document AI runs metadata checks on uploads to identify potential forgery.
*   **Behavioral & EWS Risk:** Tracks transaction variances and utility bill changes to identify payment delays early.
*   **Model Risk:** Vertex AI monitoring dashboards track accuracy rates and concepts drift.

---

## PART 11: Portfolio Management Architecture
*   **Continuous Monitoring:** Monitors active portfolios using nightly transaction feeds.
*   **Risk Migration:** Tracks borrower risk ratings transitions across different classes.
*   **Concentration Analysis:** Automates alerts when industry exposure exceeds set limits.
*   **Stress Testing:** Run simulations to test how macro trends affect borrower portfolios.

---

## PART 12: Relationship Banking Architecture
*   **AI RM Copilot:** Gemini assistant generates client reports, status alerts, and drafts proposals.
*   **Next Best Action:** Recommends credit limit top-ups during peak seasonal demands.
*   **Growth Advisory:** Automatically suggests local buyers and supplier partners.

---

## PART 13: Customer Growth Architecture
*   **ESG Readiness:** Helps clients transition to sustainable models using green rating checklists.
*   **Government Schemes:** Matches borrower profile to optimal credit guarantee and subsidy programs.
*   **Financial Literacy:** Interactive courses and sandbox tools built into the client portal.

---

## PART 14: Early Warning System (EWS) Architecture
*   **EWS Signals:** Late GST filings, drop in active EPFO employee count, late utility payments.
*   **Escalation Logic:** Low risk (email alert) -> Medium risk (RM call) -> High risk (account restriction).
*   **AI Prediction:** Identifies potential payment defaults 45 days in advance using cash-flow trends.

---

## PART 15: Enterprise Banking Dashboards
*   **Board Dashboard:** Shows NIM growth, Gross NPA, and Priority sector lending targets.
*   **Credit Underwriting Dashboard:** Tracks file queue volumes, average TAT, and exception rates.
*   **Portfolio Risk Dashboard:** Monitors sector exposure and early warning alert frequency.

---

## PART 16: Enterprise Banking KPI Framework

AAROHAN defines and monitors KPIs across six strategic dimensions:

| Category | Key Performance Indicator (KPI) | Target Baseline | Formula | Owner |
| :--- | :--- | :---: | :--- | :--- |
| **Strategic** | Return on Equity (ROE) | ROE > 15% | $\text{Net Income} / \text{Equity}$ | CFO |
| **Credit** | Gross NPA | Gross NPA < 2.0% | $\text{Default Loans} / \text{Total Loans}$ | CCO |
| **Operations**| Underwriting TAT | Underwriting < 30 mins| $\text{Approval Time} - \text{Submit Time}$ | COO |
| **Customer** | Net Promoter Score (NPS) | NPS > 75 | $\text{\% Promoters} - \text{\% Detractors}$ | CPO |
| **AI** | Recommendation Acceptance | Acceptance > 85%| $\text{Accepted AI Recs} / \text{Total AI Recs}$ | CAIO |
| **Compliance**| PSL Target Achievement | 100% compliance | $\text{PSL Loans} / \text{Target PSL}$ | CBO |

---

## PART 17: Regulatory Architecture
*   **RBI Digital Lending Guidelines:** Direct fund routing; only consented data pulled from registries.
*   **Data Privacy (DPDP Act):** Secure consent profiles stored in database registries.
*   **Model Governance:** Grounded, explainable decision paths logged for audit.

---

## PART 18: Enterprise Banking Governance
*   **Operations Committee:** Meets weekly to review SLA compliance, model drift, and platform outages.
*   **Risk Committee:** Reviews credit risk limits and industry concentrations monthly.
*   **Governance Checklists:** Enforce policy sign-offs for all system updates.

---

## PART 19: Strategic Banking Risks
*   **Model Drift Risk:** Models may fail to predict risk accurately under changed economic settings.
*   **Integration Risk:** Partner registry API timeouts may delay onboarding.
*   **Data Privacy Risk:** Risk of unauthorized customer data exposure.

---

## PART 20: Banking Assumptions
*   **Registry Availability:** Assume AA, GSTN, and ULI gateways maintain stable services.
*   **User Adoption:** Assume branch staff adopt the new digital platform workflows.
*   **Policy Stability:** Assume RBI MSME classification rules remain stable.

---

## PART 21: Five-Year Banking Transformation Roadmap
*   **Phase 1 (2026-2027):** Automated document spreading, basic credit scoring, and AA integration.
*   **Phase 2 (2028-2029):** Real-time invoice financing (TReDS), dynamic limits calculation, and CRM AI tools.
*   **Phase 3 (2030-2031):** Multi-agent underwriting coordinates, and EWS alerts integrated.
*   **Phase 4 (2032-2033):** Financial digital twins, and embedded finance portals launched.
*   **Phase 5 (2034-2035):** Fully autonomous credit checks under human audit control.

---

## PART 22: Enterprise Banking Reference Model

The reference model connects all banking components into a single framework:

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   AAROHAN BANKING REFERENCE MODEL                      │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 1. Product Layer: Cash Credit, Trade Finance, Green lending            │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 2. Journey Layer: Lead -> Digital Onboarding -> Disbursement -> EWS    │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 3. Core Platforms: Apigee Gateway, Cloud Run, AlloyDB, BigQuery        │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 4. Governance & Controls: Audit logs, Risk rules, DPDP consent tokens  │
  └────────────────────────────────────────────────────────────────────────┘
```

*   **Journeys & Capabilities:** Standardize process steps using Cloud Workflows and modular APIs.
*   **AI & Alternate Data:** Ground model recommendations in verified GST, AA, and tax registries.
*   **Governance & Compliance:** Log all credit approvals and access histories in write-once audit stores.

---

## PART 23: Conclusion
*   **Purpose:** Conclude the Enterprise Banking Architecture document.
*   **Business Objective:** Approve the target digital lending operational models.
*   **Banking Objective:** Align risk, credit, and product designs under a single reference framework.
*   **Regulatory Considerations:** Prepares the platform for regulatory inspects.
*   **Deliverables:** Approved Banking Reference Architecture.
*   **Owner:** Chief Banking Architect (CBA).
*   **Review Authority:** Board of Directors.
