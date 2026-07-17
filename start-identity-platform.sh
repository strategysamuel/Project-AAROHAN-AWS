#!/bin/sh
# Container 1: Identity + Demo Platform
# Services: auth-service, ese-admin-service
set -eu

export PYTHONUNBUFFERED=1
export PORT="${PORT:-8000}"

echo "🚀 Starting Identity + Demo Platform Container"
echo "Services: auth-service (9000), ese-admin-service (9090)"

# Seed simulation data
PYTHONPATH="/app" python /app/ese/seed/seed_all.py

# Start auth-service on port 9000
(
  cd /app/services/auth-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/auth-service" \
  PORT=9000 \
  uvicorn app.main:app --host 0.0.0.0 --port 9000 --log-level info
) &

# Start ese-admin-service on port 9090
(
  cd /app/services/ese-admin-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/ese-admin-service" \
  PORT=9090 \
  uvicorn app.main:app --host 0.0.0.0 --port 9090 --log-level info
) &

# Wait for all background services
wait
