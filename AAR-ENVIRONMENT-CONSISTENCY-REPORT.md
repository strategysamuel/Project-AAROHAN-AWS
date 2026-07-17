# AAR-ENVIRONMENT-CONSISTENCY-REPORT

## 1. Seeded Environment
The `seed_hackathon_demo.py` script executed successfully and populated the **local development environment**.
- **Host:** `localhost` (Local Docker Compose Network)
- **Ports:** `9003`, `9004`, `9005`, `9006`, `9007`, `9011`, `9012`, `9013`
- **Containers:** 
  - `onboarding-service`
  - `ckyc-service`
  - `aa-service`
  - `gst-service`
  - `epfo-service`
  - `mca-service`
  - `fhc-service`
  - `credit-decisioning`
  - `cam-generation`
- **Database:** Local containerized databases (SQLite / isolated Postgres volumes created by docker-compose)
- **API Base URL:** `http://localhost:90XX`

## 2. Browser Environment
The browser application is currently configured to point to the **AWS Cloud Environment**, not the local Docker network.
- **Frontend Config:** `apps/customer-portal/.env`
- **VITE_API_BASE_URL:** `https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com`
- **Gateway URL:** AWS API Gateway
- **ALB URL / ECS Containers:** The API Gateway routes traffic to the AWS cloud-deployed ECS tasks and AWS RDS instances, which are completely separate from the local docker-compose network.

## 3. Local Backend Verification (Customer 99)
For Customer ID 99 in the **running local Docker backend** (`localhost:90XX`), all data exists perfectly:
- **CKYC:** `http://localhost:9011/ckyc/records/99` returns `200 OK`
- **GST:** `http://localhost:9003/gst/returns/99` returns `200 OK`
- **Account Aggregator:** `http://localhost:9004/aa/analytics/99` returns `200 OK`
- **EPFO:** `http://localhost:9013/epfo/employees/99` returns `200 OK`
- **MCA:** `http://localhost:9012/mca/directors/99` returns `200 OK`
- **FHC:** `http://localhost:9005/fhc/99` returns `200 OK`

## 4. Comparison (Seeded vs Browser)
The environments differ entirely because they are physically distinct infrastructure stacks:
- **The Seeded Environment** is the local Docker network. The `seed_hackathon_demo.py` script ran locally, injecting data directly into the `localhost` endpoints, which persisted the data into the local Docker volumes.
- **The Browser Environment** is pointed at AWS API Gateway (`ryzm03zs5l...`). The cloud databases attached to this API Gateway were **never seeded**. Therefore, when the browser requests `customer_id=99` from the cloud, the cloud database returns `404 Not Found` because the "Golden Dataset" injection only occurred on the local machine.

## 5. Browser Network Requests (AWS Cloud)
If the browser attempts to load the modules, the network tab will show the following failing requests directed at the cloud:

| Module | Request URL | Status | Response Body |
|--------|-------------|--------|---------------|
| Customer Onboarding | `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/onboarding/personas/99` | 404 | `{"errorCode":"AAR-ERR-404","message":"Persona not found."...}` |
| CKYC | `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/ckyc/records/99` | 404 | `{"errorCode":"AAR-ERR-404","message":"CKYC record not found."...}` |
| EPFO | `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/epfo/employees/99` | 404 | `{"errorCode":"AAR-ERR-404","message":"EPFO profile not found."...}` |
| MCA | `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/mca/directors/99` | 404 | `{"errorCode":"AAR-ERR-404","message":"MCA Profile not found."...}` |
| FHC | `GET https://ryzm03zs5l.execute-api.ap-south-1.amazonaws.com/fhc/99` | 404 | `{"errorCode":"AAR-ERR-404","message":"FHC not found."...}` |

### Conclusion
The reported **GREEN** status from the previous certification applies **only to the local Docker runtime**. The application as configured in the browser is broken because the frontend `.env` is hardcoded to a cloud environment that lacks the required hackathon demo dataset. To resolve this and see the data in the browser, either the frontend `.env` must be updated to point to `localhost`, or the cloud databases must be seeded.
