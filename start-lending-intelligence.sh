#!/bin/sh
# Container 2: Lending Intelligence Engine
# Services: onboarding, gst, aa, ckyc, epfo, mca, fhc, credit, cam
set -eu

export PYTHONUNBUFFERED=1
export PORT="${PORT:-8000}"

echo "🚀 Starting Lending Intelligence Engine Container"
echo "Services: onboarding (9001), consent (9002), gst (9003), aa (9004), fhc (9005), credit (9006), cam (9007), ocen (9008), ckyc (9011), mca (9012), epfo (9013), rbi-fraud (9014)"

# Seeding is handled by identity-platform

# Start onboarding-service on port 9001
(
  cd /app/services/onboarding-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/onboarding-service" \
  PORT=9001 \
  uvicorn app.main:app --host 0.0.0.0 --port 9001 --log-level info
) &

# Start consent-service on port 9002
(
  cd /app/services/consent-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/consent-service" \
  PORT=9002 \
  uvicorn app.main:app --host 0.0.0.0 --port 9002 --log-level info
) &

# Start gst-service on port 9003
(
  cd /app/services/gst-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/gst-service" \
  PORT=9003 \
  uvicorn app.main:app --host 0.0.0.0 --port 9003 --log-level info
) &

# Start aa-service on port 9004
(
  cd /app/services/aa-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/aa-service" \
  PORT=9004 \
  uvicorn app.main:app --host 0.0.0.0 --port 9004 --log-level info
) &

# Start fhc-service on port 9005
(
  cd /app/services/fhc-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/fhc-service" \
  PORT=9005 \
  uvicorn app.main:app --host 0.0.0.0 --port 9005 --log-level info
) &

# Start credit-engine on port 9006
(
  cd /app/services/credit-engine
  PYTHONPATH="/app:/app/services/ese-core:/app/services/credit-engine" \
  PORT=9006 \
  uvicorn app.main:app --host 0.0.0.0 --port 9006 --log-level info
) &

# Start cam-service on port 9007
(
  cd /app/services/cam-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/cam-service" \
  PORT=9007 \
  uvicorn app.main:app --host 0.0.0.0 --port 9007 --log-level info
) &

# Start ocen-uli-service on port 9008
(
  cd /app/services/ocen-uli-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/ocen-uli-service" \
  PORT=9008 \
  uvicorn app.main:app --host 0.0.0.0 --port 9008 --log-level info
) &

# Start ckyc-service on port 9011
(
  cd /app/services/ckyc-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/ckyc-service" \
  PORT=9011 \
  uvicorn app.main:app --host 0.0.0.0 --port 9011 --log-level info
) &

# Start mca-service on port 9012
(
  cd /app/services/mca-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/mca-service" \
  PORT=9012 \
  uvicorn app.main:app --host 0.0.0.0 --port 9012 --log-level info
) &

# Start epfo-service on port 9013
(
  cd /app/services/epfo-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/epfo-service" \
  PORT=9013 \
  uvicorn app.main:app --host 0.0.0.0 --port 9013 --log-level info
) &

# Start rbi-fraud-service on port 9014
(
  cd /app/services/rbi-fraud-service
  PYTHONPATH="/app:/app/services/ese-core:/app/services/rbi-fraud-service" \
  PORT=9014 \
  uvicorn app.main:app --host 0.0.0.0 --port 9014 --log-level info
) &

# Wait for all background services
wait
