# Project AAROHAN: User & Administrator Manual
## AAR-LCP-007: Operations Handbook, Presenter Console Guidelines, and System Administration Playbook

**Document Classification:** Product User Guide & Administration Handbook  
**Platform Version:** ESE v1.0.0 (GA)  
**Target Roles:** Presenters, Banking Staff, System Administrators  
**Status:** **🟢 GENERAL DISTRIBUTION**  

---

## 1. Executive Summary
This document provides instructions for operating, presenting, and managing the **Project AAROHAN Enterprise Digital Banking Twin v1.0.0**. It guides system administrators in managing active datasets and assists presenters in running live demonstrations, stress-test comparisons, and training workshops.

---

## 2. Intended Audience
- **Demo Presenters & Sales Teams**: Hosting executive showcases and hackathons.
- **Credit & Risk Officers**: Adjusting simulated underwriting rules.
- **System Administrators**: Setting configurations, backup tasks, and active dataset profiles.

---

## 3. System Overview
AAROHAN is an interactive sandbox replicating India's MSME digital underwriting registry stack. Business processes are simulated at a transaction level, allowing users to watch events cascade from tax filings through credit appraisals up to portfolio dashboard aggregations.

---

## 4. User Roles
- **Customer**: Registers businesses and consents to registry pulls.
- **Relationship Manager**: Initiates credit checks and oversees borrower onboarding.
- **Credit Manager**: Reviews generated CAM sheets and approves loan limits.
- **Operations Officer**: Disburses approved loans and tracks repayment schedules.
- **Bank Administrator**: Sets bank policies, interest rates, and SLA targets.
- **Demo Administrator**: Launches pre-set journeys, triggers clock ticks, and switches branding templates.
- **System Administrator**: Manages databases, sets variables, and conducts backups.

---

## 5. Login & Authentication
Users access the platform via the main web UI dashboard. 
Administrators authenticate using local identity registers or secure IAM connections in staging profiles.

---

## 6. Dashboard Overview
The main console is split into three zones:
1.  **Left Column**: Controller panel for selecting active datasets, personas, and scenarios.
2.  **Center Column**: Live Timeline and Replay log, illustrating step-by-step journey stages.
3.  **Right Column**: Real-time KPI summaries, AI narrations, and download buttons.

---

## 7. Customer Registration
- **Purpose**: Initiate the digital lending onboarding flow.
- **Navigation Path**: `Presenter Console ➔ Onboard Tab ➔ Step 1: Customer Registration`.
- **Procedure**: Click 'Register New Business' and enter names, PAN, and sectors.
- **Expected Result**: System issues a unique Customer ID.
- **Screens to Capture**: Customer data entry pop-up window.
- **Common Errors**: `Invalid PAN Format`.
- **Troubleshooting**: Ensure the input matches standard alphanumeric formatting (e.g. `ABCDE1234F`).

---

## 8. CKYC Verification
- **Purpose**: Verify company directors' identities.
- **Navigation**: `Presenter Console ➔ Onboard Tab ➔ Step 2: CKYC Search`.
- **Procedure**: Click 'Execute CKYC Pull'.
- **Expected Result**: Green checkmark indicating verified status.
- **Screens to Capture**: Registry validation screen with green success alerts.
- **Common Errors**: `Record Not Found`.
- **Troubleshooting**: Validate that the input director credentials exist in the seed dataset.

---

## 9. GST Analysis
- **Purpose**: Pull transaction invoices to calculate annual turnover.
- **Navigation**: `Presenter Console ➔ Onboard Tab ➔ Step 3: GST Sync`.
- **Procedure**: Select 'Link GSTIN' and click 'Retrieve Invoices'.
- **Expected Result**: System calculates operating revenues.
- **Screens to Capture**: Monthly invoice revenue line charts.
- **Common Errors**: `GSTIN Inactive`.
- **Troubleshooting**: Switch scenario to `EXCELLENT_BORROWER` to restore active tax identifiers.

---

## 10. Account Aggregator Analysis
- **Purpose**: Retrieve bank statements to analyze monthly cash flow balances.
- **Navigation**: `Presenter Console ➔ Onboard Tab ➔ Step 4: AA Consent Flow`.
- **Procedure**: Click 'Send AA Request' followed by 'Approve Consent'.
- **Expected Result**: Displays average monthly balances.
- **Screens to Capture**: Current account balance visualizations.
- **Common Errors**: `Consent Revoked`.
- **Troubleshooting**: Restart onboarding to refresh consent tokens.

---

