# AAR-DATABASE-CONSISTENCY-REPORT

## Database Audit Summary

An extensive audit of all Python files in the repository was conducted to locate any remaining independent or standalone SQLite database connections.

The following files were found to have rogue database connections bypassing the centralized `services/shared/database.py`:

| File | Old Database Connection | New Shared Connection |
|------|-------------------------|-----------------------|
| `services/ckyc-service/app/adapters.py` | `engine = create_engine("sqlite:///./aarohan_local.db")` | `from app.database import SessionLocal` |
| `services/epfo-service/app/providers.py` | `engine = create_engine("sqlite:///./aarohan_local.db")` | `from app.database import SessionLocal` |
| `services/mca-service/app/providers.py` | `engine = create_engine("sqlite:///./aarohan_local.db")` | `from app.database import SessionLocal` |
| `services/gst-service/app/providers.py` | `engine = create_engine("sqlite:///./aarohan_local.db")` | `from app.database import SessionLocal` |
| `services/aa-service/app/providers.py` | `engine = create_engine("sqlite:///./aarohan_local.db")` | `from app.database import SessionLocal` |
| `services/ese-core/db_helper.py` | `engine = create_engine(db_url, connect_args=...)` | `from services.shared.database import SessionLocal, engine, Base` |
| `services/ese-core/dataset_generator.py` | `engine = create_engine(f"sqlite:///{db_path}")` | `from services.shared.database import SessionLocal, engine` |

## Resolution
- **Replaced Standalone Engines:** All simulation adapters across the microservices were refactored to pull the `SessionLocal` from the shared application state instead of instantiating their own SQLite engine using a relative path.
- **Unified ESE Core:** The Enterprise Simulation Engine (`ese-core`) was also updated to connect directly to the shared `aarohan_local.db` database via the `services.shared.database` module. This ensures that when new simulated mock data is generated, it is automatically synchronized into the identical database that the microservices consume.

## Certification

**CERTIFIED GREEN:** Every module (including all providers, adapters, repositories, helpers, simulation modules, middlewares, and utilities) now reads from the exact same shared database. No independent SQLite connections remain anywhere in the repository.
