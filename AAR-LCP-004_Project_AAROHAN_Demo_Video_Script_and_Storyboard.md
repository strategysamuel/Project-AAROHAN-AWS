# Project AAROHAN: Demo Video Script & Storyboard
## AAR-LCP-004: Video Production Blueprint and Presenter Narration Playbook

**Document Classification:** Product Marketing & Video Storyboard  
**Target Videos:** 2-Minute Elevator Pitch | 5-Minute Technical Deep Dive  
**Platform Version:** ESE v1.0.0 (GA)  
**Status:** **🟢 APPROVED FOR RECORDING**  

---

## 1. Executive Summary
This document provides the scene-by-scene script, storyboard, and production guidelines for recording the official Project AAROHAN demonstration video. The video is designed to capture attention in hackathon finals, boardrooms, and customer showcases by highlighting how AAROHAN's sandboxed Digital Banking Twin simplifies MSME underwriting.

---

## 2. Demo Objectives
- **Demonstrate Value**: Show how alternative data (GST, EPFO, AA) accelerates loan approvals to under 5 minutes.
- **Highlight Innovation**: Show the causal macroeconomic simulation and white-label branding engines in action.
- **Establish Credibility**: Demonstrate the sandboxed database isolation and 100% test coverage.

---

## 3. Target Audience
- **Hackathon Judges**: Evaluating innovation, technical excellence, and presentation quality.
- **Banking Executives (e.g. IDBI C-Suite)**: Seeking lower operational costs and faster time-to-market.
- **Venture Capital Investors**: Evaluating business viability and product-market fit.

---

## 4. Video Versions

### 2-Minute Pitch Layout
- **0:00 - 0:30**: Problem & Vision (collateral shortages, India's MSME credit gap).
- **0:30 - 1:15**: E2E Onboarding Demo (onboard ➔ FHC ➔ decision).
- **1:15 - 1:45**: Architecture & Scaling (isolated sandbox, dynamic branding).
- **1:45 - 2:00**: CTA & Outro.

### 5-Minute Deep Dive Layout
- **0:00 - 1:00**: Problem & The DPI opportunity.
- **1:00 - 2:30**: One-click Presenter Console walk-through.
- **2:30 - 3:30**: Scenario comparison & Macroeconomic stress simulation.
- **3:30 - 4:30**: Code walkthrough (adapters, test suite run).
- **4:30 - 5:00**: Roadmaps & Closing.

---

## 5. Storyboard (5-Minute Deep Dive)

### Scene 1: The MSME Underwriting Problem
- **Duration**: 45 Seconds
- **Screen**: Title Slide followed by a split-screen animation showing stacks of physical files vs. a modern, clean digital lending UI.
- **Presenter Script**: "Across India, millions of MSMEs are shut out of formal credit due to a lack of physical collateral. Underwriting takes weeks, requiring manual verifications across fragmented registries."
- **Camera Notes**: Zoom in on the physical paperwork, then transition to AAROHAN's blue-teal Presenter UI.
- **Key Message**: Underwriting MSME loans is slow and costly.

### Scene 2: The Digital Twin Solution
- **Duration**: 45 Seconds
- **Screen**: Presenter Console Dashboard.
- **Presenter Script**: "Introducing Project AAROHAN, a Living Enterprise Digital Banking Twin. We sandbox the complete national DPI stack, allowing banks to model credit risk with zero production risk."
- **Camera Notes**: Panning shot across the UI, highlighting CKYC, GSTN, AA, and EPFO buttons.
- **Key Message**: AAROHAN sandboxes the entire ecosystem locally.

### Scene 3: One-Click Demo Execution
- **Duration**: 60 Seconds
- **Screen**: Dynamic onboarding timeline.
- **Presenter Script**: "Watch as we select Priya Textile Works under a Cash Flow Stress scenario. With one click, the system pulls records, generates a Financial Health Card, and runs an AI Credit check in under 3 seconds."
- **Camera Notes**: Zoom in on the 'Run Journey' button click. Highlight the green checks appearing at each step of the progress bar.
- **Key Message**: End-to-end digital underwriting is completed instantly.

### Scene 4: Scenario Comparison & Stress-Testing
- **Duration**: 60 Seconds
- **Screen**: Side-by-Side Scenario Comparator.
- **Presenter Script**: "How do macro conditions affect this? Our comparator displays metrics under standard and stressed scenarios. When repo rates rise, the engine recalculates DSCR, flagging default risks."
- **Camera Notes**: Highlight the delta columns showing drop in credit score and DSCR under stress.
- **Key Message**: Macroeconomic simulation supports proactive risk mitigation.

### Scene 5: Architecture & Developer Experience
- **Duration**: 60 Seconds
- **Screen**: VS Code showing `pytest` runs and API docs.
- **Presenter Script**: "For developers, AAROHAN offers a modular environment. Our adapter factory enables switching from sandbox mocks to live APIs. The code is protected by 100% test pass rates."
- **Camera Notes**: Close-up on the green test passes in the terminal.
- **Key Message**: SOLID design ensures enterprise reliability.

### Scene 6: Outro & Call to Action
- **Duration**: 30 Seconds
- **Screen**: Closing slide with GCP Marketplace links and contact details.
- **Presenter Script**: "AAROHAN ESE v1.0.0 is officially certified and ready for deployment. Visit our repository to launch your own twin sandbox. Join us in digitizing credit."
- **Camera Notes**: Slow fade-out with call-to-action details.
- **Key Message**: Project AAROHAN is GA and ready to deploy.

---

## 6. Suggested Demo Flow
- Show standard customer onboarding.
- Modify inflation/repo settings to trigger automatic cash flow recalculations.
- Export CAM (Credit Appraisal Memorandum) reports in PDF or Markdown format.

---

## 7. Recording Checklist
- [ ] Set browser zoom to 110% to ensure legibility on mobile screens.
- [ ] Use a high-quality external microphone.
- [ ] Record at 1080p, 60fps.
- [ ] Clear terminal history before filming code walks.

---

## 8. Screen Capture Sequence
1. Presenter UI landing page.
2. Select IDBI Bank profile.
3. Click 'Run complete Journey'.
4. Navigate to the scenario comparison tab.
5. Trigger `poetry run pytest` in terminal.
6. Open downloaded CAM PDF report.

---

## 9. Voice-over Guidance
- **Tone**: Professional, confident, and energetic.
- **Pacing**: Steady, especially during technical slides. Avoid speaking over click transitions.

---

## 10. Closing Message
"With Project AAROHAN, the future of cash-flow lending is no longer a mock-up. It is a living, breathing twin."

---

## 11. Call to Action
Deploy the docker container from GCP Cloud Run today at `github.com/hackathon/project-aarohan` and request a pilot license key.
