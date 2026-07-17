#!/usr/bin/env bash
set -euo pipefail

VITE_API_BASE_URL="${VITE_API_BASE_URL:-https://aarohan-demo-platform-679889922969.asia-south1.run.app}"
VITE_AUTH_API_BASE_URL="${VITE_AUTH_API_BASE_URL:-https://aarohan-demo-platform-679889922969.asia-south1.run.app}"

if [[ -z "${PROJECT_ID:-}" ]]; then
  echo "Set PROJECT_ID before running this script." >&2
  exit 1
fi

REGION="${REGION:-asia-south1}"
SERVICE_NAME="${SERVICE_NAME:-aarohan-portal}"
IMAGE_NAME="${IMAGE_NAME:-$REGION-docker.pkg.dev/$PROJECT_ID/aarohan/$SERVICE_NAME:latest}"

export DOCKER_BUILDKIT=1

gcloud config set project "$PROJECT_ID"
gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet

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
