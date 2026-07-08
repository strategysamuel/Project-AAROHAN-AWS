import abc
import logging
import uuid

logger = logging.getLogger("consent-service")

class ConsentProviderInterface(abc.ABC):
    @abc.abstractmethod
    def trigger_consent_request(self, customer_mobile: str, purpose: str) -> str:
        """Trigger consent request to external DPI utility and return transaction ID"""
        pass

    @abc.abstractmethod
    def fetch_consent_status(self, txn_id: str) -> str:
        """Fetch consent status from provider registry"""
        pass

class AccountAggregatorMockProvider(ConsentProviderInterface):
    def trigger_consent_request(self, customer_mobile: str, purpose: str) -> str:
        txn_id = f"AA-TXN-{uuid.uuid4().hex[:8].upper()}"
        logger.info(f"MOCK AA | Triggered consent request | Mobile: {customer_mobile} | Txn: {txn_id}")
        return txn_id

    def fetch_consent_status(self, txn_id: str) -> str:
        logger.info(f"MOCK AA | Checking transaction: {txn_id}")
        return "APPROVED" # Simulate instant auto-approval for UAT flow

class GSTNMockProvider(ConsentProviderInterface):
    def trigger_consent_request(self, customer_mobile: str, purpose: str) -> str:
        txn_id = f"GST-TXN-{uuid.uuid4().hex[:8].upper()}"
        logger.info(f"MOCK GSTN | Triggered verification request | Mobile: {customer_mobile} | Txn: {txn_id}")
        return txn_id

    def fetch_consent_status(self, txn_id: str) -> str:
        return "APPROVED"

# Global provider factory registry helper
def get_provider(provider_type: str) -> ConsentProviderInterface:
    if provider_type == "ACCOUNT_AGGREGATOR":
        return AccountAggregatorMockProvider()
    return GSTNMockProvider()
