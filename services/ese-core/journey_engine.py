import sys
import os
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Bootstrap virtualenv
def bootstrap_virtualenv():
    import glob
    possible_paths = [
        "C:\\Users\\DELL\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\aarohan-backend-*\\Lib\\site-packages",
        "C:\\Users\\DELL\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\aarohan-backend-*\\lib\\site-packages"
    ]
    for pattern in possible_paths:
        for path in glob.glob(pattern):
            if path not in sys.path:
                sys.path.insert(0, path)

bootstrap_virtualenv()

# Configure logger
logger = logging.getLogger("ese-journey")

# Setup path to import app dynamically if in Local Import Mode
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Microservice port mapping for HTTP mode
PORT_MAP = {
    "onboarding-service": 9001,
    "consent-service": 9002,
    "gst-service": 9003,
    "aa-service": 9004,
    "fhc-service": 9005,
    "credit-engine": 9006,
    "cam-service": 9007,
    "rm-workspace-service": 9008,
    "exec-service": 9009,
    "ews-service": 9010,
    "ckyc-service": 9011,
    "mca-service": 9012,
    "epfo-service": 9013,
    "treds-service": 9014,
    "ocen-uli-service": 9015,
}

class DemoJourneyEngine:
    def __init__(self, mode: str = "LOCAL"):
        """
        mode: "LOCAL" (uses TestClient and direct imports) or "HTTP" (uses requests/httpx against running services)
        """
        self.mode = mode.upper()
        self.clients = {}
        self.history = []

    def _get_client(self, service_name: str):
        if service_name in self.clients:
            return self.clients[service_name]

        if self.mode == "LOCAL":
            from fastapi.testclient import TestClient
            import importlib.util
            
            file_path = os.path.join(WORKSPACE_ROOT, "services", service_name, "app", "main.py")
            module_name = f"dynamic_{service_name.replace('-', '_')}"
            
            # Clear app cache
            for k in list(sys.modules.keys()):
                if k == "app" or k.startswith("app."):
                    sys.modules.pop(k, None)
                    
            if module_name in sys.modules:
                app_instance = sys.modules[module_name].app
            else:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                
                path = os.path.join(WORKSPACE_ROOT, "services", service_name)
                sys.path.insert(0, path)
                try:
                    spec.loader.exec_module(module)
                    app_instance = module.app
                finally:
                    if path in sys.path:
                        sys.path.remove(path)
                        
            client = TestClient(app_instance)
            self.clients[service_name] = client
            return client
        else:
            # HTTP Mode
            import httpx
            port = PORT_MAP.get(service_name)
            if not port:
                raise ValueError(f"No port mapped for {service_name}")
            client = httpx.Client(base_url=f"http://localhost:{port}", timeout=10.0)
            self.clients[service_name] = client
            return client

    def run_journey(self, journey_name: str, customer_id: int = 120) -> Dict[str, Any]:
        journey_id = str(uuid.uuid4())
        start_time = time.time()
        audit_log = []
        timeline = []
        
        def log_step(step_name: str, status: str, details: Optional[str] = None):
            timestamp = datetime.utcnow().isoformat() + "Z"
            audit_log.append({
                "timestamp": timestamp,
                "step": step_name,
                "status": status,
                "details": details
            })
            timeline.append({
                "step": step_name,
                "elapsed_ms": round((time.time() - start_time) * 1000, 2)
            })
            logger.info(f"JOURNEY | {step_name} | {status} | {details}")

        log_step(f"START_JOURNEY: {journey_name}", "SUCCESS", f"Customer ID: {customer_id}")

        try:
            if journey_name == "Customer Onboarding":
                client = self._get_client("onboarding-service")
                res = client.get("/customers")
                log_step("Fetch customers list", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
            elif journey_name == "Financial Health Card":
                # GST profile
                gst_client = self._get_client("gst-service")
                res = gst_client.post(f"/gst/sync/{customer_id}", json={"gstin": f"27SIMPT0001K1Z5"})
                log_step("GST Profile Sync", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
                # AA statements
                aa_client = self._get_client("aa-service")
                res = aa_client.post(f"/aa/link/{customer_id}", json=[])
                log_step("AA Statements Link", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
                # FHC Score calculation
                fhc_client = self._get_client("fhc-service")
                res = fhc_client.post(f"/fhc/calculate/{customer_id}")
                log_step("Calculate FHC score", "SUCCESS" if res.status_code == 200 else "FAILED", f"Score: {res.json().get('fhc_score') if res.status_code == 200 else 'N/A'}")
                
            elif journey_name == "Complete MSME Lending Journey":
                # 1. CKYC search
                ckyc_client = self._get_client("ckyc-service")
                res = ckyc_client.post("/ckyc/search", json={"pan": "SIMPT0001K"})
                log_step("CKYC Registry Search", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
                # 2. Onboard & KYC verify
                res = ckyc_client.post(f"/ckyc/verify/{customer_id}", json={"customer_id": customer_id, "checked_by": "RM-101"})
                log_step("CKYC RM Identity Audit", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
                # 3. GST Sync
                gst_client = self._get_client("gst-service")
                res = gst_client.post(f"/gst/sync/{customer_id}", json={"gstin": f"27SIMPT0001K1Z5"})
                log_step("GST Filing Ledger Sync", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
                # 4. Account Aggregator Link & Sync
                aa_client = self._get_client("aa-service")
                res = aa_client.post(f"/aa/link/{customer_id}", json=[])
                res = aa_client.post(f"/aa/sync/{customer_id}", json={"consent_id": 12345})
                log_step("Account Aggregator Banking Sync", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
                # 5. EPFO Payroll Sync
                epfo_client = self._get_client("epfo-service")
                res = epfo_client.post(f"/epfo/sync/{customer_id}", json={"establishment_id": f"MHBAN00000000000000{customer_id:04d}", "esic_registration_num": "55000123450000101"})
                log_step("EPFO Corporate Payroll Audit", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
                # 6. MCA Registry Sync
                mca_client = self._get_client("mca-service")
                res = mca_client.post(f"/mca/sync/{customer_id}", json={"cin": f"U72900KA2020PTC{customer_id:06d}"})
                log_step("MCA Business Registry Verify", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
                # 7. Financial Health Card calculation
                fhc_client = self._get_client("fhc-service")
                res = fhc_client.post(f"/fhc/calculate/{customer_id}")
                log_step("Financial Health Card compilation", "SUCCESS" if res.status_code == 200 else "FAILED", f"Score: {res.json().get('fhc_score') if res.status_code == 200 else 'N/A'}")
                
                # 8. Credit Engine Evaluate
                credit_client = self._get_client("credit-engine")
                res = credit_client.post(f"/credit/evaluate/{customer_id}")
                log_step("AI Credit Appraisal Engine run", "SUCCESS" if res.status_code == 200 else "FAILED", f"Decision: {res.json().get('recommendation') if res.status_code == 200 else 'N/A'}")
                
                # 9. CAM Generation
                cam_client = self._get_client("cam-service")
                res = cam_client.post(f"/cam/generate/{customer_id}")
                log_step("CAM Compilation & Vector Load", "SUCCESS" if res.status_code == 201 else "FAILED", f"Status: {res.status_code}")
                
                # 10. OCEN Flow
                ocen_client = self._get_client("ocen-uli-service")
                res = ocen_client.post("/ocen/eligibility", json={"customer_id": customer_id, "annual_revenue": 15000000.0, "credit_score": 780, "requested_amount": 500000.0})
                res = ocen_client.post("/ocen/apply", json={"customer_id": customer_id, "requested_amount": 500000.0, "requested_tenure_months": 12, "purpose": "Expansion"})
                app_id = res.json().get("id") if res.status_code == 200 else None
                if app_id:
                    res = ocen_client.get(f"/ocen/applications/{app_id}/offers")
                    offer_id = res.json()[0]["id"] if res.status_code == 200 and len(res.json()) > 0 else None
                    if offer_id:
                        res = ocen_client.post("/ocen/offers/accept", json={"offer_id": offer_id})
                        res = ocen_client.post(f"/ocen/disburse/{app_id}")
                log_step("OCEN Smart Disbursal Gateway", "SUCCESS" if app_id else "FAILED", f"Application ID: {app_id}")
                
            elif journey_name == "Fraud Detection Journey":
                credit_client = self._get_client("credit-engine")
                res = credit_client.post(f"/credit/evaluate/{customer_id}")
                log_step("Evaluate fraud & blacklist registries", "SUCCESS" if res.status_code == 200 else "FAILED", f"Fraud Status: {res.json().get('rbi_fraud_status') if res.status_code == 200 else 'N/A'}")
                
            elif journey_name == "OCEN Marketplace Journey":
                ocen_client = self._get_client("ocen-uli-service")
                res = ocen_client.post("/ocen/eligibility", json={"customer_id": customer_id, "annual_revenue": 10000000.0, "credit_score": 720, "requested_amount": 200000.0})
                log_step("Check OCEN product eligibility", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
            elif journey_name == "AI Credit Decision Journey":
                credit_client = self._get_client("credit-engine")
                res = credit_client.post(f"/credit/evaluate/{customer_id}")
                log_step("Dispatch to Gemini Underwriter", "SUCCESS" if res.status_code == 200 else "FAILED", f"Outcome: {res.json().get('recommendation') if res.status_code == 200 else 'N/A'}")
                
            elif journey_name == "Board Presentation Journey":
                # Quick overview run of FHC + Credit + Dashboard
                fhc_client = self._get_client("fhc-service")
                res = fhc_client.post(f"/fhc/calculate/{customer_id}")
                credit_client = self._get_client("credit-engine")
                res = credit_client.post(f"/credit/evaluate/{customer_id}")
                log_step("Execute board-ready showcase flow", "SUCCESS" if res.status_code == 200 else "FAILED", f"Status: {res.status_code}")
                
            else:
                raise ValueError(f"Unknown demo journey: {journey_name}")

            log_step(f"END_JOURNEY: {journey_name}", "SUCCESS")
            status = "SUCCESS"
        except Exception as e:
            log_step(f"END_JOURNEY_FAILED: {journey_name}", "FAILED", str(e))
            status = "FAILED"

        duration_ms = (time.time() - start_time) * 1000
        summary = {
            "journey_id": journey_id,
            "journey_name": journey_name,
            "status": status,
            "duration_ms": round(duration_ms, 2),
            "timeline": timeline,
            "audit_log": audit_log
        }
        self.history.append(summary)
        return summary
