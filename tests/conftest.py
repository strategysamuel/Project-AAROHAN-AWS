import sys
import pytest
import os

@pytest.fixture(autouse=True)
def clean_app_modules_and_db():
    """
    Clears all cached 'app' modules from sys.modules and cleans up
    conflicting records in the local test database before each test.
    """
    # 1. Clear sys.modules
    for k in list(sys.modules.keys()):
        if k == "app" or k.startswith("app."):
            sys.modules.pop(k, None)
            
    # 2. Clean up SQLite database conflicts
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine("sqlite:///./aarohan_local.db")
        with engine.connect() as conn:
            tables = [
                "onboarding_customers", "onboarding_businesses", "onboarding_addresses",
                "ckyc_records", "ckyc_verification_logs",
                "mca_sync_logs", "mca_profiles",
                "epfo_sync_logs", "epfo_profiles",
                "treds_buyers", "treds_invoices",
                "linked_accounts", "aa_sync_logs", "aa_analytics",
                "gst_sync_logs", "gst_return_filings", "gst_analytics",
                "fhc_history", "ai_credit_decisions", "human_approval_logs",
                "portfolio_analytics", "ews_watchlist"
            ]
            for t in tables:
                try:
                    conn.execute(text(f"DELETE FROM {t} WHERE customer_id IN (120, 125) OR id IN (120, 125)"))
                except Exception:
                    pass
            # Specific cleanups
            try:
                conn.execute(text("DELETE FROM onboarding_customers WHERE pan IN ('FRAUD1234F', 'ABCDE1234F')"))
                conn.execute(text("DELETE FROM onboarding_businesses WHERE gstin = '27FRAUD1234F1Z1'"))
                conn.execute(text("DELETE FROM ckyc_records WHERE pan IN ('FRAUD1234F', 'ABCDE1234F')"))
            except Exception:
                pass
            conn.commit()
    except Exception:
        pass
        
    yield
