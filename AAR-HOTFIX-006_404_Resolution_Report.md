# AAR-HOTFIX-006 404 Resolution Report

## 1. 404 Endpoints Extracted & Root Causes
Based on the final acceptance test failures, the following endpoints returned 404:

| Endpoint | Service | Expected Route | Actual Route | Root Cause | Fix |
|---|---|---|---|---|---|
| `/consents/purposes` | `consent-service` | `/consents/purposes` | N/A (Offline) | ECS service not exposing the endpoint / Startup script omission | Added to `start-lending-intelligence.sh` & mapped port `9002` |
| `/ckyc/search` | `ckyc-service` | `/ckyc/search` | N/A (Test Client Route collision) | FastAPI test client crossover (Test script module cache collision) | Re-isolated `app` module imports in `test_regression_e2e.py` |
| `/gst/sync/{id}` | `gst-service` | `/gst/sync/{id}` | N/A (Test Client Route collision) | FastAPI test client crossover (Test script module cache collision) | Re-isolated `app` module imports in `test_regression_e2e.py` |
| `/credit/evaluate/{id}`| `credit-engine` | `/credit/evaluate/{id}`| N/A (Test Client Route collision) | FastAPI test client crossover (Test script module cache collision) | Re-isolated `app` module imports in `test_regression_e2e.py` |
| `/rm/tasks` | `rm-workspace-service` | `/rm/tasks` | N/A (Offline) | ECS service not exposing the endpoint / Startup script omission | Added to `start-executive-intelligence.sh` & mapped port `9010` |
| `/healthz` | `ocen-uli-service` | `/healthz` | N/A (Offline) | ECS service not exposing the endpoint / Startup script omission | Added to `start-lending-intelligence.sh` & mapped port `9008` |

## 2. Root Cause Analysis
Two distinct categories of 404 errors occurred:
1. **Container Networking Omissions**: Services (`consent-service`, `rm-workspace-service`, `ocen-uli-service`) were absent from the startup shells and docker-compose port mappings, rendering them completely unreachable via HTTP.
2. **Test Framework Module Collision**: Python's `sys.modules.pop()` approach in `test_regression_e2e.py` failed to properly clear `FastAPI` instance caches when loading multiple `app.main` modules in a single process. Consequently, the test client inadvertently tested the first loaded service instead of the target service for subsequent calls.

## 3. Files Changed
1. `start-lending-intelligence.sh` (Port 9002 & 9008)
2. `start-executive-intelligence.sh` (Port 9010)
3. `docker-compose.hackathon.yml` (Exposed 9002, 9008, 9010)
4. `tests/test_regression_e2e.py` (Improved module cache eviction logic)

## 4. Verification Results
- Containers have been successfully rebuilt via `docker compose up --build -d`.
- Re-ran the failed workflows (Customer Onboarding, CKYC, Credit Decision, RM Workspace) against the live container network. 
- All endpoints now correctly return HTTP 200/201.

## 5. Remaining Unresolved Endpoints
- **None.** All identified endpoints and routes now behave as expected and route perfectly through the container network.
