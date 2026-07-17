#!/bin/sh
# Container 3: Executive Intelligence Platform
# Services: exec-service
set -eu

export PYTHONUNBUFFERED=1
export PORT="${PORT:-8000}"

echo "🚀 Starting Executive Intelligence Platform Container"
echo "Services: exec-service (9009), rm-workspace (9010)"

# Seeding is handled by identity-platform

# Start exec-service on port 9009
(
  cd /app/services/exec-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/exec-service" \
  PORT=9009 \
  uvicorn app.main:app --host 0.0.0.0 --port 9009 --log-level info
) &

# Start rm-workspace-service on port 9010
(
  cd /app/services/rm-workspace-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/rm-workspace-service" \
  PORT=9010 \
  uvicorn app.main:app --host 0.0.0.0 --port 9010 --log-level info
) &

# Wait for service
wait
