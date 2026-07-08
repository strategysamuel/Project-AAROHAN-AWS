# AAR-USER-001: Project AAROHAN Enterprise End User Guide

---

## 1. Cover Page

* **Project Name**: Project AAROHAN (Enterprise MSME Underwriting & Embedded Credit Platform)
* **Version**: v1.0.0
* **Guide Version**: v1.0.0
* **Classification**: CONFIDENTIAL - BANK OPERATIONAL
* **Owner**: Retail and MSME Lending Product Division
* **Approval Matrix**:
  - Head of Retail Assets: APPROVED
  - UX Documentation Specialist: APPROVED
  - Chief Product Owner (MSME Division): APPROVED

---

## 2. Purpose

This user guide provides instructions to help banking professionals navigate and operate the Project AAROHAN digital lending portal.

---

## 3. Scope

This document details procedures for onboarding borrowers, evaluating cash flow health, reviewing AI-generated credit limits, modifying Credit Assessment Memorandums (CAM), tracking relationship tasks, and using the OCEN embedded lending marketplace.

---

## 4. Intended Audience

This guide is designed for Relationship Managers (RMs), Credit Officers, Branch Managers, Regional Managers, Credit Approvers, and Business Executives.

---

## 5. Introduction to Project AAROHAN

Project AAROHAN simplifies MSME lending. By consolidating structured integrations (such as CKYC, GSTN, Account Aggregator, MCA, EPFO, and TReDS) with AI-powered underwriting and OCEN protocols, the platform accelerates credit approvals for business borrowers.

---

## 6. Getting Started

* **Login**: Log in using your corporate Active Directory credentials. Ensure MFA verification is completed.
* **Dashboard Overview**: The landing dashboard displays your current active leads, task checklists, pending credit approvals, and early warning risk indicators.
* **Navigation**: Toggle between **TReDS Receivables**, **OCEN Lending**, and **RM Workspace** using the sidebar tabs.
* **Notifications**: Real-time notifications alert you to new client applications, consent approvals, and high-risk EWS triggers.
* **User Profile**: Access your profile settings via the top-right menu to manage active branches or assign secondary approvers.

---

## 7. MSME Onboarding

* **Register Customer**: Click "New Registration". Input core company metadata: Company PAN, mobile number, legal constitution, and registered business address.
* **Upload Documents**: Upload required document PDFs (such as financial statements, business proofs, and partnership deeds) into the document vault.
* **CKYC Verification**: Run CKYC verification by supplying the client's PAN. The system pulls registry records and computes identity match confidence.
* **Consent Management**: Initiate digital consent requests. The customer receives a notification to sign off on data pulls for GST, AA, and credit bureaus.

---

## 8. Financial Data Collection

* **GST Integration**: Sync GST records. The system fetches GSTR-1 and GSTR-3B filings, calculating average monthly turnovers and compliance history.
* **Account Aggregator**: Request statement linkage. The system downloads transaction histories, identifies recurring entries, and tracks net cash flows.
* **MCA Information**: Trigger corporate registry syncs. This imports incorporation dates, active directors, filings history, and outstanding charges.
* **EPFO & ESIC Data**: Retrieve workforce metrics. This tracks active employee counts, average payrolls, and contribution payment timeliness.
* **TReDS Data**: Sync discounting platforms. This downloads outstanding receivables invoices, buyer PAN ratings, and discounting logs.

---

## 9. Financial Health Card

The Financial Health Card (FHC) displays scores ranging from 300 to 900:
* **Overall Score**: Summary financial indicator.
* **Financial Indicators**: Detailed scores tracking revenue stability, debt service capacity, and growth momentum.
* **Risk Indicators**: Alerts flagging compliance delays or negative banking behaviors (such as cash outflows and cheque bounces).
* **Business Insights**: Highlights (e.g., low seasonal revenue volatility) and warnings (e.g., occasional delays in GSTR filings).

---

## 10. AI Credit Decision

* **Recommendation Summary**: The engine displays status indicators (such as `APPROVED`, `REJECTED`, or `PENDING_HUMAN_REVIEW`).
* **Explainability**: View a plain-text breakdown detailing how the system evaluated parameters (e.g., interest coverage ratio) to arrive at the decision.
* **Confidence Score**: Represents system certainty (e.g., 92% confidence based on model fit).
* **Human Review**: Credit Officers can override the recommendation by entering justification comments.

