# AAR-DEPLOY-002: Cloud Run Production Hardening Report

## Deployment Architecture

Project AAROHAN is hardened for a two-service Cloud Run deployment:

- `aarohan-portal`: React/Vite frontend served as a static SPA behind Nginx
- `aarohan-api`: FastAPI backend/API surface used by the portal

The portal no longer relies on `npm run preview` for production serving. The browser UI is built once, then served from a lightweight production web server with SPA fallback routing and explicit health endpoints.

## Files Modified

- [Dockerfile.portal](Dockerfile.portal)
- [nginx.portal.conf](nginx.portal.conf)
- [Dockerfile](Dockerfile)
- [apps/customer-portal/src/lib/api.ts](apps/customer-portal/src/lib/api.ts)
- [services/auth-service/app/main.py](services/auth-service/app/main.py)
- [CLOUD_RUN_DEPLOYMENT.md](CLOUD_RUN_DEPLOYMENT.md)
- [.env.example](.env.example)

## Cloud Run Readiness

- The portal container now serves production assets with Nginx instead of Vite preview.
- SPA refresh routing is handled with `try_files ... /index.html`.
- The portal uses explicit environment variables for backend URLs and no longer contains browser-side localhost fetch calls.
- Backend startup is Cloud Run friendly with `0.0.0.0` binding, `PORT` support, proxy headers, and a healthcheck.
- Backend health endpoints are available at `/livez`, `/health`, and `/readiness`.

## Environment Variables

Required deployment variables:

- `VITE_API_BASE_URL`
- `VITE_AUTH_API_BASE_URL`
- `PORT`
- `PYTHONPATH`

Documented example values are in [.env.example](.env.example).

## Docker Improvements

- Replaced `npm run preview` with a production Nginx image in [Dockerfile.portal](Dockerfile.portal).
- Added SPA refresh fallback and health routes in [nginx.portal.conf](nginx.portal.conf).
- Hardened the backend startup command in [Dockerfile](Dockerfile) with `PORT`, proxy headers, and a lightweight container healthcheck.
- Added explicit portal health routes so the frontend container can be checked with `/health`, `/readiness`, or `/livez`.

## Production Hardening

- Removed hardcoded localhost fetch usage from the portal source tree.
- Required deployment URLs to be injected through environment variables instead of silent localhost defaults.
- Added a deploy guide that assumes two Cloud Run services and documents build-time URL injection.
- Preserved existing business workflows and backend behavior.

## Validation Results

- `npm run build` passed successfully after the deployment hardening changes.
- The auth backend started successfully on a free local port under Uvicorn.
- `/livez`, `/health`, and `/readiness` returned valid JSON responses from the backend.
- Docker CLI is installed in this workspace.
- Docker image build validation could not be completed because the local Docker Desktop daemon is stopped and cannot be started from the current user context.

## Remaining Deployment Risks

- The local Docker daemon is unavailable in this environment, so container build validation remains a tooling gap rather than a code defect.
- The backend Cloud Run URL must be supplied explicitly through `VITE_API_BASE_URL` and `VITE_AUTH_API_BASE_URL` at build time.
- If the backend API surface is split across multiple services in production, the portal URLs must be pointed at the appropriate public gateway or load-balanced endpoint.
