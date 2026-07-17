# Deployment Guide

This guide documents the current production deployment shape without changing any source code or infrastructure.

## Frontend Deployment

- Host the React portal on AWS Amplify.
- Use the build artifacts produced from `apps/customer-portal`.
- Provide the public HTTPS API endpoints through build-time environment variables.

## Backend Deployment

- Run backend services on Amazon ECS Fargate.
- Use the ALB to route traffic to the identity, lending, and executive services.
- Keep health checks pointed at `/livez`.

## Required Runtime Inputs

- `VITE_API_BASE_URL`
- `VITE_AUTH_API_BASE_URL`
- `PYTHONPATH`
- `INTEGRATION_PROFILE=DEMO`
- `ACTIVE_DATASET=msme`

## Operational Notes

- The live portal URL is reachable from the browser.
- The runtime supports fallback behavior for missing optional data.
- No deployment actions are included in this package.

## Deployment Evidence

- Amplify deployment completed successfully.
- ECS and ALB topology are present in the repository infrastructure artifacts.
- Live AWS console verification of task health and target status remains a separate operational check.
