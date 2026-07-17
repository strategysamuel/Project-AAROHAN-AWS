# AAR-CLOUD-DEMO-SEED-REPORT

## 1. Production Persistence Layer Identification
Based on an audit of the application source code and infrastructure definitions, the production persistence layer for the AWS backend is **Ephemeral SQLite**.

**Evidence:**
- Every microservice (e.g., `ckyc-service`, `onboarding-service`, `auth-service`) hardcodes its database connection to `sqlite:///./aarohan_local.db`.
- The AWS infrastructure (`cloudformation-ecs-networking.yml`) provisions **ECS Fargate** tasks with no attached persistent storage (e.g., EFS) and no external database resources (e.g., RDS, DynamoDB).
- Consequently, any data seeded into these containers via the API will only exist in memory/ephemeral disk and will be permanently lost when the ECS tasks cycle or restart.

## 2. Seeding the Golden Dataset into AWS
Execution of the Golden Dataset seeding against the AWS environment (`https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com`) **FAILED**. 

**Root Cause:**
The AWS ALB routing is fundamentally misconfigured, preventing access to the required microservices:
- The ALB (`cloudformation-ecs-networking.yml`) only maps `/auth/*`, `/gst/*`, `/api/*`, and `/exec/*`.
- Requests for other workflows (e.g., `/ckyc/search`, `/aa/discover`, `/epfo/sync`) fall through to the ALB's **Default Action**, which forwards traffic to the `IdentityTargetGroup` (`auth-service` on port 9000).
- Since `auth-service` does not have endpoints for CKYC, AA, EPFO, etc., the FastAPI router correctly returns HTTP 404 (`{"detail":"Not Found"}`).
- Additionally, `/api/*` and `/gst/*` are both routed exclusively to Port 9001 (`onboarding-service`), completely ignoring the other 10 services running inside the Lending container on ports 9002-9013.

## 3. Verification of Browser Workflows
Due to the routing misconfigurations detailed above, the API Gateway returns HTTP 404 for the seeding endpoints. Therefore, the Golden Dataset cannot be seeded, and the Amplify frontend continues to display the "Persona not found" error alongside other fallback behaviors.

## 4. Conclusion
**Status: BLOCKED**
I cannot claim success for this objective. The AWS environment cannot be seeded until the FastAPI API routers and ALB routing rules are aligned. Resolving these 404 mismatches is a prerequisite before the cloud demo data can be populated.
