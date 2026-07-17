#!/bin/sh
set -eu

export PYTHONUNBUFFERED=1
export PORT="${PORT:-8000}"

start_service() {
  service_dir="$1"
  port="$2"
  python_path="$3"

  (
    cd "/app/services/$service_dir"
    PYTHONPATH="$python_path" PORT="$port" uvicorn app.main:app --host 127.0.0.1 --port "$port"
  ) >/proc/1/fd/1 2>/proc/1/fd/2 &
}

start_service auth-service 9001 "/app/services/auth-service:/app/services/ese-core"
start_service onboarding-service 9002 "/app/services/onboarding-service:/app/services/ese-core"
start_service aa-service 9003 "/app/services/aa-service:/app/services/ese-core"
start_service gst-service 9004 "/app/services/gst-service:/app/services/ese-core"
start_service epfo-service 9005 "/app/services/epfo-service:/app/services/ese-core"
start_service ckyc-service 9006 "/app/services/ckyc-service:/app/services/ese-core"
start_service mca-service 9007 "/app/services/mca-service:/app/services/ese-core"
start_service cam-service 9008 "/app/services/cam-service:/app/services/ese-core"
start_service exec-service 9009 "/app/services/exec-service:/app/services/ese-core"
start_service ese-admin-service 9010 "/app/services/ese-admin-service:/app/services/ese-core"
start_service fhc-service 9011 "/app/services/fhc-service:/app/services/ese-core"

exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --proxy-headers --forwarded-allow-ips='*' --timeout-keep-alive 5
