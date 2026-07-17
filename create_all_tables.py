import sys
import importlib

sys.path.append("/app")

from services.shared.database import engine, Base

services = [
    "onboarding-service",
    "gst-service",
    "ckyc-service",
    "aa-service",
    "epfo-service",
    "mca-service",
    "fhc-service",
    "credit-engine",
    "cam-service",
    "rbi-fraud-service"
]

for svc in services:
    try:
        module_name = f"services.{svc.replace('-', '_')}.app.models"
        importlib.import_module(module_name)
    except Exception as e:
        # Some are named differently, try direct paths by modifying sys.path if needed
        sys.path.insert(0, f"/app/services/{svc}")
        try:
            import app.models
        except Exception as e2:
            print(f"Failed to import models for {svc}: {e2}")
        finally:
            sys.path.pop(0)

Base.metadata.create_all(bind=engine)
print("All tables created successfully!")
