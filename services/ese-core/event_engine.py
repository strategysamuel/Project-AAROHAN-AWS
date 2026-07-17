import time
import uuid
import logging
from typing import Dict, Any, List, Callable

logger = logging.getLogger("ese-event-engine")

class BusinessEventEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BusinessEventEngine, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        self.handlers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self.event_history: List[Dict[str, Any]] = []

    def register_handler(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        logger.info(f"Registered handler for event: {event_type}")

    def dispatch(self, event_type: str, persona_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        event_id = f"evt_{uuid.uuid4().hex[:12]}"
        event_record = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "persona_id": persona_id,
            "payload": payload
        }
        self.event_history.append(event_record)
        logger.info(f"Dispatching event: {event_type} (ID: {event_id}) for persona: {persona_id}")

        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    handler(event_record)
                except Exception as e:
                    logger.error(f"Error executing handler for {event_type}: {e}")

        # Cascade logic representing the propagation loop
        self._cascade_propagation(event_record)

        return event_record

    def _cascade_propagation(self, event: Dict[str, Any]):
        event_type = event["event_type"]
        persona_id = event["persona_id"]
        payload = event["payload"]

        # 1. GST_RETURN_FILED -> TURNOVER_UPDATED
        if event_type == "GST_RETURN_FILED":
            turnover = payload.get("reported_turnover", 0.0)
            self.dispatch("TURNOVER_UPDATED", persona_id, {"turnover": turnover})

        # 2. TURNOVER_UPDATED -> CASH_FLOW_UPDATED
        elif event_type == "TURNOVER_UPDATED":
            turnover = payload.get("turnover", 0.0)
            # Estimate cash flow as 15% of turnover for general simulation
            operating_cash_flow = turnover * 0.15
            self.dispatch("CASH_FLOW_UPDATED", persona_id, {"operating_cash_flow": operating_cash_flow, "turnover": turnover})

        # 3. CASH_FLOW_UPDATED -> FHC_RECALCULATED
        elif event_type == "CASH_FLOW_UPDATED":
            ocf = payload.get("operating_cash_flow", 0.0)
            # Recalculate FHC using Causal Model
            from causal_model import FinancialCausalModel
            fcm = FinancialCausalModel()
            fhc_results = fcm.calculate_fhc(ocf=ocf)
            self.dispatch("FHC_RECALCULATED", persona_id, fhc_results)

        # 4. FHC_RECALCULATED -> CREDIT_SCORE_UPDATED
        elif event_type == "FHC_RECALCULATED":
            fhc_score = payload.get("overall_score", 80.0)
            from causal_model import FinancialCausalModel
            fcm = FinancialCausalModel()
            credit_score = fcm.calculate_credit_score(fhc_score=fhc_score)
            self.dispatch("CREDIT_SCORE_UPDATED", persona_id, {"credit_score": credit_score, "fhc_score": fhc_score})

        # 5. CREDIT_SCORE_UPDATED -> OCEN_ELIGIBILITY_UPDATED
        elif event_type == "CREDIT_SCORE_UPDATED":
            credit_score = payload.get("credit_score", 700)
            eligible = credit_score >= 580
            self.dispatch("OCEN_ELIGIBILITY_UPDATED", persona_id, {"eligible": eligible, "credit_score": credit_score})

        # 6. OCEN_ELIGIBILITY_UPDATED -> LOAN_OFFERS_REGENERATED
        elif event_type == "OCEN_ELIGIBILITY_UPDATED":
            eligible = payload.get("eligible", False)
            if eligible:
                from lenders import BankingNetworkSimulator
                network = BankingNetworkSimulator()
                # Lookup score
                credit_score = payload.get("credit_score", 700)
                offers = network.generate_offers(persona_id, credit_score)
                self.dispatch("LOAN_OFFERS_REGENERATED", persona_id, {"offers": offers})
            else:
                self.dispatch("LOAN_OFFERS_REGENERATED", persona_id, {"offers": [], "reason": "Credit score below threshold"})

        # 7. LOAN_OFFERS_REGENERATED -> EXEC_DASHBOARD_REFRESHED
        elif event_type == "LOAN_OFFERS_REGENERATED":
            self.dispatch("EXEC_DASHBOARD_REFRESHED", persona_id, {"timestamp": time.time()})

    def get_history(self) -> List[Dict[str, Any]]:
        return self.event_history

    def clear_history(self):
        self.event_history.clear()
