import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from adapters.base import ExternalIntegrationAdapter, AdapterRequest, AdapterResponse
from adapter_factory import register_adapter, CKYC, GSTN, AA, EPFO, MCA, RBI_FRAUD, OCEN, VERTEX_AI, CAM, FHC, PRODUCTION

class ProductionBaseAdapter(ExternalIntegrationAdapter):
    def fetch(self, request: AdapterRequest) -> AdapterResponse:
        raise NotImplementedError("Production adapter integration is planned for Sprint 2+.")

    def health_check(self) -> bool:
        # Production adapters default to False/unhealthy until live connections are implemented
        return False

@register_adapter(CKYC, PRODUCTION)
class ProductionCKYCAdapter(ProductionBaseAdapter):
    pass

@register_adapter(GSTN, PRODUCTION)
class ProductionGSTNAdapter(ProductionBaseAdapter):
    pass

@register_adapter(AA, PRODUCTION)
class ProductionAAAdapter(ProductionBaseAdapter):
    pass

@register_adapter(EPFO, PRODUCTION)
class ProductionEPFOAdapter(ProductionBaseAdapter):
    pass

@register_adapter(MCA, PRODUCTION)
class ProductionMCAAdapter(ProductionBaseAdapter):
    pass

@register_adapter(RBI_FRAUD, PRODUCTION)
class ProductionRBIFraudAdapter(ProductionBaseAdapter):
    pass

@register_adapter(OCEN, PRODUCTION)
class ProductionOCENAdapter(ProductionBaseAdapter):
    pass

@register_adapter(VERTEX_AI, PRODUCTION)
class ProductionVertexAIAdapter(ProductionBaseAdapter):
    pass

@register_adapter(CAM, PRODUCTION)
class ProductionCAMAdapter(ProductionBaseAdapter):
    pass

@register_adapter(FHC, PRODUCTION)
class ProductionFHCAdapter(ProductionBaseAdapter):
    pass
