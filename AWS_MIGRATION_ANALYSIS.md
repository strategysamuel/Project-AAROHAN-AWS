# AWS MIGRATION ANALYSIS
# Project AAROHAN - Phase 1

**Document Version:** 1.0  
**Date:** July 12, 2026  
**Classification:** CONFIDENTIAL - MIGRATION PLANNING  
**Author:** Principal Cloud Migration Architect  
**Status:** Analysis Complete - Awaiting Phase 2 Approval  

---

## EXECUTIVE SUMMARY

Project AAROHAN is a **fully functional MSME lending platform** currently deployed on Google Cloud Platform. Due to **GCP billing account suspension**, migration to AWS is required while **preserving ALL existing functionality**.

### Migration Scope
- **19 backend microservices** (FastAPI + Python 3.12)
- **1 frontend application** (React 19 + TypeScript + Vite)
- **Container registry** (Docker images)
- **CI/CD pipeline** (build and deployment automation)
- **AI services** (optional - has fallback adapters)

### Key Findings
✅ **Application is migration-ready** - fully containerized architecture  
✅ **Minimal code changes required** - only deployment layer and environment variables  
✅ **No cloud-specific business logic** - all services are platform-agnostic  
✅ **Local development working** - uses SQLite, no cloud database dependency  

### Migration Complexity Assessment
- **Overall Complexity:** MODERATE
- **Estimated Timeline:** 2-3 weeks
- **Risk Level:** LOW (containerized architecture simplifies migration)
- **Code Changes:** < 5% (deployment scripts and configuration only)

### Target AWS Architecture
- **Frontend:** AWS Amplify Hosting (static site)
- **Backend:** AWS App Runner (19 containerized services)
- **Registry:** Amazon ECR (container images)
- **AI (Optional):** Amazon Bedrock (future enhancement)

---

## TABLE OF CONTENTS

1. Current Architecture Overview
2. Google Cloud Dependencies Identified
3. AWS Service Mapping
4. Migration Complexity Analysis
5. Estimated Deployment Steps
6. Potential Risks & Mitigations
7. What Stays Exactly the Same
8. What Must Change
9. Timeline & Resource Estimates
10. Phase 2 Recommendations

---

## 1. CURRENT ARCHITECTURE OVERVIEW

### 1.1 Application Components

**Frontend Application:**
- **Technology:** React 19 + TypeScript + Vite
- **UI Framework:** Material UI + Emotion
- **State Management:** Zustand
- **Build Tool:** Vite (static SPA)
- **Deployment:** Nginx container serving static files
- **Current Host:** Google Cloud Run
- **Port:** 8080

**Backend Microservices (19 Services):**
- **Technology:** Python 3.12 + FastAPI + Uvicorn
- **Package Manager:** Poetry
- **ORM:** SQLAlchemy
- **Database (Current):** SQLite (local development/demo)
- **Database (Documented):** AlloyDB (not implemented)
- **Current Host:** Google Cloud Run (one service per container)


### 1.2 Backend Services Inventory

| # | Service Name | Port | Purpose |
|---|--------------|------|---------|
| 1 | auth-service | 9000 | JWT authentication & authorization |
| 2 | onboarding-service | 9001 | Customer onboarding & KYC |
| 3 | consent-service | 9002 | Consent orchestration |
| 4 | gst-service | 9003 | GST tax analytics |
| 5 | aa-service | 9004 | Account aggregator integration |
| 6 | fhc-service | 9005 | Financial health card calculation |
| 7 | credit-engine | 9006 | Credit decisioning & risk scoring |
| 8 | cam-service | 9007 | Credit appraisal memo generation |
| 9 | rm-workspace-service | 9008 | Relationship manager workspace |
| 10 | exec-service | 9009 | Executive dashboard & KPIs |
| 11 | ews-service | 9010 | Early warning system |
| 12 | ckyc-service | 9011 | KYC verification |
| 13 | mca-service | 9012 | Company registry integration |
| 14 | epfo-service | 9013 | Payroll registry integration |
| 15 | treds-service | 9014 | Trade finance |
| 16 | ocen-uli-service | 9015 | Embedded credit marketplace |
| 17 | document-service | N/A | Document management |
| 18 | portfolio-service | N/A | Portfolio analytics |
| 19 | rbi-fraud-service | N/A | Fraud registry checks |
| 20 | ese-admin-service | 9090 | Simulation admin control |

