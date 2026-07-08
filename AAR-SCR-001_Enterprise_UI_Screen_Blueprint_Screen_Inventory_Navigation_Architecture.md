# Enterprise UI Screen Blueprint, Screen Inventory & Navigation Architecture

**Document ID:** AAR-SCR-001  
**Document Name:** Enterprise UI Screen Blueprint, Screen Inventory & Navigation Architecture  
**Version:** 1.0  
**Status:** Approved for Design & Frontend Shell Development  
**Dependencies:** Entire Enterprise Repository, Executive Compendium (AAR-EXEC-BOOK-001), Board Presentation (AAR-PPT-001), Demo Storyboard (AAR-DEMO-001), UX Playbook (AAR-UX-PLAYBOOK-001), and Experience Architecture (AAR-UXA-017)  
**Target Audience:** IDBI Bank Board, CXOs, Product Managers, UX/UI Designers, Frontend Engineers, Banking SMEs, and Google Cloud Professional Services  
**Document Owner:** Chief Product Experience Architect / Enterprise UX Architect  
**Approval Authority:** Digital Transformation Office (DTO) / Enterprise Architecture Review Board (EARB)

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | Chief Product Experience Architect | Initial Release of Complete Screen Blueprint & Navigation Architecture. | DTO / EARB |

---

