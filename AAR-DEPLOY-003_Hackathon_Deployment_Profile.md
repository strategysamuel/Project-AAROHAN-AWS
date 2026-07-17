# AAR-DEPLOY-003: Hackathon Deployment Profile

## Deployment Architecture

Project AAROHAN is implemented as a hybrid, multi-service platform:

- One React/Vite customer portal
- Multiple FastAPI backend services
- A simulation/control plane for seeded demo orchestration
- A one-time seeder/init step for demo data

For hackathon operations, the simplest deployment profile is:

- Cloud Run service 1: `aarohan-portal`
- Cloud Run service 2: `aarohan-demo-platform`

This profile preserves the current portal behavior and preserves the public APIs while consolidating the backend runtime surface for the judge demo.

## Runtime Components

### Frontend

- React 19 + TypeScript + Vite customer portal
- Served as static production assets
- Uses environment-driven API URLs
- Requires SPA refresh fallback routing

### Backend

- FastAPI service modules already present in the repository
- Demo seeding and deterministic persona/state setup
- Existing auth, onboarding, registry, scoring, CAM, executive, and simulation flows

### Orchestration

- `seeder-init` is the bootstrap step for demo data
- `ese-admin-service` is the existing simulation and control-plane orchestrator
- `auth-service` is the identity entrypoint used by the portal login flow

## Existing Backend Orchestrator

Yes. The repository already contains an orchestrator/control plane:

- [services/ese-admin-service/app/main.py](services/ese-admin-service/app/main.py)

It exposes the control endpoints and health endpoints used to manage personas, scenarios, reports, and demo state.

The login entrypoint is:

- [services/auth-service/app/main.py](services/auth-service/app/main.py)

## Required Services For The Complete Judge Demo

The following services are required for the full judge-facing journey that preserves login, demo personas, lending journey, CAM generation, and executive dashboard coverage:

- `auth-service`
- `onboarding-service`
- `gst-service`
- `aa-service`
- `ckyc-service`
- `mca-service`
- `epfo-service`
- `fhc-service`
- `credit-engine`
- `cam-service`
- `exec-service`
- `ese-admin-service`
- `seeder-init`

These services support the visible judge flow and the seeded demo runtime.

## Optional Services

The following services are useful for broader platform coverage but are optional for the minimum judge demo path:

- `consent-service`
- `document-service`
- `ews-service`
- `rm-workspace-service`
- `portfolio-service`
- `rbi-fraud-service`
- `treds-service`
- `ocen-uli-service`

These services can remain available in the demo-platform runtime, but the judge demo does not depend on all of them being deployed as separate public Cloud Run services.

## Services That Can Be Hosted Inside A Single Backend Runtime Without Changing APIs

The existing backend services are already implemented as separate FastAPI apps with consistent service entry patterns. For a hackathon deployment profile, they can be co-hosted behind one backend runtime named `aarohan-demo-platform` without changing the public APIs, provided the runtime exposes the same HTTP paths.

The co-hosting profile is:

- Identity and control plane:
  - `auth-service`
  - `ese-admin-service`
- Core journey services:
  - `onboarding-service`
  - `consent-service`
  - `gst-service`
  - `aa-service`
  - `ckyc-service`
  - `mca-service`
  - `epfo-service`
  - `fhc-service`
  - `credit-engine`
  - `cam-service`
  - `exec-service`
  - `ews-service`
- Supporting demo services:
  - `document-service`
  - `rm-workspace-service`
  - `portfolio-service`
  - `rbi-fraud-service`
  - `treds-service`
  - `ocen-uli-service`

In other words, the current codebase is best treated as one portal plus one consolidated backend runtime for the hackathon profile, even though the source tree still contains separate service modules.

## Frontend

The portal should be deployed as `aarohan-portal`.

Characteristics:

- Build-time API URLs are injected through environment variables
- No browser-side localhost assumptions in production
- SPA routing must resolve refreshes to `index.html`
- The portal should call the backend through the public Cloud Run URL of `aarohan-demo-platform`

Required frontend environment variables:

- `VITE_API_BASE_URL`
- `VITE_AUTH_API_BASE_URL`
- `PORT`

## Backend

The backend profile should be deployed as `aarohan-demo-platform`.

Backend responsibilities preserved in this profile:

- Authentication and profile lookup
- Demo persona selection and scenario switching
- Lending/onboarding journey
- CAM generation
- Executive dashboard and reporting
- Health/readiness/liveness endpoints
- Demo seeding and reset behavior

The backend runtime should preserve the existing API surfaces used by the portal rather than introducing new business endpoints.

Required backend environment variables:

- `INTEGRATION_PROFILE=DEMO`
- `ACTIVE_DATASET=msme`
- `PYTHONPATH` covering the service modules needed by the runtime
- `PORT`

## Cloud Run Services

Recommended hackathon deployment profile:

1. `aarohan-portal`
2. `aarohan-demo-platform`

This is the lowest-complexity profile that still preserves the current behavior set.

If the hackathon platform needs a stricter separation, the next step would be:

1. `aarohan-portal`
2. `aarohan-api-auth`
3. `aarohan-demo-platform-core`

However, that is more complex than necessary for the current demo profile.

## Deployment Commands

### Portal build and deploy

```bash
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/aarohan/aarohan-portal:latest -f Dockerfile.portal .
gcloud run deploy aarohan-portal \
  --image=REGION-docker.pkg.dev/PROJECT_ID/aarohan/aarohan-portal:latest \
  --region=asia-south1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080
```

### Demo platform build and deploy

```bash
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/aarohan/aarohan-demo-platform:latest -f Dockerfile .
gcloud run deploy aarohan-demo-platform \
  --image=REGION-docker.pkg.dev/PROJECT_ID/aarohan/aarohan-demo-platform:latest \
  --region=asia-south1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8000
```

The portal build must inject the public HTTPS URL of `aarohan-demo-platform` into the frontend environment variables.

## Environment Variables

### Portal

- `VITE_API_BASE_URL`
- `VITE_AUTH_API_BASE_URL`
- `PORT`

### Backend

- `INTEGRATION_PROFILE`
- `ACTIVE_DATASET`
- `PYTHONPATH`
- `PORT`

### Demo control

- `INTEGRATION_PROFILE=DEMO`
- `ACTIVE_DATASET=msme`

## Known Trade-offs

- This profile reduces operational complexity by consolidating backend behavior into one Cloud Run backend runtime.
- The trade-off is that it preserves APIs but not the original one-service-per-domain deployment topology.
- The portal still needs build-time environment values, so backend URL changes require a rebuild and redeploy of the frontend.
- A fully faithful microservice-per-service Cloud Run deployment would be more complex but would mirror the current compose topology more closely.
- The demo profile is optimized for hackathon judging, not for production scale-out of every service independently.

## Validation Checklist

- Portal loads successfully from Cloud Run.
- Login succeeds through the auth surface.
- Demo persona selection works.
- Lending/onboarding journey is reachable.
- CAM generation remains available.
- Executive dashboard renders successfully.
- Demo reset and control-plane actions work.
- `/health`, `/readiness`, and `/livez` respond on the deployed backend runtime.
- No browser-side localhost dependencies remain in the production portal build.

## Summary Recommendation

Use the two-service hackathon profile:

- `aarohan-portal`
- `aarohan-demo-platform`

This is the simplest deployment shape that preserves the existing application behavior while minimizing Cloud Run operational complexity.