**Health Check Endpoints:** All services expose `/livez` for health monitoring

### 1.3 Technology Stack Summary

**Frontend:**
- React 19, TypeScript, Vite, Material UI, Zustand, Axios, React Hook Form, Zod

**Backend:**
- Python 3.12, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy, Poetry

**DevOps:**
- Docker, docker-compose, npm workspaces, Turbo, Prettier

---

## 2. GOOGLE CLOUD DEPENDENCIES IDENTIFIED

### 2.1 Critical Dependencies (BLOCKING)

#### Cloud Run (Primary Compute Platform)
- **Usage:** Hosts all 20 containerized services
- **Configuration:** Serverless auto-scaling (1-100 instances)
- **Features Used:** VPC Serverless Connectors, health checks, dynamic PORT variable
- **Files Found:**
  - `cloudbuild-portal.yaml`
  - `deploy-cloudrun.sh` (Bash deployment script)
  - `deploy-cloudrun.ps1` (PowerShell deployment script)
  - `CLOUD_RUN_DEPLOYMENT.md`
- **Hardcoded URLs:** `https://aarohan-demo-platform-679889922969.asia-south1.run.app`

#### Artifact Registry
- **Usage:** Docker image storage
- **Repository:** `asia-south1-docker.pkg.dev/aarohan-msme-platform/aarohan/`
- **Images:** `aarohan-portal:latest` + backend service images
- **Region:** asia-south1 (Mumbai)
- **References:** Found in `cloudbuild-portal.yaml`, deployment scripts

#### Cloud Build
- **Usage:** CI/CD pipeline for container builds
- **Builder Image:** `gcr.io/cloud-builders/docker`
- **Workflow:** Git push → Build → Push to Artifact Registry → Deploy to Cloud Run
- **Configuration File:** `cloudbuild-portal.yaml`

#### gcloud CLI
- **Usage:** Deployment automation
- **Commands Used:**
  - `gcloud config set project`
  - `gcloud auth configure-docker`
  - `gcloud run deploy`
  - `gcloud services enable`
  - `gcloud artifacts repositories create`


### 2.2 Python SDK Dependencies (pyproject.toml)

**Six Google Cloud packages imported:**

1. `google-cloud-secret-manager ^2.19.0` - Secret management (imported but inactive)
2. `google-cloud-storage ^2.15.0` - Object storage (imported but inactive)
3. `google-cloud-pubsub ^2.20.0` - Messaging (imported but inactive)
4. `google-cloud-logging ^3.9.0` - Logging (imported but inactive)
5. `google-genai ^2.10.0` - Gemini AI (OPTIONAL - has fallbacks)
6. `google-cloud-aiplatform ^1.44.0` - Vertex AI (OPTIONAL - has fallbacks)

**Status:** Packages are imported but current implementation uses:
- Local SQLite (not cloud storage)
- Local JSON logging (not Cloud Logging)
- Local event engine (not Pub/Sub)
- Local configuration (not Secret Manager)

### 2.3 AI Service Dependencies (OPTIONAL)

**Vertex AI Integration:**
- **Location:** `services/ese-core/adapters/`
- **Classes:** `SimulationVertexAIAdapter`, `ProductionVertexAIAdapter`, `VertexAIAdapter`
- **Credit Engine:** Supports multiple adapters: RULE_ENGINE (default), VERTEX_AI, CUSTOM_ML, OPENAI_LLM
- **Current Mode:** RULE_ENGINE (no cloud dependency)
- **Status:** ✅ **SYSTEM WORKS WITHOUT GOOGLE AI**

**Migration Impact:** AI services are optional enhancements. System fully functional without them.

### 2.4 Environment Variables & Configuration

**Google Cloud Specific:**
- `PROJECT_ID=aarohan-msme-platform`
- `REGION=asia-south1`
- Cloud Run URLs in build args
- Artifact Registry paths in scripts

**Platform-Agnostic (No Change Required):**
- `PORT` - Service port
- `PYTHONPATH` - Python module paths
- `INTEGRATION_PROFILE` - DEMO/PRODUCTION mode
- `ACTIVE_DATASET` - Simulation dataset


### 2.5 Docker Configuration

