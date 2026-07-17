# Judge FAQ

## What problem does AAROHAN solve?
It reduces the friction of MSME lending by unifying onboarding, registry checks, scoring, decisioning, and executive review into one guided flow.

## Is the workflow live or simulated?
It is a production-style portal with seeded demo behavior and fallback paths to keep the journey repeatable for judging.

## What is the role of AI?
AI is assistive. The copilot helps users navigate the workflow, surface relevant actions, and review reports.

## What AWS services are used?
Amplify hosts the frontend, ECS runs backend services, and ALB routes traffic to the task groups.

## Is the deployment fully clean?
No. The system is functional, but some optional backend routes still return 404 and live AWS control-plane metrics were not directly captured here.

## Can the demo still be completed?
Yes. The live browser session confirmed the authenticated portal, dashboard, reports, and copilot surfaces are reachable.
