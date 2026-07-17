# Project AAROHAN Enterprise Simulation Engine (ESE) / Enterprise Digital Banking Twin
## AAR-ESE-009: Sprint 3 Planning Document

**Sprint Duration:** July 23, 2026 – August 5, 2026  
**Velocity:** 42 Story Points  
**Approved By:** Agile Product Delivery Team (Product Owner, Scrum Master, Architects)  

---

### 1. Executive Summary
Following the successful completion of Sprint 2, which transformed the Enterprise Simulation Engine (ESE) into a Living Digital Banking Twin with macroeconomic causal logic and regional banking behaviors, Sprint 3 is designed to focus on **Executive Enablement, Scenario Comparison, and Training Platform Delivery**.

Sprint 3 will deliver a world-class Executive Demo Console, interactive analytic dashboards, side-by-side scenario comparisons, downloadable compliance reports (PDF/Excel), natural language AI presentation assistants, instructor-led training modes, and custom branding profiles. This allows relationship managers, credit officers, and executives to use the twin as a high-fidelity presentation platform for board meetings, committee reviews, and hackathons.

---

### 2. Sprint Goal
Deliver an enterprise-grade Executive Demonstration & Training Console enabling presenters to run interactive, branded simulations, compare scenario portfolios side-by-side, generate downloadable compliance reports, and explain credit decisions in natural language.

---

### 3. Sprint Scope
The Sprint 3 scope is organized into seven functional pillars:
1.  **Executive Demo Console**: Presenter dashboard, guided step-by-step walkthroughs, and scriptable demo launchers.
2.  **Interactive Dashboards**: Portfolio KPIs, drill-downs, sector comparisons, risk heatmaps, and OCEN analytics.
3.  **Scenario Comparison Engine**: Side-by-side delta reporting (e.g. Clean vs Fraud, PSB vs NBFC, Excellent vs Stressed).
4.  **Multi-Format Report Generator**: Downloadable PDFs, Excel ledgers, and Markdown files for FHC, CAM, and Risk assessments.
5.  **AI Presentation Assistant**: LLM-driven natural language summaries explaining credit decisions and portfolio health indicators.
6.  **Training & Demonstration Mode**: Pause/Resume controls, step-through timelines, and event highlighting.
7.  **Demo Branding Engine**: Custom themes, bank logo injections, and event branding profiles (e.g. IDBI Board, Hackathon).

---

### 4. Selected Epics
*   **EPIC-ESE-008: Executive Demo Console & Presenter UX**
*   **EPIC-ESE-009: Scenario Comparison & Analysis Engine**
*   **EPIC-ESE-010: Enterprise Reporting & Multi-Format Exporter**
*   **EPIC-ESE-011: Conversational AI Presentation Assistant**
*   **EPIC-ESE-012: Training Mode & Interactive Timeline Control**

---

### 5. Selected Features
*   **FEAT-ESE-301: Guided Walkthrough Presenter UI Console**
*   **FEAT-ESE-302: Drill-down Portfolio Dashboard & Risk Heatmap**
*   **FEAT-ESE-303: Side-by-Side Underwriting Scenario Comparator**
*   **FEAT-ESE-304: PDF/Excel FHC & CAM Report Engine**
*   **FEAT-ESE-305: Conversational Gemini Credit Advisor & explainer**
*   **FEAT-ESE-306: Timeline Step-Through & Pause/Resume Controller**
*   **FEAT-ESE-307: Dynamic White-label Branding & Custom Theme Injector**

---

### 6. User Stories & Story Points

