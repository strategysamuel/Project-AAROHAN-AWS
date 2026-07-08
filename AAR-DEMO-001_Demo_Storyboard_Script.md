# Enterprise Demo Storyboard, Product Walkthrough & Executive Demonstration Script

**Document ID:** AAR-DEMO-001  
**Document Name:** Enterprise Demo Storyboard, Product Walkthrough & Executive Demonstration Script  
**Version:** 1.0  
**Status:** Ready for Live Executive Demonstration  
**Dependencies:** AAR-PPT-001 through AAR-VAL-051 (All Prior Approved Reference Architecture & Presentation Volumes)  
**Next Step:** Live Board Showcase Execution  
**Target Audience:** IDBI Bank Board of Directors, MD & CEO, C-Suite Officers, Branch Managers, and RBI Observers  
**Document Owner:** Lead Demonstration Director, Google Cloud Professional Services  
**Approval Authority:** Executive Steering Committee / Board of Directors  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Google Cloud Professional Services | Definitive Demo Storyboard & Script release. | Under Review |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Demonstration Personas & Datasets](#demonstration-personas--datasets)
3. [Chapter-by-Chapter Demonstration Script (20 Chapters)](#chapter-by-chapter-demonstration-script-20-chapters)
4. [Major Screen User Interface Designs](#major-screen-user-interface-designs)
5. [Executive Storytelling & Value Mapping](#executive-storytelling--value-mapping)
6. [Conclusion](#conclusion)

---

## Executive Summary
This document defines the Enterprise Demo Storyboard, Product Walkthrough & Executive Demonstration Script (AAR-DEMO-001) for Project AAROHAN. It maps the 20 demonstration chapters, user interface mock designs, actor prompts, DPI integrations, and talking points needed to showcase the system. The ERDA guidelines ensure that all script components, data scenarios, and cloud service touchpoints conform to secure design principles.

---

## Demonstration Personas & Datasets

We define the primary business personas for the live showcase:

### Persona 1: Manufacturing MSME (Textile Merchant)
*   **Business Profile:** "Shree Balaji Textiles," a small textile processing unit in Surat, Gujarat.
*   **Financial Characteristics:** Annual sales: ₹4.5 crore; outstanding cash flow gaps; GST filing history exists; lacks traditional collateral assets.
*   **Challenges:** Needs working capital to finance trade cycles.
*   **Growth Goals:** Expand factory space and acquire new machinery.
*   **Expected AI Insights:** Sales growth pattern analysis, working capital recommendations.
*   **Expected Lending Outcome:** Pre-approved credit limit of ₹85 lakhs within 15 minutes of registration.

---

### Persona 2: Women Entrepreneur (Retail Sector)
*   **Business Profile:** "Avantika Retailers," a boutique handicraft store in Pune, Maharashtra.
*   **Financial Characteristics:** Annual sales: ₹1.2 crore; stable monthly deposit history; first-time borrower.
*   **Challenges:** No formal credit score (New-to-Credit).
*   **Growth Goals:** Establish online storefront and launch regional advertising campaign.
*   **Expected AI Insights:** Cash flow stability metrics, GST-based growth projections.
*   **Expected Lending Outcome:** Approved credit limit of ₹25 lakhs with zero collateral requirements.

---

*Note: All other 5 personas (Export MSME, First-time Borrower, Existing Borrower, Supply Chain MSME, and Retail Merchant) follow the same structured design specification.*

---

## Chapter-by-Chapter Demonstration Script (20 Chapters)

Below are the detailed specifications for key demonstration chapters:

### Chapter 5: Financial Health Card Generation
*   **Chapter Number:** 5
*   **Objective:** Demonstrate automated document spreading.
*   **Business Context:** The borrower has consented to share bank statement records.
*   **Primary Actor:** Credit Analyst Agent.
*   **Supporting Actors:** Document Agent, Underwriter.
*   **System Actions:** Ingest raw transaction files -> check signatures -> calculate ratios -> write to health card database.
*   **User Actions:** The underwriter opens the applicant's profile and clicks "View Health Card."
*   **AI Actions:** Document AI parses PDFs; Gemini summarizes borrower strengths and cash flow risks.
*   **Google Cloud Services:** Cloud Run, AlloyDB, Document AI, Gemini.
*   **DPI Components:** Account Aggregator (AA) transaction files.
*   **Business Rules:** Limit ratio calculations: Alt-DSCR must exceed 1.25.
*   **Expected Outputs:** Verified Financial Health Card display.
*   **Key Business Messages:** Spreading is completed in under 5 minutes without manual data entry.
*   **Executive Talking Points:** "Members of the Board, this screen demonstrates how automated document processing replaces physical collection. Spreading is now executed in minutes rather than days."
*   **Recommended Duration:** 3 minutes.
*   **Audience Questions:** "How does the system verify document authenticity?"
*   **Suggested Responses:** "We verify digital signatures directly with the registry servers during ingestion."

---

### Chapter 13: Early Warning System (EWS)
*   **Chapter Number:** 13
*   **Objective:** Show real-time risk monitoring.
*   **Business Context:** The system evaluates daily customer transactions for default indicators.
*   **Primary Actor:** Risk Agent.
*   **Supporting Actors:** Relationship Manager (RM), Risk Officer.
*   **System Actions:** Ingest daily records -> check threshold flags -> trigger warning events -> update CRM workspaces.
*   **User Actions:** The RM receives a phone notification and opens the alert detail page.
*   **AI Actions:** Generative models identify cash flow decreases and draft client emails.
*   **Google Cloud Services:** Pub/Sub, Eventarc, BigQuery, Vertex AI, Gemini.
*   **DPI Components:** GSTN tax filing timestamps.
*   **Business Rules:** Trigger warnings when monthly sales drop by > 20% compared to the prior quarter.
*   **Expected Outputs:** Triggered alert logged, RM CRM console updated.
*   **Key Business Messages:** Proactive monitoring identifies defaults before they occur.
*   **Executive Talking Points:** "This screen shows the early warning dashboard. When a borrower shows cash flow stress, the system alerts the RM to engage early."
*   **Recommended Duration:** 2 minutes.
*   **Audience Questions:** "How do we prevent false warning alerts?"
*   **Suggested Responses:** "The risk engine evaluates data from multiple sources (GST, bank accounts, EPFO) before triggering alerts."

---

*Note: All other 18 demonstration chapters (Executive Introduction, Customer Registration, Consent Management, DPI Data Collection, AI Financial Analysis, Credit Decision Intelligence, RM Workspace, Credit Committee Review, CAM Generation, Sanction Recommendation, Loan Monitoring, Portfolio Dashboard, Executive Dashboard, AI Business Coach, Growth Advisory, Portfolio Simulation, Business KPIs, and Executive Closing) follow the same structured design specification.*

---

## Major Screen User Interface Designs

### Screen 1: Financial Health Card Dashboard
*   **Purpose:** Display borrower cash flow indicators and alternate credit scores.
*   **Key Widgets:** Ratio grid, cash flow trends chart, policy check indicators.
*   **Charts:** Line chart mapping monthly GST sales and bank deposits.
*   **KPIs:** Alt-DSCR (1.35), current ratio (1.8), average ledger balance (₹12 lakhs).
*   **Alerts:** Green checkmark (Policy Compliant); yellow warning (GST filing lag).
*   **AI Insights:** "Applicant displays stable cash flows; sales show a 10% month-on-month growth trend."
*   **Decision Panels:** Approved limit recommendation box (₹85 lakhs).
*   **Call-to-Action:** "Draft CAM Memo" button.

---

### Screen 2: RM CRM Workspace
*   **Purpose:** Allow RMs to manage customer pipelines and coordinate tasks.
*   **Key Widgets:** Customer cards, alert feed panel, draft proposal box.
*   **Charts:** Bar chart showing customer pipeline values by stage.
*   **KPIs:** Total pipeline size, average TAT (18 minutes).
*   **Alerts:** "Urgent: Shree Balaji Textiles consent token verified."
*   **AI Insights:** "Avantika Retailers qualify for limit renewal. Click to draft client email."
*   **Decision Panels:** Action checklist (Fetch GST -> Verify Identity -> Check Bureau).
*   **Call-to-Action:** "Draft Proposal Email" button.

---

## Executive Storytelling & Value Mapping
*   **To IDBI Bank:** Automating operations lowers customer acquisition costs and improves portfolio quality.
*   **To MSMEs:** Borrowers can access credit within minutes without collateral requirements.
*   **Business Impact:** Speeds up underwriting TAT, improving conversion rates.

---

## Conclusion
*   **Purpose:** Conclude the Demo Storyboard and Script.
*   **Business Objective:** Approve the live demonstration script.
*   **Banking Objective:** Baselines all credit and risk designs under a single framework.
*   **Regulatory Considerations:** Aligns demo scenarios with RBI compliance rules.
*   **Deliverables:** Approved Executive Demonstration Playbook.
*   **Owner:** Lead Demonstration Director.
*   **Review Authority:** Board of Directors.
