with open("AAR-ENDPOINT-DATA-MAPPING.md", "w", encoding="utf-8") as f:
    f.write("# AAR-ENDPOINT-DATA-MAPPING\n\n")
    f.write("## Endpoints\n\n")
    
    endpoints = [
        {"route": "/customers", "service": "onboarding-service", "db": "onboarding_customers", "port": 9001},
        {"route": "/customers/{id}/start-workflow", "service": "onboarding-service", "db": "onboarding_customers", "port": 9001},
        {"route": "/gst/sync/{id}", "service": "gst-service", "db": "gst_profiles", "port": 9003},
        {"route": "/ckyc/records", "service": "ckyc-service", "db": "ckyc_records", "port": 9011},
        {"route": "/aa/link/{id}", "service": "aa-service", "db": "aa_linked_accounts", "port": 9004},
        {"route": "/epfo/sync/{id}", "service": "epfo-service", "db": "epfo_profiles", "port": 9013},
        {"route": "/mca/sync/{id}", "service": "mca-service", "db": "mca_company_profiles", "port": 9012},
        {"route": "/fhc/generate/{id}", "service": "fhc-service", "db": "fhc_cards", "port": 9005},
        {"route": "/credit/evaluate/{id}", "service": "credit-engine", "db": "ai_credit_decisions", "port": 9006},
        {"route": "/cam/generate/{id}", "service": "cam-service", "db": "cam_records", "port": 9007},
        {"route": "/exec/dashboard", "service": "exec-service", "db": "exec_kpis", "port": 9009}
    ]
    
    for ep in endpoints:
        f.write(f"### {ep['route']}\n")
        f.write(f"Frontend → API Gateway → ALB (Port {ep['port']}) → FastAPI ({ep['service']}) → Database (`{ep['db']}`) → Response\n\n")

print("Generated AAR-ENDPOINT-DATA-MAPPING.md")
