# Enterprise Demo Dataset, Banking Personas, Business Scenarios & AI Evaluation Dataset Blueprint

**Document ID:** AAR-DEMO-DATA-001  
**Document Name:** Enterprise Demo Dataset, Banking Personas, Business Scenarios & AI Evaluation Dataset Blueprint  
**Version:** 1.0  
**Status:** Approved for UAT, QA Testing & AI Evaluation  
**Dependencies:** Entire Enterprise Repository, Engineering Build Blueprint (AAR-BLD-001), API Catalogue (AAR-API-CATALOG-001), Canonical Data Model (AAR-DATA-CATALOG-001), Demo Storyboard (AAR-DEMO-001), and Screen Blueprint (AAR-SCR-001)  
**Target Audience:** Business/Credit Teams, AI/QA/UAT Engineers, Demo Squads, and Executive Leadership  
**Document Owner:** Chief Banking Domain Expert & AI Evaluation Lead  
**Approval Authority:** Digital Transformation Office (DTO) / Credit Risk Governance Committee

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Banking Domain Expert | Initial Strategic Release of Demo Dataset & AI Eval Blueprint. | Credit Governance |

---

## Table of Contents
1. [Executive Summary & Domain Context](#executive-summary--domain-context)
2. [Target Banking Personas Profile Registry (15 Personas)](#target-banking-personas-profile-registry-15-personas)
3. [End-to-End Banking Journey Scenarios](#end-to-end-banking-journey-scenarios)
4. [AI Evaluation & Model Verification Scenarios](#ai-evaluation--model-verification-scenarios)
5. [Conceptual Dashboard Datasets](#conceptual-dashboard-datasets)
6. [Google Cloud Conceptual Data Platform Mapping](#google-cloud-conceptual-data-platform-mapping)

---

## Executive Summary & Domain Context

This document outlines the strategic specifications for datasets, borrower personas, operational journeys, and AI evaluation scenarios for Project AAROHAN. Designed by a combined team of senior banking specialists and Google Cloud AI architects, this blueprint defines the parameters required to build target test databases, evaluate model performance, execute QA test cases, and conduct UAT validations.

### Strategic Goals:
1. **Represent Banking Reality:** Personas cover the full range of MSME operations, from excellent credit histories to highly distressed situations.
2. **Standardize AI Evaluation:** Define the parameters needed to evaluate model capabilities in terms of default risk, anomaly detection, and explainability.

---

## Target Banking Personas Profile Registry (15 Personas)

### 1. Manufacturing MSME
*   **Business Profile:** Precision Engineering Auto-Parts Component Manufacturer.
*   **Ownership:** Private Limited Company (Three Promoter Directors).
*   **Industry & Location:** Auto Component Manufacturing, Pune, Maharashtra.
*   **Vintage & Turnover:** 8 Years; Annual Turnover of ₹12 Crores.
*   **Cash Flow Characteristics:** Capital intensive. High receivable lag (90 days from OEMs); monthly payroll of ₹15 Lakhs; raw material cash outlays required on day 1.
*   **GST Profile:** Conforming GSTR-1 & GSTR-3B filings, monthly GST payouts of ₹8 Lakhs.
*   **UPI Behaviour:** Low frequency, high ticket size transactions (primarily via B2B NetBanking).
*   **AA Data Availability:** 12 months transactional statements from IDBI Current Account and SBI Current Account.
*   **EPFO Profile:** 42 registered employees, monthly social security payroll deposits verified.
*   **Credit History:** Active Term Loan (₹1.5 Cr, Outstanding ₹80L), CC Limit of ₹2 Cr, clean repayment record. CIBIL score = 740.
*   **Existing Banking Relationship:** Primary transactional accounts and trade financing held with IDBI Bank.
*   **Growth Objectives:** Set up new CNC machinery line to execute international export contracts.
*   **Risk Profile:** Low-to-Moderate (Exposure tied to auto industry cycle).
*   **Expected Financial Health Card:** DSCR = 1.45, Current Ratio = 1.35, Inventory Turnover Days = 45 days.
*   **Expected AI Insights:** Cash flow is highly dependent on Auto OEM payments. Prompt invoice discounting recommended.
*   **Expected Lending Recommendation:** Approve limit renewal and add Capex Term Loan of ₹1.2 Cr at ROI of 9.25%.

---

### 2. Textile MSME
*   **Business Profile:** Powerloom Cotton Garment Manufacturer.
*   **Ownership:** Partnership firm.
*   **Industry:** Textile Weaving, Coimbatore, Tamil Nadu.
*   **Vintage & Turnover:** 12 Years; Turnover of ₹8 Crores.
*   **Cash Flow Characteristics:** Seasonally driven (high purchases during harvest months).
*   **GST Profile:** Inward tax credits consistently match outward invoices.
*   **UPI Behaviour:** Medium frequency payments for local dye/yarn purchases.
*   **AA Data Availability:** Current account ledger statements retrieved.
*   **EPFO Profile:** 18 permanent staff, 35 casual contract workers.
*   **Credit History:** Clean historical repayment record, CIBIL score = 710.
*   **Risk Profile:** Moderate (Affected by cotton price fluctuations).
*   **Expected Financial Health Card:** DSCR = 1.28, Inventory Turnover = 90 days.
*   **Expected AI Insights:** Seasonal working capital shortfall predicted in Q3.
*   **Expected Lending Recommendation:** Approve seasonal working capital extension of ₹80 Lakhs.

---

### 3. Retail MSME
*   **Business Profile:** Multi-Outlet Consumer Electronics Retailer.
*   **Ownership:** Proprietorship.
*   **Industry & Location:** Consumer Retail, Bangalore, Karnataka.
*   **Vintage & Turnover:** 5 Years; Annual Turnover of ₹4 Crores.
*   **Cash Flow Characteristics:** High-volume daily cash and digital inflows. Quick inventory rotation (15 days).
*   **GST Profile:** GSTR-1 filed monthly.
*   **UPI Behaviour:** High frequency daily customer receipts (average UPI ticket size of ₹8,000).
*   **AA Data Availability:** Full integration with retail current account.
*   **EPFO Profile:** 5 registered store staff.
*   **Credit History:** Personal credit cards and small business loan history. CIBIL score = 725.
*   **Risk Profile:** Low (Consistent daily cash generation).
*   **Expected Financial Health Card:** DSCR = 1.65, Current Ratio = 1.80.
*   **Expected AI Insights:** Strong daily cash flow supports credit extensions.
*   **Expected Lending Recommendation:** Approve Working Capital CC limit of ₹40 Lakhs.

---

### 4. Export MSME
*   **Business Profile:** Handcrafted Leather Footwear Exporter.
*   **Ownership:** Private Limited.
*   **Industry & Location:** Leather Exports, Kanpur, Uttar Pradesh.
*   **Vintage & Turnover:** 6 Years; Turnover of ₹15 Crores.
*   **Cash Flow Characteristics:** Receivables denominated in USD/EUR. Lags tied to international logistics timelines (60 days).
*   **GST Profile:** Standard tax refunds claimed under export schemes.
*   **UPI Behaviour:** Negligible UPI usage; transactions processed via SWIFT/wire transfers.
*   **AA Data Availability:** Dual bank accounts linked.
*   **EPFO Profile:** 55 registered assembly workers.
*   **Credit History:** EEFC account records, packing credit history. CIBIL = 750.
*   **Risk Profile:** Moderate (Foreign exchange rate vulnerability).
*   **Expected Financial Health Card:** DSCR = 1.38, Export receivables ratio = 85%.
*   **Expected AI Insights:** Recommend packing credit limit extensions and FX hedging.
*   **Expected Lending Recommendation:** Approve Pre-shipment Export Credit of ₹2.5 Crores.

---

### 5. Agri-processing MSME
*   **Business Profile:** Spices Crushing & Packaging Enterprise.
*   **Ownership:** Partnership.
*   **Industry & Location:** Food Processing, Guntur, Andhra Pradesh.
*   **Vintage & Turnover:** 9 Years; Turnover of ₹6 Crores.
*   **Cash Flow Characteristics:** High purchases during harvest seasons (Jan-April).
*   **GST Profile:** Matches exemption standards for processed agricultural products.
*   **UPI Behaviour:** Cash deposits combined with high-frequency rural distributor UPI transfers.
*   **AA Data Availability:** Cooperative bank and commercial account statements linked.
*   **EPFO Profile:** 12 registered employees.
*   **Credit History:** Historical agri-term loans. CIBIL = 680.
*   **Risk Profile:** Moderate-to-High (Vulnerable to crop yields and rainfall variations).
*   **Expected Financial Health Card:** DSCR = 1.21, Seasonal cash flow variance = 45%.
*   **Expected AI Insights:** High risk of cash constraints in off-harvest quarters.
*   **Expected Lending Recommendation:** Approve structured inventory warehouse receipt limit of ₹75 Lakhs.

---

### 6. Women Entrepreneur
*   **Business Profile:** Organic Cosmetics Manufacturing unit.
*   **Ownership:** Proprietorship (Female Promoter).
*   **Industry & Location:** Personal Care Products, Dehradun, Uttarakhand.
*   **Vintage & Turnover:** 4 Years; Turnover of ₹2 Crores.
*   **Cash Flow Characteristics:** Direct-to-consumer online sales. Low credit period sales.
*   **GST Profile:** Standard clean filing record.
*   **UPI Behaviour:** Online gateway collections, high UPI volume.
*   **AA Data Availability:** Primary account statements.
*   **EPFO Profile:** 8 registered female employees.
*   **Credit History:** Clean personal gold loan and credit card repayment history. CIBIL = 735.
*   **Risk Profile:** Low.
*   **Expected Financial Health Card:** DSCR = 1.55, Debt-to-Equity = 0.25.
*   **Expected AI Insights:** Strong business cash flow and low debt leverage.
*   **Expected Lending Recommendation:** Approve CGTMSE-backed loan of ₹30 Lakhs under women's enterprise credit schemes.

---

### 7. Startup
*   **Business Profile:** SaaS Logistics Tracking Software Provider.
*   **Ownership:** Private Limited.
*   **Industry & Location:** IT Services / Software, Bangalore, Karnataka.
*   **Vintage & Turnover:** 2 Years; Turnover of ₹3 Crores.
*   **Cash Flow Characteristics:** High monthly technology and software spend. High cash burn rate.
*   **GST Profile:** IT service invoices filed.
*   **UPI Behaviour:** Digital vendor payouts.
*   **AA Data Availability:** Integrated current account statements.
*   **EPFO Profile:** 18 registered software engineers.
*   **Credit History:** No historical corporate debt. Founder personal CIBIL = 760.
*   **Risk Profile:** High (High overheads, potential client concentration).
*   **Expected Financial Health Card:** DSCR = 1.10, Current Ratio = 2.10, Cash Burn Rate = ₹15L/month.
*   **Expected AI Insights:** Volatile cash flows. Unsuited for high leverage term debt.
*   **Expected Lending Recommendation:** Decline term loan; approve invoice discounting limit of ₹30 Lakhs.

---

### 8. First-time Borrower
*   **Business Profile:** CNC Machine Shop Job Worker.
*   **Ownership:** Proprietorship.
*   **Industry & Location:** Engineering Workshops, Kolhapur, Maharashtra.
*   **Vintage & Turnover:** 3 Years; Turnover of ₹1.5 Crores.
*   **Cash Flow Characteristics:** Local corporate clients. High cash purchases for metals.
*   **GST Profile:** GSTR-1 filed quarterly.
*   **UPI Behaviour:** Medium frequency peer-to-peer business transactions.
*   **AA Data Availability:** Single personal-cum-business account statement.
*   **EPFO Profile:** No registered employees.
*   **Credit History:** No corporate credit bureau history. Personal CIBIL = 705.
*   **Risk Profile:** Moderate (Lack of historical credit reference).
*   **Expected Financial Health Card:** DSCR = 1.30, Net Profit Margin = 12%.
*   **Expected AI Insights:** GST filings indicate stable sales growth. Cash flow validates credit limit.
*   **Expected Lending Recommendation:** Approve micro business loan of ₹15 Lakhs under CGTMSE cover.

---

### 9. Existing Borrower
*   **Business Profile:** Plastic Moldings Supplier.
*   **Ownership:** Private Limited.
*   **Industry & Location:** Plastics, Chennai, Tamil Nadu.
*   **Vintage & Turnover:** 7 Years; Turnover of ₹10 Crores.
*   **Cash Flow Characteristics:** Stable monthly business receipts.
*   **GST Profile:** Conforming GSTR-3B filings.
*   **UPI Behaviour:** Low usage; mostly RTGS/NEFT transfers.
*   **AA Data Availability:** Multi-year bank ledgers linked.
*   **EPFO Profile:** 32 registered employees.
*   **Credit History:** Active CC limit of ₹1.5 Cr with IDBI Bank. Clean repayments over 3 years.
*   **Risk Profile:** Low.
*   **Expected Financial Health Card:** DSCR = 1.40, Limit Utilization Average = 72%.
*   **Expected AI Insights:** Constant limit utilization. Credit history supports higher limits.
*   **Expected Lending Recommendation:** Approve CC limit enhancement to ₹2.2 Crores.

---

### 10. High Growth MSME
*   **Business Profile:** Solar Rooftop Panels Installation Provider.
*   **Ownership:** Private Limited.
*   **Industry & Location:** Renewable Energy, Ahmedabad, Gujarat.
*   **Vintage & Turnover:** 3 Years; Turnover grew from ₹1.2 Cr to ₹9 Cr in 24 months.
*   **Cash Flow Characteristics:** Project-based advance payments combined with milestone billings.
*   **GST Profile:** Monthly filing. Outward GST shows high growth.
*   **UPI Behaviour:** Vendor payments managed via UPI.
*   **AA Data Availability:** Full current account records.
*   **EPFO Profile:** 28 registered staff.
*   **Credit History:** Tiny startup debt. Founder CIBIL = 745.
*   **Risk Profile:** Moderate (Fast expansion can stress cash reserves).
*   **Expected Financial Health Card:** DSCR = 1.25, Revenue growth YoY = 150%.
*   **Expected AI Insights:** Strong sales trend. Working capital enhancements required to fund project pipelines.
*   **Expected Lending Recommendation:** Approve WC limit of ₹1.5 Crores.

---

### 11. Distressed MSME
*   **Business Profile:** Brick Kiln & Clay Products Manufacturer.
*   **Ownership:** Partnership.
*   **Industry & Location:** Construction Materials, Jhajjar, Haryana.
*   **Vintage & Turnover:** 8 Years; Turnover declined 40% to ₹3 Crores.
*   **Cash Flow Characteristics:** Blocked cash reserves, delayed receivables (180+ days), tax defaults.
*   **GST Profile:** GST filings delayed by 3+ months.
*   **UPI Behaviour:** High cash withdrawals, cheque bounce alerts.
*   **AA Data Availability:** Restricted; multiple inactive accounts.
*   **EPFO Profile:** Employee registry counts fell from 15 to 4.
*   **Credit History:** Active loan (₹50 Lakhs), classified as SMA-1. CIBIL score = 560.
*   **Risk Profile:** High (Default risk).
*   **Expected Financial Health Card:** DSCR = 0.85, Current Ratio = 0.72.
*   **Expected AI Insights:** Cash flow is insufficient to cover interest payments. Financial stress identified.
*   **Expected Lending Recommendation:** Decline credit extensions. Trigger Early Warning System and route case to recovery teams.

---

### 12. Seasonal Business
*   **Business Profile:** Fruit Juice Pulp Extraction Plant.
*   **Ownership:** Proprietorship.
*   **Industry & Location:** Food Processing, Ratnagiri, Maharashtra.
*   **Vintage & Turnover:** 5 Years; Turnover of ₹3.5 Crores.
*   **Cash Flow Characteristics:** 80% of cash receipts generated between March and June. Overhead costs remain constant throughout the year.
*   **GST Profile:** High outward GST filings during seasonal months.
*   **UPI Behaviour:** Inward distributor payments.
*   **AA Data Availability:** Integrated bank ledger.
*   **Credit History:** Clean repayments on seasonal loans. CIBIL = 715.
*   **Risk Profile:** Moderate (Cash management dependency).
*   **Expected Financial Health Card:** Annual DSCR = 1.35, Q4 Cash deficit ratio = 60%.
*   **Expected AI Insights:** Predictable seasonal variance. Structuring repayments around peak sales months recommended.
*   **Expected Lending Recommendation:** Approve seasonal working capital credit of ₹60 Lakhs with bullet repayments.

---

### 13. Service Enterprise
*   **Business Profile:** IT Infrastructure Management Services.
*   **Ownership:** Partnership.
*   **Industry & Location:** IT Services, Noida, Uttar Pradesh.
*   **Vintage & Turnover:** 6 Years; Turnover of ₹5 Crores.
*   **Cash Flow Characteristics:** Consistent monthly client receipts. Low inventory overheads. Monthly payroll accounts for 70% of costs.
*   **GST Profile:** Clean filings.
*   **AA Data Availability:** Linked business current accounts.
*   **EPFO Profile:** 38 registered technical employees.
*   **Credit History:** Clean repayment record. CIBIL = 730.
*   **Risk Profile:** Low.
*   **Expected Financial Health Card:** DSCR = 1.50, Debt-to-Equity = 0.40.
*   **Expected AI Insights:** Stable monthly subscription cash inflows.
*   **Expected Lending Recommendation:** Approve business term loan of ₹50 Lakhs.

---

### 14. Digital Business
*   **Business Profile:** Direct-to-Consumer (D2C) Apparel Brand.
*   **Ownership:** Private Limited.
*   **Industry & Location:** E-commerce Retail, Mumbai, Maharashtra.
*   **Vintage & Turnover:** 3 Years; Turnover of ₹7 Crores.
*   **Cash Flow Characteristics:** High-frequency, small-ticket digital receipts. High advertising and warehouse spends.
*   **GST Profile:** Monthly filings.
*   **UPI Behaviour:** Integrated with online payment gateways. High transaction counts.
*   **AA Data Availability:** Online gateway accounts linked.
*   **EPFO Profile:** 12 staff.
*   **Credit History:** Personal founder guarantees. CIBIL = 740.
*   **Risk Profile:** Moderate.
*   **Expected Financial Health Card:** DSCR = 1.32, Inventory rotation days = 25.
*   **Expected AI Insights:** High marketing spends. Sales velocity supports credit extensions.
*   **Expected Lending Recommendation:** Approve merchant cash advance facility of ₹80 Lakhs.

---

### 15. Supply Chain Vendor
*   **Business Profile:** Tier-2 Supplier to Auto Manufacturers.
*   **Ownership:** Private Limited.
*   **Industry & Location:** Engineering, Jamshedpur, Jharkhand.
*   **Vintage & Turnover:** 10 Years; Turnover of ₹14 Crores.
*   **Cash Flow Characteristics:** Receivables tied to Tier-1 OEM approvals. Invoices discounted through TReDS.
*   **GST Profile:** Matching credit filings.
*   **AA Data Availability:** Full current account integrations.
*   **EPFO Profile:** 48 employees.
*   **Credit History:** Active working capital limits. CIBIL = 720.
*   **Risk Profile:** Low.
*   **Expected Financial Health Card:** DSCR = 1.38, Average debtor days (undiscounted) = 75.
*   **Expected AI Insights:** Invoices are clear and verified. TReDS integrations provide quick liquidity options.
*   **Expected Lending Recommendation:** Approve invoice financing limit of ₹2 Crores.

---

## End-to-End Banking Journey Scenarios

The platform coordinates borrower journeys across key operational milestones.

```
  [ Lead Creation ] ──► [ Data Consent (AA/GST) ] ──► [ Spreading & Scoring ]
                                                             │
  [ Committee Review ] ◄── [ CAM Narrative Draft ] ◄─────────┘
        │
        ▼
  [ Limit Approved ] ──► [ Digital Disbursement ]
```

### 1. New-to-Credit MSME Journey
*   **Workflow Stage:** Origination & Validation.
*   **Process flow:** Customer registers -> triggers AA consent -> Spreading Engine parses bank ledgers -> Credit Engine runs policy checks -> Gemini drafts CAM -> Limit approved -> Digitally signed contract generated.

### 2. Working Capital Enhancement
*   **Workflow Stage:** Limit Enhancement.
*   **Process flow:** RM flags account eligibility -> customer confirms enhancement request -> GST filings pulled to verify sales growth -> system adjusts limits -> automated approval triggered.

### 3. Early Warning & Stress Action
*   **Workflow Stage:** Risk Monitoring.
*   **Process flow:** EWS flags three consecutive cheque bounces -> Alert Console triggers red warning -> RM workspace receives action checklist -> drawing limit restricted.

---

## AI Evaluation & Model Verification Scenarios

AI evaluation scenarios test model outputs using distinct validation datasets.

| Scenario ID | Test Scope | Focus Area | Target AI Response |
| :--- | :--- | :--- | :--- |
| **AAR-VAL-001** | Excellent Profile | Risk Classification | Output low default probability, suggest limit enhancement. |
| **AAR-VAL-002** | Borderline Profile | Policy Exceptions | Highlight tight cash flow coverage, recommend personal guarantees. |
| **AAR-VAL-003** | Incomplete Data | Missing inputs | Prompt user to upload missing current account statements. |
| **AAR-VAL-004** | Conflicting Data | GST vs Bank ledgers | Flag discrepancy if bank deposits are 40% lower than GST sales. |
| **AAR-VAL-005** | Fraud Indicators | Round-tripping check | Flag circular transactions between related party entities. |
| **AAR-VAL-006** | Explainability Check | Citation validation | Provide direct links to policy sections for rejected applications. |

---

## Conceptual Dashboard Datasets

### 1. Executive Cockpit Dataset
*   **Key Fields:** Total Disbursed Value, Gross NPA Ratio (%), Average Process TAT, Regional Yields, Limit Utilization (%).

### 2. RM Pipeline Dataset
*   **Key Fields:** Active Leads list, Lead Conversion status, Tasks checklist, Target commissions, EWS Alerts list.

### 3. Credit Analyst Assessment Dataset
*   **Key Fields:** Calculated DSCR, Leverage Ratios, Policy compliance checks, Auto-drafted CAM narratives.

---

## Google Cloud Conceptual Data Platform Mapping

```
┌────────────────────────────────────────────────────────────────────────┐
│                              LOOKER ENGINE                             │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       BIGQUERY ANALYTICS WAREHOUSE                     │
│   ┌───────────────────────────┐         ┌──────────────────────────┐   │
│   │  MSME Master Persona Data │         │  Vertex AI Feature Store │   │
│   └───────────────────────────┘         └──────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

1. **BigQuery:** Central repository hosting historical borrower datasets, evaluation tables, and operational logs.
2. **Vertex AI Feature Store:** Serves variables like cash flow averages and debt service coverages for credit risk models.
3. **Gemini & Document AI:** Evaluates business financial records, extracts text details, and drafts credit summaries.
4. **Looker:** Standard business intelligence engine rendering charts for dashboards and RM workspaces.

---

**Approved & Signed By:**  
*Chief Banking Domain Expert, Project AAROHAN*  
*AI Evaluation Lead, Project AAROHAN*  
*Professional Services Consultant, Google Cloud*  
*Head, Credit Risk Governance, IDBI Bank*