**Dockerfile (Backend Services):**
```dockerfile
FROM python:3.12-slim
# Poetry-based dependency installation
# Installs google-cloud-* packages from pyproject.toml
ENV PYTHONPATH="/app/services/ese-core"
HEALTHCHECK CMD python -c "import os,urllib.request; ..."
CMD ["sh", "/app/start-demo-platform.sh"]
```
**Google Dependency:** Python packages only (easily replaced)

**Dockerfile.portal (Frontend):**
```dockerfile
FROM node:20-slim AS build
ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_AUTH_API_BASE_URL=http://localhost:9000
# npm build
FROM nginx:1.27-alpine
EXPOSE 8080
```
**Google Dependency:** Build args contain Cloud Run URLs (easily updated)

### 2.6 Deployment Scripts

**deploy-cloudrun.sh / deploy-cloudrun.ps1:**
- Uses `gcloud` CLI commands throughout
- Configures Docker authentication with Artifact Registry
- Builds and pushes to Artifact Registry
- Deploys to Cloud Run
- **Migration Impact:** Complete script replacement required

---

## 3. AWS SERVICE MAPPING

### 3.1 Compute & Deployment Layer

| Google Cloud Service | AWS Equivalent | Complexity | Notes |
|---------------------|----------------|------------|-------|
| **Cloud Run** | **AWS App Runner** | LOW | Both serverless container platforms |
| Cloud Run (Frontend) | **AWS Amplify Hosting** | LOW | Static site hosting with CDN |
| Artifact Registry | **Amazon ECR** | LOW | Docker container registry |
| Cloud Build | **AWS CodeBuild** | MODERATE | CI/CD pipeline |
| VPC Serverless Connector | **VPC Integration** (App Runner) | LOW | Built-in VPC support |
| Load Balancer + Cloud Armor | **Not Required** | N/A | App Runner has built-in LB |

**Recommendation:** AWS App Runner is the perfect Cloud Run equivalent:
- Serverless container platform
- Auto-scaling
- Built-in load balancing
- VPC integration
- Health check support
- Pay-per-use pricing

### 3.2 SDK & Service Dependencies

| Google Cloud SDK | AWS SDK | Complexity | Notes |
|-----------------|---------|------------|-------|
| google-cloud-secret-manager | **AWS Secrets Manager** | LOW | Direct SDK swap |
| google-cloud-storage | **boto3 (S3)** | LOW | Object storage |
| google-cloud-pubsub | **boto3 (SNS/SQS)** | LOW | Messaging |
| google-cloud-logging | **boto3 (CloudWatch Logs)** | LOW | Logging |
| google-genai | **boto3 (Bedrock)** | OPTIONAL | AI service |
| google-cloud-aiplatform | **boto3 (SageMaker/Bedrock)** | OPTIONAL | AI service |

**Migration Impact:** Since these services are currently inactive (using local implementations), SDK replacement can be deferred to Phase 3 (production hardening).


### 3.3 Proposed AWS Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Internet Users                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │   AWS Amplify Hosting (CDN)   │ ← Frontend (React SPA)
         │   - Static site hosting       │
         │   - Global CDN distribution   │
         └───────────────┬───────────────┘
                         │ HTTPS API Calls
                         ▼
         ┌───────────────────────────────┐
         │   AWS App Runner Services     │ ← Backend (19 services)
         │   - Auto-scaling containers   │
         │   - Built-in load balancing   │
         │   - VPC integration           │
         └───────────────┬───────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │   Amazon ECR Repositories     │ ← Container Images
         │   - Private registries        │
         │   - Image scanning            │
         └───────────────────────────────┘
