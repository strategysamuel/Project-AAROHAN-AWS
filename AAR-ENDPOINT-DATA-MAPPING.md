# AAR-ENDPOINT-DATA-MAPPING

## Endpoints

### /customers
Frontend → API Gateway → ALB (Port 9001) → FastAPI (onboarding-service) → Database (`onboarding_customers`) → Response

### /customers/{id}/start-workflow
Frontend → API Gateway → ALB (Port 9001) → FastAPI (onboarding-service) → Database (`onboarding_customers`) → Response

### /gst/sync/{id}
Frontend → API Gateway → ALB (Port 9003) → FastAPI (gst-service) → Database (`gst_profiles`) → Response

### /ckyc/records
Frontend → API Gateway → ALB (Port 9011) → FastAPI (ckyc-service) → Database (`ckyc_records`) → Response

### /aa/link/{id}
Frontend → API Gateway → ALB (Port 9004) → FastAPI (aa-service) → Database (`aa_linked_accounts`) → Response

### /epfo/sync/{id}
Frontend → API Gateway → ALB (Port 9013) → FastAPI (epfo-service) → Database (`epfo_profiles`) → Response

### /mca/sync/{id}
Frontend → API Gateway → ALB (Port 9012) → FastAPI (mca-service) → Database (`mca_company_profiles`) → Response

### /fhc/generate/{id}
Frontend → API Gateway → ALB (Port 9005) → FastAPI (fhc-service) → Database (`fhc_cards`) → Response

### /credit/evaluate/{id}
Frontend → API Gateway → ALB (Port 9006) → FastAPI (credit-engine) → Database (`ai_credit_decisions`) → Response

### /cam/generate/{id}
Frontend → API Gateway → ALB (Port 9007) → FastAPI (cam-service) → Database (`cam_records`) → Response

### /exec/dashboard
Frontend → API Gateway → ALB (Port 9009) → FastAPI (exec-service) → Database (`exec_kpis`) → Response

