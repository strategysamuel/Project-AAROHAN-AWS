# AAR-ESE-007: Project AAROHAN ESE Sprint 2 — Implementation Report

**Document Classification**: Engineering Handover Report  
**Sprint**: ESE Sprint 2 of 5  
**Version**: 1.0  
**Status**: 🟢 COMPLETED – READY FOR SPRINT 2 ENGINEERING REVIEW  
**Date**: July 8, 2026  
**Platform**: Project AAROHAN Enterprise Digital Banking Twin v3.0  

---

## 1. Executive Summary

This report documents the successful implementation of Sprint 2 for the **Enterprise Simulation Engine (ESE)**, transforming Project AAROHAN's testing framework into a fully functional **Living Digital Banking Twin**. 

The Digital Banking Twin now models realistic cause-and-effect relationships across the entire lending ecosystem:
- Economic drivers propagate downstream to influence financial indicators.
- Simulated events update ledgers, FHC metrics, credit recommendations, and lenders' offers automatically.
- All implementations maintain isolation from production networks and complete backward compatibility with Version 1.1 services.

---

## 2. Components Implemented

The following core modules were implemented in `services/ese-core/` and integrated into the `ese-admin-service` control center:
1.  **Business Event Engine**: Asynchronous event dispatching with cascading propagation.
2.  **Financial Causal Model**: Deterministic linkages between transactions, DSCR, FHC, and credit scores.
3.  **Macroeconomic Simulation Engine**: Dynamic variables affecting operational cash flow and default triggers.
4.  **Regional Banking Model**: Regional profiles adjusting GST compliance and risk behavior.
5.  **Banking Network Simulator**: Lender categories defining policy guidelines, SLA, and capital deployment.
6.  **Portfolio Evolution Engine**: Metrics showing outstanding portfolio volumes and NPA ratios.
7.  **Executive Replay Engine**: Step-by-step recording, events tracking, and replay summaries.

---

## 3. Business Event Engine

The **Business Event Engine (BEE)** implements a broker pattern allowing the dispatching of business events.
- **Event Schemas**: Standarized JSON events for filings, invoices, collections, salaries, fraud alerts, and EMI actions.
- **Cascade Propagation Loop**:
  `GST_RETURN_FILED` ➔ `TURNOVER_UPDATED` ➔ `CASH_FLOW_UPDATED` ➔ `FHC_RECALCULATED` ➔ `CREDIT_SCORE_UPDATED` ➔ `OCEN_ELIGIBILITY_UPDATED` ➔ `LOAN_OFFERS_REGENERATED` ➔ `EXEC_DASHBOARD_REFRESHED`

---

## 4. Financial Causal Model

The **Financial Causal Model (FCM)** establishes mathematical equations linking cash transactions to credit availability:
- **Revenue & Turnover**: $R_m = T_{gst, m} \cdot (1 - \delta_{underreport}) + C_{cash, m}$.
- **Operating Cash Flow**: $OCF_m = R_m - \text{COGS}_m - \text{OpEx}_m - T_{tax, m} - \Delta\text{NWC}_m$.
- **DSCR**: $DSCR = \frac{OCF_m + \text{InterestExpense}_m}{\text{PrincipalPaid}_m + \text{InterestExpense}_m}$.
- **FHC Score**: Weighted sum (30% Liquidity, 25% Profitability, 25% Leverage, 20% Debt Service).
- **AI Credit Score**: $CS = 300 + 600 \cdot \left[ 0.40 \cdot \left(\frac{\text{FHC}}{100}\right) + 0.30 \gamma_{repayment} + 0.15 \gamma_{gst\_consistency} - 0.15 \text{FraudFlag} \right]$.

---

## 5. Macroeconomic Simulation Engine

The **Macroeconomic Simulation Engine (MSE)** tracks six macroeconomic drivers:
- **RBI Repo Rate**: Directly affects interest charges and debt service coverage.
- **Inflation**: Triggers cost increases in COGS and OpEx, degrading profit margins.
- **Exchange Rate**: Depreciates or appreciates local currency volumes for export/import personas.
- **Fuel Prices & Commodity Prices**: Adjust cost of goods and logistics margins.
- **Monsoon Impact & Government Subsidies**: Adjust seasonal turnovers or apply interest rate relief.

---

## 6. Regional Banking Model

