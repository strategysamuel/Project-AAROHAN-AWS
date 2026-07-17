# AAR-AI-026 AI Banking Copilot Report

## Objective
Implement an enterprise-grade AI Banking Copilot inside the existing Project AAROHAN customer portal without redesigning the application or replacing any existing banking workflows.

## Components Added
- `apps/customer-portal/src/lib/copilot.ts` for intent detection, role-aware suggestions, model/provider abstraction, and API orchestration.
- `apps/customer-portal/src/components/AiBankingCopilotPanel.tsx` for the floating assistant UI, chat history, prompt suggestions, voice input, and response execution.
- `apps/customer-portal/src/App.tsx` integration to mount the copilot globally inside the existing portal shell.

## AI Architecture
The copilot is implemented as a lightweight orchestration layer that sits in the portal UI and calls existing backend APIs. It does not execute raw SQL and does not replace the current banking flows. The assistant supports multiple providers through environment-driven configuration, including mock mode, Gemini, OpenAI-compatible endpoints, Azure OpenAI, and Ollama.

## Supported Intents
- Open portal pages and banking screens
- Show customer loan status
- Identify missing onboarding documents
- Generate FHC, credit decision, and CAM guidance
- Download report packs
- Compare borrowers
- Compare scenarios
- Reset demo data
- Load demo personas
- Switch demo scenarios
- Show executive analytics
- Show GST compliance summaries
- Trigger underwriting-oriented workflows

## Supported Roles
- CUSTOMER
- RELATIONSHIP_MANAGER
- CREDIT_MANAGER
- EXECUTIVE
- ADMINISTRATOR
- DEMO_USER

Role-based prompt suggestions and permissions are enforced in the copilot orchestration layer so that users only see actions that match their operating context.

## Voice Features
- Browser speech recognition for microphone-driven prompts
- Voice response playback using speech synthesis
- Safe fallback to text input when voice APIs are unavailable
- Toggleable TTS behavior from the copilot panel

## Navigation Features
- One-click navigation from assistant responses into existing portal pages
- Global floating launcher that stays available across the portal
- Context-aware opening of onboarding, GST, FHC, credit, CAM, reports, and executive screens

## Reports
The copilot can request and download report packs through existing control-plane endpoints. Supported report outputs include FHC, credit decision, CAM, executive summary, portfolio summary, and fraud/risk reporting.

## Analytics
The assistant can summarize executive command center metrics such as approval rate, portfolio value, rejected applications, manual review queue, and top risk accounts. It also reuses GST analytics paths where available.

## APIs Reused
- `/customers`
- `/customers/load-persona`
- `/fhc/{customer_id}`
- `/fhc/calculate/{customer_id}`
- `/fhc/compare`
- `/credit/decision/{customer_id}`
- `/credit/evaluate/{customer_id}`
- `/credit/compare`
- `/cam/generate`
- `/exec/command-center`
- `/ese/control/report`
- `/ese/control/compare`
- `/ese/control/reset`
- `/ese/control/scenario`
- `/ese/control/status`

## Cloud Run Compatibility
The feature is compatible with the existing Cloud Run portal deployment model because it only depends on runtime environment variables and the existing API base URLs already used by the portal. The copilot supports environment-driven configuration for:
- `VITE_COPILOT_ENABLED`
- `VITE_VOICE_ENABLED`
- `VITE_AI_PROVIDER`
- `VITE_AI_API_KEY`
- `VITE_AI_MODEL`
- `VITE_AI_ENDPOINT`

## Validation Results
- TypeScript compilation passed for the customer portal.
- Production Vite build completed successfully.
- The new copilot files are wired into the existing portal shell without replacing existing pages or workflows.

## Outcome
Project AAROHAN now includes an enterprise-style AI Banking Copilot overlay that reuses the current service layer, supports natural language and voice interaction, and keeps the existing banking experience intact.
