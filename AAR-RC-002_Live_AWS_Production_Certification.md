# AAR-RC-002: Live AWS Production Certification

## Executive Summary

Project AAROHAN was validated against the live Amplify-hosted portal and the AWS deployment artifacts stored in the repository. The production application is operational and the authenticated workflow loads successfully in the live browser session, but the environment does not meet GREEN certification because live ECS, ALB, and CloudWatch console evidence was not directly queryable from this workspace and several optional backend endpoints still return 404 at runtime.

**Final status: YELLOW**

## Certification Summary

| Item | Result |
|---|---|
| Total pages tested | 14 |
| Total APIs tested | 20 |
| Total runtime defects | 9 confirmed |
| Critical defects | 0 |
| Minor defects | 9 |
| Deployment readiness | Conditionally ready |
| Overall status | YELLOW |

## Architecture Overview

The repository shows an AWS production profile centered on:

- An ECS Fargate cluster named `aarohan-hackathon-cluster`
- An application load balancer with HTTP routing and target groups for identity, lending, and executive services
- An Amplify-hosted frontend deployment
- FastAPI backend services with JWT auth, RBAC, CORS, and health endpoints

Primary evidence sources:

- [cloudformation-ecs-networking.yml](cloudformation-ecs-networking.yml)
- [ecs-task-identity.json](ecs-task-identity.json)
- [ecs-task-lending.json](ecs-task-lending.json)
- [ecs-task-executive.json](ecs-task-executive.json)
- [AAR-QA-002_Enterprise_Runtime_Validation_Report.md](AAR-QA-002_Enterprise_Runtime_Validation_Report.md)
- [amplify-deploy-job1.log](amplify-deploy-job1.log)
- [amplify-build-job1.log](amplify-build-job1.log)

## Infrastructure Evidence

### ECS Verification

| Evidence | Observed value | Notes |
|---|---|---|
| Cluster name | `aarohan-hackathon-cluster` | Declared in IaC template |
| Identity service | Desired count `1` | Task definition `identity-task-definition:1` |
| Lending service | Desired count `1` | Task definition `lending-task-definition:1` |
| Executive service | Desired count `1` | Task definition `executive-task-definition:1` |
| Task health checks | `/livez` | Defined for all three task families |
| Running count | Not directly queryable here | Live ECS console access unavailable |
| Pending count | Not directly queryable here | Live ECS console access unavailable |
| Task health status | Not directly queryable here | Health checks are defined, but live task state was not observable |

### ALB Verification

| Evidence | Observed value | Notes |
|---|---|---|
| Load balancer | `aarohan-alb` | Application Load Balancer in IaC |
| Listener 80 | Present | `HttpListener` forwards to identity target group by default |
| Listener 443 | Not found in reviewed IaC | Security group allows 443, but no HTTPS listener was found in the template reviewed |
| Target groups | Identity, Lending, Executive | Each uses HTTP health check on `/livez` |
| Healthy targets | Not directly queryable here | Live target group health was not observable |
| Unhealthy targets | Not directly queryable here | Live target group health was not observable |
| Routing | Path rules for `/auth/*`, `/gst/*`, `/api/*`, `/exec/*` | Defined in IaC |

### CloudWatch Verification

Direct CloudWatch console access was not available in this workspace, so the log review is limited to stored deployment logs and browser-observed runtime errors.

Observed error entries:

| Source | Error entry | Assessment |
|---|---|---|
| [amplify-build-job1.log](amplify-build-job1.log) | `Unable to clone repository due to user error code: 128` | Build-time error on first attempt, not a runtime blocker because deployment later completed |
| Live browser session | Optional backend routes returned 404 for CKYC/AA/FHC endpoints | Runtime defect, non-fatal but not GREEN |

No CRITICAL entries were found in the repository logs reviewed.

### Amplify Verification