```

**Future Enhancements (Phase 3):**
- AWS Secrets Manager (runtime secrets)
- Amazon S3 (document storage)
- Amazon RDS/Aurora (production database)
- Amazon SQS/SNS (event messaging)
- Amazon Bedrock (AI services)
- CloudWatch (monitoring & logging)

---

## 4. MIGRATION COMPLEXITY ANALYSIS

### 4.1 Low Complexity Items (Quick Wins)

#### ✅ Frontend Migration (2-4 hours)
- **Task:** Deploy React SPA to AWS Amplify Hosting
- **Changes Required:**
  1. Update build args in Dockerfile.portal with AWS App Runner URLs
  2. Build static assets: `npm run build`
  3. Deploy to Amplify Hosting via AWS Console or CLI
- **Code Changes:** None (only build configuration)

#### ✅ Container Registry Migration (1-2 hours)
- **Task:** Migrate Docker images to Amazon ECR
- **Changes Required:**
  1. Create ECR repositories
  2. Authenticate Docker with ECR
  3. Tag and push existing images
- **Code Changes:** None (images work as-is)

#### ✅ Backend Services Migration (4-8 hours per service)
- **Task:** Deploy 19 FastAPI services to AWS App Runner
- **Changes Required:**
  1. Create App Runner service from ECR image
  2. Configure environment variables
  3. Set health check to `/livez`
  4. Configure auto-scaling (1-10 instances)
- **Code Changes:** None (FastAPI code unchanged)
- **Total Estimate:** 1-2 days for all services (can parallelize)

### 4.2 Moderate Complexity Items

#### ⚠️ CI/CD Pipeline Migration (1-2 days)
- **Task:** Replace Cloud Build with AWS CodeBuild
- **Changes Required:**
  1. Create `buildspec.yml` (replaces `cloudbuild-portal.yaml`)
  2. Update deployment scripts (replace `gcloud` with `aws` CLI)
  3. Configure CodePipeline for automation
  4. Set up IAM roles
- **Alternative:** Manual deployment initially, automate later


#### ⚠️ Google Cloud SDK Replacement (2-4 days - OPTIONAL)
- **Task:** Replace google-cloud-* imports with boto3
- **Changes Required:**
  1. Update `pyproject.toml` dependencies
  2. Replace SDK imports in adapter classes
  3. Update Secret Manager calls
  4. Update Storage/Logging/Pub-Sub calls
- **Status:** Currently using local implementations
- **Recommendation:** Defer to Phase 3 (production hardening)

#### ⚠️ AI Service Migration (3-5 days - OPTIONAL)
- **Task:** Replace Vertex AI with Amazon Bedrock
- **Changes Required:**
  1. Update credit-engine adapters
  2. Replace Vertex AI SDK calls with Bedrock
  3. Test AI-based credit decisioning
- **Fallback Available:** RULE_ENGINE adapter works without AI
- **Recommendation:** Use fallback initially, migrate AI in Phase 3

### 4.3 Already Containerized (MAJOR ADVANTAGE)

✅ **Containers are platform-agnostic:**
- Dockerfile works on any container platform
- No runtime dependencies on Google Cloud inside containers
- Health checks use standard HTTP endpoints
- Environment variables follow standard patterns
- **Migration Impact:** Containers deploy to AWS with zero code changes

### 4.4 Overall Complexity Score

| Area | Complexity | Effort | Blocking |
|------|-----------|--------|----------|
| Container Registry | LOW | 1-2 hours | Yes |
| Frontend Deployment | LOW | 2-4 hours | Yes |
| Backend Deployment | LOW | 1-2 days | Yes |
| CI/CD Pipeline | MODERATE | 1-2 days | No (manual fallback) |
| SDK Replacement | MODERATE | 2-4 days | No (currently inactive) |
| AI Migration | MODERATE | 3-5 days | No (has fallback) |

**Total Blocking Work:** 2-3 days (registry + frontend + backend)  
**Total Optional Work:** 6-11 days (CI/CD + SDK + AI)

---

## 5. ESTIMATED DEPLOYMENT STEPS

### Phase 1: AWS Account Setup (1-2 hours)

**Step 1.1: Create/Configure AWS Account**
```bash
# Install AWS CLI
# Configure credentials
aws configure
# Set default region (e.g., ap-south-1 for Mumbai)
aws configure set region ap-south-1
```

**Step 1.2: Create IAM Roles**
- ECR access role
- App Runner execution role
- CodeBuild service role (optional)

### Phase 2: Container Registry Migration (1-2 hours)

**Step 2.1: Create ECR Repositories**
```bash
# Create repository for frontend
aws ecr create-repository --repository-name aarohan/portal --region ap-south-1

# Create repository for backend services
aws ecr create-repository --repository-name aarohan/backend --region ap-south-1
```

**Step 2.2: Authenticate Docker with ECR**
```bash
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.ap-south-1.amazonaws.com
```

**Step 2.3: Tag and Push Existing Images**
```bash
# Tag backend image
docker tag aarohan-backend:latest \
  <account-id>.dkr.ecr.ap-south-1.amazonaws.com/aarohan/backend:latest

# Push to ECR
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/aarohan/backend:latest

