import abc
import datetime
import os
from typing import Dict, List, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class MCAAdapter(abc.ABC):
    @abc.abstractmethod
    def fetch_company_profile(self, cin: str) -> Dict[str, Any]:
        """Fetch general corporate info from MCA registry"""
        pass

    @abc.abstractmethod
    def fetch_directors(self, cin: str) -> List[Dict[str, Any]]:
        """Fetch Board of Directors roster"""
        pass

    @abc.abstractmethod
    def fetch_charges(self, cin: str) -> List[Dict[str, Any]]:
        """Fetch open and satisfied bank charges"""
        pass

    @abc.abstractmethod
    def fetch_filings(self, cin: str) -> List[Dict[str, Any]]:
        """Fetch annual return filings history"""
        pass

    @abc.abstractmethod
    def fetch_financials(self, cin: str) -> List[Dict[str, Any]]:
        """Fetch annual audited balance sheet & P&L statements"""
        pass

class SimulationMCAAdapter(MCAAdapter):
    def fetch_company_profile(self, cin: str) -> Dict[str, Any]:
        from app.database import SessionLocal
        db = SessionLocal()
        try:
            row = db.execute(
                text("SELECT c.legal_name, b.trade_name, b.constitution_type "
                "FROM onboarding_businesses b JOIN onboarding_customers c ON b.customer_id = c.id "
                "WHERE b.cin = :cin LIMIT 1"), {"cin": cin}
            ).fetchone()
            if row:
                return {
                    "cin": cin,
                    "company_name": row[0],
                    "incorporation_date": datetime.datetime(2018, 5, 20),
                    "company_status": "ACTIVE",
                    "class_of_company": row[2] or "Private Limited",
                    "authorized_capital": 50000000.0,
                    "paid_up_capital": 35000000.0,
                    "registered_office": "101, Textile Tower, Bandra East, Mumbai - 400051",
                    "roc": "ROC Mumbai"
                }
        except Exception:
            pass
        finally:
            db.close()

        # Fallback default
        return {
            "cin": cin,
            "company_name": "Project AAROHAN Textiles Private Limited",
            "incorporation_date": datetime.datetime(2018, 5, 20),
            "company_status": "ACTIVE",
            "class_of_company": "Private Limited",
            "authorized_capital": 50000000.0,
            "paid_up_capital": 35000000.0,
            "registered_office": "101, Textile Tower, Bandra East, Mumbai - 400051",
            "roc": "ROC Mumbai"
        }

    def fetch_directors(self, cin: str) -> List[Dict[str, Any]]:
        return [
            {"din": "08192837", "full_name": "Aditya Patel", "appointment_date": datetime.datetime(2018, 5, 20), "is_disqualified": False},
            {"din": "09283746", "full_name": "Sanjay Patel", "appointment_date": datetime.datetime(2020, 8, 15), "is_disqualified": False}
        ]

    def fetch_charges(self, cin: str) -> List[Dict[str, Any]]:
        return [
            {"charge_id": "CHG-9988-293", "holder_name": "State Bank of India", "charge_amount": 15000000.0, "creation_date": datetime.datetime(2021, 10, 5), "status": "OPEN"},
            {"charge_id": "CHG-9988-555", "holder_name": "IDBI Bank", "charge_amount": 8000000.0, "creation_date": datetime.datetime(2024, 2, 11), "status": "OPEN"}
        ]

    def fetch_filings(self, cin: str) -> List[Dict[str, Any]]:
        return [
            {"form_name": "AOC-4", "filing_date": datetime.datetime(2025, 10, 22), "status": "APPROVED", "financial_year": "2024-25", "filing_delay_days": 0},
            {"form_name": "MGT-7", "filing_date": datetime.datetime(2025, 11, 5), "status": "APPROVED", "financial_year": "2024-25", "filing_delay_days": 6}
        ]

    def fetch_financials(self, cin: str) -> List[Dict[str, Any]]:
        # Returns 3 years balance sheet & P&L statements
        return [
            {"financial_year": "2022-23", "revenue": 125000000.0, "net_worth": 31000000.0, "profit_after_tax": 7500000.0, "debt": 21000000.0},
            {"financial_year": "2023-24", "revenue": 145000000.0, "net_worth": 35000000.0, "profit_after_tax": 9200000.0, "debt": 23000000.0},
            {"financial_year": "2024-25", "revenue": 168000000.0, "net_worth": 42000000.0, "profit_after_tax": 11500000.0, "debt": 25000000.0}
        ]

class SandboxMCAAdapter(MCAAdapter):
    def fetch_company_profile(self, cin: str) -> Dict[str, Any]:
        return {
            "cin": cin,
            "company_name": "Sandbox Corporate LLP",
            "incorporation_date": datetime.datetime(2020, 1, 1),
            "company_status": "ACTIVE",
            "class_of_company": "LLP",
            "authorized_capital": 1000000.0,
            "paid_up_capital": 500000.0,
            "registered_office": "Sandbox Office",
            "roc": "ROC Delhi"
        }

    def fetch_directors(self, cin: str) -> List[Dict[str, Any]]:
        return [{"din": "00000001", "full_name": "Sandbox Director One", "appointment_date": datetime.datetime(2020, 1, 1), "is_disqualified": False}]

    def fetch_charges(self, cin: str) -> List[Dict[str, Any]]:
        return []

    def fetch_filings(self, cin: str) -> List[Dict[str, Any]]:
        return [{"form_name": "AOC-4", "filing_date": datetime.datetime(2025, 10, 30), "status": "APPROVED", "financial_year": "2024-25", "filing_delay_days": 0}]

    def fetch_financials(self, cin: str) -> List[Dict[str, Any]]:
        return [{"financial_year": "2024-25", "revenue": 5000000.0, "net_worth": 1500000.0, "profit_after_tax": 300000.0, "debt": 500000.0}]

class ProductionMCAAdapter(MCAAdapter):
    def fetch_company_profile(self, cin: str) -> Dict[str, Any]:
        return {
            "cin": cin,
            "company_name": "Production Corporate Registry",
            "incorporation_date": datetime.datetime(2015, 6, 10),
            "company_status": "ACTIVE",
            "class_of_company": "Private Limited",
            "authorized_capital": 10000000.0,
            "paid_up_capital": 8000000.0,
            "registered_office": "Prod Office",
            "roc": "ROC Mumbai"
        }

    def fetch_directors(self, cin: str) -> List[Dict[str, Any]]:
        return []

    def fetch_charges(self, cin: str) -> List[Dict[str, Any]]:
        return []

    def fetch_filings(self, cin: str) -> List[Dict[str, Any]]:
        return []

    def fetch_financials(self, cin: str) -> List[Dict[str, Any]]:
        return []

def get_mca_adapter() -> MCAAdapter:
    profile = os.getenv("MCA_ADAPTER_PROFILE", "SIMULATION").upper()
    if profile in ("REAL", "PRODUCTION"):
        return ProductionMCAAdapter()
    elif profile == "SANDBOX":
        return SandboxMCAAdapter()
    else:
        return SimulationMCAAdapter()
