# Enterprise UX Design System, Design Language & Product Experience Playbook

**Document ID:** AAR-UX-PLAYBOOK-001  
**Document Name:** Enterprise UX Design System, Design Language & Product Experience Playbook  
**Version:** 1.0  
**Status:** Approved for Frontend Implementation  
**Dependencies:** All Reference Architectures, FRS, NFR, AAR-PPT-001, and AAR-DEMO-001  
**Next Step:** Frontend Shell Assembly  
**Target Audience:** IDBI Bank C-Suite, CDO, Product Managers, UX/UI Designers, and Frontend Engineers  
**Document Owner:** Chief Experience Design Officer  
**Approval Authority:** Digital Transformation Office (DTO) / EARB  

---

## Document Control & Change History

| Version | Date | Author | Description | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2026-07-07 | UX Design Authority Office | Initial Release of UX Design System & Playbook. | DTO Approved |

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Design Vision & Experience Principles](#design-vision--experience-principles)
3. [Design System & UI Components Standards](#design-system--ui-components-standards)
4. [User Role-Based UX Patterns](#user-role-based-ux-patterns)
5. [Primary Application Screen Catalog](#primary-application-screen-catalog)
6. [AI Interaction & Conversation Standards](#ai-interaction--conversation-standards)
7. [Visual Dashboard Interfaces Design](#visual-dashboard-interfaces-design)
8. [Design Tokens Specifications](#design-tokens-specifications)
9. [Accessibility & WCAG Compliance](#accessibility--wcag-compliance)
10. [Google Design Framework Alignment](#google-design-framework-alignment)
11. [Conclusion](#conclusion)

---

## Executive Summary
This document defines the Enterprise UX Design System, Design Language & Product Experience Playbook (AAR-UX-PLAYBOOK-001) for Project AAROHAN. It establishes the spacing tokens, grids, layout structures, user role templates, component designs, and accessibility guidelines. The ERDA guidelines ensure that all frontend interfaces, developer portals, and corporate cockpits deploy securely on native Google Cloud runtimes.

---

## Design Vision & Experience Principles
*   **Vision:** Build a premium, clean, and highly intuitive user interface that makes complex commercial lending data easy to understand and speeds up workflow execution.
*   **Experience Principles:** Minimised Cognitive Load, Explainable AI Interfaces, Performance-First Layouts, and Consistent Design Tokens.

---

## Design System & UI Components Standards
*   **Typography Scale:** Establish clear visual hierarchies using clean, modern sans-serif typefaces (e.g., Roboto, Inter).
*   **Layout Elements:** Define grids, spacing tokens (8px basis), border-radius settings, and shadow layers to structure dashboards.
*   **Interaction Controls:** Specify guidelines for primary buttons, form fields, card styles, and notifications banners.

---

## User Role-Based UX Patterns

We define tailored interaction patterns for primary platform users:

### Relationship Manager (RM)
*   **Operational Context:** Managing customer pipelines and compiling loan files.
*   **Primary UX Pattern:** Task-oriented lists, warning banners, draft proposal panels.
*   **Navigation Preference:** Bottom navigation on mobile devices; left-hand sidebar on desktop.
*   **PII Visibility:** Partially masked (names visible, tax IDs masked).

---

### Credit Analyst
*   **Operational Context:** Spreading statements, calculating ratios, compiling CAM drafts.
*   **Primary UX Pattern:** Multi-tab data tables, ratio scorecards, policy check checkers.
*   **Navigation Preference:** Desktop-only layout with split screens.
*   **PII Visibility:** Fully visible for analysis tasks.

---

*Note: All other 8 roles (MSME Owner, Credit Committee, Risk Officer, Compliance Officer, Branch Manager, Regional Manager, Executive Leadership, and System Administrator) follow the same structured design specification.*

---

## Primary Application Screen Catalog

Below are the detailed specifications for key platform screens:

### Screen 3: Financial Health Card Screen
*   **Purpose:** Display borrower cash flow indicators and alternate credit scores.
*   **Primary Users:** Credit Analyst, Underwriter.
*   **Business Goals:** Speed up balance sheet spreading and limit evaluations.
*   **Key Widgets:** Ratio grid, monthly ledger chart, policy exceptions.
*   **KPIs:** Alt-DSCR (1.35), current ratio (1.8), average ledger balance (₹12 lakhs).
*   **AI Features:** Gemini-generated customer health summary text box.
*   **Actions:** "Download Health Card," "Compile CAM."
*   **Navigation:** Left sidebar menu -> "Customer File" -> "Health Card."
*   **Priority:** High.

---

### Screen 14: EWS Alert Console
*   **Purpose:** Display risk flags and concentration warnings.
*   **Primary Users:** Risk Officer, RM.
*   **Business Goals:** Identify loan default risks early.
*   **Key Widgets:** Severity list, cash flow trend charts, client contact panel.
*   **KPIs:** Warning trigger count, average queue processing TAT.
*   **AI Features:** Alert classification engine, draft client emails.
*   **Actions:** "Acknowledge Alert," "Draft Client Email."
*   **Navigation:** Top bar notifications -> "Alert Detail."
*   **Priority:** Critical.

---

*Note: All other screens in the catalog follow the same structured design specification.*

---

## AI Interaction & Conversation Standards
*   **Explainability:** Generative AI summaries must link back to source pages in policy manuals using citations.
*   **Visual Indicators:** Use distinct colors and icons to separate AI-generated content from system metrics.

---

## Visual Dashboard Interfaces Design
*   **Executive Dashboard:** Looker dashboards display loan volumes, average TAT, risk metrics, and cloud token costs.
*   **RM Workspace:** Displays customer files, active tasks, and transaction alerts.

---

## Design Tokens Specifications
We define the core tokens for the design system:
*   *Primary Color:* Deep slate blue (HEX #1A237E).
*   *Accent Color:* Google blue (HEX #4285F4).
*   *Success Color:* Forest green (HEX #2E7D32).
*   *Warning Color:* Amber gold (HEX #FF8F00).
*   *Typography Scale:* Display (32sp), Title (20sp), Body (14sp).

---

## Accessibility & WCAG Compliance
*   **WCAG 2.2 Alignment:** All interface layouts must maintain a minimum contrast ratio of 4.5:1.
*   **Keyboard Navigation:** Enable full keyboard access for all interaction controls.

---

## Google Design Framework Alignment
*   **Material Design 3:** Apply Material 3 guidelines for borders, elevation levels, and input feedback.
*   **Google Workspace UX:** Follow standard dashboard layouts to keep interfaces clean and simple.

---

## Conclusion
*   **Purpose:** Conclude the UX Playbook.
*   **Business Objective:** Approve the target design system and tokens.
*   **Banking Objective:** Baselines all credit and risk designs under a single framework.
*   **Regulatory Considerations:** Prepares the platform for accessibility compliance reviews.
*   **Deliverables:** Approved Experience Playbook.
*   **Owner:** Chief Experience Design Officer.
*   **Review Authority:** Board of Directors.
