import sys
import os
import random
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from adapters.base import ExternalIntegrationAdapter, AdapterRequest, AdapterResponse
from adapter_factory import register_adapter, GSTN, AA, EPFO, MCA, RBI_FRAUD, OCEN, VERTEX_AI, CAM, FHC, DEMO, TRAINING, UAT, PERFORMANCE
from db_helper import get_sim_db_session
from models import ESEGSTRecord, ESETransaction, ESEEPFORecord, ESEMCARecord, ESELoanApplication, ESECustomer

def apply_latency():
    active_profile = os.getenv("INTEGRATION_PROFILE", "DEMO").upper()
    if active_profile in (DEMO, TRAINING):
        time.sleep(random.uniform(100.0, 300.0) / 1000.0)

# 1. GSTN Adapter
@register_adapter(GSTN, DEMO)
@register_adapter(GSTN, TRAINING)
@register_adapter(GSTN, UAT)
@register_adapter(GSTN, PERFORMANCE)
class SimulationGSTNAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        db = get_sim_db_session()
        try:
            records = db.query(ESEGSTRecord).filter(ESEGSTRecord.customer_id == request.customer_id).all()
            if not records:
                return AdapterResponse({"gstin": request.params.get("gstin", ""), "filings": []}, 200, True, 0.0)
            
            filings = [{
                "filing_month": r.filing_month,
                "revenue": r.revenue,
                "gst_paid": r.gst_paid,
                "status": r.filing_status
            } for r in records]
            
            return AdapterResponse({
                "gstin": records[0].gstin,
                "trade_name": "Simulated Corp",
                "filings": filings
            }, 200, True, 0.0)
        finally:
            db.close()

    def health_check(self) -> bool:
        return True

# 2. Account Aggregator Adapter
@register_adapter(AA, DEMO)
@register_adapter(AA, TRAINING)
@register_adapter(AA, UAT)
@register_adapter(AA, PERFORMANCE)
class SimulationAAAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        db = get_sim_db_session()
        try:
            txs = db.query(ESETransaction).filter(ESETransaction.customer_id == request.customer_id).all()
            transactions = [{
                "date": t.transaction_date,
                "amount": t.amount,
                "type": t.type,
                "balance": t.balance,
                "description": t.description
            } for t in txs]
            
            return AdapterResponse({
                "account_ref_num": f"ACC-{request.customer_id:03d}",
                "transactions": transactions
            }, 200, True, 0.0)
        finally:
            db.close()

    def health_check(self) -> bool:
        return True

# 3. EPFO Adapter
@register_adapter(EPFO, DEMO)
@register_adapter(EPFO, TRAINING)
@register_adapter(EPFO, UAT)
@register_adapter(EPFO, PERFORMANCE)
class SimulationEPFOAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        db = get_sim_db_session()
        try:
            r = db.query(ESEEPFORecord).filter(ESEEPFORecord.customer_id == request.customer_id).first()
            if not r:
                return AdapterResponse({}, 404, True, 0.0)
            return AdapterResponse({
                "establishment_id": r.establishment_id,
                "employee_count": r.employee_count,
                "pf_compliance_score": r.pf_compliance_score,
                "last_month_contribution": r.last_month_contribution
            }, 200, True, 0.0)
        finally:
            db.close()

    def health_check(self) -> bool:
        return True

# 4. MCA Adapter
@register_adapter(MCA, DEMO)
@register_adapter(MCA, TRAINING)
@register_adapter(MCA, UAT)
@register_adapter(MCA, PERFORMANCE)
class SimulationMCAAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        db = get_sim_db_session()
        try:
            r = db.query(ESEMCARecord).filter(ESEMCARecord.customer_id == request.customer_id).first()
            if not r:
                return AdapterResponse({}, 404, True, 0.0)
            return AdapterResponse({
                "cin": r.cin,
                "company_name": r.company_name,
                "date_of_incorporation": r.date_of_incorporation,
                "status": r.status
            }, 200, True, 0.0)
        finally:
            db.close()

    def health_check(self) -> bool:
        return True

# 5. RBI Fraud Registry Adapter
@register_adapter(RBI_FRAUD, DEMO)
@register_adapter(RBI_FRAUD, TRAINING)
@register_adapter(RBI_FRAUD, UAT)
@register_adapter(RBI_FRAUD, PERFORMANCE)
class SimulationRBIFraudAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        db = get_sim_db_session()
        try:
            customer = db.query(ESECustomer).filter(ESECustomer.id == request.customer_id).first()
            pan = customer.pan if customer else request.params.get("pan", "CLEAN")
            
            # Simple check
            BLACKLISTED_PANS = {"FRAUD1234F", "BLACKLIST1F", "RBI999999F"}
            
            # Check scenario JSON overrides too
            is_blacklisted = pan in BLACKLISTED_PANS or (customer and "BLACKLIST" in customer.scenario_id)
            
            if is_blacklisted:
                return AdapterResponse({
                    "rbi_fraud_status": "BLACKLISTED",
                    "rbi_verification_log": f"CRITICAL SECURITY ALERT | PAN {pan} matches blacklist entry in RBI Central Fraud Registry."
                }, 200, True, 0.0)
                
            return AdapterResponse({
                "rbi_fraud_status": "CLEAN",
                "rbi_verification_log": f"RBI Registry queried successfully for PAN: {pan}. No matches found."
            }, 200, True, 0.0)
        finally:
            db.close()

    def health_check(self) -> bool:
        return True

# 6. OCEN / ULI Adapter
@register_adapter(OCEN, DEMO)
@register_adapter(OCEN, TRAINING)
@register_adapter(OCEN, UAT)
@register_adapter(OCEN, PERFORMANCE)
class SimulationOCENAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        return AdapterResponse({
            "eligible": True,
            "offers": [
                {"id": "OFFER-001", "bank_name": "IDBI Bank", "rate": 10.5, "tenure": 12},
                {"id": "OFFER-002", "bank_name": "HDFC Bank", "rate": 11.0, "tenure": 12}
            ]
        }, 200, True, 0.0)

    def health_check(self) -> bool:
        return True

# 7. Vertex AI Adapter
@register_adapter(VERTEX_AI, DEMO)
@register_adapter(VERTEX_AI, TRAINING)
@register_adapter(VERTEX_AI, UAT)
@register_adapter(VERTEX_AI, PERFORMANCE)
class SimulationVertexAIAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        return AdapterResponse({
            "prediction": "APPROVED",
            "confidence": 88.5,
            "explainability_tags": ["DSCR_OK", "GST_GROWTH_STRONG"]
        }, 200, True, 0.0)

    def health_check(self) -> bool:
        return True

# 8. CAM Adapter
@register_adapter(CAM, DEMO)
@register_adapter(CAM, TRAINING)
@register_adapter(CAM, UAT)
@register_adapter(CAM, PERFORMANCE)
class SimulationCAMAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        return AdapterResponse({
            "cam_status": "COMPILED",
            "pdf_url": f"http://s3-mock/cam-{request.customer_id}.pdf"
        }, 200, True, 0.0)

    def health_check(self) -> bool:
        return True

# 9. FHC Adapter
@register_adapter(FHC, DEMO)
@register_adapter(FHC, TRAINING)
@register_adapter(FHC, UAT)
@register_adapter(FHC, PERFORMANCE)
class SimulationFHCAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        apply_latency()
        return AdapterResponse({
            "fhc_score": 85,
            "tier": "GOLD",
            "ds_coverage": 1.95
        }, 200, True, 0.0)

    def health_check(self) -> bool:
        return True
