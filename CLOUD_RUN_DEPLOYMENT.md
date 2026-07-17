# Cloud Run Deployment Guide

This guide publishes Project AAROHAN as two Cloud Run services:

- `aarohan-portal`: the judge-facing React frontend
- `aarohan-api`: the FastAPI backend/API surface used by the portal

## Architecture

The browser app is built from `Dockerfile.portal` and served as a static SPA on Cloud Run through Nginx. The portal reads its API targets at build time:

- `VITE_API_BASE_URL` for the main lending/domain API surface
- `VITE_AUTH_API_BASE_URL` for login and profile APIs

Cloud Run runtime still injects `PORT`, which the container honors.

## Prerequisites

1. Install and authenticate the Google Cloud CLI.
2. Select the target project.
3. Enable the required APIs.

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

4. Create an Artifact Registry repository if you do not already have one.

```bash
gcloud artifacts repositories create aarohan \
  --repository-format=docker \
  --location=asia-south1
```

5. Configure Docker authentication for Artifact Registry.

```bash
gcloud auth configure-docker asia-south1-docker.pkg.dev
```

## Build Inputs

Set these values to the public HTTPS URL of the backend service you want the portal to call:

- `VITE_API_BASE_URL`
- `VITE_AUTH_API_BASE_URL`

For local testing, the defaults in `.env.example` point to localhost.

## Suggested Deployment Shape

1. Deploy `aarohan-api` from the backend container image.
2. Deploy `aarohan-portal` from `Dockerfile.portal`.
3. Point both `VITE_API_BASE_URL` and `VITE_AUTH_API_BASE_URL` at the public HTTPS endpoint of `aarohan-api` unless you split auth onto a different backend hostname.

## Build And Deploy

### Bash

```bash
export PROJECT_ID=your-gcp-project
export REGION=asia-south1
export SERVICE_NAME=aarohan-portal
export IMAGE_NAME="$REGION-docker.pkg.dev/$PROJECT_ID/aarohan/$SERVICE_NAME:latest"
export VITE_API_BASE_URL=https://aarohan-api-xxxx.a.run.app
export VITE_AUTH_API_BASE_URL=https://aarohan-api-xxxx.a.run.app

docker build \
  -f Dockerfile.portal \
  --build-arg VITE_API_BASE_URL="$VITE_API_BASE_URL" \
  --build-arg VITE_AUTH_API_BASE_URL="$VITE_AUTH_API_BASE_URL" \
  -t "$IMAGE_NAME" .

docker push "$IMAGE_NAME"

gcloud run deploy "$SERVICE_NAME" \
  --image="$IMAGE_NAME" \
  --region="$REGION" \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080
```

### PowerShell

```powershell
$ProjectId = 'your-gcp-project'
$Region = 'asia-south1'
$ServiceName = 'aarohan-portal'
$ImageName = "$Region-docker.pkg.dev/$ProjectId/aarohan/$ServiceName:latest"
$ApiBaseUrl = 'https://aarohan-api-xxxx.a.run.app'
$AuthApiBaseUrl = 'https://aarohan-api-xxxx.a.run.app'

docker build `
  -f Dockerfile.portal `
  --build-arg VITE_API_BASE_URL=$ApiBaseUrl `
  --build-arg VITE_AUTH_API_BASE_URL=$AuthApiBaseUrl `
  -t $ImageName .

docker push $ImageName

gcloud run deploy $ServiceName `
  --image=$ImageName `
  --region=$Region `
  --platform=managed `
  --allow-unauthenticated `
  --port=8080
```

## Validation

After deployment, open the Cloud Run URL that `gcloud run deploy` returns and confirm:

1. The login page loads.
2. A successful login reaches the dashboard.
3. Demo Studio can read and write simulation state.
4. Report generation still works against the deployed API surface.
5. `/health`, `/readiness`, and `/livez` return 200 on the deployed containers.

## Rollback

If the new revision misbehaves, roll traffic back to the previous stable revision.

```bash
gcloud run services update-traffic aarohan-portal --to-revisions=PREVIOUS=100 --region=asia-south1
```

## Notes

- Do not rely on browser-side localhost URLs in Cloud Run. The portal must talk to deployed HTTPS endpoints.
- The Vite environment variables are baked into the build artifact, so changing backend URLs requires a rebuild and redeploy.
- If you want a separate backend release cadence, deploy the auth and domain services independently and update the build args for the portal.
