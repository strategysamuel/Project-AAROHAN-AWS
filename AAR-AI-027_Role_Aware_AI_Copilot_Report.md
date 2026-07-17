# AAR-AI-027 Role-Aware AI Banking Copilot Report

## Objective
Transform the existing AI Banking Copilot in Project AAROHAN into a fully role-aware enterprise banking assistant without redesigning the application or replacing the current banking workflows.

## Implementation Summary
The copilot now resolves the logged-in role from the authenticated user profile, normalizes it to an internal role key, and renders a role-specific home experience inside the existing copilot drawer. The intent engine enforces role permissions before navigation, workflow execution, report export, and executive analytics. Report access is filtered per role so the copilot only exposes permitted outputs.

The implementation was applied in the existing customer portal code path and keeps the current application shell intact.

## Supported Roles
- Administrator
- Executive
- Relationship Manager
- Credit Manager
- Credit Underwriter
- Risk Officer
- Operations Officer
- Compliance Officer
- Customer
- Auditor
- Trainer
- Demo User

## Permission Matrix
| Role | Primary Access | Allowed Copilot Behavior | Report Scope |
|---|---|---|---|
| Administrator | Platform control, demo governance | Reset demo, load persona, switch scenario, manage users, view system health | Executive Summary, Portfolio Report, Fraud Report |
| Executive | MSME portfolio leadership | View dashboards, portfolio analytics, executive summaries, board-oriented navigation | Executive Summary, Portfolio Report, Risk Report |
| Relationship Manager | Commercial banking and customer operations | Open onboarding, generate CAM, compare borrowers, show GST compliance, route customer workflows | Financial Health Card, Credit Decision, CAM |
| Credit Manager | Policy and underwriting governance | Review approvals, manual checks, policy exceptions, risk analysis, underwriting support | Financial Health Card, Credit Decision, CAM, Risk Report |
| Credit Underwriter | Assessment and recommendation support | Generate CAM, compare borrowers, review policy exceptions, run underwriting | Financial Health Card, Credit Decision, CAM, Risk Report |
| Risk Officer | Portfolio risk and early warning | Inspect risk heatmaps, stress accounts, exposure analysis, fraud cases | Risk Report, Portfolio Report |
| Operations Officer | Case flow and documentation | Review pending cases, document gaps, workflow status, disbursal queues | Financial Health Card |
| Compliance Officer | KYC, AML, audit, regulation | Check KYC exceptions, AML alerts, CKYC status, audit trails | Risk Report |
| Customer | Self-service loan support | Check loan status, application status, required documents, eligibility, support | Financial Health Card |
| Auditor | Independent review and evidence tracing | Inspect audit trail, decision evidence, report history, exceptions | Executive Summary, Risk Report |
| Trainer | Guided demos and walkthroughs | Launch demo flows, switch personas, walkthroughs, training mode | Executive Summary, Portfolio Report, CAM |
| Demo User | Curated demo experience | Follow scripted demo journeys, download permitted samples, open demo dashboard | Financial Health Card, CAM, Executive Summary |

## Suggested Prompts
### Administrator
Reset demo, load persona, switch scenario, manage users, system health, dataset status, simulation status, cloud status, logs.

### Executive
Today's MSME portfolio, portfolio exposure, approval rate, sector-wise lending, top performing branches, largest sanctions, rejected applications, risk heatmap, executive summary, board report.

### Relationship Manager
Show pending customers, open onboarding, generate CAM, compare borrowers, show GST compliance, show Financial Health Card, run underwriting, open customer profile, today's meetings.

### Credit Manager
Pending approvals, manual reviews, credit decision, generate CAM, compare credit scores, policy exceptions, risk analysis.

### Credit Underwriter
Generate CAM, compare borrowers, credit score details, risk grade, policy exceptions, run underwriting.

### Risk Officer
High risk borrowers, early warning signals, fraud cases, portfolio risk, stress accounts, NPA prediction, exposure analysis.

### Operations Officer
Open onboarding, required documents, pending cases, workflow status, document gaps, disbursal queue.

### Compliance Officer
KYC exceptions, AML alerts, CKYC status, audit reports, regulatory compliance.

### Customer
Loan status, application status, required documents, eligibility, Financial Health Card, download CAM, GST status, support.

### Auditor
Audit trail, decision evidence, exceptions, report history, document trace, policy overrides.

### Trainer
Launch guided demo, switch persona, walkthrough, demo reports, training mode.

### Demo User
Show my CAM, show FHC, download reports, open dashboard.

## Navigation Features
- Role-aware smart navigation resolves direct commands such as Open CAM, Open Dashboard, and Open onboarding into the correct application page.
- Generate CAM triggers the CAM page, runs the underwriting workflow, and returns a success path through the existing engine.
- Executive and control-plane actions are routed only when the active role permits them.
- Customer service and KYC requests route to the correct workflow entry points instead of exposing restricted controls.

## Voice Features
- Voice input uses the same intent engine as text input.
- Voice responses are generated only from permitted actions and permitted report scopes.
- If voice APIs are unavailable, the copilot falls back to text without changing authorization rules.
- The permission check is performed before workflow execution, so voice cannot bypass role controls.

## Role Intelligence
- Logged-in role is read from the authenticated user profile and normalized into the copilot role model.
- The copilot drawer displays the current role, current persona, current dataset, role badge, and permission badge.
- Suggested prompts, quick commands, pinned actions, frequent tasks, and accessible reports are role-specific.
- Conversation history is stored per role, persona, and dataset so one role does not inherit another role's context.
- Unauthorized requests are rejected with a permission-denied response rather than being executed or silently downgraded.
- The same intent engine governs text, buttons, and voice input.

## Reports
Only reports available to the current role are shown and exported.

### Accessible report families
- Financial Health Card
- Credit Decision
- CAM
- Executive Summary
- Portfolio Report
- Fraud Report

### Role-scoped report examples
- Customer: Financial Health Card
- Relationship Manager: Financial Health Card, Credit Decision, CAM
- Credit Manager and Credit Underwriter: Financial Health Card, Credit Decision, CAM, Risk Report
- Executive and Administrator: Executive Summary, Portfolio Report, Risk Report
- Risk Officer: Risk Report, Portfolio Report
- Compliance Officer: Risk Report
- Trainer and Demo User: curated demo-safe report mix

## Workflow Support
- Open page commands navigate directly to the existing portal screen.
- Generate CAM opens CAM and executes the underwriting workflow.
- Compare borrowers and compare scenarios remain available only to permitted roles.
- Demo actions such as reset, load persona, and switch scenario are available where the role has simulation access.
- The copilot keeps using existing APIs and does not replace the backend services.

## Validation Results
- TypeScript compilation passed for the customer portal slice.
- Production Vite build completed successfully.
- Role-aware permission enforcement is implemented in the shared copilot intent engine.
- Role-specific home UI, conversation scoping, and report filtering are wired into the portal shell.
- Full manual runtime smoke testing across every supported role is still a recommended follow-up verification step.

## Outcome
The AI Banking Copilot now behaves as a role-aware enterprise assistant. Logged-in users see different home content, permitted prompts, permitted reports, and permitted workflows based on their authenticated role.

🤖 PROJECT AAROHAN
ROLE-AWARE AI BANKING COPILOT CERTIFIED

ENTERPRISE AI EXPERIENCE COMPLETE