# Repeat for frontend
docker tag aarohan-portal:latest \
  <account-id>.dkr.ecr.ap-south-1.amazonaws.com/aarohan/portal:latest
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/aarohan/portal:latest
```


### Phase 3: Backend Deployment to AWS App Runner (1-2 days)

**Step 3.1: Create App Runner Service (Example: auth-service)**
```bash
aws apprunner create-service \
  --service-name aarohan-auth-service \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "<account-id>.dkr.ecr.ap-south-1.amazonaws.com/aarohan/backend:latest",
      "ImageConfiguration": {
        "Port": "9000",
        "RuntimeEnvironmentVariables": {
          "PYTHONPATH": "/app/services/ese-core:/app/services/auth-service",
          "INTEGRATION_PROFILE": "DEMO",
          "ACTIVE_DATASET": "msme"
        }
      },
      "ImageRepositoryType": "ECR"
    }
  }' \
  --instance-configuration '{
    "Cpu": "1024",
    "Memory": "2048"
  }' \
  --health-check-configuration '{
    "Protocol": "HTTP",
    "Path": "/livez",
    "Interval": 10,
    "Timeout": 5,
    "HealthyThreshold": 2,
    "UnhealthyThreshold": 3
  }' \
  --auto-scaling-configuration-arn <auto-scaling-config-arn> \
  --region ap-south-1
```

**Step 3.2: Retrieve Service URLs**
```bash
aws apprunner describe-service \
  --service-arn <service-arn> \
  --query 'Service.ServiceUrl' \
  --output text
```

**Step 3.3: Repeat for All 19 Services**

| Service | Port | Command |
|---------|------|---------|
| auth-service | 9000 | `uvicorn app.main:app --host 0.0.0.0 --port 9000` |
| onboarding-service | 9001 | `uvicorn app.main:app --host 0.0.0.0 --port 9001` |
| ... | ... | (Repeat pattern for all services) |


### Phase 4: Frontend Deployment to AWS Amplify (2-4 hours)

**Option A: Amplify Hosting (Recommended for Static SPA)**

**Step 4.1: Build Frontend with AWS Backend URLs**
```bash
cd apps/customer-portal

# Set environment variables
export VITE_API_BASE_URL=https://<app-runner-backend-url>
export VITE_AUTH_API_BASE_URL=https://<app-runner-auth-url>

# Build
npm run build
```

**Step 4.2: Deploy to Amplify**
```bash
# Create Amplify app
aws amplify create-app --name aarohan-portal --region ap-south-1

# Create deployment
aws amplify create-deployment \
  --app-id <app-id> \
  --branch-name main

# Upload build artifacts (get upload URL from previous command)
cd dist
zip -r ../build.zip .
aws s3 cp ../build.zip <presigned-upload-url>
```

**Option B: App Runner with Nginx Container (Alternative)**

**Step 4.3: Build and Deploy Container**
```bash
# Build with AWS URLs
docker build -f Dockerfile.portal \
  --build-arg VITE_API_BASE_URL=https://<app-runner-backend-url> \
  --build-arg VITE_AUTH_API_BASE_URL=https://<app-runner-auth-url> \
  -t aarohan-portal:latest .

# Push to ECR
docker tag aarohan-portal:latest \
  <account-id>.dkr.ecr.ap-south-1.amazonaws.com/aarohan/portal:latest
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/aarohan/portal:latest

# Create App Runner service
aws apprunner create-service \
  --service-name aarohan-portal \
  --source-configuration '{ ... }' \
  --instance-configuration '{"Cpu": "512", "Memory": "1024"}' \
  --region ap-south-1
```


### Phase 5: Integration Testing (1-2 days)

**Step 5.1: Health Check Validation**
```bash
# Test each backend service
for service in auth onboarding consent gst aa fhc credit cam rm exec ews ckyc mca epfo treds ocen ese-admin
do
  echo "Testing $service..."
  curl https://<app-runner-$service-url>/livez
done
```

**Step 5.2: Run Existing Test Suite**
```bash
# Backend regression tests
pytest tests/test_regression_e2e.py -v
pytest tests/test_workflow_engine.py -v
pytest tests/test_onboarding_module.py -v

