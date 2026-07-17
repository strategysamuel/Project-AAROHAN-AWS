import os
import logging
from typing import Dict, Type, Tuple
from adapters.base import ExternalIntegrationAdapter

# Configure logger
logger = logging.getLogger("ese-core")

# Integration Name Constants
CKYC = "CKYC"
GSTN = "GSTN"
AA = "AA"
EPFO = "EPFO"
MCA = "MCA"
RBI_FRAUD = "RBI_FRAUD"
OCEN = "OCEN"
VERTEX_AI = "VERTEX_AI"
CAM = "CAM"
FHC = "FHC"

ALL_INTEGRATIONS = {CKYC, GSTN, AA, EPFO, MCA, RBI_FRAUD, OCEN, VERTEX_AI, CAM, FHC}

# Supported Profiles
DEMO = "DEMO"
TRAINING = "TRAINING"
UAT = "UAT"
PERFORMANCE = "PERFORMANCE"
PRODUCTION = "PRODUCTION"

SUPPORTED_PROFILES = {DEMO, TRAINING, UAT, PERFORMANCE, PRODUCTION}

def get_dynamic_profile() -> str:
    import json
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    state_file = os.path.join(workspace_root, "ese", "ese_active_state.json")
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
                profile = state.get("active_profile", "").upper()
                if profile in SUPPORTED_PROFILES:
                    return profile
        except Exception:
            pass
            
    # Fallback to env
    profile = os.getenv("INTEGRATION_PROFILE", "").upper()
    if profile in SUPPORTED_PROFILES:
        return profile
    return DEMO

# Log warning on initial import if env is invalid and no file exists
_initial_profile = os.getenv("INTEGRATION_PROFILE", "").upper()
if _initial_profile and _initial_profile not in SUPPORTED_PROFILES:
    logger.warning(
        f"STARTUP WARNING | Invalid INTEGRATION_PROFILE env ('{_initial_profile}'). "
        f"Defaulting to '{DEMO}' mode if no state file exists."
    )

# Registry dictionary to map (integration_name, profile) -> Adapter Class
_registry: Dict[Tuple[str, str], Type[ExternalIntegrationAdapter]] = {}

# Registry for instantiated singleton adapters
_instances: Dict[Tuple[str, str], ExternalIntegrationAdapter] = {}

class AdapterNotRegisteredError(Exception):
    pass

def register_adapter(integration_name: str, profile: str):
    """
    Decorator to register a concrete adapter class for a given integration and profile.
    """
    if integration_name not in ALL_INTEGRATIONS:
        raise ValueError(f"Unknown integration name: {integration_name}")
    if profile not in SUPPORTED_PROFILES:
        raise ValueError(f"Unknown integration profile: {profile}")
        
    def decorator(cls: Type[ExternalIntegrationAdapter]):
        _registry[(integration_name, profile)] = cls
        return cls
    return decorator

class AdapterFactory:
    @staticmethod
    def get_adapter(integration_name: str) -> ExternalIntegrationAdapter:
        """
        Resolves and returns the registered adapter instance for the active profile.
        Uses a singleton pattern for resolved adapters.
        """
        profile = get_dynamic_profile()
        key = (integration_name, profile)
        
        if key in _instances:
            return _instances[key]
            
        # Lookup in registry
        if key not in _registry:
            # Fallback behavior
            # If UAT profile doesn't have a specific adapter, try PRODUCTION or DEMO depending on standard UAT mix
            # UAT defaults to PRODUCTION for internal APIs and DEMO for simulated external sources.
            # In Sprint 1, we fallback to DEMO (simulated) for simplicity if not registered,
            # or PRODUCTION if it exists.
            fallback_profile = DEMO
            if profile == UAT:
                # Check if PRODUCTION is registered, otherwise use DEMO
                if (integration_name, PRODUCTION) in _registry:
                    fallback_profile = PRODUCTION
            
            fallback_key = (integration_name, fallback_profile)
            if fallback_key not in _registry:
                raise AdapterNotRegisteredError(
                    f"No adapter registered for '{integration_name}' in profile '{profile}' "
                    f"or fallback '{fallback_profile}'."
                )
            key = fallback_key
            
        # Instantiate and cache
        adapter_cls = _registry[key]
        instance = adapter_cls()
        _instances[(integration_name, profile)] = instance
        return instance

    @staticmethod
    def get_active_profile() -> str:
        return get_dynamic_profile()

    @staticmethod
    def get_registered_adapters_status() -> list:
        status_list = []
        for name in sorted(ALL_INTEGRATIONS):
            try:
                adapter = AdapterFactory.get_adapter(name)
                is_healthy = adapter.health_check()
                # Determine mode class
                mode = "PRODUCTION" if "Production" in adapter.__class__.__name__ else "SIMULATION"
                status_list.append({
                    "name": name,
                    "mode": mode,
                    "is_healthy": is_healthy
                })
            except Exception:
                status_list.append({
                    "name": name,
                    "mode": "UNKNOWN",
                    "is_healthy": False
                })
        return status_list

# Trigger registration decorators by importing concrete adapters
try:
    import adapters.simulation.ckyc
    import adapters.simulation.all_simulators
    import adapters.production.all_production
except ImportError:
    try:
        from adapters.simulation import ckyc
        from adapters.simulation import all_simulators
        from adapters.production import all_production
    except ImportError:
        pass