## 11. Financial Health Card
- **Purpose**: Aggregate indicators (DSCR, Net Margin) into a single score out of 100.
- **Navigation**: `Presenter Console ➔ Onboard Tab ➔ Step 7: FHC Summary`.
- **Procedure**: Click 'Generate Financial Health Card'.
- **Expected Result**: Score card display (e.g., FHC Score: 85/100).
- **Screens to Capture**: Visual circular health index charts.
- **Common Errors**: `Divide by Zero in DSCR Calculation`.
- **Troubleshooting**: Check that current liabilities are greater than zero.

---

## 12. AI Credit Decision
- **Purpose**: Run credit underwriting rules to issue loan decisions.
- **Navigation**: `Presenter Console ➔ Onboard Tab ➔ Step 8: Underwriting Verdict`.
- **Procedure**: Click 'Appraise Loan'.
- **Expected Result**: Approved limit value or Rejection message, accompanied by AI explainability notes.
- **Screens to Capture**: Underwriting result card with AI narrations.
- **Common Errors**: `Appraisal Timeout`.
- **Troubleshooting**: Validate network connectivity to Vertex AI (in PRODUCTION profile) or verify seed records.

---

## 13. CAM Generation
- **Purpose**: Compile a formal Credit Appraisal Memorandum report.
- **Navigation**: `Presenter Console ➔ Onboard Tab ➔ Step 10: Export CAM`.
- **Procedure**: Click 'Download CAM PDF'.
- **Expected Result**: Browser prompts to save `CAM_Report.pdf` to local disk.
- **Screens to Capture**: PDF report download dialog window.
- **Common Errors**: `File generation failed`.
- **Troubleshooting**: Verify system write permissions for `/tmp` or the local workspace folder.

---

## 14. OCEN Marketplace
- **Purpose**: Match approved loans with lender loan offers.
- **Navigation**: `Presenter Console ➔ Marketplace Tab`.
- **Procedure**: Click 'Request Marketplace Offers'.
- **Expected Result**: List of five lender class loan offers (rates, tenures).
- **Screens to Capture**: Offers table highlighting rate differences.
- **Common Errors**: `No Active Offers`.
- **Troubleshooting**: Ensure the borrower credit score exceeds the minimum threshold of 600.

---

## 15. Executive Dashboard
- **Purpose**: Track lending operations and portfolio quality.
- **Navigation**: `Executive Console ➔ Portfolio Analytics Tab`.
- **Procedure**: Review metrics on the dashboard screen.
- **Expected Result**: Real-time charts showing outstanding balances and NPA ratios.
- **Screens to Capture**: Visual sector concentration charts.
- **Common Errors**: `Out of Date Aggregates`.
- **Troubleshooting**: Trigger clock tick to push calculations forward.

---

## 16. Enterprise Simulation Engine
Allows users to modify regional parameters and monsoon profiles, simulating realistic cause-and-effect variances.

---

## 17. Demo Mode
Switches adapters to local mocks, providing a zero-dependency environment.

---

## 18. Training Mode
Enables instructors to tick dates and pause progression to discuss event cascades.

---

## 19. Dataset Selection
Select different datasets (e.g. `agro`, `msme`) to load different persona profiles.

---

## 20. Persona Selection
Select different personas (e.g. Priya Textiles) to demonstrate specific business profiles.

---

## 21. Scenario Selection
Select scenario states (Excellent, Stressed, Blacklisted) to alter onboarding results.

---

## 22. Demo Journey Execution
Click 'Run E2E Journey' to automatically walk through onboarding steps.

---

## 23. Report Generation
Export FHC, CAM, or Risk reports in PDF, Excel, or Markdown.

---

## 24. Administration Functions
Update global parameters (e.g. Repo Rate, Inflation) via admin interfaces.

---

## 25. Monitoring & Health Checks
Query `/health` to verify system health and check loaded adapters.

---

## 26. Backup & Restore
Create snapshots of the local database files before applying modifications.

---

## 27. Troubleshooting
Consult logging files or restart services in the event of transaction locks.

---

## 28. Frequently Asked Questions
- **Is PII data secure?**  
  *Yes, all registry actions run locally in sandbox mode using synthetic dataset seeders.*
- **Can I run this without internet access?**  
  *Yes, the DEMO profile runs with zero external connections.*

---

## 29. Best Practices
- Back up active database tables before launching long simulation clock runs.
- Keep terminal screens clear during code walkthroughs to avoid presenter distraction.

---

## 30. Glossary
- **DPI**: Digital Public Infrastructure (GST, EPFO, AA).
- **DSCR**: Debt Service Coverage Ratio.
- **FHC**: Financial Health Card.

---

## 31. Appendix
- **Shortcut Cheatsheet**: Presenter key-bindings.
- **API reference**: REST endpoints map.
