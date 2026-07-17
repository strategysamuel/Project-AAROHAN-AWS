import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

logger = logging.getLogger("ese-clock")

class SimulationClock:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SimulationClock, cls).__new__(cls, *args, **kwargs)
            cls._instance.current_date = datetime(2026, 1, 1)
        return cls._instance

    def set_date(self, date_str: str):
        try:
            self.current_date = datetime.strptime(date_str, "%Y-%m-%d")
            logger.info(f"Simulation date set to: {self.current_date.strftime('%Y-%m-%d')}")
        except Exception as e:
            logger.error(f"Error parsing date string {date_str}: {e}")

    def tick(self, interval: str = "day") -> str:
        interval = interval.lower()
        if interval == "day":
            self.current_date += timedelta(days=1)
        elif interval == "week":
            self.current_date += timedelta(weeks=1)
        elif interval == "month":
            # Rough month addition
            self.current_date += timedelta(days=30)
        elif interval == "quarter":
            self.current_date += timedelta(days=90)
        elif interval == "year":
            self.current_date += timedelta(days=365)
        else:
            raise ValueError(f"Unsupported tick interval: {interval}")
            
        logger.info(f"Clock ticked. Current simulated date: {self.get_date_string()}")
        return self.get_date_string()

    def get_date_string(self) -> str:
        return self.current_date.strftime("%Y-%m-%d")
