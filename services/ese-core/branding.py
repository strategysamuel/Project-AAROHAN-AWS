import logging
from typing import Dict, Any

logger = logging.getLogger("ese-branding")

class brandingEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(brandingEngine, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_branding()
        return cls._instance

    def _init_branding(self):
        self.active_brand = "STANDARD"
        self.brands: Dict[str, Dict[str, Any]] = {
            "STANDARD": {
                "name": "Project AAROHAN standard Twin",
                "primary_color": "#1565c0",
                "secondary_color": "#0d47a1",
                "logo_url": "/assets/logo_standard.png",
                "theme": "dark"
            },
            "IDBI": {
                "name": "IDBI Bank MSME Digital Twin",
                "primary_color": "#00838f",
                "secondary_color": "#006064",
                "logo_url": "/assets/logo_idbi.png",
                "theme": "glassmorphic-teal"
            },
            "HACKATHON": {
                "name": "Hack 2 Skill Aarohan Presentation Mode",
                "primary_color": "#6a1b9a",
                "secondary_color": "#4a148c",
                "logo_url": "/assets/logo_hack.png",
                "theme": "cyberpunk-neon"
            }
        }

    def set_brand(self, brand_key: str) -> Dict[str, Any]:
        brand_key = brand_key.upper()
        if brand_key in self.brands:
            self.active_brand = brand_key
            logger.info(f"Branding switched to: {brand_key}")
            return self.brands[brand_key]
        raise ValueError(f"Brand profile {brand_key} not registered.")

    def get_brand(self) -> Dict[str, Any]:
        return self.brands.get(self.active_brand, self.brands["STANDARD"])