# Frontend smoke tests
cd apps/customer-portal
npm test
```

**Step 5.3: Manual Testing Checklist**
- [ ] Frontend loads successfully
- [ ] Login flow works (auth-service)
- [ ] Customer onboarding flow
- [ ] GST/AA/EPFO data fetch
- [ ] Credit decisioning
- [ ] Executive dashboard
- [ ] Demo Studio functionality
- [ ] Simulation engine behavior

### Phase 6: Documentation Updates (1 day)

**Step 6.1: Create New Deployment Scripts**
- `deploy-apprunner.sh` (Bash)
- `deploy-apprunner.ps1` (PowerShell)

**Step 6.2: Update Documentation**
- Create `AWS_DEPLOYMENT_GUIDE.md`
- Update `PROJECT_CONTEXT.md` with AWS details
- Update environment variable documentation
- Archive `CLOUD_RUN_DEPLOYMENT.md`

---

## 6. POTENTIAL RISKS & MITIGATIONS

### Risk 1: Service Discovery Between Microservices
**Risk Level:** MEDIUM  
**Description:** Microservices need to discover each other's URLs  
**Impact:** Inter-service communication failures  
**Mitigation:**
- Store service URLs in environment variables for each App Runner service
- Use AWS Systems Manager Parameter Store for centralized configuration
- Implement service discovery via environment variable injection
- Document all service endpoints in a central registry

### Risk 2: Container Health Check Differences
**Risk Level:** LOW  
**Description:** App Runner health check behavior may differ from Cloud Run  
**Impact:** Services may fail health checks unnecessarily  
**Mitigation:**
- All services already expose `/livez` endpoint (standard HTTP)
- Test health checks during deployment
- Adjust timeout/interval parameters if needed
- App Runner health checks are well-documented and configurable

### Risk 3: Environment Variable Management
**Risk Level:** LOW  
**Description:** 19 services require consistent environment variable configuration  
**Impact:** Configuration drift, service failures  
**Mitigation:**
- Create shell script to deploy all services with consistent env vars
- Use AWS Systems Manager Parameter Store for shared configuration
- Document all required environment variables per service
- Implement configuration validation in startup scripts

### Risk 4: Network Latency Between Services
**Risk Level:** LOW  
**Description:** Inter-service calls may have different latency characteristics  
**Impact:** Increased response times  
**Mitigation:**
- Deploy all services in same AWS region (ap-south-1)
- Enable VPC integration for private networking
- Monitor service-to-service latency
- Current architecture already handles async patterns well


### Risk 5: Cost Management
**Risk Level:** MEDIUM  
**Description:** AWS costs may differ from GCP (suspended account baseline unknown)  
**Impact:** Budget overruns  
**Mitigation:**
- Start with minimal instance sizes (1 vCPU, 2GB RAM)
- Configure auto-scaling conservatively (1-3 instances initially)
- Use AWS Cost Explorer to monitor spending
- Set up billing alerts
- Consider reserved capacity after usage patterns stabilize

### Risk 6: Data Migration (If Needed)
**Risk Level:** LOW  
**Description:** Current system uses local SQLite, no cloud database  
**Impact:** None for initial migration  
**Mitigation:**
- SQLite databases are in `ese/` folder, included in container volumes
- No external database migration required
- Future production database (RDS/Aurora) is Phase 3 concern

### Risk 7: CI/CD Pipeline Gap
**Risk Level:** MEDIUM  
**Description:** No automated deployment initially  
**Impact:** Manual deployment burden, slower iterations  
**Mitigation:**
- Phase 1: Manual deployment using AWS CLI scripts (acceptable)
- Phase 2: Implement CodePipeline + CodeBuild automation
- Document manual deployment procedure thoroughly
- Automate most critical service deployments first (auth, onboarding, credit)

### Risk 8: Rollback Complexity
**Risk Level:** LOW  
**Description:** Need to rollback if migration fails  
**Impact:** Downtime if rollback takes too long  
**Mitigation:**
- Keep GCP deployment scripts and documentation
- Document rollback procedure before starting migration
- Test rollback process in development environment
- **Note:** GCP account is suspended, so rollback may not be possible
- Consider this a one-way migration with thorough testing required

---

## 7. WHAT STAYS EXACTLY THE SAME

### ✅ Business Logic & Application Code (100% Preserved)

**Frontend (Zero Changes):**
- React 19 application code
- TypeScript components
- Material UI components
- Zustand state management
- API client code (axios)
- Form validation (React Hook Form + Zod)
- Routing logic
- Business workflows
- Demo Studio functionality
- All UI screens and pages

**Backend (Zero Changes):**
- FastAPI application code (19 services)
- Pydantic models and schemas
- SQLAlchemy database models
- Business logic and algorithms
- Credit decisioning rules
- Financial health calculations
- CAM generation logic
- Authentication & authorization (JWT)
- API endpoints and contracts
- Request/response models
- Validation logic
- Error handling
- Middleware (CORS, logging, correlation IDs)

### ✅ Project Structure (100% Preserved)

```
Project-AAROHAN/
├── apps/
│   └── customer-portal/          ← No changes
├── services/
│   ├── auth-service/             ← No changes
│   ├── onboarding-service/       ← No changes
│   ├── (17 more services)/       ← No changes
│   ├── ese-core/                 ← No changes (simulation engine)
│   └── ese-admin-service/        ← No changes
├── tests/                        ← No changes
├── ese/                          ← No changes (demo data)
├── Dockerfile                    ← No changes
└── Dockerfile.portal             ← No changes
```


### ✅ Runtime Dependencies (100% Preserved)

**Python Dependencies (pyproject.toml):**
- FastAPI, Uvicorn, Pydantic (unchanged)
- SQLAlchemy, Alembic (unchanged)
- python-jose, passlib (auth - unchanged)
- httpx (HTTP client - unchanged)
- pytest, black, mypy (dev tools - unchanged)
- **Only Change:** Remove/replace 6 google-cloud-* packages (Phase 3)

**Node Dependencies (package.json):**
- React, TypeScript, Vite (unchanged)
- Material UI, Emotion (unchanged)
- Zustand, Axios (unchanged)
- All frontend dependencies (unchanged)

### ✅ Docker Containers (100% Compatible)

**Why Containers Are Perfect for Migration:**
- Platform-agnostic runtime environment
- Dockerfile works on any container platform (GCP, AWS, Azure, local)
- No cloud-specific code inside containers
- Health checks use standard HTTP (not cloud-specific)
- Environment variables use standard patterns
- Port configuration is standard

**Result:** Containers deploy to AWS App Runner with ZERO code changes

### ✅ Database & Storage (100% Preserved)

**Current Implementation:**
- SQLite databases in `ese/` folder
- Local file system storage
- Simulation data files
- No cloud database dependency

**Migration Impact:** None. SQLite files remain in containers.

### ✅ Testing (100% Preserved)

**Test Suite:**
- `tests/test_regression_e2e.py` - End-to-end tests (unchanged)
- `tests/test_workflow_engine.py` - Workflow tests (unchanged)
- `tests/test_onboarding_module.py` - Onboarding tests (unchanged)
- All service-level tests (unchanged)

**Result:** Existing test suite validates migration success

---

## 8. WHAT MUST CHANGE

### 🔧 Critical Changes (Phase 2 - Required)

#### 1. Deployment Scripts (HIGH PRIORITY)

**Files to Replace:**
- `cloudbuild-portal.yaml` → `buildspec.yml` (AWS CodeBuild format)
- `deploy-cloudrun.sh` → `deploy-apprunner.sh`
- `deploy-cloudrun.ps1` → `deploy-apprunner.ps1`

**Changes in Scripts:**
```bash
# OLD (Google Cloud)
gcloud config set project "$PROJECT_ID"
gcloud auth configure-docker "$REGION-docker.pkg.dev"
docker push asia-south1-docker.pkg.dev/...
gcloud run deploy "$SERVICE_NAME" ...

# NEW (AWS)
aws configure set region ap-south-1
aws ecr get-login-password | docker login ...
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/...
aws apprunner create-service ...
```

#### 2. Frontend Build Configuration (HIGH PRIORITY)

**File:** `Dockerfile.portal` build arguments

**Change:**
```dockerfile
# OLD
--build-arg VITE_API_BASE_URL=https://aarohan-demo-platform-679889922969.asia-south1.run.app

# NEW
--build-arg VITE_API_BASE_URL=https://<app-runner-backend-url>.ap-south-1.awsapprunner.com
```

#### 3. Container Image Paths (HIGH PRIORITY)

**All references to:**
```
asia-south1-docker.pkg.dev/aarohan-msme-platform/aarohan/
```

**Must change to:**
```
<account-id>.dkr.ecr.ap-south-1.amazonaws.com/aarohan/
```

**Files affected:**
- `cloudbuild-portal.yaml`
- `deploy-cloudrun.sh`
- `deploy-cloudrun.ps1`
- Any CI/CD documentation