| Evidence | Observed value | Notes |
|---|---|---|
| App ID | `d2lek1l0vzlyj6` | From runtime validation report |
| Branch | `develop/v1.1` | From runtime validation report |
| Hosted URL | `https://develop-v1-1.d2lek1l0vzlyj6.amplifyapp.com/` | Live browser verified |
| Build status | `SUCCEED` | From runtime validation report and deploy log |
| Deployment status | Complete | `amplify-deploy-job1.log` |
| Environment variables | Build-time API URLs injected | `VITE_API_BASE_URL` and `VITE_AUTH_API_BASE_URL` are present in deployment config |
| Frontend accessibility | Pass | Live browser login and authenticated navigation worked |

## Application Evidence

The live portal was opened in a browser session and verified end-to-end at the login and authenticated shell level.

Observed working surfaces:

- Login page loaded successfully
- Authentication completed and the dashboard rendered
- Reports page rendered with report cards and download actions
- AI Banking Copilot opened and displayed role-aware prompts, quick actions, recent conversations, and recommended reports

Live browser evidence captured:

- Portal title: `IDBI AAROHAN - Digital MSME Lending Portal`
- Authenticated role: `RELATIONSHIP_MANAGER`
- Dashboard content rendered with customer, application, approval, and portfolio metrics
- Copilot panel displayed `AI Banking Copilot` with RM-specific suggestions

## Runtime Evidence

The live browser session reproduced non-fatal runtime errors during navigation.

Confirmed 404 endpoints from the live portal:

- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/ckyc/verification-logs`
- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/ckyc/stats`
- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/ckyc/manual-queue`
- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/aa/consents?customer_id=99`
- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/aa/accounts/99`
- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/aa/financial-info/99`
- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/aa/analytics/99`
- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/fhc/history/99`
- `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/fhc/99`

These are non-fatal fallback-path errors, but they prevent a clean-console GREEN certification.

## Security Validation

Security behavior was validated from the running code and live portal behavior.

| Control | Evidence | Result |
|---|---|---|
| JWT authentication | Auth service issues Bearer tokens and validates access tokens | Pass |
| RBAC | Permission checker is implemented in auth service and exposed through role-based navigation | Pass |
| CORS | CORS middleware is enabled in both gateway and auth service | Pass |
| Security headers | No dedicated HSTS/CSP policy was observed in the reviewed surfaces | Risk |
| Environment variables | Frontend uses build-time API env vars; ECS task defs inject runtime env vars | Pass |
| Secrets handling | No secret values were exposed in the repository evidence reviewed | Pass |

Primary security sources:

- [services/auth-service/app/main.py](services/auth-service/app/main.py)
- [app/main.py](app/main.py)
- [apps/customer-portal/src/lib/api.ts](apps/customer-portal/src/lib/api.ts)

## Performance Summary

Measured live timings from the browser session and backend probe:

| Metric | Observed value | Notes |
|---|---|---|
| Frontend load time | 94 ms | Browser navigation timing on the Amplify portal |
| API latency | 77 ms | `GET /livez` against the public API gateway base |
| Build time | About 1 minute | Customer portal production build completed successfully |
| Container startup time | Not directly measured | Live ECS console access unavailable |
| ALB response time | Not directly measured | Live ALB metrics not observable from this workspace |

## Remaining Risks

1. Live ECS running count, pending count, and task health were not directly queried from AWS.
2. Live ALB target health and listener 443 status were not directly confirmed from AWS.
3. CloudWatch log streams were not directly queried; only stored deployment logs and browser-observed runtime errors were available.
4. Optional backend endpoints still return 404 in the live browser session, even though the user journey continues via fallback behavior.
5. No explicit HSTS or CSP policy was observed in the reviewed code paths.

## Final Recommendation

**YELLOW**

The environment is operational and the primary portal workflow is reachable in live production, but it does not satisfy the GREEN bar because the runtime is not clean and full AWS control-plane verification was not directly observable from this workspace. Keep the release as conditionally ready and do not mark it production-final until the remaining 404s are removed and live ECS/ALB/CloudWatch evidence is captured.