## Table of Contents
1. [Executive Summary & Blueprint Architecture](#executive-summary--blueprint-architecture)
2. [Global Navigation & Interaction Architecture](#global-navigation--interaction-architecture)
3. [Enterprise User Modules Catalogue](#enterprise-user-modules-catalogue)
   - [3.1 Executive Portal](#31-executive-portal)
   - [3.2 Relationship Manager Portal](#32-relationship-manager-portal)
   - [3.3 Branch Operations](#33-branch-operations)
   - [3.4 Credit Analyst Portal](#34-credit-analyst-portal)
   - [3.5 Credit Committee Portal](#35-credit-committee-portal)
   - [3.6 Risk Management Portal](#36-risk-management-portal)
   - [3.7 Compliance Portal](#37-compliance-portal)
   - [3.8 Portfolio Monitoring Portal](#38-portfolio-monitoring-portal)
   - [3.9 Collections Portal](#39-collections-portal)
   - [3.10 MSME Customer Portal](#310-msme-customer-portal)
   - [3.11 Partner Portal](#311-partner-portal)
   - [3.12 Admin Portal](#312-admin-portal)
   - [3.13 AI Operations Console](#313-ai-operations-console)
   - [3.14 System Administration Portal](#314-system-administration-portal)
4. [Enterprise Report Catalogue](#enterprise-report-catalogue)
5. [AI Interaction & Conversation Catalogue](#ai-interaction--conversation-catalogue)
6. [Platform Device Matrix & Responsive Standards](#platform-device-matrix--responsive-standards)
7. [Governance & Security Standards](#governance--security-standards)

---

## Executive Summary & Blueprint Architecture

Project AAROHAN is IDBI Bank's next-generation digital credit platform for MSME lending. This document serves as the master blueprint for every interface screen across the 14 operational modules of the system. Designed in alignment with **Google Material Design 3** standards and optimized for deployment on Google Cloud (using Firebase for host delivery, Vertex AI for embedded intelligence, and Looker for dashboards), this inventory translates strategic workflows into structured screen layouts. 

### Core Design Paradigms:
1. **Minimised Cognitive Load:** Structured layouts focusing on task prioritization.
2. **AI-Native Contextualization:** Side-panels housing Gemini-powered advisors that dynamically adapt based on the active transaction.
3. **Banking-Grade Security:** Row-level and field-level masking based on role permissions.

---

## Global Navigation & Interaction Architecture

The global navigation paradigm defines how users move through the platform.

```
+----------------------------------------------------------------------------------+
|  [Logo]  Universal Search (Alt+/)  |  RM Workspace (Role)  | [Alerts (5)]  [User] |
+----------------------------------------------------------------------------------+
| (Sidebar)         |  (Main Working Canvas)                                       |
| - Dashboard       |  +---------------------------------------------------------+ |
| - Lead Pipeline   |  | Active Workspace Card                                   | |
| - Credit Queue    |  +---------------------------------------------------------+ |
| - Monitoring      |  |                                                         | |
| - Reports         |  |                                                         | |
|                   |  +---------------------------------------------------------+ |
| [AI Coach (Chat)] |  | AI Recommendation Banner                                | |
+-------------------+------------------------------------------------------------+
```

### 1. Global Navigation Layouts
*   **Desktop:** Left-hand collapsing sidebar containing primary and secondary modules, with a persistent header housing Universal Search, Role Selector, Notifications Bell, Bookmarks, and User Settings.
*   **Tablet:** Left-hand navigation rail with icons, maximizing main screen real estate for data tables.
*   **Mobile:** Bottom navigation bar containing home, pipeline/queue, alerts, and quick actions, with secondary links under a hamburger menu.

### 2. Universal Search
*   **Trigger:** Shortcut `Alt+/` or persistent input field.
*   **Features:** Search clients by PAN, GSTIN, Entity Name, or Loan ID; natural-language search ("Find all high-value proposals in Karnataka pending compliance approval").
*   **Results Canvas:** Categorized dropdown containing Quick Actions, Client Files, and FAQ documents.

### 3. Quick Actions
*   **RM Workspace:** "New Application", "Initiate Consent Request", "Draft CAM Memo".
*   **Risk & Credit Analyst:** "Spreads Statements", "Re-run Risk Models", "Escalate to Committee".
*   **MSME Portal:** "Upload Statements", "Accept Offer", "Drawdown Funds".

---

## Enterprise User Modules Catalogue

### 3.1 Executive Portal

#### Module Overview
A high-level portal providing IDBI Bank Executives (CBO, CDO, CIO, CEO) with a bird's-eye view of lending operations, financial health, AI performance metrics, and compliance ratings.

*   **Business Purpose:** Strategic oversight, portfolio steering, and operational efficiency management.
*   **Target Users:** Executive Committee, CEO, Chief Business Officer, Chief Risk Officer.
*   **Navigation Structure:** Primary Dashboard -> Portfolio Analytics -> Operational TAT -> AI Performance.

---

#### Primary Screens

##### Screen ID: AAR-SCR-EXE-001
*   **Screen Name:** Executive Board Cockpit (Strategic Dashboard)
*   **Business Purpose:** Consolidate portfolio growth, risk concentrations, and system TAT in a single view.
*   **Primary Users:** Chief Business Officer, CEO, Board Members.
*   **Business Process Supported:** Monthly performance reviews, asset-liability oversight.
*   **Navigation Path:** `Home -> Executive Dashboard -> Strategic Cockpit`
*   **Entry Conditions:** Executive User Session Authorized, MFA validation complete.
*   **Exit Conditions:** Logout, Navigation to sub-portals, or Export Action.
*   **Widgets:**
    *   *KPI Card Grid:* Total Disbursement (₹ Cr), Active Borrowers, Gross NPA (%), Average TAT.
    *   *Charts:* Portfolio Growth Trend (Line Chart), Sectoral Concentration (Donut Chart), Risk Ratings Distribution (Bar Chart).
    *   *Tables:* Top 10 High-Value Pending Deals, Regions by NPA Rate.
    *   *Filters:* Date Range, Region, Sector, Credit Limit Tier.
*   **AI Panels:** *AI Executive Assistant Panel:* Displays daily bulleted summaries of portfolio growth, major risk warnings, and actionable recommendations.
*   **Alerts:** Red banner for critical breach of regulatory limit in any industry sector.
*   **KPIs Displayed:** GNPA (%), NIM (%), Cost-to-Income (%), Disbursed Value.
*   **Reports Available:** Executive Board deck monthly report.
*   **Export Options:** PDF, PowerPoint, Looker Raw Data (CSV).
*   **Business Rules:** Data refreshed once daily at 00:00 hours; PII fully masked.
*   **Security Level:** L5 (Executive Only).
*   **Responsive Behaviour:** Grid collapses to single column on mobile, dashboards simplified to key metric cards.
*   **Dependencies:** Core Banking System (CBS), Financial Data Platform (AAR-DPS-024).

---

##### Screen ID: AAR-SCR-EXE-002
*   **Screen Name:** Portfolio Concentration & Yield Analytics
*   **Business Purpose:** Drill down into portfolio yields, interest rate splits, and risk segments.
*   **Primary Users:** Chief Risk Officer, Treasury Head.
*   **Navigation Path:** `Home -> Executive Dashboard -> Yield Analytics`
*   **Widgets:** Yield Heatmap (Interactive Map), Credit Rating Migration Matrix (Sankey Diagram).
*   **AI Panels:** *AI Portfolio Advisor:* Suggests portfolio rebalancing limits based on macroeconomic factors.
*   **Export Options:** Excel, Looker Studio.
*   **Security Level:** L5.

---

#### Dialogs, Reports, & Dashboards
*   **Dialogs:** *Rebalance Sector Limit:* Prompts executive to input new caps for high-risk sectors (e.g., real estate).
*   **Reports:** *Portfolio Health Executive Summary:* PDF report detailing monthly NPA progression.
*   **Dashboards:** Looker-integrated strategic dashboard mapping regional credit performance.

---

### 3.2 Relationship Manager Portal

#### Module Overview
A mobile-first dashboard built to assist Relationship Managers (RMs) in managing their customer leads, initiating credit requests, tracking documents, and resolving EWS alerts.

*   **Business Purpose:** Drive lead conversion, streamline customer onboarding, and monitor local portfolios.
*   **Target Users:** Relationship Managers, Branch Managers.
*   **Navigation Structure:** Pipeline -> Lead Detail -> Document Checklist -> EWS Alerts -> Client Communication.

---

#### Primary Screens

##### Screen ID: AAR-SCR-RM-001
*   **Screen Name:** RM Active Sales Pipeline & Activity Hub
*   **Business Purpose:** Track leads from discovery to disbursement and display daily tasks.
*   **Primary Users:** Relationship Managers.
*   **Business Process Supported:** Lead management, credit onboarding.
*   **Navigation Path:** `Home -> RM Portal -> Lead Pipeline`
*   **Entry Conditions:** RM User Session Authorized.
*   **Exit Conditions:** Click on Lead Details, Logout.
*   **Widgets:**
    *   *Kanban Board:* Visual columns (Lead, Consent Requested, Spreading, Underwriting, Approved, Disbursed).
    *   *Activity Panel:* Calendar checklist for site visits and document collection.
*   **AI Panels:** *AI Business Coach:* Highlights which leads are at risk of dropout and drafts outreach emails.
*   **Alerts:** Amber warnings for leads with pending consent expirations.
*   **KPIs Displayed:** Pipeline Conversion Rate (%), Pipeline Valuation (₹ Cr), Avg. Time-in-Stage.
*   **Export Options:** CSV, PDF.
*   **Business Rules:** RMs can only view leads assigned to their branch or region.
*   **Security Level:** L2 (Branch & Sales staff).
*   **Responsive Behaviour:** Bottom sheet panel for quick lead registration on mobile; full Kanban on desktop.
*   **Dependencies:** Customer Onboarding Engine, AA Consent Manager.

---

##### Screen ID: AAR-SCR-RM-002
*   **Screen Name:** Customer Onboarding & Consent Center
*   **Business Purpose:** Request consent via Account Aggregator, GSTIN, and CKYC.
*   **Primary Users:** Relationship Managers.
*   **Navigation Path:** `Home -> Lead Details -> Onboarding Portal`
*   **Widgets:** Data integration cards (AA Status, GST Verification, Bureau Status), Document Uploader.
*   **AI Panels:** *Gemini Doc Parser Panel:* Auto-fills form details from uploaded PDFs.
*   **Security Level:** L2.

---

#### Dialogs, Reports, & Dashboards
*   **Dialogs:** *Trigger AA Consent Request:* Input mobile number, choose AA, select data range (12 months), and trigger request.
*   **Reports:** *Weekly Sales Funnel Performance:* PDF summary of lead closures.
*   **Dashboards:** Lead TAT Tracker mapping bottlenecks.

---

### 3.3 Branch Operations

#### Module Overview
Provides branch staff with tools to verify physical security collaterals, validate KYC face-to-face, and handle loan disbursement exceptions.

*   **Business Purpose:** Bridge physical and digital operations, verify compliance, and manage local customer service.
*   **Target Users:** Branch Managers, Customer Service Representatives, Officers.
*   **Navigation Structure:** Queue Manager -> Document Verification -> Collateral Audit -> Branch Performance.

---

#### Primary Screens

##### Screen ID: AAR-SCR-OPS-001
*   **Screen Name:** Branch Operations Queue & Task Manager
*   **Business Purpose:** Manage and assign incoming tasks for verification, KYC overrides, and disbursements.
*   **Primary Users:** Branch Managers, Operations Officers.
*   **Navigation Path:** `Home -> Branch Ops -> Queue Manager`
*   **Widgets:**
    *   *Task Queue Grid:* Sortable by SLA Remaining, Task Type (KYC, Verification, Disbursal).
    *   *Task Detail Sidebar:* Quick overview of selected case documents.
*   **AI Panels:** *AI Queue Router:* Highlights potential bottleneck queues and automatically suggests resource reallocation.
*   **KPIs Displayed:** Branch SLA Compliance (%), Pending Tasks count, Average queue wait time.
*   **Security Level:** L2.
*   **Responsive Behaviour:** High-density desktop view, task checklist view for mobile tablets.

---

### 3.4 Credit Analyst Portal

#### Module Overview
The main analytical workspace for Credit Underwriters, allowing them to spread statements, calculate debt service ratios, adjust risk models, and generate Credit Assessment Memos (CAMs).

*   **Business Purpose:** Rigorous credit assessment, cash-flow spreading, risk scoring, and credit memo drafting.
*   **Target Users:** Credit Analysts, Underwriters, Credit Managers.
*   **Navigation Structure:** Underwriting Queue -> Financial Health Spreading -> Policy Exceptions -> CAM Compilation.

---

#### Primary Screens

##### Screen ID: AAR-SCR-CRE-001
*   **Screen Name:** Financial Health Spreading Sheet
*   **Business Purpose:** Parse and review bank statements, GST, and tax documents, adjusting calculations manually where needed.
*   **Primary Users:** Credit Analyst.
*   **Business Process Supported:** Financial Analysis, Ratio Spreading, Credit Scoring.
*   **Navigation Path:** `Home -> Underwriting Queue -> Case File -> Financial Spreading`
*   **Entry Conditions:** Case assigned, Lock active.
*   **Widgets:**
    *   *Spreading Grid:* Interactive multi-year balance sheet, P&L, Cash Flow spreadsheet.
    *   *Banking ledger chart:* Displays monthly inflows vs outflows, average credit balance.
*   **AI Panels:** *AI Credit Advisor Panel:* Computes alternative DSCR, identifies round-tripping bank transactions, and highlights anomalies.
*   **Alerts:** Warning banner for tax defaults, GST filing inconsistencies.
*   **KPIs Displayed:** DSCR, Debt-to-Equity, GST-to-Bank Inflow variance (%), Alt-DSCR.
*   **Export Options:** Excel Spreading Template, PDF.
*   **Security Level:** L3 (Underwriting Staff).
*   **Responsive Behaviour:** Desktop only. Screen requires high horizontal width (minimum 1280px) for multi-column spreadsheet layout.
*   **Dependencies:** Financial Data Engine, Bureau APIs, GSTN Gateway.

---

##### Screen ID: AAR-SCR-CRE-002
*   **Screen Name:** CAM Generation & Policy Verification
*   **Business Purpose:** Review automated credit assessment memos and exceptions.
*   **Primary Users:** Credit Analyst, Underwriter.
*   **Navigation Path:** `Home -> Underwriting Queue -> Case File -> CAM Generator`
*   **Widgets:** Policy Check Grid (shows Met/Not Met indicators), Rich-text CAM Editor.
*   **AI Panels:** *Gemini CAM Writer:* Drafts qualitative sections (industry analysis, promoter background) using customer data.
*   **Security Level:** L3.

---

#### Dialogs, Reports, & Dashboards
*   **Dialogs:** *Override Policy Exceptions:* Text prompt to document business justification for exceptions.
*   **Reports:** *Credit Assessment Memo (CAM):* Complete PDF document with balance sheet, scores, and recommendations.

---

### 3.5 Credit Committee Portal

#### Module Overview
A collaborative portal optimized for tablet and large-screen display, designed for voting members of the Credit Committee to review, debate, and approve high-value loan proposals.

*   **Business Purpose:** Collaborative credit decisioning, risk sign-off, and pricing approvals.
*   **Target Users:** Committee Members, Credit Directors, Risk Officers.
*   **Navigation Structure:** Active Committee Agenda -> Case Presentation -> Voting Panel.

---

#### Primary Screens

##### Screen ID: AAR-SCR-COM-001
*   **Screen Name:** Committee Decision Dashboard & Presentation Deck
*   **Business Purpose:** Present loan proposals with summary points, risk rating, and pricing margins for voting.
*   **Primary Users:** Committee Members, President.
*   **Navigation Path:** `Home -> Committee Portal -> Agenda -> Present Case`
*   **Widgets:**
    *   *Deal Overview Panel:* Borrower details, requested limit, pricing margin, key risk factors.
    *   *Financial Summary Grid:* High-level ratios, banking summary.
    *   *Voting Console:* Approve, Reject, Defer (with comment fields).
*   **AI Panels:** *AI Explainability Panel:* Natural-language summary of reasons for approval/rejection recommendation, highlighting risks.
*   **KPIs Displayed:** Loan Amount, Rating, Expected Loss (%), Proposed ROI (%).
*   **Security Level:** L4 (Management / Directors).
*   **Responsive Behaviour:** Optimized for tablet (landscape) with collapsible sidebar panels.

---

### 3.6 Risk Management Portal

#### Module Overview
A risk analytics dashboard designed for portfolio risk managers to monitor risk ratings, manage credit limits, track early warning indicators, and update scoring criteria.

*   **Business Purpose:** Systemic risk mitigation, portfolio health check, scoring model updates.
*   **Target Users:** Risk Officers, Portfolio Managers.
*   **Navigation Structure:** Risk Overview -> EWS Console -> Scorecard Modeler.

---

#### Primary Screens

##### Screen ID: AAR-SCR-RSK-001
*   **Screen Name:** Early Warning System (EWS) Console
*   **Business Purpose:** Track accounts showing risk signals (e.g., lower balances, bouncing cheques, poor sales).
*   **Primary Users:** Risk Officer, RM.
*   **Navigation Path:** `Home -> Risk Portal -> EWS Console`
*   **Widgets:**
    *   *Alert Table:* List of alerts categorized by severity (Red, Amber, Green).
    *   *Alert Detail Panel:* Explains the trigger metric (e.g., GST filings down 30% YoY).
*   **AI Panels:** *AI Risk Advisor:* Predicts probability of default (PD) progression and suggests actions (e.g., freeze drawing power).
*   **KPIs Displayed:** Weighted Average Score, High Risk Accounts count, Portfolio at Risk (PAR %).
*   **Security Level:** L3.

---

### 3.7 Compliance Portal

#### Module Overview
Monitors platform operations for compliance with AML (Anti-Money Laundering), KYC regulations, priority sector lending (PSL) rules, and internal policy frameworks.

*   **Business Purpose:** Ensure regulatory compliance, monitor audit logs, track PSL targets.
*   **Target Users:** Compliance Officer, Internal Auditor.
*   **Navigation Structure:** Compliance Queue -> PSL Dashboard -> Audit Trails.

---

#### Primary Screens

##### Screen ID: AAR-SCR-CMP-001
*   **Screen Name:** Compliance Verification & Audit Trail
*   **Business Purpose:** Verify client background hits, resolve AML warnings, and confirm regulatory validations.
*   **Primary Users:** Compliance Officer.
*   **Navigation Path:** `Home -> Compliance Portal -> Queue`
*   **Widgets:** PEP/Sanctions Matches Grid, Audit Log Tracker.
*   **AI Panels:** *AI Explainability Panel:* Shows reasons behind flagging (e.g., matches in global databases).
*   **Security Level:** L3.

---

### 3.8 Portfolio Monitoring Portal

#### Module Overview
A post-disbursement tracking tool to manage accounts, monitor loan covenants, assess collateral valuations, and identify early warning signals.

*   **Business Purpose:** Post-disbursement credit hygiene, covenant compliance tracking.
*   **Target Users:** Portfolio Monitoring Officer, Credit Analyst, RM.
*   **Navigation Structure:** Active Portfolio -> Covenant Dashboard -> Revaluation Portal.

---

#### Primary Screens

##### Screen ID: AAR-SCR-PTM-001
*   **Screen Name:** Covenant Monitoring & Verification Portal
*   **Business Purpose:** Monitor whether borrowers are adhering to financial and operational covenants (e.g., maintaining a DSCR > 1.25).
*   **Primary Users:** Portfolio Officer.
*   **Navigation Path:** `Home -> Portfolio Monitoring -> Covenants`
*   **Widgets:** Covenant Status Grid (Met/Breached), Financial Ratio Trends.
*   **AI Panels:** *AI Portfolio Advisor:* Flags accounts likely to breach covenants in the next quarter.
*   **Security Level:** L3.

---

### 3.9 Collections Portal

#### Module Overview
Provides collections agents with automated prioritization queues, dynamic agent scripts, payment arrangement tools, and escalation paths.

*   **Business Purpose:** Maximize debt recovery, prioritize collections lists, schedule settlements.
*   **Target Users:** Collections Agents, Collections Managers.
*   **Navigation Structure:** Calling Queue -> Account Overview -> Payment Gateway -> Settlements.

---

#### Primary Screens

##### Screen ID: AAR-SCR-COL-001
*   **Screen Name:** Smart Calling Queue & Collector Cockpit
*   **Business Purpose:** Display priority contact accounts based on likelihood of recovery and severity of delinquency.
*   **Primary Users:** Collections Agents.
*   **Navigation Path:** `Home -> Collections -> Calling Queue`
*   **Widgets:**
    *   *Delinquent Account Grid:* Name, Overdue days, Outstanding amount, Last Contact.
    *   *Action Workspace:* Call logging panel, payment link generator.
*   **AI Panels:** *AI Chat Assistant / Advisor:* Recommends payment settlement plans and updates talking scripts dynamically.
*   **Security Level:** L2.

---

### 3.10 MSME Customer Portal

#### Module Overview
A customer-facing portal designed for mobile and web, enabling MSME borrowers to apply for loans, submit documents, check limits, and execute drawdowns.

*   **Business Purpose:** Deliver a self-service onboarding, limit tracking, and drawing power drawdown experience.
*   **Target Users:** MSME Owners, Partners, Finance Managers.
*   **Navigation Structure:** Customer Dashboard -> Loan Status Tracker -> Drawing Power Calculator -> Disbursal Setup.

---

#### Primary Screens

##### Screen ID: AAR-SCR-MSM-001
*   **Screen Name:** MSME Customer Dashboard (Mobile & Web)
*   **Business Purpose:** The landing page for borrowers, showcasing credit health, current limits, and options to drawdown funds.
*   **Primary Users:** MSME Owners.
*   **Navigation Path:** `Login -> Customer Portal -> Home`
*   **Entry Conditions:** Customer Session Authorized, OTP validated.
*   **Widgets:**
    *   *Drawing Power Dial:* Shows available cash limit visually.
    *   *Pending Tasks Card:* Highlights missing documents (e.g., current GST invoice).
    *   *Drawdown Panel:* Input field to transfer funds to current account.
*   **AI Panels:** *AI Business Coach Widget:* Suggests cash flow improvements and lists buyers offering early payments.
*   **KPIs Displayed:** Available Limit, Outstanding Amount, Next Payment Date.
*   **Export Options:** Loan Statement (PDF), Interest Certificate.
*   **Security Level:** L1 (Customer Level).
*   **Responsive Behaviour:** Mobile-first design, featuring touch gestures for drawers and simple navigation buttons.

---

### 3.11 Partner Portal

#### Module Overview
Enables external stakeholders (Chartered Accountants, Direct Sales Agents, Fintech channel partners) to submit leads and track status transparently.

*   **Business Purpose:** Expand loan distribution channels, capture clean lead data.
*   **Target Users:** DSAs, Partner Agents, Chartered Accountants.
*   **Navigation Structure:** Partner Dashboard -> Lead Submission -> Commission Statement.

---

#### Primary Screens

##### Screen ID: AAR-SCR-PRT-001
*   **Screen Name:** Partner Lead Upload & Status Tracker
*   **Business Purpose:** Allow partners to register leads and track processing milestones without revealing sensitive credit details.
*   **Primary Users:** Partner Agents.
*   **Navigation Path:** `Home -> Partner Portal -> Submit Lead`
*   **Widgets:** Lead registration form, Status tracker list.
*   **Security Level:** L2.

---

### 3.12 Admin Portal

#### Module Overview
Provides product managers and operations directors with tools to manage workflows, update credit policies, configure fees, and define interest rates.

*   **Business Purpose:** System configurations, policy steering, workflow administration.
*   **Target Users:** Product Managers, System Admins.
*   **Navigation Structure:** Policy Manager -> Fee Configurator -> User Management.

---

#### Primary Screens

##### Screen ID: AAR-SCR-ADM-001
*   **Screen Name:** Policy Configurator & Credit Rules Matrix
*   **Business Purpose:** Configure automated credit rules (e.g., minimum DSCR = 1.25) without database code changes.
*   **Primary Users:** Product Managers.
*   **Navigation Path:** `Home -> Admin Portal -> Policy Manager`
*   **Widgets:** Rules Matrix Table, Value adjustment sliders, Save/Publish controls.
*   **Security Level:** L4.

---

### 3.13 AI Operations Console

#### Module Overview
Allows AI administrators and data scientists to monitor model outputs, inspect LLM call histories, track prompt versions, and verify explainability mappings.

*   **Business Purpose:** AI governance, model safety, explanation verification.
*   **Target Users:** AI Engineers, Model Valuers.
*   **Navigation Structure:** Model Health -> Prompt Manager -> Explainability Review.

---

#### Primary Screens

##### Screen ID: AAR-SCR-AIO-001
*   **Screen Name:** Prompt Versioning & LLM Latency Analytics
*   **Business Purpose:** Manage prompt configurations for Gemini templates (CAM parser, client emailer) and view API latency.
*   **Primary Users:** AI Operations Engineers.
*   **Navigation Path:** `Home -> AI Ops -> Prompt Manager`
*   **Widgets:** Prompt Code Editor, Latency Trend charts, Token Cost tracker.
*   **AI Panels:** *AI Explainability Inspector:* Traces generation outputs to validation datasets.
*   **Security Level:** L4.

---

### 3.14 System Administration Portal

#### Module Overview
Provides IT and database administrators with user management, system health metrics, API logs, and database access settings.

*   **Business Purpose:** IT operations, user access provisioning, security configuration.
*   **Target Users:** System Administrators, Security Engineers.
*   **Navigation Structure:** User Access -> Audit Logs -> System Health -> Integrations.

---

#### Primary Screens

##### Screen ID: AAR-SCR-SYS-001
*   **Screen Name:** IAM Role Provisioner & Security Configurator
*   **Business Purpose:** Manage role assignments, set field-masking criteria, and inspect security access logs.
*   **Primary Users:** System Administrators.
*   **Navigation Path:** `Home -> System Admin -> IAM Provisioner`
*   **Widgets:** User list, Role matrix table, Masking rule check grid.
*   **Security Level:** L5.

---

## Enterprise Report Catalogue

The table below catalogs reports across modules, specifying the export formats, generation schedules, and target users.

| Report ID | Report Name | Domain | Primary Target | Schedule | Export Formats |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AAR-REP-001** | Executive Board Review Deck | Executive | CIO, CBO, CEO | Monthly | PDF, PPTX |
| **AAR-REP-002** | Portfolio Credit Risk Distribution | Risk | Chief Risk Officer | Weekly | XLSX, PDF |
| **AAR-REP-003** | Credit Assessment Memo (CAM) | Credit Analyst | Underwriters | On-Demand | PDF, DOCX |
| **AAR-REP-004** | Early Warning Alert Summary | Portfolio Monitoring | Risk, RMs | Daily | CSV, PDF |
| **AAR-REP-005** | Priority Sector Lending (PSL) Report | Compliance | Compliance Officer | Monthly | XML, XLSX |
| **AAR-REP-006** | Lead Stage Conversion Report | RM Portal | Sales Management | Weekly | CSV, Looker Link |
| **AAR-REP-007** | Interest Certificate & Tax Statements | MSME | Customer | Annual | PDF |
| **AAR-REP-008** | Operations SLA & TAT Report | Operations | Ops Director | Daily | CSV, Looker Link |
| **AAR-REP-009** | Platform System Audit Trail | Audit | Regulators, Audit | On-Demand | JSON, PDF |
| **AAR-REP-010** | GenAI Output & Explanation Logs | AI Operations | AI Engineers | Weekly | JSON, CSV |

---

## AI Interaction & Conversation Standards

The platform implements seven key AI Assistants and Advisors. This section defines their behavior, UI interfaces, and visual indicators.

```
+----------------------------------------------------------------+
| [Gemini Icon] AI Risk Advisor                                  |
+----------------------------------------------------------------+
| "Based on 12 months bank statements, borrower sales decreased   |
| 15% in Q4. This triggers rule RSK-03."                         |
|                                                                |
| Source Documentation References:                                |
| [1] GSTN_Register_Dec2025.pdf (Line 142)                       |
| [2] IDBI_Credit_Policy_v3.pdf (Section 4.1)                    |
+----------------------------------------------------------------+
| Action: [Re-run Rating]   [Freeze Drawing Power]   [Ignore]    |
+----------------------------------------------------------------+
```

### 1. AI Business Coach
*   **Module Placement:** MSME Customer Portal, Partner Portal.
*   **UI Layout:** Collapsible bottom-sheet widget with card suggestions.
*   **Behavioral Pattern:** Provides advice on managing cash flows, lists suppliers offering terms, and suggests invoice finance opportunities.

### 2. AI Credit Advisor
*   **Module Placement:** Credit Analyst Portal.
*   **UI Layout:** Persistent right-hand sliding panel next to financial statements.
*   **Behavioral Pattern:** Flags suspicious circular entries, estimates debt repayment limits, and auto-fills spreading spreadsheets.

### 3. AI Portfolio Advisor
*   **Module Placement:** Portfolio Monitoring Portal.
*   **UI Layout:** Dynamic banner warnings on top of portfolio grids.
*   **Behavioral Pattern:** Recommends rebalancing industry sector allocations based on market alerts.

### 4. AI Risk Advisor
*   **Module Placement:** Risk Management Portal, Executive Portal.
*   **UI Layout:** Floating sidebar widget next to EWS logs.
*   **Behavioral Pattern:** Analyzes transaction patterns, predicts payment delays, and recommends adjustments to account limits.

### 5. AI Explainability
*   **Module Placement:** Across all employee screens displaying AI decisions.
*   **UI Layout:** Modal popup triggered via an info icon button next to AI indicators.
*   **Behavioral Pattern:** Displays clear citations referencing client files or policy manuals to justify AI outputs.

### 6. AI Chat Assistant
*   **Module Placement:** Universal interface (RM Workspace, MSME Portal).
*   **UI Layout:** Persistent floating chat circle button at the bottom-right corner.
*   **Behavioral Pattern:** Handles queries, guides users through forms, and links to relevant support documents.

### 7. AI Executive Assistant
*   **Module Placement:** Executive Portal.
*   **UI Layout:** Top section on the main dashboard.
*   **Behavioral Pattern:** Outlines platform metrics, flags exceptions, and provides key operational takeaways.

---

## Platform Device Matrix & Responsive Standards

| Module | Desktop Layout (min 1280px) | Tablet Layout (min 768px) | Mobile Layout (min 360px) | Input Priority |
| :--- | :--- | :--- | :--- | :--- |
| **Executive** | Looker Dashboards, Multi-grid | Summarized KPI Cards | KPI Alerts, Basic Read | Tap, Voice |
| **RM Portal** | Full Pipeline Kanban, CRM | Grid-list view of leads | Pipeline list, Call logger | Tap, Voice |
| **Branch Ops** | High-density Queue tables | Split-screen checklist | Barcode scanner, KYC upload | Touch, Camera |
| **Credit Analyst**| Spreadsheets, Double-screen | *Not Recommended* | *Not Supported* | Keyboard, Mouse |
| **MSME Portal** | Multi-step Form Wizard | Flex-grid layout | Single-column form, touch | Keyboard, Touch |

---

## Governance & Security Standards

### 1. Persona Security Levels
*   **L1 (Customer Level):** Users can only access their own details. No internal data visible.
*   **L2 (Sales & Operations):** RMs and Branch Staff see assigned customer profiles. Key PII (Tax IDs, personal address) masked.
*   **L3 (Analyst & Operations Officer):** Full access to client financial metrics. PII visible for credit assessment.
*   **L4 (Management / Product Admin):** System-wide summaries, policy configurations. No client PII visible.
*   **L5 (System Admin / Executive):** Strategic dashboard metrics. System admin has complete database controls.

### 2. General Security Controls
*   **Session Timeout:** L1: 15 minutes; L2-L5: 10 minutes.
*   **Multi-Factor Authentication (MFA):** Mandatory for all admin (L4, L5) actions.
*   **Data Encryption:** All client-identifiable data must be masked in compliance with RBI privacy standards.

---

**Approved & Signed By:**  
*Chief Product Experience Architect, Project AAROHAN*  
*Director, Google Cloud Professional Services*  
*Head, Digital Transformation Office (DTO), IDBI Bank*