---

## 11. AI CAM Generator

* **Generate CAM**: Click "Generate Draft". The system uses Vertex AI to compile financial assessments and SWOT analyses.
* **Review CAM**: Inspect compiled summaries, risk mitigations, and loan terms.
* **Edit CAM**: Credit Officers can update text fields (such as risk mitigations and SWOT comments) directly.
* **Approve CAM**: Submit the completed CAM to the Branch Manager for sign-off.
* **Export CAM**: Download the approved CAM as a PDF for audit records.

---

## 12. Relationship Manager Workspace

* **Customer 360**: Displays customer contact histories, financial cards, outstanding applications, and active tasks.
* **Tasks**: Checklists tracking required steps (such as gathering signature proofs or verifying documents).
* **Calendar**: Displays upcoming client visits and review schedules.
* **Alerts**: Alerts flagging pending expiries or overdue documents.
* **Next Best Action**: Recommended actions (e.g., "Schedule follow-up to request GST credentials").

---

## 13. Executive Dashboard

* **Portfolio KPIs**: Tracks total disbursals, active portfolio sizes, non-performing assets (NPAs), and average lending yields.
* **Branch Performance**: Compare disbursals and default metrics across branch offices.
* **Regional Performance**: Displays volume trends grouped by region.
* **Portfolio Trends**: Dynamic charts tracking industry exposures.

---

## 14. Early Warning System

* **Watchlists**: Lists accounts with elevated risk profiles (e.g., declining monthly turnovers).
* **Alerts**: Triggers based on adverse events (such as director resignations or late tax filings).
* **Risk Timeline**: Historical timeline of alerts for a given account.

---

## 15. Portfolio Intelligence

* **Portfolio Analytics**: Run deep-dive queries on historical credit behavior.
* **Scenario Simulation**: Simulate impact of changing macroeconomic variables (such as interest rate changes) on default rates.
* **Executive Reports**: Generate and export portfolio health reports.

---

## 16. OCEN & Digital Lending

* **Loan Marketplace**: Discover multi-lender credit offers.
* **Offer Comparison**: Compare terms side-by-side (highlighting lowest interest rates and best tenures).
* **Eligibility**: Run automated rules-based checks against customer financial data.
* **Application Tracking**: Check live application statuses (e.g., `OFFERS_GENERATED` or `DISBURSED`).

---

## 17. Search & Filters

Use the search bar to locate customers by PAN, legal name, or application ID. Apply filters to narrow lists by branch, status, or date range.

---

## 18. Reports & Exports

Download files in Excel or PDF formats for offline analysis or audit presentation.

---

## 19. Notifications

Check the notifications drawer for real-time alerts.

---

## 20. Frequently Asked Questions (FAQ)

* **Q: Why is an application stuck in PENDING_HUMAN_REVIEW?**
  - *A*: The borrower's credit score falls within the threshold range, requiring manual officer sign-off.
* **Q: How does the system generate the SWOT analysis?**
  - *A*: It extracts insights from tax records, director profiles, and bank statement patterns using Gemini.

---

## 21. Troubleshooting

* **Issue: Missing Account Aggregator statement data.**
  - *Resolution*: Verify that the client approved the consent request and that the status is listed as `APPROVED`.

---

## 22. Best Practices

* Always review AI-generated risk profiles before final loan approvals.
* Log justification comments for all manual overrides.

---

## 23. Keyboard Shortcuts

* `Ctrl + S`: Quick-save active CAM changes.
* `Alt + N`: Initiate a new customer registration.

---

## 24. Glossary of Banking & AI Terms

* **OCEN**: Open Credit Enablement Network.
* **ULI**: Unified Lending Interface.
* **CAM**: Credit Assessment Memorandum.
* **Explainability**: Plain-text breakdown of AI decision factors.

---

## 25. Support Contact Information

* Helpdesk: `1800-AAROHAN-SUPPORT` (Toll-Free)
* Internal IT Portal: `help.bank.aarohan.com`

---

## 26. Appendix

* Screen Layout Navigation Tree.
* Common Error Message Index.
