import abc
import datetime
from typing import Dict, List, Any

class GSTProviderInterface(abc.ABC):
    @abc.abstractmethod
    def fetch_gst_profile(self, gstin: str) -> Dict[str, Any]:
        """Fetch primary corporate tax registration profile details from GSTN"""
        pass

    @abc.abstractmethod
    def fetch_return_filing_history(self, gstin: str) -> List[Dict[str, Any]]:
        """Fetch chronological filing status dates for GSTR-1 and GSTR-3B returns"""
        pass

class GSTNMockProvider(GSTProviderInterface):
    def fetch_gst_profile(self, gstin: str) -> Dict[str, Any]:
        return {
            "gstin": gstin,
            "legal_name": "Project AAROHAN Auto Parts Manufacturer Private Limited",
            "trade_name": "Aarohan Auto Components",
            "registration_date": datetime.datetime(2018, 4, 15),
            "status": "ACTIVE"
        }

    def fetch_return_filing_history(self, gstin: str) -> List[Dict[str, Any]]:
        # Simulate 12 months GSTR-1 and GSTR-3B filings with seasonal patterns and occasional delays
        returns = []
        months = ["04", "05", "06", "07", "08", "09", "10", "11", "12", "01", "02", "03"]
        years = ["2025", "2025", "2025", "2025", "2025", "2025", "2025", "2025", "2025", "2026", "2026", "2026"]
        
        # Turnovers displaying a seasonal bump in Q3 (Oct-Dec)
        turnovers = [1000000, 1100000, 950000, 1050000, 1000000, 1150000, 1800000, 1950000, 1700000, 900000, 950000, 1100000]
        delays = [0, 2, 0, 0, 5, 0, 0, 0, 0, 1, 0, 0] # filing delay days
        
        for idx, (m, y) in enumerate(zip(months, years)):
            period = f"{m}{y}"
            turnover = turnovers[idx]
            delay = delays[idx]
            
            # GSTR-1 (Turnover Declaration)
            returns.append({
                "return_type": "GSTR1",
                "financial_year": "2025-26" if y == "2025" or m == "01" or m == "02" or m == "03" else "2024-25",
                "tax_period": period,
                "filing_date": datetime.datetime(int(y), int(m), 11) + datetime.timedelta(days=delay),
                "status": "FILED",
                "gross_turnover": float(turnover),
                "tax_paid": float(turnover * 0.18), # Assuming flat 18% GST tier
                "filing_delay_days": delay
            })
            
            # GSTR-3B (Summary payment details)
            returns.append({
                "return_type": "GSTR3B",
                "financial_year": "2025-26" if y == "2025" or m == "01" or m == "02" or m == "03" else "2024-25",
                "tax_period": period,
                "filing_date": datetime.datetime(int(y), int(m), 20) + datetime.timedelta(days=delay),
                "status": "FILED",
                "gross_turnover": float(turnover),
                "tax_paid": float(turnover * 0.18),
                "filing_delay_days": delay
            })
            
        return returns
