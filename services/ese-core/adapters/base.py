from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class AdapterRequest:
    integration_name: str
    customer_id: Optional[int] = None
    scenario_id: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdapterResponse:
    data: Dict[str, Any]
    status_code: int
    simulated: bool
    latency_ms: float
    message: Optional[str] = None

class ExternalIntegrationAdapter(ABC):
    """
    Abstract Base Class for all External Integration Adapters.
    Every simulation and production adapter must implement this interface.
    """

    @abstractmethod
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        """
        Executes a pull or fetch operation from the external integration.
        
        Args:
            request: The standard request parameters including customer/scenario.
            
        Returns:
            An AdapterResponse containing the result payload.
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Performs a self-check of the adapter's connectivity or status.
        
        Returns:
            bool: True if healthy, False otherwise.
        """
        pass