| ID | Title | Story Points | Description |
| :--- | :--- | :--- | :--- |
| **US-ESE-S3-001** | **Executive Presenter Console** | 8 SP | Implement the frontend Presenter Console UI with guided tour scripts, launch triggers, and navigation. |
| **US-ESE-S3-002** | **Drill-down Analytics & Heatmap** | 6 SP | Implement interactive UI widgets for portfolio aggregates, sector comparisons, and geographic risk heatmaps. |
| **US-ESE-S3-003** | **Scenario Comparator Engine** | 6 SP | Implement side-by-side comparison logic and delta displays for borrowers, lenders, and risk states. |
| **US-ESE-S3-004** | **PDF/Excel Report Exporter** | 7 SP | Code templates to generate downloadable PDF/Excel files for FHC, CAM, and Assessment summaries. |
| **US-ESE-S3-005** | **Conversational Gemini Assistant** | 6 SP | Integrate dynamic mock LLM interfaces providing conversational credit advice and risk factor evaluations. |
| **US-ESE-S3-006** | **Timeline Tick & Step-Through** | 5 SP | Implement timeline controls (Pause, Resume, Back, Next Step) linked to the simulation clock. |
| **US-ESE-S3-007** | **Dynamic Theme Customizer** | 4 SP | Build branding handlers to swap themes, logos, and color palettes on-the-fly (e.g. IDBI, Hackathon). |

**Total Sprint 3 Scope: 42 Story Points**

---

### 7. Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Report Generation Overhead** | Medium | Medium | Implement asynchronous task queues (e.g. Celery or lightweight threads) for PDF compile routines. |
| **UI State Desynchronization** | High | Low | Establish WebSocket connections in `ese-admin-service` to push simulation clock ticks to the UI in real-time. |
| **Theme Cache Latency** | Low | Medium | Store brand configurations in lightweight local storage or memory maps for zero-latency DOM re-rendering. |

---

### 8. Dependencies
*   **Sprint 2 Core Engines**: Dependent on the simulation clock, causal engines, and event structures completed in Sprint 2.
*   **Browser Compatibility**: PDF and UI rendering libraries must run seamlessly across standard enterprise browsers without external script calls.

---

### 9. Deliverables
1.  **Admin Presenter Console**: React/HTML frontend workspace under `apps/ese-console/` or admin modules.
2.  **Report Engine Service**: Updated routes in `ese-core` and libraries mapping PDF/Excel compilation.
3.  **Comparison Routers**: Comparison API endpoints in `ese-admin-service` to compute delta profiles.
4.  **Timeline Socket Service**: WebSocket broadcaster pushing simulated dates and events.
5.  **Branding Registry**: JSON assets directory supporting brand overrides and static files.

---

### 10. Definition of Done (DoD)
*   All frontend components comply with modern, premium UX/UI guidelines.
*   Unit tests cover at least 90% of comparison and report compilation engines.
*   All endpoints are registered with OpenAPI/Swagger.
*   Exported PDF/Excel files are verified for validation formatting.
*   Web layout is fully responsive and presentation-ready.

---

### 11. Sprint KPIs
*   **PDF Compile Speed**: Under 2.0 seconds.
*   **Branding Switch Time**: Under 100ms.
*   **Dashboard Aggregation Latency**: p95 under 100ms.

---

### 12. Demo Success Criteria
*   The presenter can switch the active brand from "Standard Theme" to "IDBI Bank" in one click.
*   Side-by-side comparison of Priya Textile (Healthy) vs Priya Textile (Stressed) renders delta columns instantly.
*   The presenter can download a generated FHC PDF card.
*   The AI Assistant panel answers conversational queries about sector risks in real time.

---

### 13. Expected Business Value
Sprint 3 moves ESE from a developer tool to a fully packaged corporate presentation asset. It enables leadership to showcase IDBI's digital lending vision during high-profile board meetings, customer engagements, and hackathons, accelerating product validation and approval cycles.

---

### 14. Executive Presentation Objectives
- **Wow Factor**: High-fidelity dark mode visual designs, glassmorphic card widgets, and micro-interactions.
- **Explainability**: Clear visual flow detailing why loans are approved or rejected.
- **Repeatability**: Ensure every demo journey executes identically in any presentation environment.