We configured six regional profiles defining regional characteristics:
- **Tamil Nadu**: High compliance, low risk, specialized in Textiles/Manufacturing.
- **Karnataka**: High compliance, low risk, specialized in Services/FinTech/Agro.
- **Maharashtra**: High compliance, low risk, specialized in Manufacturing/Logistics.
- **Gujarat**: Moderate compliance, moderate risk, specialized in Textiles/Chemicals.
- **Telangana**: Moderate compliance, moderate risk, specialized in Services/Logistics.
- **Kerala**: Moderate compliance, low risk, specialized in Tourism/Agro.

---

## 7. Banking Network Simulator

The **Banking Network Simulator (BNS)** models five lender categories with distinct policies:
- **Public Sector Bank**: conservative, min score $\ge 750$, rate 8.5%, SLA 15 days.
- **Private Bank**: moderate, min score $\ge 700$, rate 10.5%, SLA 3 days.
- **NBFC**: higher risk, min score $\ge 620$, rate 14.0%, SLA 1 day.
- **FinTech**: AI-driven, min score $\ge 580$, rate 16.0%, SLA real-time (<5 mins).
- **Cooperative Bank**: regional focus, min score $\ge 600$, rate 11.0%, SLA 5 days.

Lenders check capital allocation constraints and sector exposure concentration limits dynamically before issuing offers.

---

## 8. Portfolio Evolution Engine

This engine tracks portfolio metrics over time:
- **Portfolio Outstanding**: Aggregate capital deployed across all lenders.
- **NPA Ratio**: Tracking loans with missed EMIs $>90$ days.
- **Recovery Ratio**: Ratio of recovered capitals after defaults.
- **Exposure Segmentation**: Visualizes exposures by Sector, District, and State.

---

## 9. Executive Replay Engine

The **Executive Replay Engine (ERE)** adds recording and playback controls:
- **`POST /ese/control/replay/start`**: Begins recording.
- **`POST /ese/control/replay/stop`**: Halts recording, saving recorded steps, events, and portfolio snapshots.
- **`GET /ese/control/replay/{id}/export`**: Formats an executive summary of the journey.

---

## 10. AI Explainability

AI Credit Recommendations return a deterministic, compliance-aligned record:
- **Verdict & Reasons**: Specific financial factors (e.g. low DSCR, regulatory default).
- **Mitigants**: Suggested options to normalize risk (e.g. credit guarantees).
- **Appraisal Summary**: Brief description outlining loan viability.

---

## 11. Files Added

- [services/ese-core/event_engine.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/event_engine.py) (Business Event Engine)
- [services/ese-core/causal_model.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/causal_model.py) (Financial Causal Model)
- [services/ese-core/lenders.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/lenders.py) (Banking Simulator & Underwriting Policies)
- [services/ese-core/clock.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/clock.py) (Simulation Clock)
- [services/ese-core/replay_engine.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-core/replay_engine.py) (Executive Replay Engine)
- [tests/test_ese_sprint2_twin.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/tests/test_ese_sprint2_twin.py) (Unit tests for new engines)

---

## 12. Files Modified

- [services/ese-admin-service/app/main.py](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/services/ese-admin-service/app/main.py) (Registered Sprint 2 Control Center Routes)
- [pytest.ini](file:///d:/SAMUEL/HACK%202%20SKILL/IDBI%20MSME/Project%20AAROHAN/pytest.ini) (Added path dependencies for isolated service testing)

---

## 13. Test Results

All new unit tests and regression tests are passing:
- **Sprint 2 Twin Tests**: 5 passed (`pytest tests/test_ese_sprint2_twin.py`)
- **Digital Twin Tests**: 5 passed (`pytest tests/test_ese_digital_banking_twin.py`)
- **Regression E2E Tests**: 7 passed (`pytest tests/test_regression_e2e.py`)

---

## 14. Risks

- **Database Performance**: Ticking the simulation clock frequently under high concurrency might cause SQLite lock contentions.
  *Mitigation*: We configured WAL mode on SQLite connections to support concurrent reads and writes safely.

---

## 15. Technical Debt

- **AI Model Sophistication**: Causal calculations currently use deterministic heuristics mimicking AI risk grades. In Sprint 3, these will be replaced with direct LLM calls leveraging custom persona prompt contexts.

---

## 16. Sprint Completion Status

🟢 COMPLETED – READY FOR SPRINT 2 ENGINEERING REVIEW
