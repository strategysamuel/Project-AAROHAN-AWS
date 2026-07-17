# Project AAROHAN: Deployment and Operations Guide
## AAR-LCP-006: Platform Engineering, Kubernetes Configurations, and DevSecOps Playbook

**Document Classification:** Technical Operations Manual  
**Platform Version:** ESE v1.0.0 (GA)  
**Target Environment:** GKE / Cloud Run / VPC Hybrid  
**Status:** **🟢 SRE CERTIFIED & RELEASE READY**  

---

## 1. Executive Summary
This document defines the deployment architecture, configuration parameters, and operations workflows for **Project AAROHAN Enterprise Digital Banking Twin v1.0.0**. It serves as the operations manual to guide DevOps, Site Reliability Engineers, and System Administrators in launching, scaling, and maintaining the platform across diverse deployment models.

---

## 2. Supported Deployment Models
- **Local Development**: Poetry-based local python environments.
- **Docker Compose**: Containerized multi-service sandboxes for quick evaluation.
- **Kubernetes (GKE)**: Production-ready setups, utilizing HPA (Horizontal Pod Autoscaler).
- **Google Cloud Run**: Serverless deployment for low-overhead staging.
- **Hybrid Deployment**: Local sandbox DB engines running alongside secure corporate VPC links.

---

## 3. Infrastructure Requirements
- **Compute**: Minimum 2 vCPUs and 4GB RAM per microservice instance.
- **Storage**: SSD-backed persistent volumes for state SQLite databases.
- **Network**: Private subnets with outgoing NAT gateways for External API integrations (when running in PRODUCTION profile).

---

## 4. Repository Structure
```
project-aarohan/
├── deploy/
│   ├── docker-compose.yml   # Compose manifest
│   ├── kubernetes/          # Helm/K8s manifests
│   └── cloudrun.yaml        # GCP Cloud Run deployment specification
├── services/                # Application modules
└── README.md
```

---

## 5. Environment Variables
Standard configurations for all containers:
```env
PORT=8000
INTEGRATION_PROFILE=DEMO
ACTIVE_DATASET=msme
DATABASE_URL=sqlite:///ese/datasets/aarohan_ese.db
LOG_LEVEL=INFO
```

---

## 6. Integration Profiles
- **DEMO**: Fully isolated sandbox using local JSON/SQLite mocks.
- **TRAINING**: Ticking clock controls enabled, allowing presenters to step through timelines.
- **UAT**: Links sandbox models to the bank's staging APIs.
- **PERFORMANCE**: High-concurrency configurations with zero file logging.
- **PRODUCTION**: Intercepts no calls; maps database tables and external registries directly to real Core systems.

---

## 7. Database Configuration
In sandboxed execution profiles, SQLite is run under **WAL (Write-Ahead Logging)** mode:
```sql
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA cache_size=-64000;
```
This configuration supports high concurrency during timeline simulation ticks.

---

## 8. Dataset Marketplace Deployment
Static datasets (JSON configurations for Priya Textiles, GreenAgro, etc.) are distributed inside `ese/datasets/`. These are baked into the container image to prevent file dependency mismatches during deployments.

---

## 9. Enterprise Simulation Engine Deployment
The simulation clock and causality engines run within the `ese-admin-service` container. SRE teams must configure the clock scheduling tasks to prevent overlaps.

---

## 10. Production Deployment
When deploying to live staging:
- Configure custom SSL certificates.
- Set `INTEGRATION_PROFILE=PRODUCTION`.
- Mount local persistent volumes (`/ese/datasets`) to keep simulated replay packages intact.

---

## 11. CI/CD Pipeline Overview
GitHub Actions workflow pipelines automatically:
1. Run lint checks (black/flake8).
2. Execute the pytest test suites.
3. Build the Docker container images and push them to Google Artifact Registry.
4. Deploy images to Cloud Run or trigger Helm chart upgrades on Google GKE.

---

## 12. Secret Management
Never commit credentials. Use Google Cloud Secret Manager or HashiCorp Vault. Map secrets at runtime as environment variables:
```env
VERTEX_AI_API_KEY=projects/123/secrets/vertex-key/versions/latest
```

---

## 13. Monitoring & Observability
- **Metrics**: Export metrics using Prometheus endpoints (`/metrics`).
- **Dashboards**: Visualize service latency and request error rates in Grafana or Cloud Monitoring.

---

## 14. Logging Strategy
Applications output JSON-formatted standard output logs to facilitate ingestion:
```json
{"timestamp": "2026-07-08T15:43:00Z", "level": "INFO", "message": "Clock ticked to next simulation day."}
```

---

## 15. Health Checks
- **Startup Probe**: `GET /livez` (returns `{"status": "UP"}`).
- **Liveness Probe**: `GET /health` (validates active profile and database connectivity).

---

## 16. Backup & Recovery
Create daily snapshots of `/ese/datasets/` databases. Use standardized backup scripts:
```bash
sqlite3 /ese/datasets/aarohan_ese.db ".backup '/backups/aarohan_ese_$(date +%F).db'"
```

---

## 17. Disaster Recovery
In the event of a cluster crash:
1. Re-deploy the Kubernetes stateful sets from the Helm repository.
2. Restore the latest SQLite snapshot from Cloud Storage.
3. Restart the clock scheduling timers.

---

## 18. Security Hardening
- Run containers as non-root users (`USER 10001`).
- Enforce network policy rules to restrict internal pod communication.
- Scan images using GCP Artifact Analysis.

---

## 19. Performance Tuning
- Set worker counts to `2 * CPU cores + 1` in `gunicorn`/`uvicorn` launchers.
- Keep JSON payloads compact during dataset queries.

---

## 20. Scaling Strategy
Use HPA configurations in Kubernetes to auto-scale pods when CPU utilization exceeds 80%.

---

## 21. Operational Runbooks
- **Runbook-001: Changing the active dataset**:
  1. Set environment variable `ACTIVE_DATASET=agro`.
  2. Perform container restart (`kubectl rollout restart deployment/ese-admin`).
  3. Validate using the `/health` endpoint.

---

## 22. Troubleshooting Guide
- **Error: `database is locked`**:  
  *Solution*: Ensure SQLite journal mode is set to WAL. Increase database timeout setting to 30.0 seconds.
- **Error: `Profile not found`**:  
  *Solution*: Validate `INTEGRATION_PROFILE` values match registered adapter definitions.

---

## 23. Maintenance Procedures
To apply updates without downtime, perform rolling updates:
```bash
kubectl set image deployment/ese-admin ese-admin-container=gcr.io/aarohan/ese-admin:v1.0.1
```

---

## 24. Upgrade Strategy
Major database schema migrations must utilize Alembic scripts. Back up the databases before running migration commands.

---

## 25. Rollback Procedures
To rollback an upgrade:
```bash
kubectl rollout undo deployment/ese-admin
```
If schema changes occurred, restore database states using backup snapshots.

---

## 26. Appendix
- **Kubernetes Manifest Example**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ese-admin
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: ese-admin-service
        image: gcr.io/aarohan/ese-admin:v1.0.0
```
