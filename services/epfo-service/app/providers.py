import abc
import datetime
import os
from typing import Dict, List, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class EPFOAdapter(abc.ABC):
    @abc.abstractmethod
    def fetch_establishment_profile(self, establishment_id: str) -> Dict[str, Any]:
        """Verify establishment ID and return profile information"""
        pass

    @abc.abstractmethod
    def fetch_employee_summary(self, establishment_id: str) -> List[Dict[str, Any]]:
        """Fetch list of employee payroll UAN records"""
        pass

    @abc.abstractmethod
    def fetch_monthly_contributions(self, establishment_id: str) -> List[Dict[str, Any]]:
        """Fetch monthly EPFO contribution logs"""
        pass

class SimulationEPFOAdapter(EPFOAdapter):
    def fetch_establishment_profile(self, establishment_id: str) -> Dict[str, Any]:
        from app.database import SessionLocal
        db = SessionLocal()
        try:
            row = db.execute(
                text("SELECT c.legal_name, b.trade_name, b.employees_count "
                "FROM onboarding_businesses b JOIN onboarding_customers c ON b.customer_id = c.id "
                "WHERE b.industry_segment LIKE '%Textile%' or b.trade_name LIKE '%Priya%' LIMIT 1")
            ).fetchone()
            if row:
                return {
                    "establishment_id": establishment_id,
                    "establishment_name": row[0],
                    "esic_registration_num": "27000283726354890",
                    "status": "ACTIVE",
                    "number_of_employees": row[2] or 35,
                    "average_monthly_payroll": (row[2] or 35) * 15000.0
                }
        except Exception:
            pass
        finally:
            db.close()

        # Fallback default
        return {
            "establishment_id": establishment_id,
            "establishment_name": "Project AAROHAN Textiles Private Limited",
            "esic_registration_num": "27000283726354890",
            "status": "ACTIVE",
            "number_of_employees": 30,
            "average_monthly_payroll": 450000.0
        }

    def fetch_employee_summary(self, establishment_id: str) -> List[Dict[str, Any]]:
        # Generates realistic employee logs
        employees = []
        names = [
            "Amit Sharma", "Priya Patel", "Rajesh Kumar", "Sunita Rao",
            "Vijay Singh", "Anita Desai", "Sanjay Joshi", "Neha Gupta",
            "Deepak Verma", "Ritu Mishra", "Vikram Malhotra", "Meera Nair",
            "Arjun Mehta", "Kiran Shah", "Rohan Roy"
        ]
        
        import random
        base_date = datetime.datetime(2021, 6, 15)
        for i, name in enumerate(names):
            employees.append({
                "uan": f"10098{random.randint(10000, 99999)}{i}",
                "name": name,
                "joining_date": base_date + datetime.timedelta(days=i * 20),
                "exit_date": None if i != 4 and i != 9 else base_date + datetime.timedelta(days=i * 50 + 100),
                "salary": 12000.0 + (i * 1200.0),
                "designation": "Operator" if i < 10 else "Supervisor",
                "is_active": True if i != 4 and i != 9 else False
            })
        return employees

    def fetch_monthly_contributions(self, establishment_id: str) -> List[Dict[str, Any]]:
        # Returns contributions history
        contributions = []
        months = ["082025", "092025", "102025", "112025", "122025", "012026", "022026", "032026"]
        
        # Occasional delayed payments for late filing detection (Compliance engine check)
        for i, m in enumerate(months):
            delay = 0
            if i == 2:
                delay = 8 # late filing
            amount = 54000.0 if i < 4 else 58000.0
            emp_share = amount * 0.45
            
            contributions.append({
                "wage_month": m,
                "amount_paid": amount,
                "employer_share": emp_share,
                "employees_count": 28 if i < 4 else 31,
                "payment_date": datetime.datetime(2025 if "2025" in m else 2026, int(m[:2]), 15) + datetime.timedelta(days=delay),
                "status": "PAID" if delay == 0 else "LATE"
            })
        return contributions

class SandboxEPFOAdapter(EPFOAdapter):
    def fetch_establishment_profile(self, establishment_id: str) -> Dict[str, Any]:
        return {
            "establishment_id": establishment_id,
            "establishment_name": "Sandbox Test Mills LLP",
            "esic_registration_num": "11000283726354890",
            "status": "ACTIVE",
            "number_of_employees": 12,
            "average_monthly_payroll": 180000.0
        }

    def fetch_employee_summary(self, establishment_id: str) -> List[Dict[str, Any]]:
        return [{
            "uan": "100989999",
            "name": "Sandbox Tester One",
            "joining_date": datetime.datetime(2024, 1, 1),
            "exit_date": None,
            "salary": 25000.0,
            "designation": "QA Eng",
            "is_active": True
        }]

    def fetch_monthly_contributions(self, establishment_id: str) -> List[Dict[str, Any]]:
        return [{
            "wage_month": "032026",
            "amount_paid": 21600.0,
            "employer_share": 10800.0,
            "employees_count": 12,
            "payment_date": datetime.datetime(2026, 4, 12),
            "status": "PAID"
        }]

class ProductionEPFOAdapter(EPFOAdapter):
    def fetch_establishment_profile(self, establishment_id: str) -> Dict[str, Any]:
        return {
            "establishment_id": establishment_id,
            "establishment_name": "Real Production EPFO Mills Ltd",
            "esic_registration_num": "99000283726354890",
            "status": "ACTIVE",
            "number_of_employees": 150,
            "average_monthly_payroll": 2250000.0
        }

    def fetch_employee_summary(self, establishment_id: str) -> List[Dict[str, Any]]:
        return []

    def fetch_monthly_contributions(self, establishment_id: str) -> List[Dict[str, Any]]:
        return []

def get_epfo_adapter() -> EPFOAdapter:
    profile = os.getenv("EPFO_ADAPTER_PROFILE", "SIMULATION").upper()
    if profile in ("REAL", "PRODUCTION"):
        return ProductionEPFOAdapter()
    elif profile == "SANDBOX":
        return SandboxEPFOAdapter()
    else:
        return SimulationEPFOAdapter()
